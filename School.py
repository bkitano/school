import pandas as pd
import numpy as np
from collections import defaultdict
import random
import string

def get_random_string(prefix, length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return prefix + "-" + result_str

ASSIGNMENT_TYPES = ['homework', 'test']

class Assignment:
    def __init__(self, assignmentType, time):
        self.id = get_random_string('a', 5)
        self.assignmentType = assignmentType
        self.time = time
        
class Student:
    def __init__(self, name = ''):
        self.name = name
        self.id = get_random_string('s', 6)
        self.assignments = defaultdict(list)
        self.courses = {}
        self.grades = {}
    
    def show(self):
        print("--- {} ---".format(self.id))
        print("assignments: {}".format([self.assignments]))
        print("courses: {}".format([ courseId for (courseId, c) in self.courses.items() ]))
        print("\n")
        
    def addCourse(self, course):
        self.courses[course.id] = course
        
    def addAssignment(self, courseId, assignment, grade):
        self.assignments[courseId] += [(assignment, grade)]
        
    def getCumulativeGrade(self, courseId):
        course = self.courses[courseId]
        rubric = course.rubric
        assignments = self.assignments[courseId]

        totalGrade = 0
        for assignmentType in ASSIGNMENT_TYPES:
            assigmentList = list(filter(lambda a: a[0].assignmentType == assignmentType, assignments))
            assignmentWeight = np.mean([a[1] for a in assigmentList]) * rubric[assignmentType]
            totalGrade += assignmentWeight

        self.grades[courseId] = totalGrade
            
        return self.grades
    
    def getCourseGrades(self):
        for courseId in self.courses.keys():
            self.getCumulativeGrade(courseId)
        return self.grades
    
class Course:
    def __init__(self, name = '', slot = 0 ):
        self.name = name
        self.slot = slot
        self.id = get_random_string('c', 5)
        self.assignments = []
        self.teacher = None
        self.students = []
        self.rubric = dict(zip(ASSIGNMENT_TYPES, np.random.dirichlet((1, 1), 1).tolist()[0]))
        
    def setStudents(self, students):
        self.students = students
        for student in students:
            student.addCourse(self)
            
    def setTeacher(self, teacher):
        self.teacher = teacher
        teacher.addCourse(self)
        
    def createAssignment(self, assignmentType, time):
        assignment = Assignment(assignmentType, time)
        self.assignments += [assignment]
        for student in self.students:
            grade = random.random()
            student.addAssignment(self.id, assignment, grade)
            
    def getStudentGrades(self):
        return dict([(student.id, student.getCumulativeGrade(self.id)[self.id]) for student in self.students])
    
    def show(self):
        print("--- {} ---".format(self.id))
        print("teacher: {}".format(self.teacher.id))
        print("students: {}".format([s.id for s in self.students]))
        print("assignments: {}".format([a.id for a in self.assignments]))
        print("rubric: {}".format(self.rubric))
        print("\n")
        
class Teacher:
    def __init__(self, name = ''):
        self.name = name
        self.id = get_random_string('t', 5)
        self.courses = []
        
    def addCourse(self, course):
        self.courses += [course]
        
    def show(self):
        print("--- {} ---".format(self.id))
        print("courses: {}".format(self.courses))
        print("total number of students: {}".format(sum([len(course.students) for course in self.courses])))
        print("\n")