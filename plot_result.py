import bi_fast_marching_trees
import fast_marching_trees
import matplotlib.pyplot as plt

sample_n = [500, 1000, 1500, 2000, 2500, 3000]
time_elp_res_bi, cost_res_bi, col_check_res_bi, suc_rate_res_bi = bi_fast_marching_trees.main()
time_elp_res_uni, cost_res_uni, col_check_res_uni, suc_rate_res_uni = fast_marching_trees.main()

plt.clf()
plt.plot(sample_n, time_elp_res_bi, label='BFMT')
plt.plot(sample_n, time_elp_res_uni, label='FMT')
plt.title('Execution Time vs Sample Count (Basic map)')
plt.xlabel('Sample Count')
plt.ylabel('Execution Time')
plt.legend()
plt.show()

plt.clf()
plt.plot(sample_n, cost_res_bi, label='BFMT')
plt.plot(sample_n, cost_res_uni, label='FMT')
plt.title('Solution Cost vs Sample Count (Basic map)')
plt.xlabel('Solution Cost')
plt.ylabel('Execution Time')
plt.legend()
plt.show()

plt.clf()
plt.plot(sample_n, col_check_res_bi, label='BFMT')
plt.plot(sample_n, col_check_res_uni, label='FMT')
plt.title('Number of Collision Checks vs Sample Count (Basic map)')
plt.xlabel('Sample Count')
plt.ylabel('Execution Time')
plt.legend()
plt.show()

plt.clf()
plt.plot(sample_n, suc_rate_res_bi, label='BFMT')
plt.plot(sample_n, suc_rate_res_uni, label='FMT')
plt.title('Execution Time vs Sample Count (Basic map)')
plt.xlabel('Sample Count')
plt.ylabel('Execution Time')
plt.legend()
plt.show()


