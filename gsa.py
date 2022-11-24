import random
from copy import deepcopy
import config, utils

def gsa(mp = {}, enc = []):
    if(mp == {}):
        mp = deepcopy(config.mapping)

    num_pop = 100
    num_gen = 1000

    go = 5
    gamma = 0.3
    delta = 0.1
    beta = 50
    alpha = 0.5
    epsilon = 10
    ko = 1
    randi = [random.uniform(0, 1) for i in range(num_pop)]
    randj = [random.uniform(0, 1) for j in range(num_pop)]

    best_fitness = 0
    best_particle = []

    l = [i for i in range(len(config.graph))]

    X = []
    V = []

    for i in range(num_pop):
        particle = []
        vel = []
        for j in range(len(config.graph)):
            particle.append(random.randint(0, len(mp)-1))
            vel.append(0)
        
        X.append(deepcopy(particle))
        V.append(deepcopy(vel))
    
    r = random.randint(0, num_pop-1)
    X[r], _ = utils.heft(mp = mp)
    fitness = [0 for i in range(num_pop)]
    mass = [0 for i in range(num_pop)]
    
    for itr in range(num_gen):
        g = go * (ko/(itr+1)) ** gamma
        for i in range(num_pop):
            s, c, _ = utils.simulate_pso(X[i], mp = mp, l = l, enc = enc)
            fitness[i] = 1/(alpha * s + beta * (1 - alpha) * c)

            if(fitness[i] > best_fitness):
                best_particle = deepcopy(X[i])
                best_fitness = fitness[i]

        min_fitness = min(fitness)
        max_fitness = max(fitness) 

        for i in range(num_pop):
            mass[i] = (fitness[i] - min_fitness)/(max_fitness - min_fitness)

        for i in range(num_pop):
            forces = [0 for d in range(len(X[i]))]
            for j in range(num_pop):
                if(j != i):
                    dist = 0
                    for d in range(len(X[i])):
                        dist = dist + (X[i][d] - X[j][d])**2

                    dist = dist**0.5

                    for d in range(len(X[i])):
                        forces[d] = forces[d] + randj[j] * g * mass[i] * mass[j] * (X[j][d] - X[i][d]) / (dist + epsilon)
                    
            for d in range(len(X[i])):
                acc = 0
                if(mass[i] == 0):
                    acc = (forces[d]+epsilon)/(mass[i]+epsilon)
                else:
                    acc = forces[d]/mass[i]
                V[i][d] = randi[i] * V[i][d] + acc
                X[i][d] = round(X[i][d] + V[i][d])
                X[i][d] = max(0, X[i][d])
                X[i][d] = min(X[i][d], len(mp)-1)

            if(mass[i] < delta and best_particle != []):
                for d in range(len(X[i])):
                    X[i][d] = best_particle[d]
                
                r = random.randint(0, len(X[i])-1)
                X[i][r] = random.randint(0, len(mp)-1)

    s, c, r = utils.simulate_pso(best_particle, mp = mp, l = l, enc = enc)
    return s, c, r, best_particle