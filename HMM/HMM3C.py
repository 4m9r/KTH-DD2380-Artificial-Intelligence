import sys
import math
import time
import numpy as np
def main():
    input_file = open("hmm_c_N10000.in", 'r').readline()
    input_split = input_file.split(" ")
    obs = []
    for i in range(1, len(input_split)):
        obs.append(int(input_split[i]))
    # obs = obs[:100]
    A = [[0.54, 0.26, 0.20], [0.19, 0.53, 0.28], [0.22, 0.18, 0.6]]
    B = [[0.5, 0.2, 0.11, 0.19], [0.22, 0.28, 0.23, 0.27], [0.19, 0.21, 0.15, 0.45]]
    pi = [[0.3, 0.2, 0.5]]
    
    # A = np.random.uniform(0,1,(3,3))
    # B = np.random.uniform(0,1,(3,4))
    # pi = [np.random.uniform(0,1,3)]
    
    
    # A = [[.6 , .1, .3], [.2, .7, .1], [.2, .2, .6]]
    # B = [[.6, .25, .05,.05], [0.15, .35, .35,.15], [.1, .2, .1,.6]]
    # pi = [[0.9, 0.1, 0]]
    
    
    # A = [[0.54, 0.16, 0.10, .2], [0.19, 0.43, 0.28, .1], [0.22, 0.18, 0.4, 0.2], [0.1, 0.3, 0.4, 0.2 ]]
    # B = [[0.5, 0.2, 0.11, 0.19], [0.22, 0.28, 0.23, 0.27], [0.19, 0.21, 0.15, 0.45], [0.3, 0.2, 0.1, 0.4]]
    # pi = [[0.2, 0.1, 0.5, .2]]
    
    
    
    # A = [[0.54, 0.16], [0.19, 0.43]]
    # B = [[0.5, 0.2, 0.11, 0.19], [0.22, 0.28, 0.23, 0.27]]
    # pi = [[0.2, 0.1]]

    
    
    
    # for i in range(3):
    #     for j in range(3):
    #         A[i][j] = A[i][j] / sum(A[i])
    
    # for i in range(3):
    #     for j in range(4):
    #         B[i][j] = B[i][j] / sum(B[i]) 
            
            
    
    # for i in range(3):
    #     pi[0][i] = pi[0][i]/ sum(pi[0])  
    
    print(pi)
    print(A)
    print(B)
    
    old_p =  float("-inf")
    current_p = 0
    counter = 1
    start_time = time.time()
    while old_p < current_p:
        # if time.time() - start_time > 0.9:
        #     break
        if counter > 1:
            old_p = current_p
        alpha_list, scal = alpha_pass(obs, A, B, pi)
        beta_list = beta_pass(obs, A, B, pi, scal)
        gamma_list, gamma_sum = gamma_fun(obs, alpha_list, beta_list, A, B)
        pi, A, B = model_learning(obs, A, B, gamma_list, gamma_sum)
        
        current_p = prob(obs, scal)
        counter+=1
        print(current_p)
        if counter > 300:
            break

    print(counter)
    
    A_str = to_str(A)
    B_str = to_str(B)
    print(A_str)   
    print(B_str)


def alpha_pass(obs, A, B, pi):
    alpha_list = []
    scal = []
    N = len(pi[0])
    T = len(obs) 
    for t in range(T):
        temp = []
        scal_temp = 0
        for i in range(N):  
            if t == 0:
                x = pi[0][i] * B[i][obs[t]]
                scal_temp += x
                temp.append(x)
            else:
                alpha_temp = 0
                for j in range(N):
                    alpha_temp +=   alpha_list[t - 1][j] * A[j][i]
                next_alpha = alpha_temp* B[i][obs[t]]
                scal_temp += next_alpha
                temp.append(next_alpha)
        
        c = 1 / scal_temp
        for k in range(N):
            temp[k] = temp[k] * c
        scal.append(c)     
        alpha_list.append(temp)
    return alpha_list ,scal



def beta_pass(obs, A, B, pi, scal):
    T = len(obs)
    N = len(pi[0])
    beta_list = [[] for _ in range(T)]
    # initializing the beta list 
    for t in range(T):
        for _ in range(N):
            if t == T - 1:
                beta_list[t].append(scal[t])
            else:
                beta_list[t].append(0)
        
    for t in reversed(range(T - 1)):
        for i in range(N):
            beta_sum = 0
            for j in range(N):
                beta_sum += beta_list[t + 1][j] * B[j][obs[t + 1]] * A[i][j]
            beta_list[t][i] = beta_sum * scal[t]
    return beta_list


    
    
def gamma_fun(obs, alpha_list, beta_list, A, B):    
    T = len(obs)
    N = len(A)
    gamma_list = []
    gamma_sum_list = []
    alpha_nor = 0
    
    for i in range(N):
        alpha_nor += alpha_list[T - 1][i]   #Denominator
    
    for t in range(T - 1):
        gamma_sum_list_temp = []
        gamma_list_temp = []
        
        for i in range(N):
            temp = []
            gamma_sum = 0
            for j in range(N):
                nom = alpha_list[t][i] *A[i][j]* beta_list[t + 1][j] * B[j][obs[t + 1]]
                gamma_sum += nom
                temp.append(nom)
            gamma_sum_list_temp.append(gamma_sum)        
            gamma_list_temp.append(temp)
            
        gamma_list.append(gamma_list_temp) # Gamma(k,i)
        gamma_sum_list.append(gamma_sum_list_temp) # Gamma(k,i,j)
    
    gama_temp_list = [] 
    alpha_temp_list = alpha_list[t+1]
    for k in range(N):
        gama_temp_list.append(alpha_temp_list[k])
    gamma_sum_list.append(gama_temp_list)
            
    return gamma_list, gamma_sum_list  


def model_learning(obs, A, B, gamma_list, gamma_sum):
    
    T = len(obs)
    N = len(A)
    M = len(B[0])
    new_pi = [[]]
    new_A = []
    new_B = []
    
    # pi
    for i in range(N):
        new_pi[0].append(gamma_sum[0][i])
    
    # A
    for i in range(N):          
        temp = []
        a_i = 0
        for k in range(T - 1):
            a_i += gamma_sum[k][i]
        for j in range(N):
            a_ij = 0
            for t in range(T-1):
                a_temp = gamma_list[t][i]
                a_ij += a_temp[j]
            temp.append(a_ij/ a_i)
        new_A.append(temp)
    
    
    # B    
    for i in range(N):          
        temp = []
        b_i = 0
        for k in range(T):
            b_i += gamma_sum[k][i]
        for j in range(M):
            b_k = 0
            for t in range(T):
                if obs[t] == j:
                    b_k += gamma_sum[t][i]
            temp.append(b_k/ b_i)
        new_B.append(temp)

    return new_pi, new_A, new_B

def matrix_mul(matr1, matr2):
    new_matrix = []
    for i, j in zip(matr1, matr2):
        new_matrix.append(i * j)
    return new_matrix
        

def to_str(matr):
    s = ""
    s = s + str(len(matr)) + " " + str(len(matr[0]))
    for i in range(0, len(matr)):
        for j in range(len(matr[0])):
            s = s + " " + str(round(matr[i][j], 2))
    return s

def prob(obs, scal):
    T = len(obs)
    prob = 0
    for i in range(T):
        prob -= math.log(scal[i])
    return prob


if __name__ == "__main__":
    main()