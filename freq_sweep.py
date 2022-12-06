def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))


import subprocess
from csv import writer, QUOTE_MINIMAL
from os.path import exists

#test parameter
frequencyRange = [800, 1100, 1500]
archSet = ["A15","A7"]
l1Set = ["hp","lop"]

def init_config(freq, Arch, Cache):
    with open('/home/eca/gem5/configs/simulation_parameters.py', 'r', encoding='utf-8') as file:
        data = file.readlines()
    data[8] = f'l1d_memory_type = "{Cache}"  # Memory cell type ("lop", "lstp" or "hp")\n'
    data[14] = f'l1i_memory_type = "{Cache}"  # Memory cell type ("lop", "lstp" or "hp")\n'
    data[22] = f'l2_memory_type = "{Cache}"  # Memory cell type ("lop", "lstp" or "hp")\n'
    data[1] = f"core = '{Arch}'  # Choose 'A15' (big) or 'A7' (LITTLE)\n"
    data[2] = f"frequency = {freq}  # CPU clock frequency [MHz]\n"

    #print(data)    
    with open('/home/eca/gem5/configs/simulation_parameters.py', 'w', encoding='utf-8') as file:
        file.writelines(data)    

def process_output(output):
    output_list = [y for y in (x.strip() for x in output.splitlines()) if y]
    for i, x in enumerate(output_list):
        output_list[i] = x.split()
    #print(output_list)    
    output = []
    names = []
    for j in range(i):
        floats = [float(x) for x in output_list[j][1:]]
        output.append(sum(floats))
        names.append(output_list[j][0])
    return output, names  

def write_out(result, names):
    #Check if csv exists.
    #Obtain variable settings. 
    #Append data to csv
    #Step 1. Generate list
    with open('/home/eca/gem5/configs/simulation_parameters.py', 'r', encoding='utf-8') as file:
        data = file.readlines()
    #print("\n", data)
    temp = []
    for i, x in enumerate(data):
        data[i] = x.split()
    #print(data)

    l = [data[1][2], data[2][2], data[6][2], data[7][2], data[8][2], data[12][2], data[13][2], data[14][2], data[18][2], data[19][2], data[20][2], data[21][2], data[22][2]]
    #for i, x in enumerate(result):
    #    result[i] = str(x)    
    l.extend(result)    
    #print(names)

    if not exists("/home/eca/results.csv"):
        arguments = ["Core","Freq","L1d_size","L1d_assoc","L1d_mem","L1i_size","L1i_assoc","L1i_mem","l2_e","L2_pref","L2_size","L2_assoc","L2_mem"]
        arguments.extend(names)
        with open('/home/eca/results.csv', 'a', newline='') as csvfile:
            spamwriter = writer(csvfile)
            spamwriter.writerow(arguments)

    with open('/home/eca/results.csv', 'a', newline='') as csvfile:
        spamwriter = writer(csvfile)#, delimiter=' ', quotechar = '|', quoting=QUOTE_MINIMAL)
        spamwriter.writerow(l)

def main():
    for i in frequencyRange:
        for j in archSet:
            for h in l1Set:  
            #Step 1: Edit /home/eca/gem5/configs/simulation_parameters.py change frequency value
                prGreen("Running freq: " + str(i) +", Core:" + j + ", Cache: "+h)
                init_config(i,j,h)
            #Step 2: Start simulation
                prGreen("Running simulation")
                output = subprocess.run(["make", "simulate"], cwd="/home/eca/benchmark")
            #Step 3: Read and process output
                prGreen("Processing data")
                output = subprocess.run(["/home/eca/extract_stats.sh"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#, capture_output=True)
                result = output.stdout.decode("utf-8")
                #prGreen(result)
                result, names = process_output(result)    
            #Step 4: Write output to cvs
                prGreen("Writing it to csv")
                write_out(result, names)
            
            #Step 5:
                output = subprocess.run(["cp", "lincoln_out.bmp", "licoln_out_" + str(i) +".bmp"], cwd="/home/eca/benchmark/results")
            prGreen("Finished")


if __name__ == "__main__":
    main()