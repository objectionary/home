# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Objectionary.com
# SPDX-License-Identifier: MIT

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, call, mock_open, patch


spec = importlib.util.spec_from_file_location(
    "auto_pull", Path(__file__).with_name("auto_pull.py")
)
auto_pull = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_pull)


class ReleaseVersionsTest(unittest.TestCase):
    def test_compares_numeric_components_in_order(self):
        for newest, current, expected in [
            ("0.62.10", "0.63.2", False),
            ("1.9.9", "2.0.0", False),
            ("2.1.9", "2.2.0", False),
            ("2.2.0", "2.2.1", False),
            ("2.2.1", "2.2.1", False),
            ("3.0.0", "2.9.9", True),
            ("2.3.0", "2.2.9", True),
            ("2.2.10", "2.2.9", True),
            ("1.0.0", "1.0", False),
            ("1.0.1", "1.0", True),
        ]:
            with self.subTest(newest=newest, current=current):
                self.assertEqual(auto_pull.compare(newest, current), expected)

    def test_reads_versions_before_mapping_runtime_repository(self):
        source = (
            "+rt jvm org.eolang:eo-runtime:1.2.3\n"
            "+rt jvm org.eolang:eo-runtime:tests:2.3.4\n"
            "+rt jvm org.eolang:eo-files:tests:3.4.5\n"
            "+rt jvm org.eolang:eo-runtime-helper:4.5.6\n"
            "+rt jvm org.eolang:missing-version\n"
            "+rt jvm org.eolang:eo-runtime::1.2.3\n"
            "+rt jvm org.eolang:eo-runtime:tests:1.2.3:extra\n"
        )
        with patch.object(auto_pull.os, "walk", return_value=[("objects", [], ["a.eo"])]):
            with patch("builtins.open", mock_open(read_data=source)):
                self.assertEqual(
                    auto_pull.dependencies(),
                    {"eo:1.2.3", "eo:2.3.4", "eo-files:3.4.5", "eo-runtime-helper:4.5.6"},
                )

    def test_downgrade_does_not_pull_or_rewrite_pom(self):
        response = Mock()
        response.json.return_value = [{"tag_name": "1.9.9"}]
        with patch.object(auto_pull.requests, "get", return_value=response):
            with patch.object(auto_pull.os, "system") as command:
                auto_pull.pull_release({"eo:2.0.0"})
                command.assert_not_called()

    def test_upgrade_still_updates_library_and_pom(self):
        response = Mock()
        response.json.return_value = [{"tag_name": "1.2.4"}]
        with TemporaryDirectory() as directory:
            environment = Path(directory) / "github-env"
            with patch.dict(auto_pull.os.environ, {"GITHUB_ENV": str(environment)}):
                with patch.object(auto_pull.requests, "get", return_value=response):
                    with patch.object(auto_pull.os, "system", return_value=0) as command:
                        auto_pull.pull_release({"eo:1.2.3"})
                        self.assertEqual(command.call_args_list, [
                            call("./pull.sh objectionary/eo"),
                            call("./.github/pom.sh 1.2.4"),
                        ])
            self.assertEqual(environment.read_text(), "eo_lib_version=eo-1.2.4")


if __name__ == "__main__":
    unittest.main()
