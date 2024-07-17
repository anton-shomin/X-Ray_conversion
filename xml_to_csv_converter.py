import os
import csv
import xml.etree.ElementTree as ET
import re

def xml_to_csv(dir_path):
  csv_file_name = os.path.split(os.path.abspath(dir_path))[-1]  # get parent directory name
  csv_file_path = os.path.join(dir_path, f"{csv_file_name}.csv")

  try:
    with open(csv_file_path, mode='w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["Issue Id", "Test Summary", "Description", "Action", "Data", "Result",
                       "Labels", "Labels", "Labels"])
      for i, filename in enumerate(os.listdir(dir_path), start=1):
        if filename.endswith(".xml"):
          tree = ET.parse(os.path.join(dir_path, filename))
          root = tree.getroot()

          summary_element = root.find('.//summary/cell')
          summary = summary_element.text if summary_element is not None else ""

          description_element = root.find('.//description')
          description = description_element.text if description_element is not None else ""

          label_elements = root.findall('.//label')
          file_label = os.path.splitext(filename)[0]  # Remove extension
          file_label = re.sub(r'_\d+$', '', file_label)  # Remove _number at the end
          xml_labels = [elem.text for elem in label_elements if elem.text is not None]
          labels = [file_label] + xml_labels
          labels = labels[:3] + [""] * (3 - len(labels))  # Ensure 3 labels

          steps = root.findall('.//step')

          for j, step in enumerate(steps):
            action_element = step.find('action')
            action = action_element.text if action_element is not None else ""

            result_element = step.find('result')
            result = result_element.text if result_element is not None else ""

            data_element = step.find('data')
            data = data_element.text if data_element is not None else ""

            writer.writerow([i, summary if j == 0 else "", description if j == 0 else "",
                             action, data, result] + labels) # Write all fields and labels for all steps

  except Exception as e:
    print(f"An error occurred: {str(e)}")
