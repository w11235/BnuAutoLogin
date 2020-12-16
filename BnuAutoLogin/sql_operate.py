from BnuAutoLogin.configs.sql_config import DATABASE
import sqlite3


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
        self.get_connection().close()

    def query_execute(self, grammar,args=(), one=False):
        # 查询数据
        cur = self.get_connection().execute(grammar,args)
        rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def insert_execute(self,grammar):
        # 插入数据
        self.get_connection().execute(grammar)
        self.get_connection().commit()

    def update_execute(self,grammar,args):
        # 修改数据
        pass

    def delete_execute(self,grammar,args):
        # 删除数据
        pass

if __name__ == "__main__":
    obj=DataConnect()
    # sql=f"select * from users"
    # print(obj.query_execute(sql))
    # sql1=f"select * from users where username = ?"
    # print(obj.query_execute(sql1,['李四'],one=True))
    sql2=f"insert into users ('username','account_number','password_hash','create_time') values ('张三',11312018521,'test_pass','2020-12-14 14:38:29')"
    obj.insert_execute(sql2)