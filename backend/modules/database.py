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

    @connect
    def remove_party(self, *, cnx=None, party_id=None):
        if cnx is None:
            raise ValueError("Database connection cannot be None!")
        if party_id is None:
            raise ValueError("PartyID cannot be None!")

        cursor = cnx.cursor()

        delete_hook = ("DELETE FROM parties WHERE id=%s;")

        try:
            cursor.execute(delete_hook, (party_id,))
            cnx.commit()
            return_value = {"status": "success"}
        except mysql.connector.Error as err:
            logger.error(err)

            return_value = {"status": "Error: " + str(err)}
        finally:
            cursor.close()

        return return_value

    @connect
    def get_webhook(self, *, cnx=None, ide=None):
        if cnx is None:
            raise ValueError("Database connection cannot be None!")
        if ide is None:
            raise ValueError("Webhook identifier cannot be None!")

        cursor = cnx.cursor(dictionary=True)

        hook_query = ("SELECT * FROM webhooks WHERE identifier=%s LIMIT 1;")

        try:
            cursor.execute(hook_query, (ide,))
            return_value = {"status": "success",
                            "webhook": cursor.fetchone()[0]}
        except mysql.connector.Error as err:
            logger.error(err)

            return_value = {"status": "Error: " + str(err)}
        finally:
            cursor.close()

        return return_value

    @connect
    def get_all_webhooks(self, *, cnx=None):
        if cnx is None:
            raise ValueError("Database connection cannot be None!")

        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM `webhooks`;")

        try:
            cursor.execute(query, ())
            return_value = {"status": "success", "webhooks": cursor.fetchall()}
        except mysql.connector.Error as err:
            logger.error(err)

            return_value = {"status": "Error: " + str(err)}
        finally:
            cursor.close()

        return return_value

    @connect
    def add_webhook(self, *, cnx=None, webhook=None):
        if cnx is None:
            raise ValueError("Database connection cannot be None!")
        if webhook is None:
            raise ValueError("Webhook object cannot be None!")

        cursor = cnx.cursor(dictionary=True)



        add_hook = (
            "INSERT INTO webhooks (identifier, name, type, channel, icon_url) VALUES (%(ide)s, %(name)s, %(type)s, %(channel)s, %(icon_url)s);")

        try:
            logger.debug(webhook)
            cursor.execute(add_hook, {
                "ide": ide,
                "name": webhook.get('name', ""),
                "type": webhook.get('type', ""),
                "channel": webhook.get("channel", ""),
                "icon_url": webhook.get("icon_url", "")
            })
            cnx.commit()
        except mysql.connector.Error as err:

            logger.error(err)
            cursor.close()
            return "ERROR: " + str(err.msg)

        cursor.close()
        return ide