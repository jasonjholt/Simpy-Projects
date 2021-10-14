# meeting students for remedial classes
import random
import simpy

env = simpy.Environment()
students = simpy.PriorityStore(env)

# (grade, name)
# if priority is in letters, prio is alphabetical
grades = [simpy.PriorityItem("90", "Manav"),
          simpy.PriorityItem("88", "Katherine"),
          simpy.PriorityItem("86", "Denzel"),
          simpy.PriorityItem("76", "Freyja"),
          simpy.PriorityItem("78", "Hannah"),
          simpy.PriorityItem("92", "Rebecca"),
          simpy.PriorityItem("91", "Elle"),
          simpy.PriorityItem("89", "Inayah"),
          simpy.PriorityItem("85", "Hannah"),
          simpy.PriorityItem("90", "Malikah"),
          simpy.PriorityItem("92", "Chester")
          ]
t = len(grades)

# mention the container!!
def exam(env,students):
        for student in grades:
                yield env.timeout(1) # time it takes to test them?
                print(student.item, "tested", student.priority)
                yield students.put(student)

def remed(env, students):
        while True: # running so long as the sim is
                yield env.timeout(5) # time taken per item
                student = yield students.get() # taking from the store in order
                if env.now//8 == 0:
                        print(student.item, "with grades", student.priority, "tutored on 1st day;", env.now%8, "hours")
                elif env.now//8 == 1:
                        print(student.item, "with grades", student.priority, "tutored on 2nd day;", env.now%8, "hours")
                else:
                        print(student.item, "with grades", student.priority, "tutored on", str(env.now//8)+"th day;", env.now%8, "hours")

gr_p = {}
gr_a = {}

def retest(env, students):
        yield env.timeout(t*6) # day 5
        for student in grades:
                n = random.uniform(1.02, 1.2)
                n_s = str(n - 1)
                m = str(float(student.priority)*n)
                print(student.item, "with initial grades", student.priority, "retested with grades", m[:7], "improved by", n_s[:7] + "%")
                if student.item not in gr_p.keys() and student.item not in gr_a.keys():
                        gr_p[student.item] = student.priority
                        gr_a[student.item] = m
                
                

# env.process(function(env, resource))
i = env.process(exam(env, students))
z = env.process(remed(env, students))
print("________")
env.timeout(5)
r = env.process(retest(env, students))

env.run()
        
