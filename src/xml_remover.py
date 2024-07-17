#remove all xml files in the directory and sub-directories
import os

root_dir = "/Users/antonshomin/Downloads/CPS Projects"

def remove_xml_files(dir_path):
  for root, dirs, files in os.walk(dir_path):
    for file in files:
      if file.endswith(".xml"):
        os.remove(os.path.join(root, file))

def main():
  remove_xml_files(root_dir)

if  __name__ == "__main__":
  main()

