import os
import mimetypes
import re

pn_re = re.compile(r"([A-Za-z0-9_-]+-*[A-Za-z0-9_-]+) .*")

#DIR_LIST = ["F:/名优分类", "E:/Download", "G:/tmp/bt" ]


def find_jp_movie(root_dir:str, stop_dirs:tuple=(), skip_dirs:list=[]) -> dict:
  '''
    find japanese movie, traverse the dir, find the folder contains video 
      Arguments
      ---------
        root_dir - root directory start traversing
        stop_dirs - directory list, stop traverse when meet the directory
        skip_dirs - directory list, skip finding video in the directory, but keep on traverse the sub directory
      Returns
      ---------
        r - movies found

  '''
  r = {"known":{}, "unknown": {}}
  
  for dirpath, sub_dirs, files in os.walk(root_dir):
    folder = os.path.split(dirpath)[-1]
    if dirpath.startswith(stop_dirs):
      continue

    if dirpath not in skip_dirs:

      video_found = False 
      for file in files:
        file_path = os.path.join(dirpath, file)
 
        (ftype, fencoding) = mimetypes.guess_type(file_path)
        if ftype is not None and ftype.startswith('video'):
          video_found = True
          print('-------------------------------------------------------')
          print('File Path:' + os.path.join(dirpath, file))
          print(f"Movie File:{file}")
          print('-------------------------------------------------------')
     
      if video_found:
        m = pn_re.match(folder)
        if m:
          pn = m.group(1)
          r["known"][folder] = {"PN": pn, "loc": dirpath, "files": files, "dirs": dirs}
     
        else:
          r["unknown"][folder] = {"PN": "", "loc": dirpath, "files": files, "dirs": dirs}
   
  return r
