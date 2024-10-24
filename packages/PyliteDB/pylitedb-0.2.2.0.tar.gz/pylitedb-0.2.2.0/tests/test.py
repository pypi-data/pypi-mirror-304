from src.Pylite import Database


db = Database("DataBase.pylite", "Pass123", True)
# print(db)
print(db.Meetings.Get(Time=9).Date)