from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


class Grade(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(64))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey(Grade.id))


@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        name = request.form.get('nm')
        password = request.form.get('paw')
        u1 = Student.query.filter(Student.name==name,Student.password==password).first()
        if u1:
            return redirect(url_for('a'))
        else:
            return '登录失败！！'


@app.route('/add_l/',methods=['GET','POST'])
def add_l():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        classname = request.form.get('ca')
        name = request.form.get('nm')
        email = request.form.get('em')
        password = request.form.get('paw')
        u1 = Grade.query.filter(Grade.name==classname).first()
        if u1:
            u2 = Student(name=name,email=email,password=password,role_id=u1.id)
            db.session.add(u2)
            db.session.commit()
            return print('Ok')
        else:
            u3 = Grade(name=classname)
            db.session.add(u3)
            db.session.commit()
            u4 = Student(name=name, email=email, password=password, role_id=u3.id)
            db.session.add(u4)
            db.session.commit()
            return print('Ok')




# ajax
from flask import Flask, url_for, render_template
from flask_restful import Api, Resource, reqparse, inputs

api = Api(app)


class Get_ajax(Resource):
    def get(self):
        pass

    def post(self):
        print(1111)
        # 获取解析对象
        parser = reqparse.RequestParser()
        # 获取username  是否是str类型  ，提示用户名验证错误！
        parser.add_argument("email", required=True)
        parser.add_argument("password", required=True)
        # 拿到这个传来的参数
        args = parser.parse_args()

        email = args.get('email')
        print(email)
        password = args.get('password')
        # print(year)
        name_ = Student.query.filter(Student.email == email,Student.password == password)
        api_list = []
        dict_l = {
            'email':email,
            'password':password
        }

        api_list.append(dict_l)
        print(type(api_list))
        print(api_list)
        # api_json = json.dumps(api_list)
        return {'api': api_list}

api.add_resource(Get_ajax, "/login/")

# 注册
class Zhuce_ajax(Resource):
    def get(self):
        pass

    def post(self):
        print(1111)
        # 获取解析对象
        parser = reqparse.RequestParser()
        # 获取username  是否是str类型  ，提示用户名验证错误！
        parser.add_argument("classname", required=True)
        parser.add_argument("name", required=True)
        parser.add_argument("email", required=True)
        parser.add_argument("password", required=True)
        # 拿到这个传来的参数
        args = parser.parse_args()
        classname = args.get('classname')
        name = args.get('name')
        email = args.get('email')
        print(email)
        password = args.get('password')
        # print(year)
        name_ = Grade.query.filter(name==classname).first()

        if name_:
            api_list = []
            dict_l = {
                'classname':classname,
                'name': name,
                'email': email,
                'password':password
            }
            api_list.append(dict_l)
            print(type(api_list))
            print(api_list)
            # api_json = json.dumps(api_list)
            print('*',99)
            return {'api': api_list}
        else:
            x = Grade(name=classname)
            db.session.add(x)
            db.session.commit()
            c = Student(name=name, email=email, password=password, role_id=x.id)
            db.session.add(c)
            db.session.commit()
            app_list = []
            dict_x = {
                'classname': classname,
                'name': name,
                'email': email,
                'password': password
            }
            app_list.append(dict_x)
            print('成功')
            return {'api': app_list}

api.add_resource(Zhuce_ajax, "/add/")


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    s1 = Grade(name="一班")
    s2 = Grade(name="二班")
    s3 = Grade(name="三班")
    db.session.add_all([s1, s2, s3])
    db.session.commit()

    s4 = Student(name="谢一", password="123", email="448995656@163.com", role_id=s1.id)
    s5 = Student(name="谢二", password="1515336", email="44899565@163.com", role_id=s2.id)
    s6 = Student(name="张三", password="5157162", email="448995165@163.com", role_id=s3.id)
    s7 = Student(name="李四", password="5145162", email="448979565@163.com", role_id=s2.id)
    s8 = Student(name="王五", password="5151262", email="448929565@163.com", role_id=s3.id)
    db.session.add_all([s4, s5, s6, s7, s8])
    db.session.commit()
    app.run(debug=True)