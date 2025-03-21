import mysql.connector
from mysql.connector import Error
import socket
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException

class Db_access:
    def __init__(self):
        self.server = "192.168.100.25"
        self.username="ukdw"
        self.password=""
        self.database_name="labjaringan"

    def is_server_on(self):
        try:
            mydb = mysql.connector.connect(
                host=self.server,
                user=self.username,
                password=self.password,
                database=self.database_name,
                connection_timeout=10
            )
            if mydb.is_connected():
                mydb.close()
                return True
        except Error as e:
            print(f"Error connecting to the database: {e}")
            return False
    
    def get_version(self):
        mydb = mysql.connector.connect(
            host=self.server,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        cursor=mydb.cursor()
        cursor.execute(f"select * from configuration_version")
        result=cursor.fetchall()
        cursor.close()
        mydb.close()
        print("Versi\tDesc")
        for i in result:
            print(f"{i[0]}.\t{i[1]}")
        print("--\t--")
    
    def set_version(self,desc):
        mydb = mysql.connector.connect(
            host=self.server,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO configuration_version (description) VALUES (%s)", (desc,))
        cursor.execute("SELECT LAST_INSERT_ID()")
        version_id = cursor.fetchone()[0]
        mydb.commit()
        cursor.close()
        mydb.close()
        return version_id

    def get_pirantiInfo(self,nama_piranti=None,ip_address=None, blok=None,tipe_piranti=None):
        query_conditions = []

        if nama_piranti:
            if isinstance(nama_piranti, list):
                nama_piranti_conditions = " OR ".join([f"nama_piranti='{np}'" for np in nama_piranti])
                query_conditions.append(f"({nama_piranti_conditions})")
            else:
                query_conditions.append(f"nama_piranti='{nama_piranti}'")

        if ip_address:
            if isinstance(ip_address, list):
                ip_conditions = " OR ".join([f"ip_address='{ip}'" for ip in ip_address])
                query_conditions.append(f"({ip_conditions})")
            else:
                query_conditions.append(f"ip_address='{ip_address}'")

        if blok:
            if isinstance(blok, list):
                blok_conditions = " OR ".join([f"blok='{blok1}'" for blok1 in blok])
                query_conditions.append(f"({blok_conditions})")
            else:
                query_conditions.append(f"blok='{blok}'")

        if tipe_piranti:
            if isinstance(tipe_piranti, list):
                piranti_conditions = " OR ".join([f"tipe_piranti='{piranti}'" for piranti in tipe_piranti])
                query_conditions.append(f"({piranti_conditions})")
            else:
                query_conditions.append(f"tipe_piranti='{tipe_piranti}'")

            #query_conditions.append(f"tipe_piranti='{tipe_piranti}'")

        if query_conditions:
            where_clause = " AND ".join(query_conditions)
            command = f"SELECT * FROM piranti WHERE {where_clause} ORDER BY blok ASC, ip_address;"
        else:
            command = "SELECT * FROM piranti ORDER BY blok ASC, ip_address;"
        mydb = mysql.connector.connect(
            host=self.server,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        cursor=mydb.cursor()
        cursor.execute(command)
        result=cursor.fetchall()
        cursor.close()
        mydb.close()
        return result

    def input_defaultConfig(self,piranti,versi):
        mydb = mysql.connector.connect(
            host=self.server,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        cursor = mydb.cursor()
        query = "INSERT INTO default_configuration (nama_piranti, versi) VALUES (%s, %s)"
        values = (piranti[0], versi)
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()
        return True

    def cancel_input(self,version):
        mydb = mysql.connector.connect(
            host=self.server,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        cursor = mydb.cursor()
        cursor.execute(f"DELETE FROM configuration_version WHERE version={version}")
        mydb.commit()
        cursor.close()
        mydb.close()
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self.server, username='ukdw', password='ukdw', look_for_keys=False)
            ssh_client.exec_command(f'rm backup/default_config/*V{version}.*')
            ssh_client.exec_command(f'rm backup/default_config/*V{version}')
            #print("AAAAAAAAAAA")
        except (EOFError, TimeoutError, socket.timeout) as e:
            print(f"Deleting version failed: {e}, cancelled configurations might not be saved.")
            return False



    def get_groupBY(self,inputan):
        mydb = mysql.connector.connect(
            host=self.server,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        cursor=mydb.cursor()
        cursor.execute(f'SELECT count({inputan}),{inputan} FROM piranti GROUP BY {inputan}')
        result=cursor.fetchall()
        cursor.close()
        mydb.close()
        return result




