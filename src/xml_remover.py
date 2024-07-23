#remove all xml files in the directory and sub-directories
import os

root_dir = "/Users/antonshomin/Downloads/CPS Projects"

def remove_xml_files(dir_path):
  """
  Removes all XML files in the specified directory and its subdirectories.

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None
  """
  for root, dirs, files in os.walk(dir_path):
    for file in files:
      if file.endswith(".xml"):
        os.remove(os.path.join(root, file))

def main():
  remove_xml_files(root_dir)

if  __name__ == "__main__":
  main()

