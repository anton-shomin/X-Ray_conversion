import os
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

# Obsolete method for now
# def test_case_tag_creator(dir_path, old_tag, new_tag):
#     for root, dirs, files in os.walk(dir_path):
#         for file in files:
#             if file.endswith(".xml"):
#                 file_path = os.path.join(root, file)
#                 tree = ET.parse(file_path)
#                 root = tree.getroot()

#                 new_element = ET.Element(new_tag)

#                 for old_element in root.iter(old_tag):
#                     if old_element.attrib.get('name').lower() != "test case info":
#                         old_element.append(new_element)

#                 tree.write(file_path)


def description_maker(dir_path):
  """
  Generates a description tag for each XML file in the given directory that ends with "_0.xml".

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None

  This function iterates over each file in the given directory. If a file ends with "_0.xml", it parses the XML file
  and creates a new 'description' tag. It then searches for rows in the XML file that contain a cell with the text
  "prerequisites" (case-insensitive) and sets the text of the 'description' tag to the joined text of all cells in
  that row. Finally, it writes the modified XML file back to disk.
  """
  for filename in os.listdir(dir_path):
    if filename.endswith("_0.xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()
      description = ET.SubElement(root, 'description')
      for row in root.findall('row'):
        cell = row.find('cell')
        if cell is not None and "prerequisites" in cell.text.lower():
          description.text = ' '.join(
            c.text for c in row.findall('cell'))
      tree.write(os.path.join(dir_path, filename))


def add_labels(dir_path, label):
  """
  A function that adds a new tag <label> with the specified text to all XML files in the specified directory.

  Args:
      dir_path (str): The path to the directory containing the XML files.
      label (str): The specified text to be added as the content of the <label> tag.

  Returns:
      None
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()
      ET.SubElement(root, 'label').text = label
      tree.write(os.path.join(dir_path, filename))
  pass


def remove_header(dir_path):
  """
  Removes the header row in XML files that meet specific criteria in the given directory.

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None
  """
  for filename in os.listdir(dir_path):
    if re.search(r"_\d+.xml$", filename) and not filename.endswith("_0.xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()

      for row in root.findall('row'):
        cells = row.findall('cell')
        if len(cells) == 4 and cells[0].text == "Step #" and cells[1].text == "Test Steps" and cells[2].text == "Expected Results" and cells[3].text == "Comments":
          root.remove(row)

      tree.write(os.path.join(dir_path, filename))


def get_description_tag(dir_path, base_filename):
  """
  Retrieves the 'description' tag from the XML file located in the specified directory.

  Args:
      dir_path (str): The path to the directory containing the XML file.
      base_filename (str): The base name of the XML file.

  Returns:
      Element: The 'description' tag element from the XML file, or None if it is not found.
  """
  tree = ET.parse(os.path.join(dir_path, base_filename + "_0.xml"))
  root = tree.getroot()
  return root.find('description')


def add_description(dir_path):
  """
  Adds the description tag from the XML file located in the specified directory to all XML files with the same base filename.

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None
  """
  for base_filename in set(f.rstrip("_0.xml") for f in os.listdir(dir_path) if f.endswith("_0.xml")):
    description = get_description_tag(dir_path, base_filename)

    for filename in os.listdir(dir_path):
      if re.search(r"\d+.xml$", filename) and not filename.endswith("_0.xml") and filename.startswith(base_filename):
        tree = ET.parse(os.path.join(dir_path, filename))
        root = tree.getroot()

        # remove old description tag if exist
        old_description = root.find('description')
        if old_description is not None:
          root.remove(old_description)

        # add a new description tag
        new_description = ET.SubElement(root, 'description')
        new_description.text = description.text

        tree.write(os.path.join(dir_path, filename))

def clear_source(dir_path):
  """
  Clears the source directory by removing all XML files that meet specific criteria.

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None

  This function iterates over each file in the given directory. If a file ends with ".xml" and either ends with "_0.xml" or does not end with a number followed by ".xml", it is removed from the directory.
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml") and (filename.endswith("_0.xml") or not re.search(r'\d+.xml$', filename)):
      os.remove(os.path.join(dir_path, filename))

def remove_prerequisites(dir_path):
  """
  Removes rows from XML files in the given directory that contain cells with the text "prerequisites" or "pre-requisites" (case-insensitive).

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None

  This function iterates over each file in the given directory. If a file ends with ".xml", it parses the XML file and searches for rows that contain a cell with the text "prerequisites" or "pre-requisites" (case-insensitive). It removes these rows from the XML file and writes the modified XML file back to disk.
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()

      prerequisites_rows = [row for row in root.findall('row') if row.find('cell').text.lower(
      ) == "prerequisites" or row.find('cell').text.lower() == "pre-requisites"]
      for row in prerequisites_rows:
        root.remove(row)

      tree.write(os.path.join(dir_path, filename))

def summary_maker(dir_path):
  """
  Generates summary tags in XML files for rows that match a specific pattern.
  Args:
      dir_path (str): The path to the directory containing the XML files.
  Returns:
      None
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()

      for row in root.findall('row'):
        cells = row.findall('cell')
        if cells and re.match(r"Case\s+\d+[a-zA-Z]*", cells[0].text):
          # Remove the cell
          row.remove(cells[0])
          # rename row to summary
          row.tag = 'summary'
        if not cells:
          # if no cells, change row to summary
          row.tag = 'summary'

      tree.write(os.path.join(dir_path, filename))

def steps_creator(dir_path):
  """
  A function that creates steps in an XML file based on the content of the file.
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()

      description = root.find('description')
      root.remove(description)

      steps = ET.Element('steps')

      append_to_steps = False
      for element in list(root):
        if element.tag == 'summary':
          append_to_steps = True
          continue
        if append_to_steps:
          steps.append(element)
          root.remove(element)

      root.append(steps)
      root.append(description)

      tree.write(os.path.join(dir_path, filename))

def steps_polisher(dir_path):
  """
  Remove the first cell from each row in XML files in the given directory.

  Parameters:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None

  This function iterates over each file in the given directory. If a file ends with ".xml", it parses the XML file
  and removes the first cell from each row. The modified XML file is then written back to disk.

  The function uses the `os.listdir` function to get a list of files in the directory. It then iterates over each file
  and checks if it ends with ".xml". If it does, the function parses the XML file using the `ET.parse` function and
  retrieves the root element. It then iterates over each row in the XML file using the `iter` method. For each row, it
  finds the first cell using the `find` method and checks if it exists and its text matches the regular expression
  pattern `\d+`. If both conditions are met, the first cell is removed from the row using the `remove` method.

  Finally, the modified XML file is written back to disk using the `write` method.
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()

      for row in root.iter('row'):
        first_cell = row.find('cell')
        if first_cell is not None and re.fullmatch(r'\d+', first_cell.text):
          row.remove(first_cell)

      tree.write(os.path.join(dir_path, filename))

def steps_formatter(dir_path):
  """
  A function that formats the steps in an XML file by changing the tag from 'row' to 'step'.

  Parameters:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml"):
      xml_file = os.path.join(dir_path, filename)
      tree = ET.parse(xml_file)
      root = tree.getroot()

      for steps in root.findall('steps'):
        for row in steps.findall('row'):
          row.tag = 'step'

      # Save the modified xml
      tree.write(xml_file)

def steps_finalizer(dir_path):
  """
  Finalizes the steps in XML files located in the specified directory by changing the tag from 'cell' to 'action', 'result', or 'data' based on their index.

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None

  This function iterates over each file in the directory that ends with ".xml". It parses each XML file, finds all 'step' elements, and for each step, it finds all 'cell' elements. It then changes the tag of each 'cell' element to 'action', 'result', or 'data' based on its index. If a step has less than 3 'cell' elements, an empty 'data' element is added. Finally, the modified XML file is saved back to disk.
  """
  for filename in os.listdir(dir_path):
    if filename.endswith(".xml"):
      tree = ET.parse(os.path.join(dir_path, filename))
      root = tree.getroot()

      for step in root.iter('step'):
        cells = step.findall('cell')
        for i, cell in enumerate(cells):
          if i == 0:
            cell.tag = 'action'
          elif i == 1:
            cell.tag = 'result'
          elif i == 2:
            cell.tag = 'data'

        # if there's no <data> cell, add an empty one
        if len(cells) < 3:
          ET.SubElement(step, 'data')

      # Save the modified xml
      tree.write(os.path.join(dir_path, filename))

def tc_maker(dir_path, label):
  description_maker(dir_path)
  remove_header(dir_path)
  add_description(dir_path)
  clear_source(dir_path)
  summary_maker(dir_path)
  remove_prerequisites(dir_path)
  steps_creator(dir_path)
  steps_polisher(dir_path)
  steps_formatter(dir_path)
  add_labels(dir_path,label)
  steps_finalizer(dir_path)
