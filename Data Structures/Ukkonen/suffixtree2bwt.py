# NAME: Vhera Kaey Vijayaraj
# STUDENT ID: 28903013

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import sys
sys.path.append('..')
from ukkonen import Suffix_tree



def in_order_traversal(node,suffix_array):
    """
    This function recursively traverses through the suffix tree lexicographically to get the leaves
    so that we can build a suffix array. It is a recursive function that calls itself until the last node
    so that we can get its leaves.
    :param node: The node we are currently on
    :param suffix_array: suffix array that we are generating that holds all the suffix ids.
    :return:
    """
    current = node
    n = 256
    i = 0
    # we loop 256 times because we have 256 possible alphabets
    for i in range(256):

        # if our current nodes next node is not none, it means we have to still traverse some more
        # we will go to out next node
        if current.next_nodes[i] != None:
            in_order_traversal(current.next_nodes[i],suffix_array)

        # once we have found the node, we now have to check the edges of that node. If the edge is a leaf,
        # then only we will get the suffix id value stored at the leaf.
        else:
            if current.edges[i] != None:
                if current.edges[i].leaf_value != None:
                    suffix_array.append(current.edges[i].leaf_value)

def bwt(suffix_array, string):
    """
    This function builds a bwt string from a suffix array. I learnt how to construct a bwt string froma suffix array with this link: https://www.youtube.com/watch?v=4n7NPk5lwbI
    :param suffix_array: suffix array that contains all the sorted suffixes.
    :param string: string that we used to build the suffix array
    :return: returns a bwt string
    """
    bwt_string = ""
    for i in range(len(suffix_array)):
        if suffix_array[i] == 0:
            bwt_string += "$"
        else:
            bwt_string += string[suffix_array[i] - 1]
    return bwt_string


if __name__ == '__main__':
    argument_0 = sys.argv[0]

    argument_1 = sys.argv[1]

    text_file = open(argument_1,'r')
    output_file = open('output_bwt.txt','w')

    for line in text_file:
        text = line

    text = text + "$"
    suffixtree = Suffix_tree(text)
    suffixtree.build_suffix_tree()
    suffix_array = []
    in_order_traversal(suffixtree.root,suffix_array)
    bwt_string = bwt(suffix_array,text)
    output_file.write(bwt_string)

    text_file.close()
    output_file.close()

