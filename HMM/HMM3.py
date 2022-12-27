import sys
import math
import time
def main():
    temp = []
    counter = 0
    for line in sys.stdin:
        counter += 1
        temp.append(line.split()) 
        if counter == 4:
            break
        
  
    sample_input1 = temp[0]
    A = [[] for _ in range(int(sample_input1[0]))]

   
    for i in range(2, len(sample_input1)):
        A[(i - 2) // int(sample_input1[1])].append(float(sample_input1[i]))
        

    sample_input2 = temp[1]
    B = [[] for _ in range(int(sample_input2[0]))]

  
    for i in range(2, len(sample_input2)):
        B[(i - 2) // int(sample_input2[1])].append(float(sample_input2[i]))
        
 
    sample_input3 = temp[2]
    pi = [[] for _ in range(int(sample_input3[0]))]

  
    for i in range(2, len(sample_input3)):
        pi[(i - 2) // int(sample_input3[1])].append(float(sample_input3[i])) 
    
    sample_input4 = temp[3]    
    obs = []
    
    for i in range(1, len(sample_input4)):
        obs.append(int(sample_input4[i]))
    
    
    
    
    old_p =  float("-inf")
    current_p = 0
    counter = 1
    start_time = time.time()
    
    # iterate till convergence
    while old_p < current_p:
        if time.time() - start_time > 0.9:
            break
        if counter > 1:
            old_p = current_p
        alpha_list, scal = alpha_pass(obs, A, B, pi)
        beta_list = beta_pass(obs, A, B, pi, scal)
        gamma_list, gamma_sum = gamma_fun(obs, alpha_list, beta_list, A, B)
        pi, A, B = model_learning(obs, A, B, gamma_list, gamma_sum)
        
        current_p = prob(obs, scal)
        counter+=1
        
        
    
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
        
        # scaling
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


    
# finding the gamma and di-gamma
def gamma_fun(obs, alpha_list, beta_list, A, B):    
    T = len(obs)
    N = len(A)
    
    gamma_list = [] #di_gamma
    gamma_sum_list = [] #gamma
    
    for t in range(T - 1):
        gamma_sum_list_temp = []
        gamma_list_temp = []
        
        for i in range(N):
            temp = []
            gamma_sum = 0
            for j in range(N):
                gamma_value = alpha_list[t][i] *A[i][j]* beta_list[t + 1][j] * B[j][obs[t + 1]]
                gamma_sum += gamma_value
                temp.append(gamma_value)
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

def to_str(matr):
    s = ""
    s = s + str(len(matr)) + " " + str(len(matr[0]))
    for i in range(0, len(matr)):
        for j in range(len(matr[0])):
            s = s + " " + str(matr[i][j])
    return s


def prob(obs, scal):
    T = len(obs)
    prob = 0
    for i in range(T):
        # to avoid underflow we use log
        prob -= math.log(scal[i])
    return prob


if __name__ == "__main__":
    main()