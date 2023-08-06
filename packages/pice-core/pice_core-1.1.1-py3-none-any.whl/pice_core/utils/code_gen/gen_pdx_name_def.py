"""
This file is used to generate service,request,structure in PDX file to Enum class.

@Author: Siwei.Lu
@Date: 2023.3.10
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from ...can_related import parse_canoe_tools

project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\project'
retry_times = 3
projects = os.listdir(project_path)
print("All project show as following:")

for index, project in enumerate(projects):
    print("{index}:{project}".format(index=index + 1, project=project))

print("Choose the number of project:")
for i in range(retry_times):
    try:
        line = input()
        project_name = projects[int(line)-1]
        print(project_name)
        dbc = parse_canoe_tools.PDXHandler(project_name)
        dbc.write_pdx_data_to_enum_class(project_name)
        break
    except BaseException as err:
        print("Please choose the correct number!")


