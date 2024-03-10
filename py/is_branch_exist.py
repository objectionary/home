import os
import subprocess
import sys

make_pr = False
if len(sys.argv) > 1:
    eo_lib_version = sys.argv[1]
    if eo_lib_version != '':
        print('cmd entry:', eo_lib_version)
        command = f'git ls-remote --exit-code --heads origin update-{eo_lib_version}'
        result = subprocess.run(command, shell=True, capture_output=True)
        make_pr = result.returncode != 0
else:
    print("eo_lib_version was not set to sys.argv")
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as file:
    env = f'make_pr={"true" if make_pr else "false"}'
    file.write(env)
    print(f'written to GITHUB_ENV "{env}"')
print(f'Added to env: {make_pr}')
