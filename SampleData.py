import sqlite3
import datetime
import random


def getRandomProduct():
    products = ["prod1","prod2","prod3"]
    user_Index = random.randint(0, 2)
    return products[user_Index]

def getRandomUser():
    user = ["Karim","John","Martha","Ibrahim","Selina","Janosch","Merry","Uli","Jason","Otto","Emra","Masud","Anastsia","Oraz","Qui","Joe","Than","Laura","Nataliya","Lamisa"]
    user_Index = random.randint(0, 19)
    return user[user_Index]

def getRandomTime():
    return datetime.date(2020, 5, random.randint(1,29))

def getRandomMsg():
    message = ["StrongNegative","WeakNegative","Neutral","Weak Positive","Strong Positive"]
    msg_Index = random.randint(0, 4)
    return message[msg_Index]

def getRandomSentiment():
    sentiment = [-2, -1, 0, 1, 2]
    sentiment_Index = random.randint(0, 4)
    return sentiment[sentiment_Index]

def getRandomRating():
    ratings = [
        [-2, "StrongNegative"],
        [-1, "WeakNegative"],
        [0, "Neutral"],
        [1, "WeakPositive"],
        [2,"StrongPositive"]
    ]
    return ratings[random.randint(0,4)]

def create_Random_Record(SID):
    randomRating = getRandomRating()
    record_dict = {
        "SID": SID,
        "Product": getRandomProduct(),
        "User": getRandomUser(),
        "Date": getRandomTime(),
        "Message": randomRating[1],
        "Sentiment": randomRating[0],
    }
    return record_dict

# Created Records for the table
Records = []
for i in range(0, 1000):
    Records.append(create_Random_Record(i+1))

# create database
conn = sqlite3.connect('database_product.db')
print("Opened database successfully")
# create a cursur
c = conn.cursor()
# create a table
c.execute("""CREATE TABLE IF NOT EXISTS dataTable  (sid INTEGER , product TEXT ,
           user TEXT, date DATE, message TEXT, sentiment INTEGER)""")
print("Table created successfully")

Sql_statement = "INSERT INTO dataTable VALUES(?,?,?,?,?,?)";
for rec in Records:
    # Create tuple from dict.
    values = (rec["SID"], rec["Product"], rec["User"], rec["Date"], rec["Message"], rec["Sentiment"])
    c.execute(Sql_statement, values)

conn.commit()

for row in c.execute("SELECT * FROM dataTable"):
    print(row)

c.close()




