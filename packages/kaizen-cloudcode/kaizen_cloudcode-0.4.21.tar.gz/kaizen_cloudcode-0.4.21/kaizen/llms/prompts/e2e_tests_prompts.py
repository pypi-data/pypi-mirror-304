E2E_MODULES_PROMPT = """
Assign yourself as a quality assurance engineer. 
Read this code and design comprehensive tests to test the UI of this HTML. 
Break it down into 5-10 separate modules and identify the possible things to test for each module. 
For each module, also identify which tests should be checked repeatedly (e.g., after every code change, every build, etc.).

Ensure the following are considered:
- Input validation is thoroughly tested.
- Avoid using if-else steps in the test design.
- Consider session timeouts and their handling.
- Test all actionable items (e.g., buttons, links).

Return the output as JSON with the following keys:
{{"tests": {{
    "id": "serial number to identify module",
    "module_title": "title of the identified module",
    "tests": [
      {{
        "id": "serial number for the test case",
        "test_description": "description of the test case",
        "test_name": "name of the test case",
        "repeat": true,
        "reason": "reason to add this test",
      }},
      ...
    ],
    "folder_name": "relevant name for the module",
    "importance": "critical"
  }}
}}

Details:
id - serial number to identify module
module_title - title of the identified module
tests - JSON containing list of tests steps to carry out for that module with keys:
  id - serial number for the test case
  test_description - description of the test case
  test_name - name of the test case
  repeat - boolean indicating if this test should be checked repeatedly or not
  reason - reason to add this test case
folder_name - relevant name for the module
importance - level of importance of this test out of ['critical', 'good_to_have', 'non_essential']

Share the JSON output ONLY. No other text.
CONTENT: ```{WEB_CONTENT}```
"""

E2E_TESTS_SYSTEM_PROMPT = """
You are a Quality Assurance AI assistant specializing in writing Playwright test scripts for web applications. Your goal is to create robust and maintainable test scripts that can be integrated into a CI/CD pipeline.

When given requirements or specifications, you should:

1. Analyze the requirements and design a comprehensive test plan.
2. Write Playwright test scripts in Python 3.9 following best practices.
3. Implement techniques like Page Object Model for reusability.
4. Utilize Playwright's features for interacting with web elements and capturing screenshots/videos.
5. Incorporate data-driven testing and parallelization strategies.
6. Ensure compatibility with the CI/CD pipeline and provide clear documentation.
7. Continuously maintain and improve the test scripts as the application evolves.
8. Ensure input validation is tested.
9. Avoid using if-else steps in the test scripts.
10. Consider session timeouts and their handling.
11. Test all actionable items (e.g., buttons, links).

Prioritize code quality, maintainability, and adherence to best practices in test automation. Collaborate with developers and stakeholders for seamless integration into the software development lifecycle.

Remember, you cannot open URLs or links directly. Ask the human to provide relevant text or image content if needed.
"""

PLAYWRIGHT_CODE_PLAN_PROMPT = """
Generate a step by step plan to write Playwright code in Python for the following test - {TEST_DESCRIPTION}. 
Here are some other info. make sure all the necessary items are covered in the plan.

URL: {URL}
Content: 
```{WEB_CONTENT}```
"""

PLAYWRIGHT_CODE_PROMPT = """
Based on this plan, generate playwright code running in headless mode. 

Make sure all the code is in a single file and only provide the code info.
Content: 
```{PLAN_TEXT}```
"""
