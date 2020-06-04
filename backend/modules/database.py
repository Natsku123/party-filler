import mysql.connector
import logging
from mysql.connector import errorcode

# TODO not sure if this really works lol
from backend.modules.tables import TABLES


logger = logging.getLogger('database')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Connection decorator
def connect(f):
    def wrap(*args, **kwargs):
        try:
            cnx = mysql.connector.connect(**args[0].get_config())
        except mysql.connector.Error as err:
            logger.error(err)

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return_value = {"status": "Error: Unable to access database with given user and password."}
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return_value = {"status": "Error: Database doesn't exist."}
            else:
                return_value = {"status": "Error: " + str(err)}
        else:
            return_value = f(*args, **kwargs, cnx=cnx)
            cnx.close()
        return return_value

    return wrap


class Database:
    def __init__(self, name, user, password):
        self.__config = {
            'user': user,
            'password': password,
            'host': 'db',
            'database': name,
            'raise_on_warnings': True
        }

    def get_config(self):
        return self.__config

    # TODO different return message
    @connect
    def setup(self, *, cnx=None):
        if cnx is None:
            raise ValueError("Database connection cannot be None!")

        status = {"status": "", "tables_exist": [], "errors": ""}

        cursor = cnx.cursor(dictionary=True)

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                logger.error(err)

                status["status"] = "Error!"
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    status['tables_exist'].append(table_name)
                else:
                    status['errors'] += err.msg + "\n"
            else:
                status["status"] = "Tables created."

        cursor.close()
        return status