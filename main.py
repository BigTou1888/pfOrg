import os
#import shutil
import mimetypes
import re
import pymysql

pn_re = re.compile(r"([A-Za-z0-9_-]+-*[A-Za-z0-9_-]+) .*")

DIR_LIST = ["F:/名优分类", "E:/Download", "G:/tmp/bt" ]

pn_path = {}

def find_movie(dir):
  for root, dirs, files in os.walk(dir):
    '''
    for sub_dir in dirs:
      find_movie(os.path.join(dir, sub_dir))
    '''
    parent_dir = os.path.split(root)[-1]

    video_found = False 
    for file in files:
      file_path = os.path.join(root, file)

      (ftype, fencoding) = mimetypes.guess_type(file_path)
      if ftype is not None and ftype.startswith('video'):
        video_found = True
        print('-------------------------------------------------------')
        print('File Path:' + os.path.join(root, file))
        print(f"Movie File:{file}")
        print('-------------------------------------------------------')
    
    if video_found:
      m = pn_re.match(parent_dir)
      if m:
        pn = m.group(1)
        print ('find PN: {}'.format(pn))
        if pn not in pn_path:
          pn_path[pn] = []
        if root not in pn_path[pn]:
          pn_path[pn].append(root)
      else:
        if 'unknown' not in pn_path:
          pn_path['unknown'] = []
        if root not in pn_path['unknown']:
          pn_path['unknown'].append(root)

for dir in DIR_LIST:
  find_movie(dir)

f = open("duplicate.txt", "w", encoding="utf-8")
for pn in pn_path:
  if len(pn_path[pn]) > 1:
    f.write('duplicate {}\n'.format(pn))
    for film in pn_path[pn]:
        
      f.write('  {}\n'.format(film))
      for root, dirs, files in os.walk(film):
        for file in files:
          file_path = os.path.join(root, file)

          (ftype, fencoding) = mimetypes.guess_type(file_path)
          if ftype is not None and ftype.startswith('video'):
            f.write('    {}: {}G\n'.format(file_path, os.path.getsize(file_path)/1000000000.0))