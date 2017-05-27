import sqlite3 as lite
import sys


def open_file(file_name):
    cont = list()
    with open(file_name, "r", encoding="utf-8") as file:
        pre_content = file.readlines()
    for index in range(len(pre_content) // 2):
        user_name = pre_content[index * 2].strip()
        user_link = pre_content[index * 2 + 1].strip()
        if user_link and user_name:
            yield (user_name, user_link)

con = lite.connect('test.db')

with con:
    cur = con.cursor()
    # cur.execute("DROP TABLE IF EXISTS Cars")
    cur.execute("DROP TABLE IF EXISTS Nodes")
    cur.execute("CREATE TABLE Nodes(Id INT, Name TEXT, Url TEXT)")
    user_id = 0
    for user_name, user_link in open_file("data/will_go_lst.txt"):
        cur.execute('INSERT INTO Nodes VALUES(?, ?, ?)', (user_id, user_name, user_link))
        #cur.execute("CREATE TABLE Nodes"+str(user_id)+"(Id INT, Name TEXT, Url TEXT)")
        cur.execute("DROP TABLE IF EXISTS Nodes" + str(user_id))
        # u_id = 0
        # try:
        #     for u_name, u_link in open_file("db/" + user_name + ".txt"):
        #         cur.execute('INSERT INTO Nodes' + str(user_id) + ' VALUES('+ str(u_id) +', '+ u_name +', '+ u_link +')')
        #         u_id += 1
        # except Exception as e:
        #     print(e)
        user_id += 1
