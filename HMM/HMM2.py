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
        

    delta_1 = matrix_mul(initial_matrix[0], get_col(B, emission_seq[0]))
    
    out_put = Viterbi(obs[1:], A, B, delta_1, len(initial_matrix[0]), [] )
    
    s = ""
    for i in range(len(out_put)):
        s = s + str(out_put[i])
        if i != len(out_put) - 1:
            s = s + " "
    print(s)

   




def Viterbi(obs_seq, A , B, delta ,num_state, best_paths):
    
    if len(obs_seq) == 0:
        state_seq = []
        prev_seq = delta.index(max(delta))
        state_seq.append(prev_seq)
        
        i =  len(best_paths) - 1  
        while i != - 1:
            state_seq.insert(0, best_paths[i][prev_seq])
            prev_seq = best_paths[i][prev_seq]
            i -= 1
            
        return state_seq
    
    temp = []
    for i in range(num_state):
        temp.append([delta[j] * A[j][i] * B[i][obs_seq[0]] for j in range(num_state)])

    
    next_delta = [max(item) for item in temp]
    
    x = []
    for i in range(len(temp)):
        x.append(temp[i].index(next_delta[i]))
    best_paths.append(x)

    return Viterbi(obs_seq[1:], A, B, next_delta, num_state, best_paths)
   
    

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