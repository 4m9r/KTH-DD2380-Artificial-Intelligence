input_file = open("hmm_c_N1000.in", 'r').readline()
input_split = input_file.split(" ")
obs = []
for i in range(1, len(input_split)):
    obs.append(int(input_split[i]))
print( obs)