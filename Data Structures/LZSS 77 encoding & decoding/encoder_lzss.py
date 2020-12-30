# NAME: Vhera Kaey Vijayaraj
# STUDENT ID: 28903013

import heapq
import sys

def z_algorithm_ori(string,start,end):
    """
    This z algorithm runs in a range of the string from start until the end. In this assignment,
    I use it to get the zarray of the lookahead buffer.
    :param string: string to run the z algorihtm on
    :param start: starting position to run z algorithm
    :param end: ending position to stop
    :return:
    """

    z_array = [0]*(end-start+1)
    z_array[0] = end-start+1
    z_box = [start, start]  # stores L at index 0 and R at index 1

    for i in range(start+1, end+1):
        # Case 1: either no previously computed z-box OR i is not in the z-box
        # Explicit matching is done here
        if z_box == [start, start] or i > z_box[1]:
            x = i
            y = start
            matches= 0
            while x <= end and string[x] == string[y]:
                x += 1
                y += 1
                matches+= 1
            z_array[i-start] = y-start

            # checks for the case of first letter not matching. If it does not, then no z box is made
            if y != start:
                z_box = [i, i+matches-1]
        else:
            # Case 2: i is in the z-box
            remaining = z_box[1] - i + 1
            k = i - z_box[0]
            if z_array[k] < remaining:
                z_array[i-start] = z_array[k]
            elif z_array[k] > remaining:
                z_array[i-start] = remaining
            elif z_array[k] == remaining:
                # checks if string[remaining+i...] = string[remaining....]
                a = i + remaining
                b = remaining

                # if no matches are found, the value at position i will be the same as the remaining
                if a > end or string[a] != string[b]:
                    z_array[i-start] = remaining
                else:

                    matches = 0
                    # if a match is found, this loop will stop when there is a mismatch
                    while a <= end and string[a] == string[b]:
                        b += 1
                        a += 1
                        matches += 1
                    # z box is only updated if it exceeds the current one
                    if z_box[1] < a:
                        z_box = [i, i + matches-1]
                    z_array[i-start] = b
    return z_array


def z_algorithm(string, window_start, pointer, window_size, buffer_size):
    """
    This z algorithm makes a z array using precomputed values from the previous zarray of the look ahead buffer.
    It compares the characters starting from the window start with the characters in the buffer
    :param string: string we want to encode
    :param window_start: starting position of the window
    :param pointer: current position we are at (starting of lookahead buffer)
    :param window_size: current window size
    :param buffer_size: current buffer size
    :return:
    """

    # first we create a z array based on the lookahead buffer
    lookahead_zarray = z_algorithm_ori(string,pointer,pointer+buffer_size-1)
    z_array = [0] * window_size
    z_array = lookahead_zarray+z_array # z array from lookahead buffer is combined
    current_best = [1,0]    # [offset,length of matched]

    z_box = [0, 0]  # stores L at index 0 and R at index 1
    max_compare = pointer + buffer_size - 1

    for i in range(window_start, pointer):
        # Case 1: either no previously computed z-box OR i is not in the z-box
        # Explicit matching is done here
        if z_box == [0, 0] or i > z_box[1]:
            x = i  # from pointer
            y = pointer  # from starting of the window
            matches = 0

            # compare characters until the lookahead buffers end
            while x <= max_compare and y <= max_compare and string[x] == string[y]:
                x += 1
                y += 1
                matches += 1

            current = [pointer-i,matches]
            # will update the current best if it needs to be updated
            # if the matches are more, we will update the current best
            if current[1] > current_best[1]:
                current_best = current
            # if the matches are equal, we will choose the nearest one
            elif current[1] == current_best[1]:
                if current[0] < current_best[0] and y != pointer:
                    current_best = current


            z_array[i - window_start +buffer_size] = y - pointer

            # checks for the case of first letter not matching. If it does not, then no z box is made
            if y != pointer:
                z_box = [i, i + y - pointer - 1]
        else:
            # Case 2: i is in the z-box
            remaining = z_box[1] - i + 1
            k = i - z_box[0]
            if z_array[k] < remaining:
                z_array[i - window_start +buffer_size] = z_array[k]
            elif z_array[k] > remaining:
                z_array[i - window_start+buffer_size] = remaining
            elif z_array[k] == remaining:
                # checks if string[remaining+i...] = string[remaining....]
                a = pointer
                b = i

                # if no matches are found, the value at position i will be the same as the remaining
                if a > max_compare or string[a] != string[b]:
                    z_array[i- window_start+buffer_size] = remaining
                else:
                    matches = 0
                    # if a match is found, this loop will stop when there is a mismatch
                    while a <= max_compare and string[a] == string[b]:
                        b += 1
                        a += 1
                        matches += 1

                    current = [pointer-i,matches]

                    # will update the current best if it needs to be updated
                    # if the matches are more, we will update the current best
                    if current[1] > current_best[1]:
                        current_best = current
                    elif current[1] == current_best[1]:
                        # if the matches are equal, we will choose the nearest one
                        if current[0] < current_best[0] and b != remaining:
                            current_best = current

                    z_array[i-window_start+buffer_size] = matches

    return current_best


def decimal_to_binary(dec_num):
    """
    This function converts a decimal number into binary
    :param dec_num: decimal number to convert
    :return: a string of binary
    """
    binary = ""
    if dec_num == 1:
        return "1"
    elif dec_num == 0:
        return "0"
    else:
        while dec_num != 0:
            remainder = dec_num % 2
            binary = str(remainder) + binary
            dec_num = dec_num // 2
        return  binary

def huffman_encoding(input_list):
    """
    This function gives the huffman encoding by building a heap and the popping 2 values
    and putting it back into the heap until there is only one element left.
    :param input_list: list of unique characters and frequencies
    :return: returns a list of encodings for each unique character in the string
    """
    heap = heapq
    heap.heapify(input_list)
    encoding = ['' for _ in range(128)]

    # if we only have 1 letter in the input list, we can just make '0' the encoding
    if len(input_list) == 1:
        encoding[ord(input_list[0][1])] = '0'

    while len(input_list) != 1:
        # pop two elements from the heap
        first_pop = heap.heappop(input_list)
        second_pop = heap.heappop(input_list)

        # append all the characters to the list from the node that is popped
        for i in range(len(first_pop[1])):
            encoding[ord(first_pop[1][i])] = '0'+ encoding[ord(first_pop[1][i])]

        for i in range(len(second_pop[1])):
            encoding[ord(second_pop[1][i])] = '1' + encoding[ord(second_pop[1][i])]

        # combine the string and frequencies and put it back into the heap
        new_str = first_pop[1]+second_pop[1]
        new_val = first_pop[0]+second_pop[0]
        heap.heappush(input_list, [new_val, new_str])

    return encoding

def get_frequency(string):
    """
    This function gets the unique characters and frequencies of it from a string
    :param string: string to get frequencies from
    :return:
    """
    frequency_list = [0]*128
    for i in range(len(string)):
        frequency_list[ord(string[i])] += 1

    result = []
    unique_chars = 0
    for i in range(len(frequency_list)):
        if frequency_list[i] != 0:
            result.append([frequency_list[i],chr(i)])
            unique_chars += 1
    return unique_chars,result

def elias_encoding(number):
    """
    This function gives an elias encoding of a number
    :param number: number to get elias encoding
    :return: binary value in a string
    """
    bin_string = ""

    # gets the binary value of the number
    binary = decimal_to_binary(number)
    bin_string = binary
    number = len(binary)-1
    while number >= 1:
        # converts the binary number to a decimal
        binary = decimal_to_binary(number)
        if number == 1:
            bin_string = "0" + bin_string
        else:
            # changes the first bit to 0
            list_bin = list(binary)
            list_bin[0] = "0"
            binary = ''.join(list_bin)
            bin_string = binary + bin_string
        number = len(binary)-1
    return bin_string

def lzss_encode(string,window_size,buffer_size):
    """
    This function performs lzss encoding and returns the number of fields from the string
    :param string: string to encode
    :param window_size: size of the window
    :param buffer_size: size of the lookahead buffer
    :return: the fields from the string
    """
    total = len(string)
    original_buffer_size = buffer_size
    original_window_size = window_size
    pointer = 0
    window_start = 0
    current_window_size = 0
    current_buffer_size = buffer_size
    fields = []

    # adds the first character to the fields list since there are no characters in the window
    fields.append([1,string[0]])
    pointer += 1

    while pointer <= len(string)-1:
        # sets appropriate window size of the current size of the window
        if pointer - window_size < 0:
            current_window_size = pointer
        else:
            window_start = pointer-window_size
            current_window_size = original_window_size

        # sets appropriate look ahead buffer size of the current size of the lookahead buffer
        if pointer + buffer_size > len(string)-1:
            current_buffer_size = len(string)-pointer
        else:
            current_buffer_size = original_buffer_size

        # gets the offsets and shifts returned from the z algorithm
        [offset, shifts] = z_algorithm(string,window_start,pointer,current_window_size,current_buffer_size)

        # if we have more than 3 matches, we will use format 0
        if shifts >= 3:
            fields.append([0,offset,shifts])

        # if we have less than 3 characters matching, we will use format 1
        else:
            if shifts == 0:
                shifts = 1
            shifts = 1
            fields.append([1,string[pointer+shifts-1]])

        pointer += shifts

    return fields


def convert_to_ascii(dec_num):
    """
    This function converts an ascii value to a 7 bit binary string
    :param dec_num:
    :return:
    """
    binary = ""
    if dec_num == 1:
        return "1"
    elif dec_num == 0:
        return "0"
    else:
        while dec_num != 0:
            remainder = dec_num % 2
            binary = str(remainder) + binary
            dec_num = dec_num // 2
        # make sure the binary length is 7
        if len(binary) != 7:
            rem = 7-len(binary)
            binary = ('0'*rem)+binary
        return binary


def encode(string,window_size,buffer_size):
    """
    This function encodes information using lzss algorithm
    :param string: string to encode
    :param window_size: size of the window
    :param buffer_size: size of the look ahead buffer
    :return:
    """

    # gets the number of unique characters and its frequency
    unique_chars, freq_list = get_frequency(string)
    input_list = freq_list.copy()
    header = ''

    # encodes number of unique characters using elias encoding
    header += elias_encoding(unique_chars)

    # gets the code words of each unique letter using huffman encoding
    code_words = huffman_encoding(input_list)

    # making the header using the code words
    for i in range(len(freq_list)):

        # converts ascii number of character to binary
        header += convert_to_ascii(ord(freq_list[i][1]))
        code_word = code_words[ord(freq_list[i][1])]

        # encode length of codeword using elias encoding
        header += elias_encoding(len(code_word))

        # encode the code word
        header += code_word

    # gets the fields
    fields = lzss_encode(string, window_size, buffer_size)
    data = ''
    data += elias_encoding(len(fields))

    # encodes the fields
    for i in range(len(fields)):
        if fields[i][0] == 1:
            [bit, char] = fields[i]
            data += "1" + code_words[ord(char)]
        else:
            [bit, offset, matches] = fields[i]
            data += "0" + elias_encoding(offset) + elias_encoding(matches)

    # pads the string to be able to split it into bytes
    new_str = pad_string(header+data)

    # outputs the bytes to a binary file
    output_to_binfile(new_str)


def pad_string(string):
    """
    Pads the string so that it can be divided by 8
    :param string:
    :return:
    """
    pads = 8-len(string)%8
    if pads == 0:
        return string
    else:
        temp = '0'*pads
        string += temp
        return string

def binary_to_decimal(binary_str):
    """
    Converts a binary value to a decimal
    :param binary_str:
    :return:
    """
    value = 0
    power = 0
    for i in range(len(binary_str) - 1, -1, -1):
        if binary_str[i] == "1":
            value = value + 2 ** power
        power += 1
    return value

def output_to_binfile(string):
    """
    This function will output the binary string to the file using a byte array
    :param string: binary string to convert to bytes
    :return:
    """
    arr = bytearray()
    start = 0
    end = 8

    # split the string into bits of length 8, convert it into an integer and append it to the byte array
    while end <= len(string):
        num = string[start:end]
        num = binary_to_decimal(num)
        arr.append(num)
        start += 8
        end += 8

    # writes to the file
    file = open('output_encoder_lzss.bin','wb')
    file.write(arr)



if __name__ == '__main__':
    argument_0 = sys.argv[0]

    argument_1 = sys.argv[1]
    argument_2 = sys.argv[2]
    argument_3 = sys.argv[3]

    text_file = open(argument_1, 'r')
    txt = ''
    for line in text_file:
        txt += line

    window = int(argument_2)
    buffer = int(argument_3)
    encode(txt,window,buffer)




