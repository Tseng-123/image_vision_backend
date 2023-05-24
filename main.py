import sqlalchemy
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# 创建MySQL连接并配置参数，如下所示
engine = create_engine('mysql+pymysql://root:zxcv2580@localhost:3306/daily_things?charset=utf8mb4')

Base = sqlalchemy.orm.declarative_base()
Session = sessionmaker(bind=engine)


# 定义映射到数据库表的类
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    __table_args__ = (UniqueConstraint('username', name='_username_uc'),)


# 注册API
@app.route('/register', methods=['POST'])
def register():
    # 获取请求体中的JSON数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    session = Session()
    # 检查用户名是否已存在
    if len(username) <= 4 or session.query(User).filter_by(username=username).first() is not None:
        return jsonify({'status': 'fail', 'message': 'Invalid username.'}), 400

    # 如果用户名不存在，则将新用户添加到数据库中
    user = User(username=username, password=password)
    session.add(user)
    session.commit()

    return jsonify({'status': 'success', 'message': 'User registered successfully.'}), 201


if __name__ == '__main__':
    # 创建所有表格并运行应用程序
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
