# NAME: Vhera Kaey Vijayaraj
# STUDENT ID: 28903013
import sys

class Node:
    """
    The Node class stores the nodes of binary search tree
    """
    def __init__(self):
        self.data = None
        self.leaf = False
        self.left = None
        self.right = None

class BinaryTree:
    """
    This class is a binary search tree class
    """
    def __init__(self):
        self.root = Node()
        self.node_list = None

    def add_encoding(self,character,binary_encoding):
        """
        This function adds a binary encoding into the binary search tree
        It will insert the character that it represents after we have added the encoding
        :param character: character to add
        :param binary_encoding: encoding of character
        :return: does not return anything
        """

        # we start from the root
        current = self.root
        pointer = 0
        while pointer < len(binary_encoding):
            # if current binary value is 0, it means we have to move to the left
            if binary_encoding[pointer] == "0":
                previous = current
                current = current.left

                # if no node is there, we have to add a new node
                if current == None:
                    current = Node()
                    previous.left = current
                pointer += 1
                # if current binary value is 1, it means we have to move to the right
            else:
                previous = current
                current = current.right

                # if no node is there, we have to add a new node
                if current == None:
                    current = Node()
                    previous.right = current
                pointer += 1

        # add the character at appropriate node
        current.data = character
        current.leaf = True


    def retrieve_letter(self,binary_str,pointer):
        """
        This function retrives the letter based on the binary string
        :param binary_str: binary string we want to find the letter at
        :param pointer: current pointer of where we are in the string
        :return:
        """
        length_to_skip = 0
        letter = None
        current = self.root
        current_char = binary_str[pointer]
        found = False

        while found == False:
            prev = current
            # if the current value of the binary string is 0, we will go to the left
            if current_char == '0':
                current = current.left
                length_to_skip += 1
                if pointer+length_to_skip <= len(binary_str)-1:
                    current_char = binary_str[pointer+length_to_skip]

            # if the current value of the binary string is 1, we will go to the right
            else:
                current = current.right
                length_to_skip += 1
                if pointer+length_to_skip <= len(binary_str)-1:
                    current_char = binary_str[pointer+length_to_skip]

            # if we have reached a leaf, it means we have found the letter and can return it
            if current == None:
                if prev.leaf == True:
                    return prev.data, length_to_skip-1


def binary_to_decimal(binary_str):
    """
    This function gets the decimal value of a binary number
    :param binary_str: binary string we want to get the decimal value of
    :return: returns the decimal value
    """
    value = 0
    power = 0
    for i in range(len(binary_str) - 1, -1, -1):
        if binary_str[i] == "1":
            value = value + 2 ** power
        power += 1
    return value


def elias_decode(bit_string, pointer):
    """
    This function follows elias decoding for numbers
    :param bit_string: bit string to use
    :param pointer: current position in the string
    :return: returns the decimal value of the decoded area and the pointer after decoding
    """
    current = pointer
    length = 1

    while bit_string[current] == "0":
        # if it is 0, we keep going
        if bit_string[current] == "0":
            prev_length = length

            # changing first bit to 1
            list_bin = list(bit_string)
            list_bin[current] = "1"
            bit_string = ''.join(list_bin)

            # converting the binary number to a decimal
            dec_num = binary_to_decimal(bit_string[current:current + length])
            length = dec_num + 1
            current += prev_length

    # once we exit the loop, it means we have reached a one.
    return binary_to_decimal(bit_string[current:current + length]), current + length


def get_letters(places_back, repeat,string):
    """
    This function goes back a certain number of positions in the string and repeats the characters from
    that position and add it to the string
    :param places_back: offset from current position
    :param repeat: number of characters to repeat
    :param string: string to use
    :return:
    """
    curr_len = len(string)
    pointer = curr_len - places_back
    for i in range(repeat):
        string += string[pointer]
        pointer += 1
    return string


def lzss_decode(binary):
    """
    This function follows lzss to decode a binary string. It will first decode the header, then use what
    we got from the header to build the binary search tree. After that we will use the binary search tree
    to decode the data part.
    :param binary: binary string to decode
    :return: returns the decoding of the binary string
    """
    current = 0
    n = len(binary) - 1

    # gets the number of unique character after using elias decoding
    unique_char_num,current = elias_decode(binary,current)
    chars_left = unique_char_num - 1
    huffman_decode =[]

    # decoding the header
    # we use the number of unique characters to determine how many times to loop
    while chars_left >= 0:
        # converts the 7 bit ascii character to a decimal value
        ascii_char = binary_to_decimal(binary[current:current+7])
        current = current + 7

        # decodes the length of the encoded code word using elias decoding
        length,current = elias_decode(binary,current)

        # decodes the code word
        code_word = binary[current:current+length]
        current += length
        huffman_decode.append([ascii_char,code_word])
        chars_left -= 1

    # builds a binary tree using the code words
    binaryTree = BinaryTree()
    for i in range(len(huffman_decode)):
        binaryTree.add_encoding(chr(huffman_decode[i][0]), huffman_decode[i][1])

    # gets the total number of fields from the encoding using elias
    total_fields,current = elias_decode(binary,current)
    fields_left = total_fields

    final_encoding = ''
    while fields_left > 0:
        # if the fields is 1, we will find the character from the binary tree that we built using the code words
        if binary[current] == '1':
            current += 1
            letter, skipped = binaryTree.retrieve_letter(binary,current)
            current += skipped
            final_encoding += letter
        # if the field is 0, we just have to use elias decoding to retrieve the offset and number of letter we have to repeat
        else:
            current += 1
            go_back,current = elias_decode(binary,current)
            repeat_letters,current = elias_decode(binary,current)
            final_encoding = get_letters(go_back,repeat_letters,final_encoding)
        fields_left -=1

    return final_encoding


def decimal_to_binary(dec_num):
    """
    This function converts a decimal value to a 8 bit binary value
    :param dec_num: decimal value we want to convert
    :return:
    """
    binary = ""
    if dec_num == 1:
        binary =  "1"
    elif dec_num == 0:
        binary = "0"
    else:
        while dec_num != 0:
            remainder = dec_num % 2
            binary = str(remainder) + binary
            dec_num = dec_num // 2
    if len(binary) != 8:
        rem = 8-len(binary)
        binary = ('0'*rem)+binary
    return  binary


def read_file(file_name):
    """
    This function reads the file name and converts the filename
    :param file_name: file that needs to be read
    :return:
    """
    file = open(file_name,'rb')
    bin_string = ''

    bytes = file.read()

    for b in bytes:
        b = int(b)
        b = decimal_to_binary(b)
        bin_string = bin_string + b

    return bin_string

if __name__ == '__main__':
    argument_0 = sys.argv[0]

    argument_1 = sys.argv[1]

    bin_str = read_file(argument_1)
    decoded_str = lzss_decode(bin_str)

    output_file = open('output_decoder_lzss.txt','w')
    output_file.write(decoded_str)
