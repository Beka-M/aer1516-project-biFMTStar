import bi_fast_marching_trees
import fast_marching_trees
import matplotlib.pyplot as plt
import numpy as np

sample_n = [500, 1000, 1500, 2000, 2500, 3000]
time_elp_res_uni, cost_res_uni, col_check_res_uni, suc_rate_res_uni = fast_marching_trees.main()
time_elp_res_bi, cost_res_bi, col_check_res_bi, suc_rate_res_bi = bi_fast_marching_trees.main()

if 0 in suc_rate_res_bi:
    idx = [i for i in range(len(suc_rate_res_bi)) if suc_rate_res_bi[i] != 0]
    sample_n_bi = [sample_n[i] for i in idx]
    time_elp_res_bi = [time_elp_res_bi[i] for i in idx]
    cost_res_bi = [cost_res_bi[i] for i in idx]
    col_check_res_bi = [col_check_res_bi[i] for i in idx]
    suc_rate_res_bi = [suc_rate_res_bi[i] for i in idx]
else:
    sample_n_bi = sample_n

if 0 in suc_rate_res_uni:
    idx = [i for i in range(len(suc_rate_res_uni)) if suc_rate_res_uni[i] != 0]
    sample_n_uni = [sample_n[i] for i in idx]
    time_elp_res_uni = [time_elp_res_uni[i] for i in idx]
    cost_res_uni = [cost_res_uni[i] for i in idx]
    col_check_res_uni = [col_check_res_uni[i] for i in idx]
    suc_rate_res_uni = [suc_rate_res_uni[i] for i in idx]
else:
    sample_n_uni = sample_n

plt.clf()
plt.plot(sample_n_bi, time_elp_res_bi, '-o', label='BFMT')
plt.plot(sample_n_uni, time_elp_res_uni, '-o', label='FMT')
plt.title('Execution Time vs Sample Count (Basic map)')
plt.xlabel('Sample Count')
plt.ylabel('Execution Time')
plt.legend()
plt.show()

plt.clf()
plt.plot(sample_n_bi, cost_res_bi, '-o', label='BFMT')
plt.plot(sample_n_uni, cost_res_uni, '-o', label='FMT')
plt.title('Solution Cost vs Sample Count (Basic map)')
plt.xlabel('Sample Count')
plt.ylabel('Solution Cost')
plt.legend()
plt.show()

plt.clf()
plt.plot(sample_n_bi, col_check_res_bi, '-o', label='BFMT')
plt.plot(sample_n_uni, col_check_res_uni, '-o', label='FMT')
plt.title('Number of Collision Checks vs Sample Count (Basic map)')
plt.xlabel('Sample Count')
plt.ylabel('Collision Checks')
plt.legend()
plt.show()

plt.clf()
plt.plot(sample_n_bi, suc_rate_res_bi, '-o', label='BFMT')
plt.plot(sample_n_uni, suc_rate_res_uni, '-o', label='FMT')
plt.title('Success Rate vs Sample Count (Basic map)')
plt.xlabel('Sample Count')
plt.ylabel('Success Rate')
plt.legend()
plt.show()


