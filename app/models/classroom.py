import pickle
import os

class Activity:
    def __init__(self):
        self.title = ""
        self.description = ""

class Student:
    def __init__(self, name):
        self.name = name
        self.puuid = 0
        self.activities = []

class Teacher:
    def __init__(self, name):
        self.name = name
        self.activities = []

class Classroom:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
        self.teachers = []
        self.students = []

    def addTeacher(self, name):
        newTeacher = Teacher(name)
        self.teachers.append(newTeacher)

    def addStudent(self, name):
        newStudent = Student(name)
        self.students.append(newStudent)
        
class ClassroomManager:

    @staticmethod
    def save_pickle(classroom: Classroom, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(classroom, f)

    @staticmethod
    def load_pickle(filename: str) -> Classroom:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Classroom not found {filename}")
        with open(filename, "rb") as f:
            return pickle.load(f)

# myClass = Classroom()
# myClass.addTeacher("Alex")
# myClass.addStudent(student)
# ClassroomManager.save_pickle(myClass, "classroom.pkl")
# myClass = ClassroomManager.load_pickle("classroom.pkl")