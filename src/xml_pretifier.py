# for all xml files in the directory

import os
import xml.etree.ElementTree as ET
import re


# remove cells with text "None" in it


def remove_none_cells(dir_path):
  """
  Removes cells with text "None" in all XML files within the specified directory path.
  """
  for root, dirs, files in os.walk(dir_path):
    for file in files:
      if file.endswith(".xml"):
        file_path = os.path.join(root, file)
        tree = ET.parse(file_path)
        root = tree.getroot()
        for row in root.findall(".//row"):
          for cell in row.findall("cell"):
            if cell.text.lower() == "None".lower():
              row.remove(cell)
        tree.write(file_path)

# remove empty <row> tags


def remove_empty_rows(dir_path):
  """
  Removes empty rows from XML files within the specified directory path.

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      None

  This function traverses through all XML files in the specified directory path and removes empty rows from each file.
  An empty row is considered to have no child <cell> elements.

  The function uses the `os.walk` function to recursively iterate through all files in the directory and its subdirectories.
  For each XML file, it parses the file using the `ET.parse` function from the `xml.etree.ElementTree` module.
  It then finds all <worksheet> elements in the root element of the XML tree.
  For each <worksheet> element, it collects all empty <row> elements and stores them in the `rows_to_remove` list.
  After collecting all empty rows, it removes each row from its parent <worksheet> element.
  Finally, it saves the modified XML tree back to the file using the `tree.write` function.

  Note: This function assumes that each <row> element is nested inside a <worksheet> element. Adjust the code as per your actual XML structure.
  """
  for root, dirs, files in os.walk(dir_path):
    for file in files:
      if file.endswith(".xml"):
        file_path = os.path.join(root, file)
        tree = ET.parse(file_path)
        root_element = tree.getroot()

        # Assuming each <row> is nested inside a <worksheet>, adjust as per your actual structure
        for worksheet in root_element.findall('.//worksheet'):
          rows_to_remove = []

          # Collect all empty <row> elements
          for row in worksheet.findall('.//row'):
            if not row.findall("cell"):
              rows_to_remove.append(row)

          # Remove collected <row> elements
          for row in rows_to_remove:
            worksheet.remove(row)

        # Save the modifications
        tree.write(file_path)


def clear_test_case_info_sheet(dir_path):
  """
  Clears the "Test Case Info" sheet in all XML files within the specified directory path.

  Args:
      dir_path (str): The path to the directory containing the XML files.

  Returns:
      str: The text of the cell next to the last found "Test ID" cell, or an empty string if no "Test ID" cells are found.

  This function traverses through all XML files in the specified directory path and clears the "Test Case Info" sheet.
  It finds all worksheets in each XML file and checks if their name is case-insensitively equal to "Test Case Info".
  If a worksheet is found, it searches for rows that do not contain the required cell content "Test ID" or "Test Case Purpose".
  These rows are removed from the worksheet.
  The text of the cell next to the last found "Test ID" cell is returned.
  """
  label = []
  for root, dirs, files in os.walk(dir_path):
    for file in files:
      if not file.endswith(".xml"):
        continue

      file_path = os.path.join(root, file)
      tree = ET.parse(file_path)
      root_element = tree.getroot()

      for worksheet in root_element.findall(".//worksheet"):
        # Check worksheet name case-insensitively
        if worksheet.attrib.get('name', '').lower() == "test case info":
          rows_to_remove = []

          for row in worksheet.findall("row"):
            cells = row.findall("cell")
            keep_row = False

            for i in range(len(cells)):
              cell_text = cells[i].text.lower(
              ) if cells[i].text else ""
              # Check cell content case-insensitively
              if "test id" in cell_text:
                keep_row = True
                if i+1 < len(cells):  # Ensure next cell exists
                  # Get text of cell next to test id
                  labels_text = cells[i + 1].text
                  labels_list = re.split(",|\n|\s", labels_text)
                  label.extend([label.strip() for label in labels_list])
                break
              elif "test case purpose" in cell_text:
                keep_row = True
                break

            if not keep_row:
              rows_to_remove.append(row)

          # Remove rows that don't contain the required cell content
          for row in rows_to_remove:
            worksheet.remove(row)

        # Save the changes back to the file
        tree.write(file_path)
  return label
