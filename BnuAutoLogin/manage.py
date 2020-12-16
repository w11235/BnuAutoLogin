# 该py文件没用

from BnuAutoLogin.configs import sql_config
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

# 初始化sql
db = SQLAlchemy()
from BnuAutoLogin.web.app import app

# 需要把映射到数据库中的模型导入到manage.py文件中
from src.model import Users

# 导入sql配置
app.config.from_object(sql_config)

# 初始化
db.init_app(app)
manager = Manager(app)

# 用来绑定app和db到flask_migrate的
Migrate(app, db)
# 添加Migrate的所有子命令到db下
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
