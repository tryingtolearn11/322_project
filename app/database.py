import json
import os
from flask import current_app as app

class DB:

    def __init__(self):
        datafile = os.path.join(app.static_folder, 'data', 'data.json')
        with open(datafile) as f:
            self.data = json.load(f)
            self.class_json = self.data["class"]
            self.students_grade = self.data["student_grade"]
            self.users = self.data["user"]
            self.taboo_words = self.data["taboo_words"]
            self.reviews = self.data["reviews"]

    def getTopRatedClass(self):
        self.class_json.sort(key=lambda x: x["avg_rating"],reverse=True)
        for t in self.class_json[:5]:
            user = next(x for x in self.users if x["id"]==t["professor_id"])
            t["name"] = user["fname"]+" "+user["lname"]
        return self.class_json[:5]

    def getLowRatedClass(self):
        self.class_json.sort(key=lambda x: x["avg_rating"])
        for t in self.class_json[:5]:
            user = next(x for x in self.users if x["id"]==t["professor_id"])
            t["name"] = user["fname"]+" "+user["lname"]
        return self.class_json[:5]

    def getTopStudents(self):
        self.students_grade.sort(key=lambda x: x["gpa"],reverse=True)
        for t in self.students_grade[:5]:
            user = next(x for x in self.users if x["id"]==t["user_id"])
            classname = next(x for x in self.class_json if x["id"]==t["class_id"])
            t["name"] = user["fname"]+" "+user["lname"]
            t["classname"] = classname["class_name"]
        return self.students_grade[:5]

    def getTabooWords(self):
        return self.taboo_words

    def insertReview(self,user_id,class_id,rating,review):
        datafile = os.path.join(app.static_folder, 'data', 'data.json')
        with open(datafile,"r") as f:
            temp = json.load(f)
        temp["reviews"].append({"user_id":user_id,"class_id":class_id,"rating":rating,"review":review})
        with open(datafile,"w") as f:
            json.dump(temp, f)

    # def getClasses(self):
    #     for t in self.class_json[:]:
    #         user = next(x for x in self.users if x["id"]==t["professor_id"])
    #         t["name"] = user["fname"]+" "+user["lname"]
    #     return self.class_json[:]
