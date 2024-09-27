# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

#数据库连接
db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
cursor = db.cursor()

#后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/login/list', methods=['POST'])
def login_list():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        cursor.execute("select id,username,role,ctime from login")
        data = cursor.fetchall()
        temp={}
        result=[]
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["role"]=i[2]
                temp["ctime"]=i[3]
                result.append(temp.copy()) #特别注意要用copy，否则只是内存的引用
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])

@app.route('/login/add', methods=['POST'])
def login_add():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ifsame = cursor.execute("SELECT 1 FROM login WHERE username = %s",(username,))
        if ifsame:
            return "0"
        try:
            cursor.execute("insert into login(username,password) values (\""
                            +str(username)+"\",\""+str(password)+"\")")
            db.commit() #提交，使操作生效
            print("add a new user successfully!")
            return "1"
        except Exception as e:
            print("add a new user failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

@app.route('/login/login', methods=['POST'])
def login_login():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor.execute("select id,username,role,ctime from login where username=\""
                       +str(username)+"\" and password=\""+str(password)+"\"")
        data = cursor.fetchone()
        if(data!=None):
            print("result:",data)
            jsondata = {"id":str(data[0]),"username":str(data[1]),
                        "role":str(data[2]),"ctime":str(data[3])}
            return jsonify(jsondata)
        else:
            print("result: NULL")
            jsondata = {}
            return jsonify(jsondata)

@app.route('/login/update', methods=['POST'])
def login_update():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        id = request.form.get("id")
        password = request.form.get("password")
        try:
            cursor.execute("update login set password=\""+str(password)
                            +"\" where id="+str(id))
            db.commit()
            print("update password successfully!")
            return "1"
        except Exception as e:
            print("update password failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

@app.route('/login/update_role', methods=['POST'])
def login_update_role():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        id = request.form.get("id")
        role = request.form.get("role")
        try:
            cursor.execute("update login set role=\""+str(role)
                            +"\" where id="+str(id))
            db.commit()
            print("update role successfully!")
            return "1"
        except Exception as e:
            print("update role failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

@app.route('/login/del', methods=['POST'])
def login_del():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("delete from login where id="+str(id))
            db.commit()
            print("delete user"+str(id)+" successfully!")
            return "1"
        except Exception as e:
            print("delete the user failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"


@app.route('/data/list', methods=['POST'])
def data_list():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    try:
        uid = request.form.get("uid")
        if not uid != 0:
            sql = "SELECT * FROM data WHERE uid = %s ORDER BY likes DESC, id ASC"
            uid = int(uid)  # 确保 uid 是整数类型
        else:
            sql = "SELECT * FROM data ORDER BY likes DESC, id ASC"
        print("Executing SQL:", sql)
        print("UID value:", uid)
        if not uid != 0:
            cursor.execute(sql, (uid,))
        else:
            cursor.execute(sql)
        data = cursor.fetchall()
        print("Data fetched:", data)
        temp={}
        result=[]
        if(data is not None):
            for i in data:
                temp["id"]=i[0]
                temp["uid"]=i[1]
                temp["dataname"]=i[2]
                temp["likes"]=i[3]
                temp["material1"]=i[4]
                temp["material2"]=i[5]
                temp["orientation"]=i[6]
                temp["potentialEnergy"] = i[7]
                temp["potentialFunctionURL"] = i[8]
                temp["pictureURL"] = i[9]
                temp["shipeiweicuotuURL"] = i[10]
                temp["weiyixiangliangtuURL"] = i[11]
                temp["initialModelURL"] = i[12]
                temp["finalModelURL"] = i[13]
                temp["ctime"] = i[14]
                temp["state"] = i[15]
                result.append(temp.copy()) #特别注意要用copy，否则只是内存的引用
            print("result:",len(data))
            return jsonify(result)
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/data/add', methods=['POST'])
def data_add():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        uid = request.form.get("uid")
        dataname = request.form.get("dataname")
        material1 = request.form.get("material1")
        material2 = request.form.get("material2")
        orientation = request.form.get("orientation")
        potentialEnergy = request.form.get("potentialEnergy")
        state = request.form.get("state")
        try:
            sql = "INSERT INTO data (uid, dataname, material1, material2, orientation, potentialEnergy, state) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (uid, dataname, material1, material2, orientation, potentialEnergy, state))
            db.commit() #提交，使操作生效
            print("add a new data successfully!")
            return "1"
        except Exception as e:
            print("add a new data failed in",e)
            db.rollback() #发生错误就回滚
            return "-1"

@app.route('/data/del', methods=['POST'])
def data_del():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("delete from data where id="+str(id))
            db.commit()
            print("delete data"+str(id)+" successfully!")
            return "1"
        except Exception as e:
            print("delete the data failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"
        
@app.route('/data/update', methods=['POST'])
def data_update():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        id = request.form.get("id")
        dataname = request.form.get("dataname")
        material1 = request.form.get("material1")
        material2 = request.form.get("material2")
        orientation = request.form.get("orientation")
        potentialEnergy = request.form.get("potentialEnergy")
        try:
            cursor.execute("update data set dataname=\""+str(dataname)
                            +"\", material1=\""+str(material1)+"\", material2=\""+str(material2)+"\", orientation=\""
                            +str(orientation)+"\", potentialEnergy=\""+str(potentialEnergy)+"\" where id="+str(id))
            db.commit()
            print("update data successfully!")
            return "1"
        except Exception as e:
            print("update data failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

@app.route('/data/likes', methods=['POST'])
def data_likes():
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="interface of materials")
    cursor = db.cursor()
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("UPDATE data SET likes = likes + 1 WHERE id = %s", (id,))
            if cursor.rowcount == 0:  # 如果没有行被更新
                print("No rows updated.")
                return "-1"
            db.commit()  # 提交事务
            print("likes++ successfully!")
            return "1"
        except Exception as e:
            print("likes++ failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9090)
    db.close()
    print("Good bye!")