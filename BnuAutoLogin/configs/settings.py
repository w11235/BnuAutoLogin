from pathlib import Path
import os

# 根目录
root_path = Path(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))))

# ######项目类######
# 项目目录
project_path = root_path /"BnuAutoLogin"
# 数据库目录
DATA_DIR = project_path / "db"
# logs目录
LOGS_DIR = project_path / "logs"

# ######测试类######
# 测试目录
TEST_DIR = project_path / "test"


if __name__ == "__main__":
    print(root_path)
    print(project_path)
    print(DATA_DIR)