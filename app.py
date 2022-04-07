from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import pyodbc

app = Flask(__name__)

CORS(app)

# mysql connection configuration
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "HHaa1414@"
app.config["MYSQL_DB"] = "mytestdb"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
# mysql connection configuration

# ms - access connection configuration
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\Black Rule\Desktop\govan.accdb;'
)


# ms - access connection configuration


@app.route("/mysql", methods=['POST'])
def insetImages():
    response = jsonify({})
    image_data = request.form["imageData"]
    image_name = request.form["imageName"]
    print(image_name)
    cur = mysql.connection.cursor()
    # cur.execute("""SELECT user, host FROM mysql.user""")
    cur.execute("INSERT INTO mytestdb.image (`imageData`, `imageName`) VALUES(%s,%s)", [image_data, image_name])
    rv = cur.connection.commit()
    return jsonify({
        "message": "done",
    })


@app.route("/mysql", methods=['GET'])
def retrieve_num_of_image():
    cur = mysql.connection.cursor()
    # cur.execute("""SELECT user, host FROM mysql.user""")
    cur.execute("select * from mytestdb.image ORDER BY imageId DESC limit 1")
    # cur.execute("select * from mytestdb.image ORDER BY rand() DESC limit 1")
    rv = cur.fetchall()
    return jsonify(rv)


@app.route("/access", methods=['POST'])
def assess_inset_images():
    response = jsonify({})
    image_data = request.form["imageData"]
    image_name = request.form["imageName"]
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # cursor.execute("INSERT INTO assetData('imageData') VALUES(" + image_name + ")")

    cursor.execute("INSERT INTO assetData(`imageData`, `imageName`) VALUES(?,?);", image_data, image_name)

    cursor.connection.commit()
    return jsonify({
        "message": "done",
    })


@app.route("/access", methods=['GET'])
def access_retrieve_num_of_image():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM assetData ORDER BY[imageId] DESC")

    rv = cursor.fetchone()
    return jsonify([{
        "imageId": rv[0],
        "imageName": rv[1],
        "imageData": rv[2],
    }])


# sql server connection configuration

sql_server_str_conn = (
    r'Driver={SQL Server};'
    r'Server=BLACK\SQLEXPRESS;'
    r'Database=mytestdb;'
    r'Trusted_Connection=yes;'
)


# sql server connection configuration

@app.route("/sqlserver", methods=['POST'])
def sqlserver_inset_images():
    image_data = request.form["imageData"]
    image_name = request.form["imageName"]

    conn = pyodbc.connect(sql_server_str_conn)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO image(imageData, imageName) VALUES(?,?);", image_data, image_name)

    cursor.commit()
    return jsonify({
        "message": "done",
    })


@app.route("/sqlserver", methods=['GET'])
def sqlserver_retrieve_num_of_image():
    conn = pyodbc.connect(sql_server_str_conn)
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM[mytestdb].[dbo].[image] ORDER BY[imageId] DESC")
    rv = cursor.fetchone()

    return jsonify([{
        "imageId": rv[0],
        "imageName": rv[1],
        "imageData": rv[2],

    }])


if __name__ == "__main__":
    app.run(debug=True)
