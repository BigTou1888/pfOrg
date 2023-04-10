import os
import shutil

DIR_LIST = []

for dir in DIR_LIST:
  os.chdir(dir)  path = os.path.abspath(r'.\Movie_files')
  for p, d, f in os.walk(r'C:\Users\carte\Downloads'):
    for file in f:
      if file.endswith('.mp4') or file.endswith('.mkv'):
        print('-------------------------------------------------------')
        print('File Path:' + os.path.abspath(file))
        print(f"Movie File:{file}")
        print('-------------------------------------------------------')
        movie_file_path =os.path.abspath(file)
        shutil.move(movie_file_path, path)