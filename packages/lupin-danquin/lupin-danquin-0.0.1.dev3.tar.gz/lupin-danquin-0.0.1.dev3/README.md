# Documentation extraction

## Purpose

"documentation_extraction.py" Python script allow to create SDD documentation from source code.

## Run it

1. Go to current directory.
2. Execute
> python documentation_extraction.py
3. Result is available in "./val3_documentation.md"

## Add documentation

### For a program (pgx file)

Edit your program and add one or more lines of comments the line after "begin" keyword.

### For an application

Create a text file named "README.md" at the same level as "pjx" file. And add one or more lines of description.

## Improvements oportunities

- Improve table for sockets
- Allow to end docstring with 10 * "/"

## Other ideas

To create a sanitizer:

- detect unused variables (private, public?): already done for local variables and parameters (not global variables)
- detect wrongly named variables (l_, x_, s/b/n/st, t, Out): DONE
- validate plantuml diagram from pjx files
- code coverage ? find if all return values are tested
