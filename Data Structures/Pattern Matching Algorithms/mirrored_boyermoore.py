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
                    # z box is only updated if it exceeds the current one
                    if z_box[1] < a:
                        z_box = [i,i+b-1]
                    z_array[i] = b

    return z_array

def preprocess_pat(pattern):
    """
    This function is used to preprocess the pattern by creating a bad character table,
    good prefix and match suffix lists. It runs in O(m). m = length of pattern
    :param pattern: pattern to preprocess
    :return: returns a bad character table, good prefix and match suffix lists
    """
    # This function preprocesses the pattern to be used for Boyer Moore
    # This function runs in O(m) where m is the length of the pattern
    bc_table = [None] * 256

    # initializing all the values in the table
    # creating a list only for unique alphabets in the pattern
    for i in range(len(pattern)):
        bc_table[ord(pattern[i])] = [-1] * len(pattern)

    # putting the characters positions from the string in a list
    for i in range(len(pattern) - 1, -1, -1):
        bc_table[ord(pattern[i])][i] = i

    # filling up the table accordingly by changing the values to the right if they are -1
    # loop : O(M)
    for i in range(len(bc_table) - 1):
        if bc_table[i] != None:
            for j in range(len(pattern) - 1, -1, -1):
                if j <= len(pattern) - 2:
                    if bc_table[i][j] == -1:
                        bc_table[i][j] = bc_table[i][j + 1]

    # getting values from z array to create the good prefix array. The good prefix array
    # stores the index of the next right substring that matches the prefix before the mismatch occurs
    zarray = z_algorithm(pattern)
    goodprefix = [0] * (len(pattern) + 1)
    for i in range(len(pattern) - 1, -1, -1):
        a = zarray[i]
        goodprefix[a] = i

    # reversing the pattern
    reverse = ''
    for i in range(len(pattern) - 1, -1, -1):
        reverse += pattern[i]

    # getting the zarray on reversed pattern
    zarray = z_algorithm(reverse)

    # creating match suffix array based on the z array
    matchsuffix = [0] * (len(zarray) + 1)
    for i in range(len(zarray) - 1, -1, -1):
        if zarray[i] + i == len(pattern):
            matchsuffix[i] = zarray[i]
        else:
            matchsuffix[i] = matchsuffix[i + 1]

    # we need to reverse the match suffix because now we are comparing left to right
    matchsuffix = matchsuffix[::-1]

    return bc_table, goodprefix, matchsuffix

def bad_character(string,bc_table,i,j,m,starting,pattern):
    """
    :param string: string that we need to find the pattern in
    :param bc_table: bad character table that store the values of the rightmost character of pattern that matches the mismatched
    #                character from the string
    :param i: current index of pattern
    :param j: current index of string
    :param m: length of pattern
    :param starting: where we started comparing from
    :param pattern: pattern that we are trying to match
    :return: returns the number of places to shift to and a true or false value depending on whether we have a character that matches
    """
    value = 0
    flag = False
    # if pattern does not have an alphabet that matches the mismatched string alphabet
    if (bc_table[ord(string[j])]) != None:
        if (bc_table[ord(string[j])][i]) != -1:
            value = bc_table[ord(string[j])][i]
            shift_places = value-i
            shift_places = max(shift_places, 1)
            flag = True # flag will be true if we have found a matching character
        else:
            # counts the shift places
            checked = j-starting
            shift_places = len(pattern)-checked
    else:
        # counts the shift places
        checked = j - starting
        shift_places = len(pattern) - checked

    return shift_places, flag

def good_prefix(pattern, gp_array, matchsuffix, m, starting, i, j):
    """
    :param pattern: attern that we are trying to match
    :param gp_array: array that stores the index of the next right substring that matches the prefix before the mismatch occurs
    :param matchsuffix: array that store the suffix that matches the prefix
    :param m: length of pattern
    :param starting: where we started comparing from
    :param i: current index of pattern
    :param j: current index of string
    :return: returns the number of places to shift and also the matched range that we can skip
    """
    # if pattern does not have an alphabet that matches the mismatched string alphabet
    if gp_array[i] != 0:
        shift_places = gp_array[i]
        mismatch_range = [j, starting + 1]
    else:
        shift_places = len(pattern) - matchsuffix[i]
        # if we are shifting all the way past, we dont need to do galils optimisation
        if shift_places == len(pattern):
            mismatch_range = None
        else:
            mismatch_range = [starting, starting + matchsuffix[i]]

    return shift_places, mismatch_range

def boyermoore(string,pattern):
    """
    This function runs O(m+n). This is the main mirrored boyer moore function.
    It compares from left to right and shifts left. It will compare until a mismatch is found, and then
    uses either a good prefix, match suffix or bad character rule to shift.
    :param string: String to find the pattern in
    :param pattern: Pattern to be found in the string
    :return: returns the positions of the pattern that is found in the string
    """
    bc_table, goodprefix, matchsuffix = preprocess_pat(pattern)

    m = len(pattern) - 1
    n = len(string) - 1
    i = 0
    j = len(string) - len(pattern)
    starting = j
    matches = []
    matched_range = None    # This stores the matched range to be used for galils optimisation
    occurences = 0

    while j >= 0 and starting >= 0:

        # if the pattern matches the string
        if i > len(pattern)-1:
            # we shift by matchsuffix[len(pattern)-2] because its the longest suffix that matches the prefix
            shift_by = len(pattern) - matchsuffix[len(pattern)-2]

            # updates the matched range so we know the characters we already compared
            matched_range = [starting,starting+matchsuffix[1]]
            matches.append(starting+1)

            # updates all the variables. We start comparing from the beginning of pattern again
            i = 0
            j = starting - shift_by
            starting = j
            occurences += 1

        # if the string matches the pattern, we move right
        if (string[j] == pattern[i]):
            i += 1
            j += 1

        # if we have a mismatch it will go through this else statement
        else:
            # gets the good character and good prefix/ match suffix shifts
            bc_shift,flag = bad_character(string,bc_table,i,j,m,starting,pattern)
            gp_shift,mr = good_prefix(pattern, goodprefix,matchsuffix,m, starting, i,j)

            # if bad character shift is more than the good prefix shifts, we will use that. Otherwise,
            # we will use good prefix shifts. Good prefix shifts also take priority
            if bc_shift > gp_shift:
                # if character is found in the bc table meaning we have a matching character to the right of the string
                if flag == True:
                    matched_range = [j, j+1]
                    j = starting - bc_shift
                    i = 0
                    starting = j
                # if character is not found in the bc table meaning we dont have a matching character to the right of the string
                else:
                    j = starting - bc_shift
                    i = 0
                    starting= j
                    matched_range = None
            else:
                matched_range = mr
                j = starting - gp_shift
                i = 0
                starting = j

        # skips already matched characters (galils optimisation)
        # if we are in the matches range (meaning characters we have already matched before shifting),
        # we will completely skip comparing them
        if (matched_range != None) and (j >= matched_range[0] and j < matched_range[1]):
            skips = matched_range[1] - matched_range[0]
            j += skips
            i += skips
            matched_range = None    # resets the range back to none once we have already skipped past it

    return matches


if __name__ == '__main__':
    argument_0 = sys.argv[0]

    argument_1 = sys.argv[1]
    argument_2 = sys.argv[2]

    text_file = open(argument_1,'r')
    pat_file = open(argument_2,'r')
    output_file = open('output_mirrored_boyermoore.txt','w')

    text = text_file.read()
    pattern = pat_file.read()

    matches = boyermoore(text,pattern)
    matches = matches[::-1]

    for i in range(len(matches)):
        output_file.write((matches[i]).__str__()+"\n")

    text_file.close()
    pat_file.close()
    output_file.close()

