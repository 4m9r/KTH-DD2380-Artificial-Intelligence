import sys

def main():

    # using sys to get the inputs as suggest on kattis
    temp = []
    counter = 0
    for line in sys.stdin:
        counter += 1
        temp.append(line.split()) 
        if counter == 3:
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
        
  
    next_state = matrix_mul(initial_matrix, A)
    out_put =  matrix_mul(next_state, B)  
        
    print(to_str(out_put))

   



def matrix_mul(matr1, matr2):
    #Helper function for matrix multipication
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
    #simple to_string function
    s = ""
    s = s + str(len(matr)) + " " + str(len(matr[0]))
    for i in range(0, len(matr)):
        for j in range(len(matr[0])):
            s = s + " " + str(matr[i][j])
    return s
    
    


if __name__ == "__main__":
    main()