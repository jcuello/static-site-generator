import sitehelpers
import sys

def main():
  basepath = "/"
  if len(sys.argv) > 1:
    basepath = sys.argv[1]

  sitehelpers.copy_dir("./static", f"./docs")  
  sitehelpers.generate_pages_recursive("content", "template.html", f"./docs", basepath)

if __name__ == "__main__":
  main()