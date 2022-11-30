from copy import deepcopy
import math
import config, utils


def simulate_list(mp = {}, l = []):
    if(l == []):
        l =  utils.fcws_ranks()
    
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

                    if(pr%3 == 0):
                        if(pr1%3 == 0):
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
                    
                    elif(pr%3 == 1):
                        if(pr1%3 == 1):
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
                        if(pr1%3 == 2):
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

            if(pr%3 == 0):
                num_slots = math.ceil(pt/60)
                    
            elif(pr%3 == 1):
                    num_slots = math.ceil(pt/3600)
                    
            else:
                num_slots = max(0, math.ceil((pt-600)/60))
                tp = int((pr-2)/3)
                cost += config.fixed_prices[tp][cl]
                    
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