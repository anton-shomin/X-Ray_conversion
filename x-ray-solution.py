from src import xml_pretifier, excel_to_xml_converter, test_case_updater, xml_to_cases_splitter
import xml_to_csv_converter
import argparse

def main(dir_path):
    label = ''
    excel_to_xml_converter.main(dir_path)
    xml_pretifier.remove_none_cells(dir_path)
    xml_pretifier.remove_empty_rows(dir_path)
    label = xml_pretifier.clear_test_case_info_sheet(dir_path)
    # print(label)
    # xml_to_cases_splitter.split_cases(dir_path)
    # test_case_updater.tc_maker(dir_path, label)
    # xml_to_csv_converter.xml_to_csv(dir_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, help="Directory path where the files are located")
    args = parser.parse_args()
    main(args.path)