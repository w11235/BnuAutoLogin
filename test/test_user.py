import unittest

from BnuAutoLogin.configs.sql_config import engine
from sqlalchemy.orm import sessionmaker
from src.model import Users


# engine是2.2中创建的连接
Session = sessionmaker(bind=engine)

# 创建Session类实例
session = Session()


class TestUserApi(unittest.TestCase):

    def add_user(self):
        # 创建User类实例
        # ed_user = Users(username='张三', account_number=11312019220, password_hash='edspassword')
        # # 将该实例插入到users表
        # session.add(ed_user)

        # 一次插入多条记录形式
        session.add_all(
            [Users(username='李四', account_number=11312019220, password_hash='edspassword'),
            Users(username='王五', account_number=11312019220, password_hash='edspassword'),
            Users(username='刘六', account_number=11312019220, password_hash='edspassword')]
        )

        # 当前更改只是在session中，需要使用commit确认更改才会写入数据库
        session.commit()

    def query_user(self):
        # 查询用户示例
        username='张三'
        # one_user = Users.query.filter_by(username=username).first()
        # 指定User类查询users表，查找name为'ed'的第一条数据
        one_user = session.query(Users).filter_by(username=username).first()

        return one_user.account_number

    def update_user(self):
        # 修改用户示例
        username='张三'
        # 要修改需要先将记录查出来
        mod_user = session.query(Users).filter_by(username=username).first()

        # 将ed用户的密码修改为modify_paswd
        mod_user.password_hash = 'modify_passwd'

        # 确认修改
        session.commit()

    def del_user(self):
        username='张三'
        # 要删除需要先将记录查出来
        del_user = session.query(Users).filter_by(username=username).first()

        # 将ed用户记录删除
        session.delete(del_user)

        # 确认删除
        session.commit()

        # 遍历查看，已无ed用户记录
        for user in session.query(Users):
            print(user)

    def test_all(self):
    
        # 新建用户
        self.add_user()
        # 查询用户
        # self.query_user()
        # 修改用户
        # self.update_user()
        # 删除用户
        # self.del_user()


if __name__ == "__main__":
    unittest.main()
