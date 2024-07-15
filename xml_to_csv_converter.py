import os
import csv
import xml.etree.ElementTree as ET
import re    # Regex module

def xml_to_csv(dir_path):
    csv_file_name = os.path.basename(dir_path)
    csv_file_path = os.path.join(dir_path, f"{csv_file_name}.csv")

    try:
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Issue Id", "Test Summary", "Description", "Action", "Data", "Result", "Label"])

            for i, filename in enumerate(os.listdir(dir_path), start=1):
                if filename.endswith(".xml"):
                    tree = ET.parse(os.path.join(dir_path, filename))
                    root = tree.getroot()

                    summary_element = root.find('.//summary/cell')
                    summary = summary_element.text if summary_element is not None else ""

                    description_element = root.find('.//description')
                    description = description_element.text if description_element is not None else ""

                    steps = root.findall('.//step')
                    label = os.path.splitext(filename)[0]    # Remove extension
                    label = re.sub(r'_\d+$', '', label)      # Remove _number at the end

                    for j, step in enumerate(steps):
                        action_element = step.find('action')
                        action = action_element.text if action_element is not None else ""

                        result_element = step.find('result')
                        result = result_element.text if result_element is not None else ""

                        data_element = step.find('data')
                        data = data_element.text if data_element is not None else ""

                        if j == 0:    # write summary, description and label only for the 1st step
                            writer.writerow([i, summary, description, action, data, result, label])
                        else:
                            writer.writerow([i, "", "", action, data, result, ""])
    except Exception as e:
        print(f"An error occurred: {str(e)}")


dir_path = "/Users/antonshomin/Downloads/CPS Projects/Email Notifications/A8N-1071 Welcome Email"


def main(dir_path):
    xml_to_csv(dir_path)


if __name__ == "__main__":
    main(dir_path)