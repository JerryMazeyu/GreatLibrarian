import pymysql
import json


def get_db_connection(hostname, port, username, password, dbname):
    try:
        db = pymysql.connect(
            host=hostname, port=port, user=username, password=password, db=dbname
        )
        return db

    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        return None


def write_data_to_database(db, tablename, data):
    try:
        cur = db.cursor()

        sql_query = f"""INSERT INTO {tablename} (llm_name, prompt, history, response, status, time)
                        VALUES (%s, %s, %s, %s, %s, %s)"""

        llm_name = data.get("llm_name", "")
        prompt = data.get("prompt", "")
        history = json.dumps(
            data.get("history", []), ensure_ascii=False
        )  # convert list to string
        response = data.get("response", "")
        status = data.get("status", 0)
        time = data.get("time", "")

        values = (llm_name, prompt, history, response, status, time)
        cur.execute(sql_query, values)
        db.commit()

    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        db.rollback()

    finally:
        if db:
            db.close()


# username = 'root'
# password =
# host = '149.248.14.165'
# port = 3306
# database = 'chatglm_1'
# tablename = 'records'
#
# db = get_db_connection(host, port, username, password, database)
#
# if db:
#     print("Connection successful!")
# else:
#     print("Connection failed.")
