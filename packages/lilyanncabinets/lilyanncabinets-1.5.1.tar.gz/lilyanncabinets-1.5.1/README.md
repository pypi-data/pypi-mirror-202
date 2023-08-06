Version 1.5.1

patch notes: 
===========================================================================
- [1.5.1]: "Creating a new "build" added an auto spreadsheet creating and updating function for use with both robot and manual data tracking, 

- added createNewSheet(): to create the sheet (names the sheet the current date)

- added writeToSheet(): Use to write data to the created sheet although running "createNewSheet()" is not required as the function will create one if a sheet under the current date cannot be located. Format for the function is writeToSheet(Row, Column, data)

===========================================================================

- [0.5.2]: "Added equations for "limelight" functions"

===========================================================================

- [0.5.1]: "Started Unstable build 0.5"

===========================================================================

reminder to py -m build
and py -m twine upload --repository pypi dist/*