import simpy
from collections import namedtuple
import collections
import random

""" 
different classes/colleges that can only accept 50 students per course
minimum grade to get in is 85, if the grade is lower, they have to leave and are added to failed_applications
if the course is full, they are added to overflow_applications
time is in hours, and the sim runs for 5 days, 5 hours a day

variables needed
- a list of courses : 5 courses?
- total slots : 50 per course
- how many counters are open (resource capacity=2)
- students' grades
- stores failed_applications
- stores overflow_applications
- when is the course filled?
events:
- course_filled
"""
days = 7
hours = 8
total_time = days*hours # total time for enrollment
total_students = 0
enrolled_students = 0

def student(env, course, college, grades):
    global total_students
    global enrolled_students
    total_students += 1
    with college.counters.request() as enroll:
        ans = yield enroll | college.course_filled[course]
    print("Student Enrolling. . .")
    # what if the grades don't meet the minimum
    if grades < college.min_grade[course]:
        college.failed_applications[course] += 1
        print(f"REJECTED for {course}: Grades are too low.")
        return
    
    if enroll not in ans:
        college.overflow_applications[course] += 1
        print(f"REJECTED: {course} Full")
        return
    
    college.available[course] -= 1
    college.total_applications[course] += 1
    enrolled_students += 1
    print(f"ACCEPTED into {course}")

    if college.available[course] == 0:
        college.course_filled[course].succeed()
        t_day = str(int(env.now//8))
        t_hour = str(int(env.now%8))
        print(f"{course} filled on day {t_day}, hour {t_hour}.")
        if college.when_course_filled[course] == None:
            college.when_course_filled[course] = t_day
        #college.available[course] = 0
    print("Enrollment Process Completed")
    yield env.timeout(random.uniform(0.05, 0.3))

def enroll(env, college):
    while True:
        yield env.timeout(random.uniform(0.05, 0.3))
        # pick a course
        course = random.choice(college.courses)
        grades = random.uniform(75, 96)
        if college.available[course]:
            env.process(student(env, course, college, grades))
        else:
            college.overflow_applications[course] += 1
            print(f"REJECTED: {course} Full")


# set up the environment
College = collections.namedtuple("College", 'counters, courses, available, course_filled, when_course_filled, overflow_applications,failed_applications, total_applications, min_grade')
        

env = simpy.Environment()

counters = simpy.Resource(env, capacity=5) #  office has n counters
courses = ["BS Physics", "BS Chemistry","BS Mathematics","BA Linguistics","BA History", "BA Philosophy"]
available = {
    "BS Physics" : 20,
    "BS Chemistry" : 20,
    "BS Mathematics" : 20,
    "BA Linguistics" : 30,
    "BA History" : 30,
    "BA Philosophy" : 30,
}
course_filled = {course: env.event() for course in courses}
when_course_filled = {course: None for course in courses}
overflow_applications = {course: 0 for course in courses}
failed_applications = {course: 0 for course in courses}
total_applications = {course: 0 for course in courses}
min_grade = {
    "BS Physics" : 85,
    "BS Chemistry" : 85,
    "BS Mathematics" : 85,
    "BA Linguistics" : 83,
    "BA History" : 83,
    "BA Philosophy" : 80,
}
any = College(counters, courses, available,course_filled, when_course_filled, overflow_applications,failed_applications, total_applications, min_grade)

print("Start Applications:")
env.process(enroll(env, any)) # enter env and class
env.run(until=total_time)

# print analysis
"""
for each course, info needed:
    - number of failed applications
    - number of overflow applications
    - when did the course get filled
"""
print("___________________")

print("Enrollment Period:", days, "days")
print("Students Served:", total_students)
print("Students Enrolled:", enrolled_students)
print("Students Rejected:", total_students - enrolled_students)
print("___________________")
for course in courses:
    print(course + " Applications:", any.total_applications[course])
    print(f"    Failed Applications: {any.failed_applications[course]}")
    print(f"    Overflow Applications: {any.overflow_applications[course]}")
    if any.when_course_filled[course] != None:
        print("    Course filled on day {}.".format(any.when_course_filled[course]))
    else:
        print("    Course not filled.")
