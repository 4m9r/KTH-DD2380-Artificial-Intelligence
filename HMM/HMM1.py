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
    initial_matrix = [[] for x in range(int(sample_input3[0]))]

  
    for i in range(2, len(sample_input3)):
        initial_matrix[(i - 2) // int(sample_input3[1])].append(float(sample_input3[i])) 
    
    sample_input4 = temp[3]    
    emission_seq = []
 
    for i in range(1, len(sample_input4)):
        emission_seq.append(int(sample_input4[i]))
        

    alpha_init = matrix_mul(initial_matrix[0], get_col(B, emission_seq[0]))
    
    out_put = alpha_p(emission_seq, A, B, initial_matrix) 
    print(round(sum(out_put[len(out_put) - 1]), 6))

   




def forward_algo (obs_seq, A , B, alpha ,num_state):
    if len(obs_seq) == 0:
        return alpha
    temp = []
    for j in range(num_state):
        temp.append(sum(matrix_mul(alpha, get_col(A, j))))   
    next_alpha = matrix_mul(temp, get_col(B, obs_seq[0]))
    return forward_algo(obs_seq[1:], A, B, next_alpha, num_state)


def alpha_p(obs, A, B, pi):
    alpha_list = []
    for t in range(len(obs)):
        temp = []
        for i in range(len(pi[0])):
            if t == 0:
                temp.append(pi[0][i] * B[i][obs[t]])
            else:
                alpha_temp = 0
                for j in range(len(pi[0])):
                    alpha_temp+=   alpha_list[t - 1][j] * A[j][i]
                next_alpha = alpha_temp* B[i][obs[t]]
                temp.append(next_alpha)      
        alpha_list.append(temp)
    return alpha_list    
    
def matrix_dot(matr1, matr2):
    if len(matr1[0]) != len(matr2):
        raise Exception("incorrect number of rows and columns")   
    new_matrix = [[] for _ in range(len(matr1))]
    for i,row in enumerate(matr1):
        for j in range(len(matr2[0])):
            temp = 0
            for k,item in enumerate(row):
                temp = temp + item * matr2[k][j]
            new_matrix[i].append(round(temp, 2))
    return new_matrix

def to_str(matr):
    s = ""
    s = s + str(len(matr)) + " " + str(len(matr[0]))
    for i in range(0, len(matr)):
        for j in range(len(matr[0])):
            s = s + " " + str(matr[i][j])
    return s

def matrix_mul(matr1, matr2):
    new_matrix = []
    for i, j in zip(matr1, matr2):
        new_matrix.append(i * j)
    return new_matrix
        
        


def get_col(matr, col_num):
    col = []
    for i in range(len(matr)):
        col.append(matr[i][col_num])
    return col
    
    


if __name__ == "__main__":
    main()