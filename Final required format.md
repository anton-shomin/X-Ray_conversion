python script to get data from excel files to xml. Name of xml files should correspond to the name of source excel file.

"Test Case info" sheet
row with "Test ID" (not case sensitive) - copy this cell and neighboring. Put them to tag <caseId>
row with "Test Case Purpose"(not case sensitive) - copy this cell and neighboring. Put them to tag <casePurpose>
All other cases if sheet name does not contain word "checklist"
copy data to such structure

`<issues>`
`<issue id="1">`
`<summary>Here's the best summary here for case one</summary>`
`<description>here's the best description here for case one</description>`
`<steps>`
`<step>`
`<action>step one</action>`
`<data>some data for this step one</data>`
`<result>result one</result>`
`<label>Label one</label>`
`</step>`
`<step>`
`<action>step two</action>`
`<data>some data for this step two</data>`
`<result>result two</result>`
`</step>`
`<step>`
`<action>step three</action>`
`<data>data for step three</data>`
`<result>result three</result>`
`</step>`
`</steps>`
`</issue>`
`<issue id="2">`
`<summary>Here's the best summary here for case two</summary>`
`<description>here's the best description here for case two</description>`
`<steps>`
`<step>`
`<action>case two step one</action>`
`<data>some data for this step one case 2</data>`
`<result>expected result for case two step one</result>`
`<label>label one</label>`
`</step>`
`<step>`
`<action>case two step 2</action>`
`<data>some data for this step two case 2</data>`
`<result>expected result for case two step 2</result>`
`</step>`
`<step>`
`<action>case two step 3</action>`
`<data>some data for this step 3 case 2</data>`
`<result>expected result for case two step 3</result>`
`</step>`
`<step>`
`<action>case two step 4</action>`
`<data>some data for this step 4 case 2</data>`
`<result>expected result for case two step 4</result>`
`</step>`
`</steps>`
`</issue>`
`</issues>`
