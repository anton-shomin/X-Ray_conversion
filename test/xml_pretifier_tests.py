# Removes rows without "test id" or "test case purpose" from 'Test Case info' sheet
import * from ./xml_pretifier


def test_removes_rows_without_test_id_or_purpose(self, tmpdir):
    # Create a temporary XML file with a 'Test Case info' sheet
    xml_content = '''<workbook>
                            <worksheet name="Test Case info">
                                <table>
                                    <row><cell>Test ID</cell></row>
                                    <row><cell>Some other data</cell></row>
                                    <row><cell>Test Case Purpose</cell></row>
                                </table>
                            </worksheet>
                         </workbook>'''
    xml_file = tmpdir.join("test.xml")
    xml_file.write(xml_content)

    # Run the function
    clear_test_case_info_sheet(tmpdir)

    # Parse the modified XML file
    tree = ET.parse(str(xml_file))
    root = tree.getroot()

    # Check that only the rows with "Test ID" or "Test Case Purpose" remain
    rows = root.find(
        ".//worksheet[@name='Test Case info']/table").findall('row')
    assert len(rows) == 2
    assert any(
        "Test ID" in cell.text for row in rows for cell in row.findall('cell'))
    assert any(
        "Test Case Purpose" in cell.text for row in rows for cell in row.findall('cell'))
    # Directory contains no XML files

    def test_directory_contains_no_xml_files(self, tmpdir):
        # Create a temporary directory with no XML files
        non_xml_file = tmpdir.join("test.txt")
        non_xml_file.write("This is a text file.")

        # Run the function
        clear_test_case_info_sheet(tmpdir)

        # Check that the non-XML file is still there and unchanged
        assert non_xml_file.read() == "This is a text file."
