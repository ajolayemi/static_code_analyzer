A simple static code analyser written as one of HyperSkill's project. 
As the name implies, it analises python scripts making use of regular expressions and AST nodes. 
It checks that the following part of python complies with PEP 8 rules:
1. That statements doesn't end with unnecessary semicolons
2. That there are at least two spaces when before an inline comments
3. That function names follow the snake_case naming convention
4. That classes names follow the CamelCase naming convention
5. That the names of function parameters follow the snake_case naming convention
6. That the default arguments of function parameters are immutable data type, i.e they aren't a list, set or dict.
7. For the presence of more than 2 blank lines between lines of codes. 
8. For the presence of comments with TODO
9. That variables inside a function body are named according to snake_case naming convention. 
