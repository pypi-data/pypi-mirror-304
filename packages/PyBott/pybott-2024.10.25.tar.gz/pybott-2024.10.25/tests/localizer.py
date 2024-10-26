import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import ldl

from pythtb import *

from pseudopy import NonnormalAuto, demo
from matplotlib import pyplot
from scipy.linalg import eigvals

plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

def localized_dirac_operator(lambda_param, x_op, y_op, ham):
    """
    Generates the localized dirac operator based on https://arxiv.org/abs/1907.11791 eq. (2.3)
    
    L_lambda(X0, Y0, H) = [[ H - lambda_3,  (X0 - lambda_1) + i*(Y0 - lambda_2) ],
                           [ (X0 - lambda_1) - i*(Y0 - lambda_2), -H + lambda_3 ]]
    
    Args:
    - x_op (numpy.ndarray): The matrix corresponding to X0 in the formula.
    - y_op (numpy.ndarray): The matrix corresponding to Y0 in the formula.
    - ham (numpy.ndarray): The matrix corresponding to H in the formula.
    - lambda_param (numpy.ndarray): A vector of three elements [lambda_1, lambda_2, lambda_3].
    
    Returns:
    - result (numpy.ndarray): The resulting matrix from the given formula, with complex entries.
    """
    n_size = ham.shape[0]
    
    lambda_1 = lambda_param[0]
    lambda_2 = lambda_param[1]
    lambda_3 = lambda_param[2]
    
    top_left = ham - lambda_3*np.eye(n_size)
    top_right = (x_op - lambda_1*np.eye(n_size)) - 1j * (y_op - lambda_2*np.eye(n_size))
    bottom_left = (x_op - lambda_1*np.eye(n_size)) + 1j * (y_op - lambda_2*np.eye(n_size))
    bottom_right = -ham + lambda_3*np.eye(n_size)
    
    result = np.block([[top_left, top_right], [bottom_left, bottom_right]])
    
    return result

def localizer_index(kappa, lambda_param, x_op, y_op, ham):
    ldo = localized_dirac_operator(lambda_param, kappa*x_op, kappa*y_op, ham)
    L, D, perm = ldl(ldo)

    n_blocks = D.shape[0] // 2
    eigenvalues = []

    for i in range(n_blocks):
        block = D[2*i:2*i+2, 2*i:2*i+2]
        vals = np.linalg.eigvals(block)
        eigenvalues.extend(vals)

    eigenvalues = np.array(eigenvalues)

    # Λ, _ = np.linalg.eig(ldo) # opt: avoid finding eigenvalues, prefer LDLT
    # return 1/2*(np.sum(np.where(Λ>=0))-np.sum(np.where(Λ<0)))
    return 1/2*(np.sum(np.where(eigenvalues>=0))-np.sum(np.where(eigenvalues<0)))/kappa
    
def haldane_model(n_side=6, t1=1, t2=0.2j, delta=0, pbc=True):
    t2c = t2.conjugate()

    lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
    orb=[[1./3.,1./3.],[2./3.,2./3.]]

    my_model=tb_model(2,2,lat,orb)

    my_model.set_onsite([-delta,delta])

    my_model.set_hop(t1, 0, 1, [ 0, 0])
    my_model.set_hop(t1, 1, 0, [ 1, 0])
    my_model.set_hop(t1, 1, 0, [ 0, 1])

    my_model.set_hop(t2 , 0, 0, [ 1, 0])
    my_model.set_hop(t2 , 1, 1, [ 1,-1])
    my_model.set_hop(t2 , 1, 1, [ 0, 1])
    my_model.set_hop(t2c, 1, 1, [ 1, 0])
    my_model.set_hop(t2c, 0, 0, [ 1,-1])
    my_model.set_hop(t2c, 0, 0, [ 0, 1])

    # cutout finite model first along direction x
    tmp_model=my_model.cut_piece(n_side,0,glue_edgs=pbc)
    # cutout also along y direction 
    fin_model=tmp_model.cut_piece(n_side,1,glue_edgs=pbc)
    
    (evals,evecs)=fin_model.solve_all(eig_vectors=True)
    
    return fin_model.get_orb(), evals, evecs.T, fin_model._gen_ham()

def plot_heatmap(kappa, lambda_3, x_op, y_op, ham, grid_size, side_length):
    data_matrix = np.zeros((grid_size, grid_size))
    for idx,x in enumerate(sample):
        for idy,y in enumerate(sample):
            lambda_param = np.array([x*kappa, y*kappa, lambda_3])
            li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
            data_matrix[idx, idy] = li

    # plt.imshow(data_matrix, extent=(-side_length, side_length, -side_length, side_length), origin='lower', cmap='hot', interpolation='nearest')
    plt.imshow(data_matrix, extent=(0, side_length, 0, side_length), origin='lower', cmap='hot', interpolation='nearest')
    plt.colorbar(label='Localizer Index')
    plt.title(f'Heatmap of Localizer Index $\\kappa={np.round(kappa,2)}$ and $\\lambda_3={np.round(lambda_3,2)}$')
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f"localizer/kappa_{np.round(kappa,2)}_l3_{np.round(lambda_3,2)}.png",format="png",bbox_inches='tight')
    plt.clf()
    plt.cla()


def li_lambda3(n_side, t1, t2, delta, a, lambda_3s):
    grid, eigenvalues, eigenvectors, ham = haldane_model(
        n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=False
    )
    x_grid,y_grid = grid.T
    x_op = np.diag(x_grid)
    y_op = np.diag(y_grid)

    lis = []

    for lambda_3 in lambda_3s:
        lambda_param = np.array([1,1,lambda_3])
        li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
        lis.append(li)
        print(li)

    return lis

    

if __name__ == "__main__":
    n_side = 20
    t1 = 1
    t2 = 1j
    delta = 0
    a = 1
    grid, eigenvalues, eigenvectors, ham = haldane_model(
        n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=False
    )

    x_grid,y_grid = grid.T

    x_op = np.diag(x_grid)
    y_op = np.diag(y_grid)

    lambda_param = np.array([0,0,1])

    grid_size = 10
    side_length = 12
    # sample = np.linspace(-side_length,side_length,grid_size)
    sample = np.linspace(0,side_length,grid_size)

    kappa = 0.5
    lambda_3 = 0.

    # plot_heatmap(kappa, lambda_3, x_op, y_op, ham, grid_size, side_length)
    # exit()
    
    lambda_3s = np.linspace(-1.1,1.1,200)
    lis_trivial = li_lambda3(n_side, t1, 0, 1, a, lambda_3s)
    lis_topo = li_lambda3(n_side, t1, 0.2j, 0, a, lambda_3s)
    plt.plot(lambda_3s, lis_trivial, color="black", label="trivial")
    plt.plot(lambda_3s, lis_topo, color="red", label="topo")
    plt.legend(fontsize=20)
    plt.xlabel(r"$\lambda_3$",fontsize=20)
    plt.ylabel(r"Localizer index",fontsize=20)
    plt.title(f"$\\kappa={kappa}\\quad N={grid.shape[0]}$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig("li_lambda3.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    
    
    # kappa = 1
    # for idkappa, kappa in enumerate(np.linspace(0.75, 1.5, 15)):
    #     print(kappa)
    #     plot_heatmap(kappa, lambda_3, x_op, y_op, ham, grid_size, side_length)

    # for idlambda_3, lambda_3 in enumerate(np.linspace(2.1, 4, 10)):
    #     print(lambda_3)
    #     plot_heatmap(kappa, lambda_3, x_op, y_op, ham, grid_size, side_length)
