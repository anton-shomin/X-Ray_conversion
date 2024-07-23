import os
import xml.etree.ElementTree as ET
import re


def create_sub_xml(name, buffer, case_count, dir_path):
  """
  Create a sub-XML file with the given name, buffer, case count, and directory path.

  Parameters:
  - name (str): The name of the sub-XML file.
  - buffer (list): The list of lines to be written to the sub-XML file.
  - case_count (int): The count of the case.
  - dir_path (str): The path to the directory where the sub-XML file will be saved.

  Returns:
  None
  """
  if buffer:
    root = ET.Element('testcase')
    for line in buffer:
      root.append(line)
    tree = ET.ElementTree(root)
    tree.write(os.path.join(dir_path, f"{name}_{case_count}.xml"))


def split_cases(dir_path):
  """
  Splits cases in XML files based on certain conditions and creates sub-XML files.

  Parameters:
  - dir_path (str): The directory path containing the XML files.

  Returns:
  None
  """
  for filename in os.listdir(dir_path):
    if filename.endswith('.xml'):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()
      for ws in root.findall('worksheet'):
        name = ws.get('name')
        if "checklist" not in name.lower() and "test case info" not in name.lower():
          rows = ws.findall('row')
          buffer, case_count = [], 0
          for i, row in enumerate(rows):
            cell = row.find('cell')
            if cell is not None and re.search(r"Case\s+\d+[a-zA-Z]*", cell.text):
              create_sub_xml(name, buffer, case_count, dir_path)
              buffer = [rows[i - 1]] if i > 0 and ("prerequisites" in rows[i - 1].text.lower(
              ) or "pre-requisites" in rows[i - 1].text.lower()) else []
              case_count += 1
            buffer.append(row)
          create_sub_xml(name, buffer, case_count, dir_path)
