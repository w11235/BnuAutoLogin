import sqlite3

from BnuAutoLogin.configs import settings
from flask import g

DATABASE = settings.DATA_DIR / "auto_login.db"

class DataConnect:

    def __init__(self):
        self.db=None

    def connect_db(self):
        return sqlite3.connect(str(DATABASE))

    def get_connection(self):
        # 开始连接
        if self.db is None:
            self.db = self.connect_db()
        return self.db

    def lose_connection(self):
        # 清除连接
        self.db.close()

    def query_execute(self, grammar,args=(), one=False):
        # 查询数据
        cur = self.get_connection().execute(grammar,args)
        rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def insert_execute(self,grammar,args):
        # 插入数据
        pass

    def update_execute(self,grammar,args):
        # 修改数据
        pass

    def delete_execute(self,grammar,args):
        # 删除数据
        pass

if __name__ == "__main__":
    obj=DataConnect()
    sql=f'select * from user'
    print(obj.query_execute(sql))
    sql1=f'select * from user where username = ?'
    print(obj.query_execute(sql1,['梁腾飞'],one=True))
