import sys

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
    pi = [[] for x in range(int(sample_input3[0]))]

  
    for i in range(2, len(sample_input3)):
        pi[(i - 2) // int(sample_input3[1])].append(float(sample_input3[i])) 
    
    sample_input4 = temp[3]    
    obs = []
 
    for i in range(1, len(sample_input4)):
        obs.append(int(sample_input4[i]))
        

    
    out_put = alpha_pass(obs, A, B, pi) 
    print(round(sum(out_put[len(out_put) - 1]), 6))

   




def alpha_pass(obs, A, B, pi):
    """Forward algorithm 
    :param obs: The emission matrix
    :param A: The transition matrix
    :param B: observation matrix
    :param pi: state probability vector
    """
    alpha_list = []
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
    return alpha_list
    
    


if __name__ == "__main__":
    main()