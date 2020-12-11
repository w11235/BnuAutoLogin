'''把该项目路径添加到当前python环境项目目录里'''
from distutils.sysconfig import get_python_lib
from pathlib import Path
import os

# 项目根目录
project_path = Path(os.path.dirname((os.path.abspath(__file__))))

# pth文件目录
site_packages_path = Path(get_python_lib())
pth_path = site_packages_path / "project.pth"

if pth_path.is_file():
    data = pth_path.read_text(encoding="utf-8")
    paths = [Path(path) for path in data.split()]
    if project_path not in paths:
        paths.append(project_path)
    data = '\n'.join([str(path) for path in paths])
    pth_path.write_text(data, encoding="utf-8")
else:
    data = str(project_path)
    pth_path.write_text(data, encoding="utf-8")
