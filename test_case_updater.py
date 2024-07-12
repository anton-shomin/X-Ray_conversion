import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse


def description_maker(dir_path):
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


def remove_header(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".xml"):
                tree = parse(os.path.join(root, file))
                root_element = tree.getroot()

                for row in root_element.findall(".//row"):
                    cell_texts = [cell.text for cell in row.findall(
                        "cell") if cell.text]
                    if cell_texts == ['Step #', 'Test Steps', 'Expected Results', 'Comments']:
                        # Remove this row from its parent
                        parent = root_element.findall(".")[0]
                        parent.remove(row)


def add_description(dir_path):
    pass
