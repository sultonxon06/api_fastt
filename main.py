from fastapi import FastAPI
import uvicorn
import config
import pymysql
import jwt
import datetime
app = FastAPI()

# MySQL database configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'my_wallet',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,

}

@app.on_event("startup")
async def startup():
    # Create a database connection pool on startup
    app.db_connection = pymysql.connect(**config, autocommit=True)

@app.on_event("shutdown")
async def shutdown():
    # Close the database connection pool on shutdown
    app.db_connection.close()

# authentication
@app.post('/login/')
def login(password: str):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "SELECT * FROM user WHERE  password='"+str(password)+"'"
            cursor.execute(sql)

            # Fetch all the rows
            result = cursor.fetchall()
            print(result)
        if result:
            return {"status":"success!",}
        else:
            return {"status", "error!"}
    except Exception as e:
        print(e)
        return {"error": str(e)}

@app.delete('/logout/')
def login(password: str):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "UPDATE user SET password = NULL WHERE password = %s"
            cursor.execute(sql, (password,))
            app.db_connection.commit()
        print(cursor.rowcount)
        if cursor.rowcount > 0:
            return {"Status", "Logout!"}
        else:
            return {"Status", "parolda hatolik !"}
    except Exception as e:
        print(e)
        return {"error": str(e)}
# end auth

# start kirim
@app.post('/kirim/yangi/')
def login(izoh: str, summa:str):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "INSERT INTO kirim (narx, izoh, sana, vaqt) VALUES ('"+str(summa)+"', '"+str(izoh)+"', DATE(NOW()), TIME(NOW()) )"
            cursor.execute(sql)

            app.db_connection.commit()
            return {"status":"success!",}
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post('/kirim/tahrirlash/')
def login(izoh: str, summa:str, id:int):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "UPDATE kirim SET narx='"+str(summa)+"', izoh='"+str(izoh)+"' WHERE id='"+str(id)+"'"
            cursor.execute(sql)

            app.db_connection.commit()
            return {"status":"success!",}
    except Exception as e:
        print(e)
        return {"error": str(e)}

@app.delete('/kirim/ochirish/')
def login(id:int):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "DELETE FROM kirim WHERE id='"+str(id)+"'"
            cursor.execute(sql)

            app.db_connection.commit()
            return {"status":"success!"}
    except Exception as e:
        print(e)
        return {"error": str(e)}


# start chiqim
@app.post('/chiqim/yangi/')
def login(izoh: str, summa:str):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "INSERT INTO chiqim (narx, izoh, sana, vaqt) VALUES ('"+str(summa)+"', '"+str(izoh)+"', DATE(NOW()), TIME(NOW()) )"
            cursor.execute(sql)

            app.db_connection.commit()
            return {"status":"success!",}
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post('/chiqim/tahrirlash/')
def login(izoh: str, summa:str, id:int):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "UPDATE chiqim SET narx='"+str(summa)+"', izoh='"+str(izoh)+"' WHERE id='"+str(id)+"'"
            cursor.execute(sql)

            app.db_connection.commit()
            return {"status":"success!",}
    except Exception as e:
        print(e)
        return {"error": str(e)}

@app.delete('/chiqim/ochirish/')
def login(id:int):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "DELETE FROM chiqim WHERE id='"+str(id)+"'"
            cursor.execute(sql)

            app.db_connection.commit()
            return {"status":"success!"}
    except Exception as e:
        print(e)
        return {"error": str(e)}


# kirim hisobot
@app.get('/hisobot')
def login(sana1:str, sana2:str):
    try:
        with app.db_connection.cursor() as cursor:
            # Execute a SQL query
            sql = "SELECT (SELECT FORMAT(IFNULL(SUM(IFNULL(narx,0)),0), 0) FROM kirim WHERE sana BETWEEN DATE(%s) AND DATE(%s)) as kirim, (SELECT FORMAT(IFNULL(SUM(IFNULL(narx,0)),0), 0) FROM chiqim WHERE sana BETWEEN DATE(%s) AND DATE(%s)) as chiqim"
            values = (sana1, sana2, sana1, sana2)
            cursor.execute(sql, values)
            result = cursor.fetchall()
            return {"status": "success!", "data": result}
    except Exception as e:
        print(e)
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)