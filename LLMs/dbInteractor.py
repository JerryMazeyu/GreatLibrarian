import MySQLdb
import configparser

# config = configparser.ConfigParser(allow_no_value=True)
# config.read('./LLMs.ini')
#
# host = config.get('DataBase_Settings', 'host')
# user = config.get('DataBase_Settings', 'username')
# passwd = config.get('DataBase_Settings', 'password')
# db = config.get('DataBase_Settings', 'database')
# tablename = config.get('DataBase_Settings', 'tablename1')

# config = configparser.ConfigParser(allow_no_value=True)
# config.read('./LLMs.ini')
#
# tablename = config.get('DataBase_Settings', 'tablename1')

# todo:这里prompt从哪里调用未知，所以我暂时用常量替代。
prompt = '你好'


def get_db_connection(hostname, username, password, dbname):
    try:
        db = MySQLdb.connect(host=hostname,
                             user=username,
                             passwd=password,
                             db=dbname)
        return 0

    except MySQLdb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        return None


def write_data_to_database(db, tablename, data):
    try:
        cur = db.cursor()

        sql_query = f"""INSERT INTO {tablename} (llm_name, prompt, history, response, status, time)
                        VALUES (%s, %s, %s, %s, %s)"""

        # todo:这里实在不知道history要不要，如果是以后做对话的测评，那肯定是要的。如果要的话，那么后面我在写预处理。
        cur.execute(sql_query, (data["llm_name"], data["prompt"], data["history"], data["response"], data['status'],
                                data['time']))

        db.commit()

    except MySQLdb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        db.rollback()

    finally:
        if db:
            db.close()