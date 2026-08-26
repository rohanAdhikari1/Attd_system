import mysql.connector as connector
from mysql.connector import Error
from tkinter import messagebox
from configparser import ConfigParser
import sqlite3
import sys


class DBhelper:
    def __init__(self):
        file = 'data/config.ini'
        config = ConfigParser()
        config.read(file)
        if config.has_section('database'):
            databas = config['database']
            db_type = databas.get('type', 'sqlite').lower()
            try:
                if db_type == 'mysql':
                     self.con = connector.connect(host=databas['host'], port='3306', user=databas['username'], password=databas['password'],
                                             database=databas['database'])
                else:
                     self.con = sqlite3.connect(databas['database'])
                
            except Error as e:
                messagebox.showerror("Connection Failed!", "Couldn't connect to server. Please try again")
                sys.exit("Error message")

    def insert_data(self, query):
        cur = self.con.cursor()
        try:
            cur.execute(query)
            self.con.commit()
            return True
        except:
            self.con.rollback()

    def update_user(self, id, newtime):
        query = "update users set last_attendance_time='{}' where uid = {}".format(newtime, id)
        cur = self.con.cursor()
        try:
            cur.execute(query)
            self.con.commit()
            return True
        except:
            self.con.rollback()

    def fetch_all(self):
        query = "select * from users"
        cur = self.con.cursor()
        cur.execute(query)
        return cur

    def fetch_by_id(self, id):
        query = "SELECT users.uid,users.name,users.last_attendance_time,count(reports.id) as totalattendance FROM " \
                "users LEFT JOIN reports On (reports.uid=users.uid) WHERE users.uid = {} LIMIT 1".format(id)
        cur = self.con.cursor()
        cur.execute(query)
        data = cur.fetchone()
        self.con.commit()
        if cur.arraysize == 1:
            return data
        elif cur.arraysize == 0:
            return 0
        else:
            return 1
