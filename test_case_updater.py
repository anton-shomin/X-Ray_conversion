import os
import re
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
    tree = ET.parse(os.path.join(dir_path, base_filename + "_0.xml"))
    root = tree.getroot()
    return root.find('description')


def add_description(dir_path):
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
    for filename in os.listdir(dir_path):
        if filename.endswith(".xml") and (filename.endswith("_0.xml") or not re.search(r'\d+.xml$', filename)):
            os.remove(os.path.join(dir_path, filename))
