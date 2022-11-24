import random
import numpy as np

def init(n):
    global providers
    global smin
    global smax
    global inter
    global ext
    global boot_time
    global max_tasks
    global graph
    global size
    global center
    global prices
    global fixed_prices
    global params
    global mapping
    global mp
    global topological_levels
    global suites
    global weights
    global message_vul
    global v_max

    providers = 6
    smin = 10
    smax = 10**5
    inter = 100
    ext = 20
    boot_time = 97
    max_tasks = 0
    v_max = 0

    graph = []
    size = []
    center = []
    prices = []
    fixed_prices = []
    params = []
    mapping = {}
    mp = {}
    suites = [[98, 3.08], [67, 3.58], [34, 4.15], [10, 4.63], [0, 5.21]]
    topological_levels = []
    weights = []
    message_vul = []

    nodes = int((n-4)/4)

    for i in range(n):
        graph.append([])
        weights.append([])
        for _ in range(n):
            graph[i].append(0)
            weights[i].append(0)

    curr_lvl = [i+1 for i in range(0, nodes)]

    for i in curr_lvl:
        graph[0][i] = random.randint(smin, smax)
    
    for _ in range(3):
        next_lvl = [curr_lvl[i]+nodes for i in range(len(curr_lvl))]

        for i in range(len(curr_lvl)):
            graph[curr_lvl[i]][next_lvl[i]] = random.randint(smin, smax)
        
        curr_lvl = next_lvl[:]
    
    for i in curr_lvl:
        graph[i][n-3] = random.randint(smin, smax)
    
    graph[n-3][n-2] = random.randint(smin, smax)
    graph[n-2][n-1] = random.randint(smin, smax)

    vertices = []
    for i in range(1, len(graph)):
        flag = 0
        for j in range(len(graph)):
            if(graph[j][i] > 0):
                flag = 1
                break
        
        if(flag == 0):
            vertices.append(i)
    
    for i in vertices:
        graph[0][i] = 1

    topological_levels = [0 for _ in range(len(graph))]
    for i in range(1, len(graph)):
        max_lvl = 0
        for j in range(len(graph)):
            if(graph[j][i] > 0 and topological_levels[j] > max_lvl):
                max_lvl = topological_levels[j]

        topological_levels[i] = max_lvl+1

    m1 = min(topological_levels)
    m2 = max(topological_levels)
    max_tasks = 0

    for i in range(m1, m2+1):
        tasks = 0
        for j in range(len(graph)):
            if(topological_levels[j] == i):
                tasks += 1
        
        max_tasks = max(max_tasks, tasks)

    v_max = 0
    for i in range(len(graph)):
        for j in range(len(graph)):
            if(graph[i][j] > 0):
                weights[i][j] = random.randint(0, 100)
                v_max = v_max + weights[i][j]*suites[0][0]

    message_vul = []
    for i in range(len(graph)):
        message_vul.append([])
        for _ in range(len(graph)):
            message_vul[i].append(0)
        
    for i in range(len(graph)):
        for j in range(len(graph)):
            if(graph[i][j] > 0):
                message_vul[i][j] = suites[random.randint(0, len(suites)-1)][0]

    size = []
    unit_price = 0.001
    center = []
    prices = []
    vm_available = 0

    for i in range(len(graph)):
        size.append(random.randint(smin, smax))

    for i in range(int(providers/3)):
        fixed_prices.append([])

    for i in range(providers):
        vms = random.randint(1, 32)
        center.append([])
        prices.append([])
        j = 0
        while(j < vms):
            cap = random.randint(1, 32)
            if(cap not in center[i]):
                vm_available += cap
                center[i].append(cap)
                c = unit_price*center[i][j]
                c = np.random.normal(loc=c, scale=c/10) 
                if(i%3 == 0):
                    prices[i].append(c)
                elif(i%3 == 1):
                    c = c*60*(1-random.randint(1,3)/10000)
                    prices[i].append(c)
                    
                else:
                    tp = int((i-2)/3)
                    fixed_prices[tp].append(c*random.randint(11, 15))
                    prices[i].append(c)
                j += 1

    mapping = {}
    ctr = 0
    for i in range(len(graph)):
        for pr in range(len(center)):
            for cl in range(len(center[pr])):
                mapping[ctr] = [pr, cl, i]
                ctr += 1

    mp = {}
    ctr = 0
    for i in range(max_tasks):
        for pr in range(len(center)):
            for cl in range(len(center[pr])):
                mp[ctr] = [pr, cl, i]
                ctr += 1

    params = []

    for i in range(providers):
        params.append([])
        for j in range(providers):
            params[i].append(0)
    
    assert(len(params) == len(params[0]) == providers == len(center))

    for i in range(providers):
        for j in range(providers):
            params[i][j] = random.randint(10, 100)/10**9
            params[j][i] = params[i][j]