"""
This file is used to generate all the autotest-able testcase from codebeamer.

Please make sure the account have REST API permission.

@Author: Siwei.Lu
@Date: 2023.3.16
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from cb_related.codebeamer_connect import CodeBeamerHandler

project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\project'
retry_times = 3
projects = os.listdir(project_path)
print("\nThis tool is used to generate all the autotest-able testcase from codebeamer.\n")
print("All project show as following:")

for index, project in enumerate(projects):
    print("{index}:{project}".format(index=index + 1, project=project))

print("Choose the number of project:")
for i in range(retry_times):
    try:
        line = input()
        print("Enter codebeamer Account name:")
        name = input()
        print("Enter codebeamer Password:")
        password = input()

        project_name = projects[int(line)-1]
        print("\n{}: Start create test case file...".format(project_name))

        cb = CodeBeamerHandler(project_name, name, password)
        cb.write_case_to_py()

        print("\n{}: test case write successfully! \n".format(project_name))

        break
    except BaseException as err:
        print("Please choose the correct number!", err)


