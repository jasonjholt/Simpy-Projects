import simpy

# time is in minutes

def student(env,name,resource):
    with resource.request() as borrow:
        yield borrow
        print(f"Student {name} has borrowed book.")
        yield env.timeout(60)
        print(f"Student {name} has returned book.")
        print("---------------")

def student_gen(env, resource):
    names = ["Alline","Digna","Tera","Ashley","Tyson","Amos","Edward","Jules"]
    for name in names:
        yield env.timeout(5) # five minutes to find a book
        env.process(student(env, name, resource))
        

env = simpy.Environment()
book = simpy.Resource(env, capacity=1)

env.process(student_gen(env, book))
env.run()
