from copy import deepcopy
import math
import config, utils

def reverse_allocation(l = [], mp = {}):
    if(mp == {}):
        mp = deepcopy(config.mapping)
    
    if(l == []):
        l = utils.ranks()

    particle = [-1 for _ in range(len(config.graph))]

    m1 = min(config.topological_levels)
    m2 = max(config.topological_levels)

    task_order = [[] for _ in range(m1, m2+1)]

    for i in range(len(l)):
        task_order[config.topological_levels[l[i]] - m1].append(l[i])


    for i in range(len(task_order)-1, -1, -1):
        vms_taken = []
        for j in range(len(task_order[i])):
            vms_task = []

            min_span = float('inf')
            max_span = 0
            min_cost = float('inf')
            max_cost = 0
            min_rel = float('inf')
            max_rel = 0

            for id in mp:
                cost = 0
                pr1, cl1, _ = mp[id]
                dec_time = 0
                enc_time = 0
                transfer_time = 0
                exec_time = config.size[task_order[i][j]]/config.center[pr1][cl1]
                rel = 1

                for k in range(len(config.graph)):
                    # if(config.graph[k][task_order[i][j]] > 0):
                    #     dec_time += config.graph[k][task_order[i][j]]*suites[enc[k][task_order[i][j]]][1]/(config.center[pr1][cl1] * 16)
                        
                    if(config.graph[task_order[i][j]][k] > 0):
                        pr2, _, _ = mp[particle[k]]
                        comm_time = 0

                        if(id != particle[k]):
                            # enc_time += config.graph[task_order[i][j]][k]*suites[enc[task_order[i][j]][k]][1]/(config.center[pr1][cl1] * 16)
                            if(pr1 == pr2):
                                comm_time = config.graph[task_order[i][j]][k]/config.inter
                                
                            else:
                                comm_time = config.graph[task_order[i][j]][k]/config.ext
                        
                        transfer_time += comm_time
                        rel = rel * math.exp(-config.params[pr1][pr2] * comm_time)

                        data = config.graph[task_order[i][j]][k]/1000
                        if(pr1 == pr2):
                            continue

                        if(pr1%3 == 0):
                            if(pr2%3 == 0):
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
                        
                        elif(pr1%3 == 1):
                            if(pr2%3 == 1):
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
                            if(pr2%3 == 2):
                                cost += 0.05*data
                            elif(data <= 1*1000):
                                cost += 0.19*data
                            elif(data <= 10*1000):
                                cost += 0.18*data
                            else:
                                cost += 0.15*data
                
                pt = dec_time + exec_time + enc_time + transfer_time

                if(pr1%3 == 0):
                    slots = math.ceil(pt/3600)
                elif(pr1%3 == 1):
                    slots = math.ceil(pt/60)
                else:
                    slots = max(math.ceil(pt/60)-10, 0)
                    tp = int((pr1-2)/3)
                    cost += config.fixed_prices[tp][cl1]
                        
                cost += slots*config.prices[pr1][cl1]
                rel = rel * math.exp(-config.params[pr1][pr1] * pt)

                min_span = min(min_span, pt)
                max_span = max(max_span, pt)
                min_cost = min(min_cost, cost)
                max_cost = max(max_cost, cost)
                min_rel = min(min_rel, rel)
                max_rel = max(max_rel, rel)

                vms_task.append([id, pt, cost, rel])

            for id in range(len(vms_task)):
                metric = vms_task[id][2]
                if(min_span != max_span and min_rel != max_rel):
                    metric = 0.7*(vms_task[id][2] - min_cost)/(max_cost - min_cost) + 0.2*(vms_task[id][1] - min_span)/(max_span - min_span) + 0.1*(max_rel - vms_task[id][3])/(max_rel - min_rel)
                    
                elif(min_span != max_span):
                    metric = 0.8*(vms_task[id][2] - min_cost)/(max_cost - min_cost) + 0.2*(vms_task[id][1] - min_span)/(max_span - min_span)
                    
                # if(min_rel != max_rel):
                #     metric = 0.9*(vms_task[id][2] - min_cost)/(max_cost - min_cost) + 0.1*(max_rel - vms_task[id][3])/(max_rel - min_rel)

                vms_task[id].append(metric)
                
            vms_task.sort(key=lambda x: x[4])
            
            for k in range(len(vms_task)):
                if(vms_task[k][0] not in vms_taken):
                    particle[task_order[i][j]] = vms_task[k][0]
                    vms_taken.append(vms_task[k][0])
                    break
    
    return particle