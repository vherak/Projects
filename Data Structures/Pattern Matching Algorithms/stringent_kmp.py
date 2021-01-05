import sys

# Name: Vhera Kaey Vijayaraj
# Student ID: 28903013

def z_algorithm(string):
    """
    This function is a z algorithm used for preprocessing the pattern. It runs in O(m)
    Where m = length of pattern
    :param string: string to run the z algorithm on
    :return: returns a z array that stores the longest substring that matches the prefix
    """
    # z algorithm to be used for preprocessing the pattern
    if string=="":
        return []
    z_array = [0]*len(string)
    z_array[0] = len(string)
    z_box = [0,0] # stores L at index 0 and R at index 1
    for i in range(1,len(string)):
        # Case 1: either no previously computed z-box OR i is not in the z-box
        # Explicit matching is done here
        if z_box == [0,0] or i > z_box[1]:
            x = i
            y = 0
            while x <= len(string)-1 and string[x] == string[y]:
                x+=1
                y += 1
            z_array[i] = y

            # checks for the case of first letter not matching. If it does not, then no z box is made
            if y != 0:
                z_box = [i,i+y-1]
        else:
            # Case 2: i is in the z-box
            remaining = z_box[1]-i+1
            k = i-z_box[0]
            if z_array[k] < remaining:
                z_array[i] = z_array[k]
            elif z_array[k] > remaining:
                z_array[i] = remaining
            elif z_array[k] == remaining:
                # checks if string[remaining+i...] = string[remaining....]
                a = i+remaining
                b = remaining

                # if no matches are found, the value at position i will be the same as the remaining
                if a > len(string)-1 or string[a] != string[b]:
                    z_array[i] = remaining
                else:

                # if a match is found, this loop will stop when there is a mismatch
                    while a <= len(string)-1 and string[a] == string[b]:
                        b += 1
                        a += 1
                    if z_box[1] < a:
                        z_box = [i,i+b-1]
                    z_array[i] = b

    return z_array


def preprocess_pat(pattern):
    """
    This function preprocesses the pattern in order to obtain the sp array and SPix values.
    Time Complexity: O(M*256) = O(M) where M is the length of the pattern. 256 = number of characters
    :param pattern: the pattern we are pre processing in order to match it
    :return: returns a table of SPix values which will store the values to determine how to shift
    """
    # using the z algorithm on the pattern
    zarray = z_algorithm(pattern)
    sp_array = [0]*len(pattern)

    # creating SP ix table. I create the lists of size len(pattern)+1 because if we mismatch at
    # position 0, it will look at the last row which will be all -1 values.
    spix_table = [None]*256
    for i in range(len(spix_table)):
        for j in range(len(pattern)):
            spix_table[ord(pattern[j])] = [-1]*(len(pattern)+1)

    # initializing the whole first row except for the last element in that row to 0. This is due to
    # mismatches on character c. If we mismatched on c, we can always go to the first character
    # (at position 0) unless there is a longer suffix that matches the prefix (which will be over written
    # when we use the z array)
    first_char = pattern[0]
    for i in range(len(spix_table)):
        if spix_table[i] != None:
            for j in range(len(spix_table[i])-1):
                spix_table[ord(first_char)][j] = 0

    # These loops fill in the rest of the values for the table and the sp array. We can get the next character by using pattern[zarray[i]].
    # at position i, it is length of the longest suffix of pat[0..i] that matches the prefix.
    # This spix_table then stores the values if we happen to mismatch on character i+1 at spix_table[mismatch char][i].
    for j in range(len(pattern) - 1, 0, -1):
        i = j + zarray[j] - 1
        sp_array[i] = zarray[j]
        x = zarray[j]
        spix_table[ord(pattern[x])][i] = zarray[j]
    return sp_array,spix_table

def kmp_algo(string, pattern):
    """
    This is the main KMP function. It compares the pattern with the string using SPix values. If there is a mismatch,
    the SPix table will try and find a prefix which matches the suffix which also has the mismatched character after it
    Time Complexity: O(m+n) m is the size of the pattern and n is the size of the string
    :param string: string for the pattern to be found in
    :param pattern: pattern to be found in the string
    :return:
    """

    # getting the spix array and table
    sp_array,spix_table = preprocess_pat(pattern)
    n = len(string)-1
    i = 0
    j = 0
    starting = 0    # to keep track of where we start comparing from
    end = len(pattern)-1    # to keep track of where our string ends
    matched_range = None    # to store values to be used for galils optimisation
    matches = []
    while j <= n and end <= len(string)-1:
        # if the character in the string matches the pattern, we check to the right
        if string[j] == pattern[i]:
            i += 1
            j += 1
        else:
            mismatched_char = string[j]
            if spix_table[ord(mismatched_char)] != None:
                if spix_table[ord(mismatched_char)][i-1] != -1:
                    # if pattern has the mismatched character and it is also after the prefix that matches the suffix
                    shifts = i-spix_table[ord(mismatched_char)][i-1]
                    matched_range = [starting+shifts,j]     # keeps track of the characters we have compared previously
                    j = starting + shifts
                    i = 0
                    starting = j
                    end = starting + len(pattern)-1
                else:
                    # if pattern has the mismatched character, but does not have the mismatched character in the prefix
                    shifts = i-(-1)
                    j = starting + shifts
                    i = 0
                    starting = j
                    end = starting + len(pattern)-1
                    matched_range = None    # no skips can be done here
            else:
                # if mismatched character is not in pattern, completely shift past it.
                shifts = i+1
                j = starting + shifts
                i = 0
                starting = j
                end = starting + len(pattern)-1
                matched_range = None    # no skips can be done here

        # if we have found the pattern that matched the string
        if i == len(pattern):
            shifts = len(pattern)-sp_array[len(pattern)-1]
            matched_range = [j-sp_array[len(pattern)-1],j-1]        # we can also skip some character comparisons here:

            # adds the starting index to the matches list
            matches.append(starting)
            j = starting + shifts
            i = 0
            starting = j
            end = starting + len(pattern)-1

      # galils optimization: skipping characters we have already compared and already know they matched
      # This skips all the characters we have already matched by moving the pointers
        if matched_range != None and (j >= matched_range[0] and j <= matched_range[1]):
            skips = matched_range[1] - matched_range[0] + 1
            i += skips
            j = skips + starting
            matched_range = None

    # prints out the matching positions
    return matches

if __name__ == '__main__':
    argument_0 = sys.argv[0]

    argument_1 = sys.argv[1]
    argument_2 = sys.argv[2]

    text_file = open(argument_1,'r')
    pat_file = open(argument_2,'r')
    output_file = open('output_kmp.txt','w')

    text = text_file.read()
    pattern = pat_file.read()

    matches = kmp_algo(text,pattern)

    for i in range(len(matches)):
        output_file.write((matches[i]+1).__str__()+"\n")

    text_file.close()
    pat_file.close()
    output_file.close()

