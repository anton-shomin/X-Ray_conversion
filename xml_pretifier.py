# for all xml files in the directory

import os
import xml.etree.ElementTree as ET

# remove cells with text "None" in it


def remove_none_cells(dir_path):
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
    labels = ""
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
                                    labels = cells[i+1].text
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
    return labels
