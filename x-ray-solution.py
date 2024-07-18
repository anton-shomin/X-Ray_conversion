import glob
import os
import json
from src import xml_pretifier, excel_to_xml_converter, test_case_updater, xml_to_cases_splitter
import xml_to_csv_converter
import argparse

def remove_files_in_directory(dir_path, extension):
    """
    Removes all files with specified extension in directory.

    Args:
        dir_path (str): The path to the directory.
        extension (str): The extension of the files to remove.
    """
    # Ensure extension variable is properly formatted
    if not extension.startswith('.'):
        extension = '.' + extension

    # Search for all files with the specified extension and remove them
    for file in glob.glob(os.path.join(dir_path, '*' + extension)):
        os.remove(file)

def get_path_data_from_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data['path'], data['repository_path']

def main(dir_path,path_to_repository):
    label = ''
    excel_to_xml_converter.main(dir_path)
    xml_pretifier.remove_none_cells(dir_path)
    xml_pretifier.remove_empty_rows(dir_path)
    label = xml_pretifier.clear_test_case_info_sheet(dir_path)
    print(label)
    xml_to_cases_splitter.split_cases(dir_path)
    test_case_updater.tc_maker(dir_path, label)
    xml_to_csv_converter.xml_to_csv(dir_path, path_to_repository)
    remove_files_in_directory(dir_path, 'xml')
    remove_files_in_directory(dir_path, 'xlsx')

if __name__ == '__main__':
    path, repository_path = get_path_data_from_json('path_config.json')
    main(path, repository_path)