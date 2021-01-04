# NAME: Vhera Kaey Vijayaraj
# STUDENT ID: 28903013

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import sys
sys.path.append('..')
from ukkonen import Suffix_tree

class LcpsPointer:
    def __init__(self):
        self.active_node = None
        self.active_edge = None

def lcps(suffix_tree,pair,string):
    '''
    This function gets the longest prefix that is common to the suffixes starting at i and j.
    It traverses the suffix tree and checks if the letters match.
    :param suffix_tree: suffix tree to get the lcps pairs from
    :param pair: a list of 2 values (i & j)
    :param string: the string to find the lcps from i and j
    :return: returns the number of characters of the longest common prefix suffix
    '''
    i = pair[0]
    j = pair[1]
    n = len(string)-1
    matched = 0     # this variable stores the length of the longest common prefix that is common to the suffixes
    pointer = LcpsPointer()     # this pointer keeps track of the active node and edge

    # initializes the pointer to start from the root and edge to follow string[i]
    pointer.active_node = suffix_tree.root
    pointer.active_edge = pointer.active_node.edges[ord(string[i])]

    # if the strings are equal, we know that string[i..current edge length] = string[j..current edge length]
    # using this information, we can go to the next node.
    while j <= n and string[i] == string[j]:
        if pointer.active_node != None and pointer.active_edge != None:
            curr_node = pointer.active_node
            current_edge_length = pointer.active_edge.get_edge_length()

            pointer.active_node = curr_node.next_nodes[ord(string[i])]
            matched += current_edge_length  # we match with all the characters at the edge

            # increment i and j as they match
            i += current_edge_length
            j += current_edge_length

            # if j > n, it means we have reached the end of the string. we can break the loop
            if j > n:
                break
            pointer.active_edge = pointer.active_node.edges[ord(string[j])]
        else:
            break

    return matched




if __name__ == '__main__':
    argument_0 = sys.argv[0]

    argument_1 = sys.argv[1]
    argument_2 = sys.argv[2]

    text_file = open(argument_1,'r')
    pairs_file = open(argument_2,'r')
    output_file = open('output_lcps.txt','w')

    text = ''
    for line in text_file:
        text = line
    text = text+"$"
    pairs_list = []
    # gets the pairs from the file and converts them to integers
    for line in pairs_file:
        line = line.strip()
        line = line.split(' ')
        line[0] = int(line[0])
        line[1] = int(line[1])
        pairs_list.append(line)

    # constructs a suffix tree
    suffix_tree = Suffix_tree(text)
    suffix_tree.build_suffix_tree()

    lcps_list =[]
    for i in range(len(pairs_list)):
        temp = pairs_list[i].copy()
        # since index starts at 0 for the string, i minus 1 from the file numbers.
        temp[0] = temp[0]-1
        temp[1] = temp[1] -1
        lcps_list.append(lcps(suffix_tree,temp,text))

    # writes pairs and matches into the output file.
    for i in range(len(pairs_list)):
        output_file.write(pairs_list[i][0].__str__() + " "+ pairs_list[i][1].__str__() + " " + lcps_list[i].__str__()+ "\n")

    text_file.close()
    pairs_file.close()
    output_file.close()