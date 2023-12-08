#
# 迁移python的venv虚拟机环境
# by ssw 2023.10.09，参考：https://blog.csdn.net/m0_57110410/article/details/131266980
# 1.修改pyvenv.cfg，把其中的python环境和版本设置为当前
# 2.执行当前脚本
# 3.重新打开改项目，选择当前venv的python解析器，并执行\.venv\Scripts\activate
#

import os
import shutil

# 当前py文件目录
work_dir = os.path.dirname(os.path.abspath(__file__))

# 新的venv环境目录，默认为当前py下venv目录
new_virtual_env_value = work_dir + r'\.venv'

# 获取当前目录下的.venv\Scripts文件夹中的四个文件
file_names = [r'\.venv\Scripts\activate', 
              r'\.venv\Scripts\activate.bat', 
              r'\.venv\Scripts\activate.fish', 
              r'\.venv\Scripts\activate.nu']

# 获取原venv环境的VIRTUAL_ENV的值
activate_bat_file_path = work_dir + file_names[1]  # activate.bat文件的路径
def get_old_virtual_env_value(activate_bat_file_path):
    with open(activate_bat_file_path, 'r') as file:
        for line in file:
            if line.startswith('@set "VIRTUAL_ENV='):
                return line.split('=')[1].strip().strip('"')
old_virtual_env_value = get_old_virtual_env_value(activate_bat_file_path)

# 遍历每个文件，将其中的匹配文本替换为替换文本
for file_name in file_names:
    file_path = work_dir + file_name
    with open(file_path, 'r') as file:
        file_content = file.read()
    file_content = file_content.replace(old_virtual_env_value, new_virtual_env_value)
    with open(file_path, 'w') as file:
        file.write(file_content)

print('\n' + '------开始迁移venv环境------')
print(f'1.成功替换4个文件的[{old_virtual_env_value}] 为 [{new_virtual_env_value}]')

# 调用函数删除文件夹
def delete_pip_folders(directory):
    # 获取目录下的所有文件夹
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    # 遍历文件夹，删除以"pip"开头的文件夹
    for folder in folders:
        if folder.startswith('pip'):
            folder_path = os.path.join(directory, folder)
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")
delete_pip_folders(work_dir + r'\.venv\Lib\site-packages')
print(f'2.成功删除\.venv\Lib\site-packages下的以pip开头的文件夹')

os.system('cd ' + work_dir + r'\.venv\Scripts &&' + "python -m ensurepip")
os.system('cd ' + work_dir + r'\.venv\Scripts &&' + "easy_install pip")  # 报错可注释掉
os.system('cd ' + work_dir + r'\.venv\Scripts &&' + "python -m pip install --upgrade pip -i https://pypi.douban.com/simple/")
print(f'3.成功重装pip环境')

activate_file_path = work_dir + file_names[0]  # activate文件的路径
os.system(activate_file_path)
print(f'4.成功activate环境')

print('------结束迁移venv环境------' + '\n')
