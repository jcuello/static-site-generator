import os
import shutil
import helpers
from pathlib import Path

def copy_dir(src_path:str, dest_path:str, confirm_delete=True) -> None:
  abs_src_path, abs_dest_path = os.path.abspath(src_path), os.path.abspath(dest_path)
  if not os.path.exists(abs_src_path):
    raise Exception(f"source path '{abs_src_path}' does not exist")
  
  if not os.path.isdir(abs_src_path):
    raise Exception(f"source path '{src_path}' is not a directory")
  
  if confirm_delete:
    while True:
      confirm_deletion = input(f"Do you want to delete ALL contents in directory '{abs_dest_path}'? (y/n) ").strip()
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

def extract_title(markdown:str) -> str:
  if  markdown == None or len(markdown) == 0:
    raise ValueError("markdown is required")

  if markdown.startswith("# "):
    return markdown.split("\n")[0].lstrip("# ").rstrip()
  
  raise Exception("no header (h1) found")

def generate_page(from_path:str, template_path:str, dest_path:str, basepath="/") -> None:
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  markdown: str = ""
  with open(from_path) as f:
    markdown = f.read()
  
  template: str = ""
  with open(template_path) as f:
    template = f.read()

  html = helpers.markdown_to_html_node(markdown).to_html()
  title_page = extract_title(markdown)
  template = template.replace("{{ Title }}", title_page).replace("{{ Content }}", html)
  template = template.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
  dest_dir = os.path.dirname(dest_path)

  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  with open(dest_path, "w") as f:
    f.write(template)

def generate_pages_recursive(dir_path_content:str, template_path:str, dest_dir_path:str, basepath="/"):
  content_dir = Path(dir_path_content)
  for item in content_dir.rglob("*"):
    abs_item_path = str(item.resolve())
    if os.path.isfile(abs_item_path):
      #TODO: Fix this (eventually), it works but there has to be a better way??
      root_content_dir = os.path.dirname(str(item)).replace(dir_path_content, "./")
      abs_dest_path = os.path.abspath(os.path.join(dest_dir_path, root_content_dir, f"{item.stem}.html"))
      generate_page(abs_item_path, template_path, abs_dest_path, basepath)
