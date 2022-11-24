from copy import deepcopy
import math
import config, utils, lbs, gsa, biobjective
import argparse
import matplotlib.pyplot as plt

results = [[0, 0, 0, 0] for _ in range(5)]

parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME -p PASSWORD -size 20000
parser.add_argument("-num", dest = "num", default = 24, type=int)
parser.add_argument("-itr", dest = "itr", default = 5, type=int)
parser.add_argument("-p", dest = "p", default = 6, type=int)
parser.add_argument("-V", dest = "V", default = 0.5, type=float)
parser.add_argument("-smin", dest = "smin", default = 10, type=int)
parser.add_argument("-smax", dest = "smax", default = 10**3, type=int)

args = parser.parse_args()

config.providers = args.p
config.smin = args.smin
config.smax = args.smax

for gen in range(args.itr):
    print("Iteration: ", gen+1)
    print("Number:", args.num)
    config.init(args.num)
    _, _, _, gsa_particle = gsa.gsa(mp = config.mp, enc = [])
    my_particle = lbs.reverse_allocation(mp = config.mp)
    _, _, _, sc = biobjective.span_cost(mp = config.mp, enc = [])
    _, _, _, cr = biobjective.cost_rel(mp = config.mp, enc = [])
    _, _, _, sr = biobjective.span_rel(mp = config.mp, enc = [])

    gsa_particle_imp = deepcopy(gsa_particle)
    my_particle_imp = deepcopy(my_particle)
    sc_imp = deepcopy(sc)
    cr_imp = deepcopy(cr)
    sr_imp = deepcopy(sr)

    # _, _, _, gsa_particle_imp = improved_allocation(gsa_particle_imp, mp = config.mp)
    # _, _, _, my_particle_imp = improved_allocation(my_particle_imp, mp = config.mp)
    # _, _, _, sc_imp = improved_allocation(sc_imp, mp = config.mp)
    # _, _, _, cr_imp = improved_allocation(cr_imp, mp = config.mp)
    # _, _, _, sr_imp = improved_allocation(sr_imp, mp = config.mp)

    V = math.ceil(args.V * config.v_max)
    print("Constraint: ", V)

        
    enc, vul = utils.determine_enc(V, config.message_vul, gsa_particle, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(gsa_particle, mp = config.mp, enc = enc)
    print(f"Algo: GSA No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    results[0][0] += s/3600
    results[0][1] += c
    results[0][2] += r
    results[0][3] += vul

    # enc, vul = utils.determine_enc(V, config.message_vul, gsa_particle_imp, mp = config.mp)
    # s, c, r = utils.simulate_pso_actual(gsa_particle_imp, mp = config.mp, enc = enc)
    # print(f"Algo: GSA+LS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    # results[5][0] += s/3600
    # results[5][1] += c
    # results[5][2] += r
    # results[5][3] += vul

        
    enc, vul = utils.determine_enc(V, config.message_vul, my_particle, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(my_particle, mp = config.mp, enc = enc)
    results[1][0] += s/3600
    results[1][1] += c
    results[1][2] += r
    results[1][3] += vul
    print(f"Algo: LBS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
        
    # enc, vul = utils.determine_enc(V, config.message_vul, my_particle_imp, mp = config.mp)
    # s, c, r = utils.simulate_pso_actual(my_particle_imp, mp = config.mp, enc = enc)
    # print(f"Algo: LBS+LS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    # results[6][0] += s/3600
    # results[6][1] += c
    # results[6][2] += r
    # results[6][3] += vul

        
    enc, vul = utils.determine_enc(V, config.message_vul, sc, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(sc, mp = config.mp, enc = enc)
    print(f"Algo: Span-Cost No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    results[2][0] += s/3600
    results[2][1] += c
    results[2][2] += r
    results[2][3] += vul

    # enc, vul = utils.determine_enc(V, config.message_vul, sc_imp, mp = config.mp)
    # s, c, r = utils.simulate_pso_actual(sc_imp, mp = config.mp, enc = enc)
    # print(f"Algo: Span-Cost+LS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    # results[7][0] += s/3600
    # results[7][1] += c
    # results[7][2] += r
    # results[7][3] += vul

    enc, vul = utils.determine_enc(V, config.message_vul, cr, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(cr, mp = config.mp, enc = enc)
    print(f"Algo: Cost-Rel No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    results[3][0] += s/3600
    results[3][1] += c
    results[3][2] += r
    results[3][3] += vul

    # enc, vul = utils.determine_enc(V, config.message_vul, cr_imp, mp = config.mp)
    # s, c, r = utils.simulate_pso_actual(cr_imp, mp = config.mp, enc = enc)
    # print(f"Algo: Cost-Rel+LS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    # results[8][0] += s/3600
    # results[8][1] += c
    # results[8][2] += r
    # results[8][3] += vul

    enc, vul = utils.determine_enc(V, config.message_vul, sr, mp = config.mp)
    s, c, r = utils.simulate_pso_actual(sr, mp = config.mp, enc = enc)
    print(f"Algo: Span-Rel No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    results[4][0] += s/3600
    results[4][1] += c
    results[4][2] += r
    results[4][3] += vul

    # enc, vul = utils.determine_enc(V, config.message_vul, sr_imp, mp = config.mp)
    # s, c, r = utils.simulate_pso_actual(sr_imp, mp = config.mp, enc = enc)
    # print(f"Algo: Span-Rel+LS No. of vertices: {len(config.graph)} Span:{s/3600} Cost: {c} Rel: {r} Vul: {vul}")
    # results[9][0] += s/3600
    # results[9][1] += c
    # results[9][2] += r
    # results[9][3] += vul

    print("\n")

for i in range(len(results)):
    for j in range(len(results[i])):
            results[i][j] = results[i][j]/args.itr

print(f"Algo: GSA No. of vertices: {len(config.graph)} Span:{results[0][0]} Cost: {results[0][1]} Rel: {results[0][2]} Vul: {results[0][3]}")
print(f"Algo: LBS No. of vertices: {len(config.graph)} Span:{results[1][0]} Cost: {results[1][1]} Rel: {results[1][2]} Vul: {results[1][3]}")
print(f"Algo: Span+Cost No. of vertices: {len(config.graph)} Span:{results[2][0]} Cost: {results[2][1]} Rel: {results[2][2]} Vul: {results[2][3]}")
print(f"Algo: Cost+Rel No. of vertices: {len(config.graph)} Span:{results[3][0]} Cost: {results[3][1]} Rel: {results[3][2]} Vul: {results[3][3]}")
print(f"Algo: Span+Rel No. of vertices: {len(config.graph)} Span:{results[4][0]} Cost: {results[4][1]} Rel: {results[4][2]} Vul: {results[4][3]}")

algos = ["GSA", "LBS", "Span+Cost", "Cost+Rel", "Span+Rel"]
costs = [results[i][1] for i in range(len(results))]
spans = [results[i][0] for i in range(len(results))]
rels = [results[i][2] for i in range(len(results))]
vuls = [results[i][3] for i in range(len(results))]

plt.subplot(1, 2, 1)
plt.bar(algos, costs, color ='blue')
plt.xlabel("Algorithms")
plt.ylabel("Cost($)")
plt.title("Cost comparison")

plt.subplot(1, 2, 2)
plt.bar(algos, spans, color ='red')
plt.xlabel("Algorithms")
plt.ylabel("Makespan(sec)")
plt.title("Makespan comparison")

plt.show()
