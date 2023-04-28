#Name: Chong Kah Ying
#Student ID: 28900057
import sys

def hd1_patmatch(ptn,txt):
    m = len(ptn)
    n = len(txt)
    z_values = [m]
    left_i = -1
    right_i = -1
    combine = ptn + '$' + txt
    found_indices = []

    #this true/false value is for determining when to start saving positions
    # where matching pattern occurs in text. It is set to true after computing
    # the z-values of the pattern
    #
    stop_adding_z_values = False
    if m <= n and m > 0:
        for i in range(1, n + m + 1 - m + 1):
            z_i = 0
            mismatch = False
            #end of pattern is marked by $ sign 
            if combine[i] == "$":
                stop_adding_z_values = True
            else:
                if i > right_i:
                    #assume that substring has hamming distance of 0 
                    if stop_adding_z_values:
                        found_indices.append([i-m-1,0])
                    for j in range(m):
                        if combine[i+j] == combine[j] :
                            z_i += 1
                        else:
                            #if it mismatches one char in the pattern 
                            #change hamming distance to 1

                            if not mismatch and stop_adding_z_values:
                                mismatch = True
                                found_indices[-1][1] = 1  

                            #since hamming distance > 1, we no longer want 
                            # the position and hamming distance information   
                            else:
                                if stop_adding_z_values:    
                                    found_indices.pop()
                                break
    
                else:
                    if z_values[i-left_i] >= right_i - i + 1:
                        if stop_adding_z_values:
                            found_indices.append([i-m-1,0])
                        z_i = z_values[i-left_i]
                        for j in range(z_i,m):
                            if combine[i+j] == combine[j]:
                                z_i += 1
                            else:
                                if not mismatch and stop_adding_z_values:
                                    mismatch = True   
                                    found_indices[-1][1] = 1     
                                else:    
                                    if stop_adding_z_values:    
                                        found_indices.pop()
                                    break        
                    else:
                        # we do not assume that there is a match here because
                        # the substring here is definitely shorter than the pattern length 
                        z_i = z_values[i-left_i]

            if z_i > 0:
                left_i = i
                right_i = left_i + z_i - 1
            
            # save z values 
            #when z[1] == q, the next q-1 characters is the same as txt[0] and txt[1]
            #so add the respective values into the z-values list without needing to 
            #compare the characters manually at each iteration
            #if text has more characters than q+2, the z-value of txt[q+2] will be 0 
            #only use the z-algo cases above after skipping unneeded iterations which is updated
            #here using i += 1
            if not stop_adding_z_values:
                z_values.append(z_i)
                if len(z_values) == 2 and z_i > 0:
                    for z in range(z_values[-1]-1,0,-1):
                        z_values.append(z)
                        i += 1
                    if len(z_values) < len(ptn):
                        z_values.append(0)
                        i += 1
            
        return found_indices
    else:
        return None
        
def readInput(txtFileName,ptnFileName):
    txtFile = open(txtFileName,'r')
    txt = txtFile.read()
    txtFile.close()

    patFile = open(ptnFileName, 'r')
    pat = patFile.read()
    patFile.close()
    
    return txt,pat

def writeOutput(indices):
    outputFile = open('output_hd1_patmatch.txt','w')
    if indices == None or indices == []:
        outputFile.write("")
    else:
        outputFile.write(str(indices[0][0]) + "\t" + str(indices[0][1]))

        for i in range(1,len(indices)):
            outputFile.write("\n")
            outputFile.write(str(indices[i][0]) + "\t" + str(indices[i][1]))

    outputFile.close()

if __name__ == "__main__":
    txtFileName = sys.argv[1]
    patFileName = sys.argv[2]
    text, pattern = readInput(txtFileName, patFileName)
  
    indices = hd1_patmatch(pattern,text)
    writeOutput(indices)