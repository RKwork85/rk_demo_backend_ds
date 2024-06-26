from datetime import datetime
from flask import Flask, jsonify, render_template, request, session, g
from flask_migrate import Migrate
from flask_cors import CORS
from models import UserModel, DatasetsModel

from exts import db
import config

app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True)

# 绑定配置文件
app.config.from_object(config)



db.init_app(app)  # 先创建，后绑定

migrate = Migrate(app, db)


@app.route("/")
def hello():
    return "你好啊，木子！这是测数据集接口的服务"


@app.post("/login")
def login_by_uuid():
    data = request.get_json()
    uuid = data.get("uuid")
    print(uuid)
    if uuid:
        session['uuid'] = uuid
        uuid = session.get("uuid")
        print("设置好的uuid：",uuid)
        
    # print(g.user)
    # data = request.get_json()
    # uuid = data.get("uuid")
    # user = UserModel.query.filter_by(uuid=uuid).first()
    # if user:
    #     return jsonify(msg="错误,用户已注册请登录")
    # else:
    #     new_user = UserModel(uuid=uuid, join_time=datetime.now())

    #     db.session.add(new_user)
    #     db.session.commit()
    #     return jsonify(msg="注册成功！已连接到数据库")
    return jsonify(msg='nothing')


@app.post("/register")
def register_by_uuid():
    data = request.get_json()
    uuid = data.get("uuid")
    user = UserModel.query.filter_by(uuid=uuid).first()
    if user:
        return jsonify(msg="错误,用户已注册请登录")
    else:
        new_user = UserModel(uuid=uuid, join_time=datetime.now())

        db.session.add(new_user)
        db.session.commit()
        return jsonify(msg="注册成功！已连接到数据库")


@app.get("/rkwork/register")  # 走后门的接口
def register_by_rkwork():
    username = request.args.get("username")
    password = request.args.get("password")
    user = UserModel.query.filter_by(username=username).first()
    if user:
        return jsonify(msg="错误,用户已注册请登录")
    else:
        new_user = UserModel(
            username=username,
            password=password,
            uuid=username,
            join_time=datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify(msg="注册成功！已连接到数据库")


# 添加单条数据集
@app.post("/dataset")
def add_dataset():
    uuid = session.get("uuid")
    print("查看已有的uuid：",uuid)
    data = request.get_json()
    # 拿
    instruction = data.get("instruction")
    output = data.get("output")
    uuid = data.get("uuid")
    # user = UserModel.query.filter_by(uuid=uuid).first()
    print(g.user)
    if g.user:  # 我需要返回该条数据集的id号  待解决
        dataset = DatasetsModel(
            instruction=data.get("instruction"),
            output=data.get("output"),
            user_id=g.user.id,
        )
        db.session.add(dataset)
        db.session.commit()
        return jsonify(msg="用户单条数据添加成功", dataset=dataset.get_dataset())
    else:
        # 存
        dataset = DatasetsModel(
            instruction=data.get("instruction"), output=data.get("output")
        )
        db.session.add(dataset)
        db.session.commit()
        # 显示
        print(dataset)
        return jsonify(
            msg="添加单条数据", dataset=data.get("dataset"), output=data.get("output")
        )


# 添加多条数据集 要和用户关联
@app.post("/datasets")
def add_datasets():
    data = request.get_json()
    # 拿
    datasets = data.get("datasets")  # [[],[],[]]
    for i in datasets:
        instruction = i[1]
        output = i[2]
        # 存
        dataset = DatasetsModel(instruction=instruction, output=output)
        db.session.add(dataset)
        db.session.commit()

        # 显示
    print(dataset)
    return jsonify(msg="ok", dataset=data.get("dataset"), output=data.get("output"))


@app.get("/dataset")
def get_dataset_all():
    datasets = DatasetsModel.query.all()
    datasets_json = [(dataset.id, dataset.get_dataset()) for dataset in datasets]
    for i in datasets_json:
        print(i, "\n")

    return jsonify(msg="ok", data=datasets_json)


@app.route("/dataset/<int:id>", methods=["GET"])
def get_dataset_by_id(id):
    print(id)
    try:
        dataset = db.get_or_404(
            DatasetsModel, id
        )  # 在尝试数据库查询的的时候，可能会报错，导致程序直接返回，要有对应的处理
        if dataset:
            data = dataset.get_dataset()  # 序列化之后变得无序，所以还是在前端组织顺序？
            print(data)
            return jsonify(data)
    except:
        # 如果没有找到用户，返回一个错误消息
        return jsonify(msg=f"{id}数据集不存在！！！")


@app.route("/dataset/<string:uuid>", methods=["GET"])
def get_dataset_by_uuid(uuid):
    print(uuid)
    user = UserModel.query.filter_by(uuid=uuid).first()
    if user:
        datasets = user.datasets  # 序列化之后变得无序，所以还是在前端组织顺序？
        print(datasets)
        allDataset = []
        for dataset in datasets:
            allDataset.append([dataset.id, dataset.get_dataset()])
        return jsonify(
            msg="用户数据查询成功", allDataset=allDataset
        )  # 这个返回的是字符串我希望是数组
        # pass
    else:
        # 如果没有找到用户，返回一个错误消息
        return jsonify(msg=f"{id}数据集不存在！！！")


@app.put("/dataset/<int:uid>")
def update_dataset(uid):
    try:
        instruction = request.args.get("instruction")
        output = request.args.get("output")
        print(instruction, output)
        dataset = db.get_or_404(DatasetsModel, uid)
        olddataset = dataset.get_dataset()
        if dataset:
            print(dataset)
            dataset.instruction = instruction
            dataset.output = output
            db.session.commit()
            dataset = db.get_or_404(DatasetsModel, uid)

            return {
                "msg": "数据集数据更新成功",
                "oldDataset": olddataset,
                "newDataset": dataset.get_dataset(),
            }
        else:
            return jsonify({"msg": "数据库中没有数据！"})
    except Exception as e:
        # 打印异常信息并返回错误响应
        print(f"An error occurred: {e}")
        return jsonify({"msg": "发生内部错误，无法删除用户！", "error": str(e)}), 500


# 通过字段删除数据, query用法
@app.delete("/dataset/<int:id>")
def del_dataset_by_id(id):
    try:
        # 使用 username 来查询用户
        dataset = DatasetsModel.query.filter_by(
            id=id
        ).first()  # first(), all(), order_by()

        if dataset:
            db.session.delete(dataset)
            db.session.commit()
            return jsonify({"msg": "删除成功!", "data": f"{id}"})
        else:
            return jsonify({"msg": "数据库中没有该数据集！"})
    except Exception as e:
        # 打印异常信息并返回错误响应
        print(f"An error occurred: {e}")
        return jsonify({"msg": "发生内部错误，无法删除用户！", "error": str(e)}), 500

@app.route('/api/login', methods=['GET'])
def login():
    # 这里应该有验证用户名和密码的逻辑
    session['uuid'] = 'rkwork'
    return jsonify({'uuid': session['uuid']})

@app.route('/api/dashboard')
def dashboard():
    print(g.user.uuid)
    if 'uuid' in session:
        return jsonify({'message': f'Welcome! Your session UUID is: {session["uuid"]}'})
    else:
        return jsonify({'error': 'Not logged in'})


@app.before_request  #  在请求之前就自动获取变量值， 每次请求都要写代码，获取用户的信息
def my_before_request():
    uuid = session.get("uuid")
    print("before_request", uuid)
    if uuid:
        user = UserModel.query.filter_by(uuid=uuid).first()
        setattr(g, "user", user)
    else:

        setattr(g, "user", None)


if __name__ == "__main__":
    app.run(debug=True)
"""
1 返回到前端的数据无序 需在前端重新处理数据
2 
"""
