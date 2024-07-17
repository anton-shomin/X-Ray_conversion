import os
import xml.etree.ElementTree as ET
import re


def create_sub_xml(name, buffer, case_count, dir_path):
  if buffer:
    root = ET.Element('testcase')
    for line in buffer:
      root.append(line)
    tree = ET.ElementTree(root)
    tree.write(os.path.join(dir_path, f"{name}_{case_count}.xml"))


def split_cases(dir_path):
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
