"""
This file is used to generate mapping file in veristand to parameter.

@Author: Zhihong.Lin
@Date: 2023.3.15
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from ...veristand_related import gen_mapping

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
        gen_mapping.gen_mapping_function(project_name)
        break
    except BaseException as err:
        print("Please choose the correct number!", err)


