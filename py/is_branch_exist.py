import os
import subprocess
import sys

eo_lib_version = sys.argv[1]
print('cmd entry:', eo_lib_version)
branch_name = "update-" + eo_lib_version

command = f'git rev-parse --verify {branch_name}'
result = subprocess.run(command, shell=True, capture_output=True)
is_exist = result.returncode == 0
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    myfile.write(f'is_exist={"true" if is_exist else "false"}')
print(f'Added to env: {is_exist}')