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


def remove_prerequisites(dir_path):
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
