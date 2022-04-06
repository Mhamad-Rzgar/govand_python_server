from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import pyodbc

app = Flask(__name__)


CORS(app)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "HHaa1414@"
app.config["MYSQL_DB"] = "mytestdb"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# ms - access
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\Black Rule\Desktop\govan.accdb;'
    )



# ms - access




@app.route("/mysql", methods=['POST'])
def insetImages():
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
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
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    image_data = request.form["imageData"]
    image_name = request.form["imageName"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO mytestdb.image (`imageData`, `imageName`) VALUES(%s,%s)", [image_data, image_name])
    rv = cur.connection.commit()
    return jsonify({
        "message": "done",
    })


conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute("SELECT TOP 1 * FROM assetData ORDER BY[imageId] DESC")
# cursor.execute("insert into assetData (imageData, imageName) values('slaw', 'nazanm')")

# rv = cursor.connection.commit()
rv = cursor.fetchone()

print(rv)


@app.route("/access", methods=['GET'])
def access_retrieve_num_of_image():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM assetData ORDER BY[imageId] DESC")

    rv = cursor.fetchone()
    return jsonify([{
        "imageId": rv[0],
        "imageData": rv[1],
        "imageName": rv[2],
    }])


if __name__ == "__main__":
    app.run(debug=True)
