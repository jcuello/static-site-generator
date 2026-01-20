import os
import shutil

def copy_dir(src_path:str, dest_path:str, confirm_delete=False) -> None:
  abs_src_path, abs_dest_path = os.path.abspath(src_path), os.path.abspath(dest_path)
  if not os.path.exists(abs_src_path):
    raise Exception(f"source path '{abs_src_path}' does not exist")
  
  if not os.path.isdir(abs_src_path):
    raise Exception(f"source path '{src_path}' is not a directory")
  
  if confirm_delete:
    while True:
      confirm_deletion = input(f"Do you want to delete ALL contents in directory '{abs_dest_path}'? (y/N) ").strip()
      if len(confirm_deletion) == 0:
        continue
      
      first_letter = confirm_deletion[0].lower()
      if first_letter == 'y':
        break

      if first_letter == 'n':
        print("Cancelled deletion, aborting!")
        exit()
  
  if os.path.exists(abs_dest_path):
    if not os.path.isdir(abs_dest_path):
      raise Exception(f"destination path '{abs_dest_path}' is not a directory")
    shutil.rmtree(abs_dest_path)
  
  os.mkdir(abs_dest_path)
  
  def copy_files(ls_items:list[str], src, dest):
    for item in ls_items:
      abs_item_src = os.path.join(src, item)
      abs_item_dest = os.path.join(dest, item)

      if os.path.isfile(abs_item_src):
        print(f"copying '{abs_item_src}' -> '{abs_item_dest}'")
        shutil.copy(abs_item_src, abs_item_dest)
      else:
        os.mkdir(abs_item_dest)
        copy_files(os.listdir(abs_item_src), abs_item_src, abs_item_dest)

  copy_files(os.listdir(abs_src_path), abs_src_path, abs_dest_path)

