import math
from copy import deepcopy
import config


def ranks():
    avg_bw = (config.inter + (config.providers - 1)*config.ext)/config.providers

    x = [[i, 0] for i in range(len(config.graph))]

    sz = []
    for j in range(len(config.center)):
        for k in range(len(config.center[j])):
            sz.append(config.center[j][k])

    avg_size = sum(sz)/len(sz)

    enc_times = []
    for pr in range(len(config.center)):
        for cl in range(len(config.center[pr])):
            for s in range(len(config.suites)):
                tt = config.suites[s][1]/(config.center[pr][cl] * 16)
                enc_times.append(tt)
    
    avg_enc_time = sum(enc_times)/len(enc_times)

    for i in range(len(config.graph)-1, -1, -1):
        mt = 0
        comm_time = 0
        enc_time = 0
        dec_time = 0

        for j in range(len(config.graph)):
            if(config.graph[i][j] > 0):
                mt = max(mt, x[j][1])
                comm_time = comm_time + config.graph[i][j]/avg_bw
                enc_time = enc_time + config.graph[i][j]*avg_enc_time
            
            if(config.graph[j][i] > 0):
                dec_time = dec_time + config.graph[j][i]*avg_enc_time
        
        x[i][1] = mt + dec_time + config.size[i]/avg_size + enc_time + comm_time

    x.sort(key=lambda x: x[1], reverse= True) 
    return [x[i][0] for i in range(len(x))]

def determine_enc(V, message_vul, particle, mp = {}):
    if(mp == {}):
        mp = deepcopy(config.mapping)

    vul = 0
    encoding = []
    edge_mapping = []
    ctr = 0

    for i in range(len(config.graph)):
        encoding.append([])
        for j in range(len(config.graph[i])):
            encoding[i].append(0)
            if(config.graph[i][j] > 0):
                edge_mapping.append([i, j])

    dp = []
    for i in range(len(edge_mapping)):
        dp.append([])
        for j in range(V+1):
            dp[i].append(0)
    

    for i in range(len(edge_mapping)):
        v1, v2 = edge_mapping[i]
        pr1, cl1, _ = mp[particle[v1]]
        pr2, cl2, _ = mp[particle[v2]]

        for j in range(V+1):
            min_time = float('inf')
            min_idx = -1
            for k in range(len(config.suites)):
                if(i == 0):
                    if(config.weights[v1][v2] * config.suites[k][0] <= j and config.suites[k][0] <= message_vul[v1][v2]):
                        dp[i][j] = [k, config.suites[k][1]*config.graph[v1][v2]/(config.center[pr1][cl1] * 16) + config.suites[k][1]*config.graph[v1][v2]/(config.center[pr2][cl2] * 16)]
                        break
                
                else:
                    if(config.weights[v1][v2] * config.suites[k][0] <= j and config.suites[k][0] <= message_vul[v1][v2]):
                        v_target = j - config.weights[v1][v2] * config.suites[k][0]
                        if(dp[i-1][v_target][1] + config.suites[k][1]*config.graph[v1][v2]/(config.center[pr1][cl1] * 16) + config.suites[k][1]*config.graph[v1][v2]/(config.center[pr2][cl2] * 16) < min_time):
                            min_time = dp[i-1][v_target][1] + config.suites[k][1]*config.graph[v1][v2]/(config.center[pr1][cl1] * 16) + config.suites[k][1]*config.graph[v1][v2]/(config.center[pr2][cl2] * 16)
                            min_idx = k

            if(i != 0):
                dp[i][j] = [min_idx, min_time]
    
    v_target = V
    for i in range(len(edge_mapping)-1, -1, -1):
        v1, v2 = edge_mapping[i]
        encoding[v1][v2] = dp[i][v_target][0]
        v_target = v_target - config.weights[v1][v2] * config.suites[encoding[v1][v2]][0]
        vul = vul + config.weights[v1][v2] * config.suites[encoding[v1][v2]][0]
    
    return encoding, vul

def simulate_pso(particle, mp = {}, l = [], enc = []):
    if(l == []):
        l = [i for i in range(len(config.graph))]
    
    if(mp == {}):
        mp = deepcopy(config.mapping)

    R = {}
    M = {}
    rel = 1
    for i in range(len(l)):
        pr1, cl1, _ = mp[particle[l[i]]]
        exec_time = config.size[l[i]]/config.center[pr1][cl1]
        s = 0
        transfer = 0
        dec_time = 0
        enc_time = 0
        for j in range(len(config.graph)):
            if(config.graph[j][l[i]] > 0):
                # if(particle[l[i]] != particle[j]):
                #     dec_time += config.graph[j][l[i]]*config.suites[enc[j][l[i]]][1]/(config.center[pr1][cl1] * 16)
                s = max(s, M[j][2])
                
            if(config.graph[l[i]][j] > 0):
                pr2, _, _ = mp[particle[j]]
                comm_time = 0

                if(particle[l[i]] != particle[j]):
                    # enc_time += config.graph[l[i]][j]*config.suites[enc[l[i]][j]][1]/(config.center[pr1][cl1] * 16)
                    if(pr1 == pr2):
                        comm_time = config.graph[l[i]][j]/config.inter
                    
                    else:
                        comm_time = config.graph[l[i]][j]/config.ext
                
                transfer += comm_time
                rel = rel * math.exp(-comm_time * config.params[pr2][pr1])
            
        if(particle[l[i]] in R):
            s = max(s, R[particle[l[i]]][1])
            
        else:
            s = max(s, config.boot_time)
            R[particle[l[i]]] = [s-config.boot_time, s]

        f = s + dec_time + exec_time + enc_time + transfer
        M[l[i]] = [particle[l[i]], s, f]
        R[particle[l[i]]][1] = f
        
    makespan = 0
    for task in M:
        makespan = max(makespan, M[task][2])
        
    cost = 0
    for id in R:
        time = R[id][1] - R[id][0]
        if(time < 0):
            print("Something went wrong negative time", R[id][3], R[id][2])
            quit()

        pr = mp[id][0]
        cl = mp[id][1]
        slots = 0
        if(pr%3 == 0):
            slots = math.ceil(time/3600)
        elif(pr%3 == 1):
            slots = math.ceil(time/60)
        else:
            tp = int((pr-2)/3)
            cost += config.fixed_prices[tp][cl]
                
        cost += slots*config.prices[pr][cl]
        rel = rel * math.exp(-time * config.params[pr][pr])
    
    for i in range(len(config.graph)):
        pr = R[particle[i]][0]
        for j in range(len(config.graph)):
            pr1 = R[particle[j]][0]
            if(config.graph[i][j] > 0):
                data = config.graph[i][j]/1000
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
    
    return makespan, cost, rel

def simulate_pso_actual(particle, mp = {}, l = [], enc = []):
    if(l == []):
        l = [i for i in range(len(config.graph))]
    
    if(mp == {}):
        mp = deepcopy(config.mapping)

    R = {}
    M = {}
    rel = 1
    for i in range(len(l)):
        pr1, cl1, _ = mp[particle[l[i]]]
        exec_time = config.size[l[i]]/config.center[pr1][cl1]
        s = 0
        transfer = 0
        dec_time = 0
        enc_time = 0
        for j in range(len(config.graph)):
            if(config.graph[j][l[i]] > 0):
                if(particle[l[i]] != particle[j]):
                    dec_time += config.graph[j][l[i]]*config.suites[enc[j][l[i]]][1]/(config.center[pr1][cl1] * 16)
                s = max(s, M[j][2])
                
            if(config.graph[l[i]][j] > 0):
                pr2, _, _ = mp[particle[j]]
                comm_time = 0

                if(particle[l[i]] != particle[j]):
                    enc_time += config.graph[l[i]][j]*config.suites[enc[l[i]][j]][1]/(config.center[pr1][cl1] * 16)
                    if(pr1 == pr2):
                        comm_time = config.graph[l[i]][j]/config.inter
                    
                    else:
                        comm_time = config.graph[l[i]][j]/config.ext
                
                transfer += comm_time
                rel = rel * math.exp(-comm_time * config.params[pr2][pr1])
            
        if(particle[l[i]] in R):
            s = max(s, R[particle[l[i]]][1])
            
        else:
            s = max(s, config.boot_time)
            R[particle[l[i]]] = [s-config.boot_time, s]

        f = s + dec_time + exec_time + enc_time + transfer
        M[l[i]] = [particle[l[i]], s, f]
        R[particle[l[i]]][1] = f
        
    makespan = 0
    for task in M:
        makespan = max(makespan, M[task][2])
        
    cost = 0
    for id in R:
        time = R[id][1] - R[id][0]
        if(time < 0):
            print("Something went wrong negative time", R[id][3], R[id][2])
            quit()

        pr = mp[id][0]
        cl = mp[id][1]

        if(pr%3 == 0):
            slots = math.ceil(time/3600)
        elif(pr%3 == 1):
            slots = math.ceil(time/60)
        else:
            tp = int((pr-2)/3)
            slots = max(math.ceil(time/60)-10, 0)
            cost += config.fixed_prices[tp][cl]
                
        cost += slots*config.prices[pr][cl]
        rel = rel * math.exp(-time * config.params[pr][pr])
    
    for i in range(len(config.graph)):
        pr = R[particle[i]][0]
        for j in range(len(config.graph)):
            pr1 = R[particle[j]][0]
            if(config.graph[i][j] > 0):
                data = config.graph[i][j]/1000
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
    
    return makespan, cost, rel

def improved_allocation(particle, mp = {}, l = [], span = float('inf'), num_iter = 30):
    if(l == []):
        l = ranks()
    
    if(mp == {}):
        mp = deepcopy(config.mapping)

    old_particle = deepcopy(particle)

    for itr in range(num_iter):
        # random.shuffle(l)
        for i in range(len(l)):
            d = {}
            cmin = float('inf')
            cmax = 0
            rmin = float('inf')
            rmax = 0
            smin = float('inf')
            smax = 0
            for id in mp:
                particle[l[i]] = id
                s, c, r = simulate_pso(particle, mp = mp)
                cmin = min(c, cmin)
                cmax = max(c, cmax)
                rmin = min(r, rmin)
                rmax = max(r, rmax)
                smin = min(s, smin)
                smax = max(s, smax)
                d[id] = [s, c, r]
                
            best_metric = float('inf')
            best_vm = -1

            best_span = float('inf')
            best_vm2 = -1

            for id in d:
                if(d[id][0] <= span):
                    metric = d[id][1]
                    if(smin != smax and rmin != rmax):
                        metric = 0.7*(d[id][1] - cmin)/(cmax - cmin) + 0.2*(d[id][0] - smin)/(smax - smin) + 0.1*(rmax - d[id][2])/(rmax - rmin)
                    
                    elif(smin != smax):
                        metric = 0.8*(d[id][1] - cmin)/(cmax - cmin) + 0.2*(d[id][0] - smin)/(smax - smin)
                    
                    elif(rmin != rmax):
                        metric = 0.9*(d[id][1] - cmin)/(cmax - cmin) + 0.1*(rmax - d[id][2])/(rmax - rmin)

                    if(metric < best_metric):
                        best_vm = id
                        best_metric = metric
                
                elif(d[id][0] < best_span):
                    best_vm2 = id
                    best_span = d[id][0]
                
                elif(d[id][0] == best_span and d[id][1] < d[best_vm2][1]):
                    best_vm2 = id
            
            if(best_vm == -1):
                best_vm = best_vm2

            particle[l[i]] = best_vm
        
        if(particle == old_particle):
            break
            # pos = random.randint(0, len(config.graph)-1)
            # vm = random.randint(0, len(mp)-1)
            # particle[pos] = vm
        
        old_particle = deepcopy(particle)
    
    s, c, r = simulate_pso(particle, mp = mp)
    return s, c, r, particle

def heft(mp = {}):
    if(mp == {}):
        mp = deepcopy(config.mapping)

    l = ranks()
    R = {}
    M = {}
    makespan = 0

    for k in mp:
        pr, cl, _ = mp[k]
        R[k] = [pr, cl, 0, 0]

    # s, c = simulate_pso(particle, mapping, orders[it])
    for i in range(len(l)):
        min_vm = -1
        min_fin = float('inf')
        for vm in mp:
            s = 0
            if(R[vm][3] != 0):
                s = R[vm][3]
                pr = R[vm][0]
                cl = R[vm][1]
                exec_time = config.size[l[i]]/config.center[pr][cl]
                for j in range(len(config.graph)):
                    if(config.graph[j][l[i]] > 0):
                        pr1 = R[M[j][0]][0]
                        if(vm != M[j][0]):
                            if(pr == pr1):
                                s = max(s, M[j][2] + config.graph[j][l[i]]/config.inter)
                            else:
                                s = max(s, M[j][2] + config.graph[j][l[i]]/config.ext)
                        
                        else:
                            s = max(s, M[j][2])
            
            else:
                s = config.boot_time
                pr = R[vm][0]
                cl = R[vm][1]
                exec_time = config.size[l[i]]/config.center[pr][cl]
                for j in range(len(config.graph)):
                    if(config.graph[j][l[i]] > 0):
                        pr1 = R[M[j][0]][0]
                        if(pr == pr1):
                            s = max(s, M[j][2] + config.graph[j][l[i]]/config.inter)
                        else:
                            s = max(s, M[j][2] + config.graph[j][l[i]]/config.ext)
            
            f = s + exec_time
            if(f < min_fin):
                min_vm = vm
                min_fin = f
        
        pr = R[min_vm][0]
        cl = R[min_vm][1]
        s = min_fin - config.size[l[i]]/config.center[pr][cl]

        if(R[min_vm][3] == 0):
            R[min_vm][2] = s - config.boot_time

        R[min_vm][3] = min_fin
        M[l[i]] = [min_vm, s, min_fin]
        makespan = max(makespan, min_fin)
    
    particle = [0 for _ in range(len(config.graph))]

    for i in M:
        particle[i] = M[i][0]

    return particle, makespan