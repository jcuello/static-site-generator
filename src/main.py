import sitehelpers

def main():
  sitehelpers.copy_dir("./static", "./public")
  sitehelpers.generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
  main()