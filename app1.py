from flask import Flask, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
db = SQLAlchemy()
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

    def json(self):  
        return {  
            'id': self.id,  
            'username': self.username,  
            'email': self.email  
        }  

with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return '你好啊，木子！'

# 添加用户
@app.post("/user")    
def add_user():
    data = request.get_json()
    username = data.get("username")  
    email = data.get("email")  
    # 查询数据库看是否存在相同的用户名  
    existing_user = User.query.filter_by(username=username).first()  

    if existing_user:  
        # 如果用户名已存在，返回错误消息  
        return jsonify(msg="用户已经存在."),400  
    else:  
        user = User(username=data.get("username"), email=data.get("email"))
        db.session.add(user)
        db.session.commit()
        print(user)
        return jsonify(msg="ok", username=data.get("username"),email=data.get("email"))
    
# 查询所有用户
@app.get("/users")
def get_users():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()       # excute(数据库操作命令)    
    print('发生一次get请求')
    return {"message": "ok", "data": [user.json() for user in users]}

# 查询用户按id
@app.route('/user/<int:uid>', methods=['GET'])  
def get_user_by_id(uid):  
    print(uid)
    try:
       user = db.get_or_404(User, uid)   # 在尝试数据库查询的的时候，可能会报错，导致程序直接返回，要有对应的处理
       if user:  
            return jsonify({'id': user.id, 'username': user.username, 'email': user.email})  
    except:
        # 如果没有找到用户，返回一个错误消息  
        return jsonify(msg = '用户已经存在！！！')
    
# 分页获取数据
# get /user?page=1&per_page=10 
@app.get("/user")
def get_user_page():
    q = db.select(User).order_by(User.id)

    page = request.args.get('page', type=int, default=1)

    per_page = request.args.get('per_page', type=int, default=10)
    paginate = db.paginate(q, page= page, per_page = per_page)
    print(paginate)            # 对象
    print(paginate.items)      # 数组 每一个数组元素是一个类user 类里面有一个类方法 json()
    print(paginate.total)      # 属性
    print(paginate.pages)      # 属性

    for user in paginate.items:
        print(user.json())
    return {"message": "ok", "data": [user.json() for user in paginate.items]}

# 通过id去删除数据, db.get_or_404主键
@app.delete("/user/<int:uid>")     # 这里一个空格错误 alueError: malformed url rule: '/user/<int: id>'
def del_user_by_id(uid):
    try:
        user = db.get_or_404(User, uid)     # 还是要先去try一下看看有没有数据不然报错
        if user:
            db.session.delete(user)
            db.session.commit()
            
            print(user)
            return jsonify({"msg":"删除成功!","data":f"{user.id},{user.username}"})    # 这个删除后，字段id没有了，不会重新开始吗？
    except:
        return jsonify({"msg":"数据库中没有该数据！"})

# 通过字段删除数据, query用法
@app.delete("/user/<string:username>")  
def del_user_by_username(username):  
    try:  
        # 使用 username 来查询用户  
        user = User.query.filter_by(username=username).first()   # first(), all(), order_by()
          
        if user:  
            db.session.delete(user)  
            db.session.commit()  
            return jsonify({"msg": "删除成功!", "data": f"{user.id},{user.username}"})  
        else:  
            return jsonify({"msg": "数据库中没有该用户！"})  
    except Exception as e:  
        # 打印异常信息并返回错误响应  
        print(f"An error occurred: {e}")  
        return jsonify({"msg": "发生内部错误，无法删除用户！", "error": str(e)}), 500
    
    
@app.put("/user/<int:uid>")
def update_user(uid):
    try:
        username = request.args.get('username')
        email = request.args.get('email')
        print(username, email)
        user = db.get_or_404(User, uid)
        if user:
            print(user)
            user.username = username
            user.email = email
            db.session.commit()
            return {"msg":"数据更新成功"}
        else:  
            return jsonify({"msg": "数据库中没有该用户！"})  
    except Exception as e:  
        # 打印异常信息并返回错误响应  
        print(f"An error occurred: {e}")  
        return jsonify({"msg": "发生内部错误，无法删除用户！", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)




'''
所以说设计程序要有具体的场景来作为设计蓝图
什么要做什么不要做
不然 乱
'''

'''
这里存在一个问题 本地数据库文件找不到位置
需要每次都在f3根目录下执行
'''