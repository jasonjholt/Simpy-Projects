import simpy as s
import random

# measure time in nights used
# time willing to wait

def astrophys(name, env, resource, nights, wait, prio):
	""" each astrophysicist requests time on a telescope
	
	given in order of priority
	"""
    print(f"{name} has requested {nights} nights of telescope time. Priority: {prio}")
    with resource.request(priority=prio) as req_granted:
        rep = yield req_granted | env.timeout(wait)
        
    if req_granted not in rep:
        print("Telescope time not granted.")
        return

    print(f"{name} granted {nights} nights of telescope time starting from night {env.now}, hour {12 - env.now%12}.")
    yield env.timeout(nights)
    #print(f"{name} finished with the telescope on night {env.now}, hour {12 - env.now%12}.")

def gen(env,resource,name):
    yield env.timeout(0.3)
    nights = random.randint(1,5)
    wait = random.randint(3,7)
    prio = random.randint(-2,2)
    env.process(astrophys(name, env, resource, nights, wait, prio))
        
        

env = s.Environment()
telescope = s.PriorityResource(env, capacity=1)

scientists = ["Alexis", "Bram","Catherine","Dawson","Eden","Frank","Gaia"]

for scientist in scientists:
    env.process(gen(env, telescope, scientist))


env.run()
