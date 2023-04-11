import iluxaMod as ilm

database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot", host="illyashost.ddns.net")
database.init_DB(settings=True, stages=True, staff=True, balance=True, stdout=False)

db = database.db
sql = database.sql

stages = database.stages
staff = database.staff
settings = database.settings

