from copy import deepcopy
import numpy as np
import math
import config

def fcws_ranks():
    l = [[i, 0] for i in range(len(config.graph))]
    cap = []
    p = []
    for i in range(len(config.center)):
        if(i%3 == 0):
            for j in range(len(config.center[i])):
                cap.append(config.center[i][j])
                p.append(config.prices[i][j])
    
    start = []
    fins = []
    rents = []

    cap = np.median(cap)
    p = np.median(p)

    for i in range(len(config.graph)):
        start.append(0)
        fins.append(0)
        rents.append(0)
    
    for i in range(len(config.graph)):
        s = 0
        t = 0
        exec_time = config.size[i]/cap
        if(i > 0):
            t = float('inf')
            for j in range(len(config.graph)):
                if(config.graph[j][i] > 0):
                    comm_time = config.graph[j][i]/config.inter
                    t = min(t, fins[j])
                    s = max(s, fins[j]+comm_time)

        f = s + exec_time
        rents[i] = f-t
    
    for i in range(len(config.graph)-1, -1, -1):
        m = 0
        for j in range(len(config.graph)):
            if(config.graph[i][j] > 0):
                m = max(m, l[j][1])
        
        l[i][1] = m + p*rents[i]
    
    l.sort(key=lambda x: x[1], reverse=True)
    l = [l[i][0] for i in range(len(config.graph))]
    return l

def simulate_list(mp = {}, l = []):
    if(l == []):
        l =  fcws_ranks()
    
    if(mp == {}):
        mp = deepcopy(config.mapping)

    R = {}
    M = {}
    particle = [0]

    for i in range(len(config.graph)):
        particle.append(0)

    for k in mp:
        R[k] = []
    
    for i in range(len(l)):
        d = {}
        for id in R:
            pr = mp[id][0]
            cl = mp[id][1]
            exec_time = config.size[l[i]]/config.center[pr][cl]
            s = 0
            min_fins = []
            
            cost = 0
            r = 1

            for j in range(len(config.graph)):
                if(config.graph[j][l[i]] > 0):
                    vm = M[j][0]
                    pr1 = mp[vm][0]
                    comm_time = 0

                    if(id != vm):
                        if(pr == pr1):
                            comm_time = config.graph[j][l[i]]/config.inter
                        else:
                            comm_time = config.graph[j][l[i]]/config.ext

                    r = r * math.exp(-config.params[pr1][pr] * comm_time)
                    s = max(s, M[j][2] + comm_time)
                    min_fins.append(M[j][2])

                    data = config.graph[j][l[i]]/1000
                    if(pr == pr1):
                        continue

                    if(pr < config.aws_providers):
                        if(pr1 < config.aws_providers):
                            cost += 0.02*data
                        elif(data <= 100):
                            cost += 0
                        elif(data <= 10*1000):
                            cost += 0.09*data
                        elif(data <= 40*1000):
                            cost += 0.085*data
                        elif(data <= 100*1000):
                            cost += 0.07*data
                        else:
                            cost += 0.05*data
                        
                    elif(pr < config.aws_providers + config.ma_providers):
                        if(pr1 < config.aws_providers + config.ma_providers):
                            cost += 0.08*data
                        elif(data <= 100):
                            cost += 0
                        elif(data <= 10*1000):
                            cost += 0.11*data
                        elif(data <= 40*1000):
                            cost += 0.075*data
                        elif(data <= 100*1000):
                            cost += 0.07*data
                        else:
                            cost += 0.06*data
                        
                    else:
                        if(pr1 >= config.aws_providers + config.ma_providers):
                            cost += 0.05*data
                        elif(data <= 1*1000):
                            cost += 0.19*data
                        elif(data <= 10*1000):
                            cost += 0.18*data
                        else:
                            cost += 0.15*data

            t = 0
            if(len(min_fins) > 0):
                t = min(min_fins)
            
            f = s + exec_time
            
            pt = f - s

            r = r * math.exp(-config.params[pr][pr] * pt)

            if(pr < config.aws_providers):
                num_slots = math.ceil(pt/60)
                    
            elif(pr < config.aws_providers + config.ma_providers):
                    num_slots = math.ceil(pt/3600)
                    
            else:
                num_slots = max(0, math.ceil(pt/60) - 10)
                cost += config.fixed_prices[pr - config.aws_providers - config.ma_providers][cl]
                    
            cost += config.prices[pr][cl] * num_slots
            d[id] = [id, s, f, t, cost, r]
        
        best_vm = -1
        best_metric = float('inf')
        min_cost = float('inf')
        max_cost = 0
        min_rel = float('inf')
        max_rel = 0
        min_fin = float('inf')
        max_fin = 0

        for id in d:
            min_cost = min(min_cost, d[id][4])
            max_cost = max(max_cost, d[id][4])
            min_rel = min(min_rel, d[id][5])
            max_rel = max(max_rel, d[id][5])
            min_fin = min(min_fin, d[id][2])
            max_fin = max(max_fin, d[id][2])
        
        for id in d:
            metric = d[id][4]

            if(min_rel != max_rel):
                metric = 0.8*(d[id][4] - min_cost)/(max_cost - min_cost) +0.2*(max_rel - d[id][5])/(max_rel - min_rel)

            if(metric < best_metric):
                best_vm = id
                best_metric = metric
        
        assert(len(d) == len(mp))
        if(R[best_vm] == []):
            R[best_vm] = [d[best_vm][3], d[best_vm][2]]
        
        else:
            R[best_vm][1] = d[best_vm][2]
        
        M[l[i]] = [best_vm, d[best_vm][1], d[best_vm][2], d[best_vm][4], d[best_vm][5]]
        particle[l[i]] = best_vm


    return particle