from copy import deepcopy
import numpy as np
import random
import config, utils

def select_parent(fitness):
    if(min(fitness) == 0):
        for i in range(len(fitness)):
            fitness[i] += 0.01

    for i in range(len(fitness)):
        fitness[i] = 1/fitness[i]

    s = sum(fitness)

    for i in range(len(fitness)):
        fitness[i] = fitness[i]/s
    
    pop = [i for i in range(len(fitness))]

    return np.random.choice(pop, p = fitness)

def span_cost(mp = {}, enc = []):
    if(mp == {}):
        mp = deepcopy(config.mapping)

    num_pop = 100
    num_gen = 1500

    X = []

    smin = float('inf')
    smax = 0
    cmin = float('inf')
    cmax = 0
    rmin = float('inf')
    rmax = 0

    best_fitness = float('inf')
    best_idx = -1

    for i in range(num_pop):
        particle = [random.randint(0, len(mp)-1) for _ in range(len(config.graph))]
        s, c, r = utils.simulate_pso(particle, mp = mp, enc = enc)

        smin = min(s, smin)
        smax = max(s, smax)
        cmin = min(c, cmin)
        cmax = max(c, cmax)
        rmin = min(r, rmin)
        rmax = max(r, rmax)

        X.append([deepcopy(particle), s, c, r])
    
    for gen in range(num_gen):
        fitness = []
        for i in range(num_pop):
            ft = 0.9*(X[i][2] - cmin)/(cmax - cmin) + 0.1*(X[i][1] - smin)/(smax - smin)
            if(ft < best_fitness):
                best_fitness = ft
                best_idx = i
            
            fitness.append(ft)
        
        if(random.uniform(0, 1) <= 0.9):
            p1 = X[select_parent(fitness)][0]
            p2 = X[select_parent(fitness)][0]

            k = random.randint(0, len(config.graph)-1)

            pnew = p1[:k] + p2[k:]

            if(random.uniform(0, 1) <= 0.02):
                r1 = random.randint(0, len(config.graph)-1)
                r2 = random.randint(0, len(mp)-1)

                pnew[r1] = r2

            s, c, r = utils.simulate_pso(pnew, mp = mp, enc = enc)
            smin = min(s, smin)
            smax = max(s, smax)
            cmin = min(c, cmin)
            cmax = max(c, cmax)
            rmin = min(r, rmin)
            rmax = max(r, rmax)

            ft = 0.9*(c - cmin)/(cmax - cmin) + 0.1*(s - smin)/(smax - smin)
            best_fitness = 0.9*(X[best_idx][2] - cmin)/(cmax - cmin) + 0.1*(X[best_idx][1] - smin)/(smax - smin)

            r3 = random.randint(0, num_pop-1)

            if(ft < best_fitness):
                X[r3] = [deepcopy(pnew), s, c, r]
                best_fitness = ft
                best_idx = r3
            
            else:
                while(r3 == best_idx):
                    r3 = random.randint(0, num_pop-1)

                X[r3] = [deepcopy(pnew), s, c, r]
    
    return X[best_idx][1], X[best_idx][2], X[best_idx][3], X[best_idx][0]

def cost_rel(mp = {}, enc = []):
    if(mp == {}):
        mp = deepcopy(config.mapping)

    num_pop = 100
    num_gen = 1500

    X = []

    smin = float('inf')
    smax = 0
    cmin = float('inf')
    cmax = 0
    rmin = float('inf')
    rmax = 0

    best_fitness = float('inf')
    best_idx = -1

    for i in range(num_pop):
        particle = [random.randint(0, len(mp)-1) for _ in range(len(config.graph))]
        s, c, r = utils.simulate_pso(particle, mp = mp, enc = enc)

        smin = min(s, smin)
        smax = max(s, smax)
        cmin = min(c, cmin)
        cmax = max(c, cmax)
        rmin = min(r, rmin)
        rmax = max(r, rmax)

        X.append([deepcopy(particle), s, c, r])
    
    for gen in range(num_gen):
        fitness = []
        for i in range(num_pop):
            ft = 0.8*(X[i][2] - cmin)/(cmax - cmin) + 0.2*(rmax - X[i][3])/(rmax - rmin)
            if(ft < best_fitness):
                best_fitness = ft
                best_idx = i
            
            fitness.append(ft)
        
        if(random.uniform(0, 1) <= 0.9):
            p1 = X[select_parent(fitness)][0]
            p2 = X[select_parent(fitness)][0]

            k = random.randint(0, len(config.graph)-1)

            pnew = p1[:k] + p2[k:]

            if(random.uniform(0, 1) <= 0.02):
                r1 = random.randint(0, len(config.graph)-1)
                r2 = random.randint(0, len(mp)-1)

                pnew[r1] = r2

            s, c, r = utils.simulate_pso(pnew, mp = mp, enc = enc)
            smin = min(s, smin)
            smax = max(s, smax)
            cmin = min(c, cmin)
            cmax = max(c, cmax)
            rmin = min(r, rmin)
            rmax = max(r, rmax)

            ft = 0.8*(c - cmin)/(cmax - cmin) + 0.2*(rmax - r)/(rmax - rmin)
            best_fitness = 0.8*(X[best_idx][2] - cmin)/(cmax - cmin) + 0.2*(rmax - X[best_idx][3])/(rmax - rmin)

            r3 = random.randint(0, num_pop-1)

            if(ft < best_fitness):
                X[r3] = [deepcopy(pnew), s, c, r]
                best_fitness = ft
                best_idx = r3
            
            else:
                while(r3 == best_idx):
                    r3 = random.randint(0, num_pop-1)

                X[r3] = [deepcopy(pnew), s, c, r]
    
    return X[best_idx][1], X[best_idx][2], X[best_idx][3], X[best_idx][0]

def span_rel(mp = {}, enc = []):
    if(mp == {}):
        mp = deepcopy(config.mapping)

    num_pop = 100
    num_gen = 1500

    X = []

    smin = float('inf')
    smax = 0
    cmin = float('inf')
    cmax = 0
    rmin = float('inf')
    rmax = 0

    best_fitness = float('inf')
    best_idx = -1

    for i in range(num_pop):
        particle = [random.randint(0, len(mp)-1) for _ in range(len(config.graph))]
        s, c, r = utils.simulate_pso(particle, mp = mp, enc = enc)

        smin = min(s, smin)
        smax = max(s, smax)
        cmin = min(c, cmin)
        cmax = max(c, cmax)
        rmin = min(r, rmin)
        rmax = max(r, rmax)

        X.append([deepcopy(particle), s, c, r])
    
    for gen in range(num_gen):
        fitness = []
        for i in range(num_pop):
            ft = 0.8*(X[i][1] - smin)/(smax - smin) + 0.2*(rmax - X[i][3])/(rmax - rmin)
            if(ft < best_fitness):
                best_fitness = ft
                best_idx = i
            
            fitness.append(ft)
        
        if(random.uniform(0, 1) <= 0.9):
            p1 = X[select_parent(fitness)][0]
            p2 = X[select_parent(fitness)][0]

            k = random.randint(0, len(config.graph)-1)

            pnew = p1[:k] + p2[k:]

            if(random.uniform(0, 1) <= 0.02):
                r1 = random.randint(0, len(config.graph)-1)
                r2 = random.randint(0, len(mp)-1)

                pnew[r1] = r2

            s, c, r = utils.simulate_pso(pnew, mp = mp,enc = enc)
            smin = min(s, smin)
            smax = max(s, smax)
            cmin = min(c, cmin)
            cmax = max(c, cmax)
            rmin = min(r, rmin)
            rmax = max(r, rmax)

            ft = 0.8*(s - smin)/(smax - smin) + 0.2*(rmax - r)/(rmax - rmin)
            best_fitness = 0.8*(X[best_idx][1] - smin)/(smax - smin) + 0.2*(rmax - X[best_idx][3])/(rmax - rmin)

            r3 = random.randint(0, num_pop-1)

            if(ft < best_fitness):
                X[r3] = [deepcopy(pnew), s, c, r]
                best_fitness = ft
                best_idx = r3
            
            else:
                while(r3 == best_idx):
                    r3 = random.randint(0, num_pop-1)

                X[r3] = [deepcopy(pnew), s, c, r]
    
    return X[best_idx][1], X[best_idx][2], X[best_idx][3], X[best_idx][0]