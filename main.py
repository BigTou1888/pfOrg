import os
import shutil

DIR_LIST = ["F:\名优分类"]

def find_movie(dir):
  for root, dirs, files in os.walk(dir):
    for sub_dir in dirs:
      find_movie(os.path.join(dir, sub_dir))
    for file in files:
      if file.endswith('.mp4') or file.endswith('.mkv'):
        print('-------------------------------------------------------')
        print('File Path:' + os.path.join(root, file))
        print(f"Movie File:{file}")
        print('-------------------------------------------------------')
for dir in DIR_LIST:
  find_movie(dir)


