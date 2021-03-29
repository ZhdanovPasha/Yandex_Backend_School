from application.serivce import make_app
from pymongo import MongoClient

db_uri = '0.0.0.0'
port = 27017
db_name = 'db'
client = MongoClient(db_uri, port)
db = client[db_name]
app = make_app(db)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')