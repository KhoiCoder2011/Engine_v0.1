import subprocess
import build_config

config = build_config.config

folder_name = config['folder_name']
exe_name = config['exe_name']
path = config['path']

print('Run tool.')

subprocess.run([f'{path}/{folder_name}/{exe_name}.exe'])
