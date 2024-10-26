import sys
sys.path.append("../src/pybott/")

import bott

import time

import matplotlib.pyplot as plt
import numpy as np
import scipy

import photonic
import haldane


plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

if __name__ == "__main__":
    n_side = 16
    t1 = 1
    t2 = 0.2j
    delta = 0
    pbc = True
    grid, ham = haldane.haldane_ham(
        n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=pbc
    )


    # τ0 = time.time()
    # eigenvalues, eigenvectors = scipy.linalg.eigh(ham, subset_by_value=(-2,2), driver="evr")
    # eigenvalues, eigenvectors = scipy.linalg.eigh(ham,  driver="syevr")
    # eigenvalues, eigenvectors = np.linalg.eigh(ham)
    # τ1 = time.time()
    # eigenvalues, eigenvectors = scipy.linalg.eigh(ham, subset_by_value=(-1.1,0), driver="evr")
    # sparse_matrix = scipy.sparse.csr_matrix(ham)
    # print(sparse_matrix)
    # eigenvalues, eigenvectors = scipy.sparse.linalg.eigsh(sparse_matrix, 100, which='SM')
    # τ2 = time.time()

    # print(τ1-τ0)
    # print(τ2-τ1)
    # exit()

    # cut_off = 30
    
    # for _ in range(cut_off):
    #     eigenvalues = np.delete(eigenvalues, 0, axis=0)
    #     eigenvectors = np.delete(eigenvectors, 0, axis=1)

    # eigenvalues, eigenvectors = bott.sorting_eigenvalues(
    #     eigenvalues, eigenvectors, False
    # )

    epsilon = 0.1
    gap_min = -np.abs(delta-3*np.sqrt(3)*np.abs(t2)) - epsilon
    gap_max = -gap_min
    bott_index = bott.all_bott(grid, ham)
    n_size = ham.shape[0]

    # print(f"The Bott index for the given parameters δ={delta} and {t2=} is: {bott_index}")

    plt.hist(bott_index.keys(), color="black", bins=80, histtype='step')

    for energy in bott_index.keys():
        plt.scatter(energy, bott_index[energy], color="red")

    plt.xlabel("Energy",fontsize=20)
    plt.ylabel("DOS and Bott index",fontsize=20)
    plt.title(f"$N={n_size}$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f"hist_all_bott_{pbc=}.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()
