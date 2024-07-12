import excel_to_xml_converter
import xml_pretifier
import test_case_updater

dir = "/Users/antonshomin/Projects/X-RAY challenge/check-tests"
excel_to_xml_converter.main(dir)
xml_pretifier.main(dir)
test_case_updater.test_case_tag_creator(dir, "worksheet", "testcases")
test_case_updater.restructure_cases(dir)
