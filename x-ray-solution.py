from src import xml_pretifier, excel_to_xml_converter, test_case_updater, xml_to_cases_splitter

# get general label for all test cases in a file
label = ""
dir = "/Users/antonshomin/Projects/X-RAY challenge/check-tests"

excel_to_xml_converter.main(dir)
xml_pretifier.remove_none_cells(dir)
xml_pretifier.remove_empty_rows(dir)
label = xml_pretifier.clear_test_case_info_sheet(dir)
print(label)
xml_to_cases_splitter.split_cases(dir)
test_case_updater.tc_maker(dir, label)
