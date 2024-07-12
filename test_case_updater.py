import os
import xml.etree.ElementTree as ET
import re

# for all xml files in the directory


def dummy_text_replacer():
    # replace text in all cells with "lorem ipsum" with "dolor sit amet"

    pass


def description_maker():
    # if there's "prerequisites" cell and cell next to it in the same row not empty get text from both of them, create tag <description> and move this data to it
    description_text = ""
    return description_text


def test_case_tag_creator(dir_path, old_tag, new_tag):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                tree = ET.parse(file_path)
                root = tree.getroot()

                new_element = ET.Element(new_tag)

                for old_element in root.iter(old_tag):
                    if old_element.attrib.get('name').lower() != "test case info":
                        old_element.append(new_element)

                tree.write(file_path)


def get_labels(dir_path):
    pass


def restructure_cases(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)

                tree = ET.parse(file_path)
                root_element = tree.getroot()

                for worksheet in root_element.findall('.//worksheet'):
                    name_attrib = worksheet.attrib.get('name', '')
                    if 'checklist' not in name_attrib.lower() and 'test case info' not in name_attrib.lower():
                        forward_rows = []
                        previous_rows = []
                        step_found = False

                        for row in worksheet.findall('.//row'):
                            cell_texts = ''.join(cell.text for cell in row.findall('cell') if cell.text)
                            if re.search(r'Step\s+#', cell_texts, re.IGNORECASE):
                                if step_found and previous_rows:
                                    new_root = ET.Element('testcase')
                                    labels = ET.SubElement(new_root, 'labels')
                                    label = ET.SubElement(labels, 'label')
                                    label.text = name_attrib
                                    for add_row in previous_rows:
                                        new_root.append(add_row)
                                    new_dir_path = os.path.join(dir_path, os.path.splitext(file)[0])
                                    os.makedirs(new_dir_path, exist_ok=True)

                                    file_num = 1
                                    while os.path.exists(os.path.join(new_dir_path, f"{name_attrib}{file_num}.xml")):
                                        file_num += 1

                                    new_tree = ET.ElementTree(new_root)
                                    new_tree.write(os.path.join(new_dir_path, f"{name_attrib}{file_num}.xml"))
                                previous_rows = forward_rows.copy()
                                previous_rows.append(row)
                                step_found = True
                            else:
                                if step_found:
                                    previous_rows.append(row)
                                    forward_rows = [row]
                                else:
                                    if 'prerequisites' in cell_texts:
                                        forward_rows.append(row)
                                    elif len(forward_rows) == 2:
                                        forward_rows.pop(0)
                                        forward_rows.append(row)
                                    else:
                                        forward_rows.append(row)



