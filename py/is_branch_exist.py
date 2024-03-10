import os
import subprocess
import sys

is_exist = False
if len(sys.argv) > 1:
    eo_lib_version = sys.argv[1]
    print('cmd entry:', eo_lib_version)
    command = f'git ls-remote --exit-code --heads origin update-{eo_lib_version}'
    result = subprocess.run(command, shell=True, capture_output=True)
    is_exist = result.returncode == 0
else:
    print("eo_lib_version was not set to sys.argv")
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    env = f'is_exist={"true" if is_exist else "false"}'
    myfile.write(env)
    print(f'written to GITHUB_ENV "{env}"')
with open(env_file, "r") as file:
    print(f'Read from GITHUB_ENV {file.read()}')
print(f'Added to env: {is_exist}')
