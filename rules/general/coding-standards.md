# Code Standards

General instructions (as rules, exceptions may exist) for all technologies and stacks:

- Follow principles:
  -  KISS (Keep It Simple Stupid)
  -  DRY (Don't repeat yourself)
  -  Single Responsibility Principle
  -  YAGNI (You Ain't Gonna Need It)
- Avoid overengineering
- Keep documentation and comments up to date
- Tests should always be created first, then the code
- The resulting code should pass all the tests, including existing ones
- Guarantee small functions (< 30 lines)
- When naming functions:
  - use explicit naming — verb + noun/noun phrase structure, for example, `calculateTotalPrice` or `validateEmailAdress`
  - be descriptive: prefer `calculateTotalPrice` over a vague `calculateTotal` or `doCalculation`
