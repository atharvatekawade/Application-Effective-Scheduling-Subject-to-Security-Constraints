import math
import config, utils, lbs, gsa, fcws
import argparse
import matplotlib.pyplot as plt

results = [[0, 0, 0, 0] for _ in range(3)]
vv = 0

parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME -p PASSWORD -size 20000
parser.add_argument("-num", dest = "num", default = 24, type=int)
parser.add_argument("-itr", dest = "itr", default = 5, type=int)
parser.add_argument("-aws", dest = "aws", default = 2, type=int)
parser.add_argument("-ma", dest = "ma", default = 2, type=int)
parser.add_argument("-gcp", dest = "gcp", default = 2, type=int)
parser.add_argument("-V", dest = "V", default = 0.5, type=float)
parser.add_argument("-smin", dest = "smin", default = 10, type=int)
parser.add_argument("-smax", dest = "smax", default = 10**3, type=int)

args = parser.parse_args()

config.smin = args.smin
config.smax = args.smax

for gen in range(args.itr):
    print("Iteration: ", gen+1)
    config.init(args.aws, args.ma, args.gcp, args.num)
    _, _, _, gsa_particle = gsa.gsa(mp = config.mp, enc = [])
    my_particle = lbs.reverse_allocation(mp = config.mp)
    fcws_particle = fcws.simulate_list(mp = config.mp)

    V = math.ceil(args.V * config.v_max)
    vv += V
    print("Constraint: ", V)

        
    enc, vul = utils.determine_enc(V, config.message_vul, gsa_particle, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(gsa_particle, mp = config.mp, enc = enc)
    print(f"Algo: GSA No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    results[0][0] += s/3600
    results[0][1] += c
    results[0][2] += r
    results[0][3] += vul

    enc, vul = utils.determine_enc(V, config.message_vul, my_particle, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(my_particle, mp = config.mp, enc = enc)
    results[1][0] += s/3600
    results[1][1] += c
    results[1][2] += r
    results[1][3] += vul
    print(f"Algo: LBS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
        

    enc, vul = utils.determine_enc(V, config.message_vul, fcws_particle, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(fcws_particle, mp = config.mp, enc = enc)
    print(f"Algo: FCWS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    results[2][0] += s/3600
    results[2][1] += c
    results[2][2] += r
    results[2][3] += vul


    print("\n")

for i in range(len(results)):
    for j in range(len(results[i])):
            results[i][j] = results[i][j]/args.itr

print(f"Algo: GSA No. of vertices: {len(config.graph)} Span:{results[0][0]} Cost: {results[0][1]} Rel: {results[0][2]} Vul: {results[0][3]}")
print(f"Algo: LBS No. of vertices: {len(config.graph)} Span:{results[1][0]} Cost: {results[1][1]} Rel: {results[1][2]} Vul: {results[1][3]}")
print(f"Algo: FCWS No. of vertices: {len(config.graph)} Span:{results[2][0]} Cost: {results[2][1]} Rel: {results[2][2]} Vul: {results[2][3]}")

algos = ["GSA", "LBS", "FCWS"]
costs = [results[i][1] for i in range(len(results))]
spans = [results[i][0] for i in range(len(results))]
rels = [results[i][2] for i in range(len(results))]
vuls = [results[i][3] for i in range(len(results))] + [vv/args.itr]

plt.subplot(2, 2, 1)
plt.bar(algos, costs, color ='blue')
# plt.xlabel("Algorithms")
plt.ylabel("Cost($)")
plt.title("Cost comparison")

plt.subplot(2, 2, 2)
plt.bar(algos, spans, color ='red')
# plt.xlabel("Algorithms")
plt.ylabel("Makespan(sec)")
plt.title("Makespan comparison")

plt.subplot(2, 2, 3)
plt.bar(algos, rels, color ='maroon')
# plt.xlabel("Algorithms")
plt.ylabel("Rel")
plt.title("Reliability comparison")

plt.subplot(2, 2, 4)
plt.bar(algos + ["Vul_constraint"], vuls, color ='pink')
# plt.xlabel("Algorithms")
plt.ylabel("Vulnerability")
plt.title("Security constraint")


plt.show()
