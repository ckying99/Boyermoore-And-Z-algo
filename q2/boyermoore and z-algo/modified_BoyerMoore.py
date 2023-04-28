#Name: Chong Kah Ying
#Student ID: 28900057
import sys

FIRST_PRINTABLE_ASCII_CODE = ord(" ")
NUMBER_OF_PRINTABLE_ASCII = 95
def ascii_index(char):
    '''
    param: char 
    converts decimal code of character which is assumed to be among the 95
    printable ascii characters into a number between 0-94.
    '''
    return ord(char)-FIRST_PRINTABLE_ASCII_CODE

def z_algo(txt):
    '''
    param: string input 
    function: computes the z-value for each character of the string input, 
    and adds it to a list that will always have the same length as the given 
    string input
    return: a list of z-values 
    '''
    n = len(txt)

    z_values = [n] #because z value is always the length of provided pattern 
    #represents the left and right end indices of the latest z_box that occurs before index i. 
    left_i = -1
    right_i = -1
    i = 1
    #start comparison from the 2nd letter onwards, which is index = 1 in 0 indexing
    while i < n:
        z_i = 0
  
        if i > right_i:
        #manually compare characters when current index(i) is larger than the right side of the 
        # latest z-box
            for j in range(n-i):
                if txt[i+j] == txt[j]:
                    z_i += 1
                else:
                    #stop comparison when there is a mismatch 
                    break
            
        else:
            if z_values[i-left_i] >= right_i - i + 1:
                #start a loop to manually compare characters from outside the z-box 
                z_i = z_values[i-left_i]
                for j in range(z_i,n):
                    if txt[i+j] != txt[j]:
                        break
                    else:
                        z_i += 1

            else:
                #copy z[i-beginning index of the z-box] when i is within the latest z-box
                z_i = z_values[i-left_i]
            
        z_values.append(z_i)

        #update latest z-box
        if z_i > 0:
            left_i = i
            right_i = left_i + z_i - 1
        
        #when z[1] == q, the next q-1 characters is the same as txt[0] and txt[1]
        #so add the respective values into the z-values list without needing to 
        #compare the characters manually at each iteration
        #if text has more characters than q+2, the z-value of txt[q+2] will be 0 
        #only use the z-algo cases above after skipping unneeded iterations which is updated
        #here using i += 1 
        if len(z_values) == 2 and z_i > 0:
            for z in range(z_values[-1]-1,0,-1):
                z_values.append(z)
                i += 1
            if len(z_values) < len(txt):
                z_values.append(0)
                i += 1
        i += 1
    return z_values

def generate_z_suffix(ptn):
    #[::-1] flips the pattern text and the z-algo values to produce 
    # z_suffix values
    return z_algo(ptn[::-1])[::-1]

def generate_char_goodsuffix(ptn):
    '''
    param: pattern string
    this is a modification of the good suffix rule. The positions are saved
    according to the character in front of the matching good suffix 
    '''
    z_suffix = generate_z_suffix(ptn)
    good_suffix = []
    temp = []
    
    #initialization of good suffix values 
    for _ in range(len(ptn)+1):
        temp.append(-1)
    #initialize char_gs array - it is fixed size, according to the number of 
    #printable ascii characters
    #array has the form :
    # [
    #     (accessed using index0, it represents [empty space]) None
    #     (accessed using index1, it represents !) None
    #     .
    #     .
    #     .
    #     (accessed using index94, it represents [Delete]) None
    # ]
    # None becomes an array of good suffix values are saved according to the 
    # character in front of the matching good suffix
    
    for _ in range(NUMBER_OF_PRINTABLE_ASCII):
        good_suffix.append(None)

    for p in range(len(ptn)-1):
        j = len(ptn) - z_suffix[p]
        if z_suffix[p] < j:
            if p-z_suffix[p] != -1:
                char_index = ascii_index(ptn[p-z_suffix[p]])
                if good_suffix[char_index] == None:
                    good_suffix[char_index] = temp.copy()
                good_suffix[char_index][j] = p

    return good_suffix

def modified_BoyerMoore(txt,ptn):
    mp = generate_matched_prefix_values(z_algo(ptn))
    char_suffix = generate_char_goodsuffix(ptn)
    i = 0

    #variables for skipping comparison 
    #since comparison is from right to left, 
    #the start variable if the right end of the good suffix/matching prefix
    #end is the left end of it, it is quite redundant to have both end and 
    #resume but both are included for code readability purposes
    start = -1 
    end = -1 
    resume = -1 

    found_index = []
    
    # skip comparisons where substring of text is shorter than length of 
    # pattern to be matched 
    while i < len(txt) - len(ptn) + 1:
        full_match = True
        j = len(ptn)-1
        shift = -1  
        # comparison stops when it finishes comparing the first char in pattern
        while j >= 0:
            if txt[i+j] == ptn[j]:
                #for skipping comparisons where there is a good suffix/matching
                # -prefix pattern
                if j == start:
                    j = resume 
                else:
                    j -= 1
            else:
                full_match = False

                '''
                if it doesn't match, we shift by the positions recorded in the 
                char_good suffix array
                '''
                #char_good suffix does not exist within the pattern, so shift by len-matched prefix length 
                if  char_suffix[ascii_index(txt[i+j])] == None:
                    shift = len(ptn) - mp[j+1]
                    end = 0
                    start = mp[j+1]-1
                    resume = -1

                else:
                    gs_value = char_suffix[ascii_index(txt[i+j])][j+1]
                    #same as above 
                    if gs_value == -1:
                        shift = len(ptn) - mp[j+1]
                        end = 0
                        start = mp[j+1]-1
                        resume = -1
                    #skip comparisons
                    else:
                        shift = j - gs_value
                        length = len(ptn) - (j + 1)
                        start = j - shift 
                        end = start - length
                        resume = end - 1 
                #stop comparison
                break
                    
        if full_match:
            #no mismatch at all, so there is an occurence of pattern in the text
            #save the position where it occured
            found_index.append(i)
            '''
            if it matches completely, we shift by m - mp(1) 
            '''
            i += len(ptn) - mp[1]
        else:
            #begin a new iteration according to shift places
            i += shift

    return found_index
    
def generate_matched_prefix_values(z_values):
    i = len(z_values)-1
    #matching prefix starts with 0 
    mp_i = [0]
    while i > 0:
        if z_values[i] + i == len(z_values):
            if len(mp_i) == 0 or z_values[i] > mp_i[-1]:
                mp_i.append(z_values[i])
            else:
                mp_i.append(mp_i[i-1])
        else:
            if len(mp_i) > 0:
                mp_i.append(mp_i[-1])
            else:
                mp_i.append(0)
        i -= 1
    mp_i.append(len(z_values))
    return mp_i[::-1]
           
def readInput(txtFileName,ptnFileName):
    txtFile = open(txtFileName,'r')
    txt = txtFile.read()
    txtFile.close()

    patFile = open(ptnFileName, 'r')
    pat = patFile.read()
    patFile.close()
    
    return txt,pat

def writeOutput(indices):
    outputFile = open('output_modified_BoyerMoore.txt','w')
    if indices == []:
        outputFile.write("")

    else:
        outputFile.write(str(indices[0]))
        for i in range(1,len(indices)):
            outputFile.write("\n")
            outputFile.write(str(indices[i]))
        outputFile.close()

if __name__ == "__main__":
    txtFileName = sys.argv[1]
    patFileName = sys.argv[2]

    text, pattern = readInput(txtFileName, patFileName)

    indices = modified_BoyerMoore(text,pattern)
    writeOutput(indices)
