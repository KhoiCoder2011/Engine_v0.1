import os
import shutil
import subprocess
from Manager.build_config import *
from Manager.render_time import Time


class EngineBuilder:
    def __init__(self):
        self.config = config
        self.exe_name = config['exe_name']
        self.folder_name = config['folder_name']
        self.time = Time()

    def copy_folder(self, src, dest):
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest)

    def delete_folder(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def build_executable(self):
        if os.path.exists('dist'):
            shutil.rmtree('dist')

        os.system(f'''pyinstaller --onefile\
                  --add-data "{self.config['gllib']};."\
                  {self.exe_name}.py
        ''')

    def cleanup(self):
        self.delete_folder('build')
        os.remove(f'{self.exe_name}.spec')

    def copy_assets(self):
        self.copy_folder(self.config['config'], 'dist/config')
        self.copy_folder(self.config['font'], 'dist/Font')
        self.copy_folder(self.config['shader'], 'dist/shaders')
        self.copy_folder(self.config['assets'], 'dist/assets')

    def rename_dist_folder(self):
        os.rename('dist', self.folder_name)

    def move_folder(self):
        self.delete_folder(self.config['path'] +
                           "/" + self.config['folder_name'])
        shutil.move(self.folder_name, self.config['path'])

    def open_executable(self):
        exe_path = f'{self.config["path"]}/{self.folder_name}/{self.exe_name}.exe'

        subprocess.run([exe_path])

    def run(self):
        self.time.start()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.build_executable()
        self.cleanup()
        self.copy_assets()
        self.rename_dist_folder()
        self.move_folder()

        self.time.end()

        print(f"Time elapsed: {self.time.get_time():.3f} seconds")
        print(f'Run the executable file in the {self.folder_name} folder')
        print(f'Open at: {self.config["path"]}/{self.folder_name}/{self.exe_name}.exe')

        self.open_executable()
