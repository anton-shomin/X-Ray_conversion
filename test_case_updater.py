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


def process_XML(file_path, new_file):
    tree = ET.parse(file_path)
    root = tree.getroot()
    new_root = ET.Element('testcases')

    rows_to_add = []
    start_collecting = False

    for row in reversed(root.findall('.//row')):
        if 'Step #' in ''.join(cell.text for cell in row.findall('cell')):
            start_collecting = True
            rows_to_add.append(row)
        elif start_collecting:
            cell_texts = ''.join(
                cell.text for cell in row.findall('cell')).lower()

            # Search for 'Case X' or 'prerequisites' in the row
            if re.search(r'case\s\d+', cell_texts, re.IGNORECASE) or 'prerequisites' in cell_texts:
                rows_to_add.append(row)
            else:
                break

    testcase = ET.SubElement(new_root, 'testcase')
    for row in reversed(rows_to_add):
        testcase.append(row)

    new_tree = ET.ElementTree(new_root)
    new_tree.write(new_file)


def restructure_cases(dir_path):
    # locate row with cells Step #, Test Steps, Expected Results, Comments.
    # from "prerequisites" to "prerequisites" or from
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".xml"):
                process_XML(os.path.join(root, file), f"{
                            file.name}_restructured.xml")
