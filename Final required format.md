python script to get data from excel files to xml. Name of xml files should correspond to the name of source excel file.

"Test Case info" sheet

row with "Test ID" (not case sensitive) - copy this cell and neighboring. Put them to tag <caseId>

row with "Test Case Purpose"(not case sensitive) - copy this cell and neighboring. Put them to tag <casePurpose>

All other cases if sheet name does not contain word "checklist"

copy data to such structure

`<testCase>`
`<caseId> data from cell "Case X" where X is number</caseId>`
`<summary>data from cell next to Case X in the same row</summary>`
`<description>cell with word "prerequisites" one row before current Case X + data from cell next to Prerequisites in the same row </description>`
`next go row by row and get data from row with words Step # Test Steps  Expected Results Comments (skip this row)`
`<steps>`
`<stepNo>data from cell in column B</stepNo>`
`<stepDesc>data from cell in column C</stepDesc>`
`<stepData>data from column E </stepData>`
`<stepResult>data from cell in column D</stepResult>`
`</steps>`
`</testCase>`

test case end is empty row

continue parsing excel file till the next Case X row

cases from each sheet should be added to tag <worksheet></worksheet>
