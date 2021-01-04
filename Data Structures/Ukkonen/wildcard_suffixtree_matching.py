# NAME: Vhera Kaey Vijayaraj
# STUDENT ID: 28903013

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import sys
sys.path.append('..')
from ukkonen import Suffix_tree


class wildcardPointer:
    def __init__(self):
        self.length = 0
        self.current_node = None
        self.current_edge = None
        self.potential_nodes = None
        self.potential_edges = None

# in order traversal to checked for edges that are matched so we can get the leaf value
def in_order_matched(matched_array,current):
    for i in range(256):
        if current.next_nodes[i] != None:
            in_order_matched(matched_array,current.next_nodes[i])
        else:
            if current.edges[i] != None:
                if current.edges[i].matched == True:
                    if current.edges[i].leaf_value != None:
                        matched_array.append(current.edges[i].leaf_value)

# in order traversal to set the edges to match from a given node
def in_order_traversal(node):
    current = node
    n = 256
    i=0
    for i in range(256):
        if current.next_nodes[i] != None:
            in_order_traversal(current.next_nodes[i])
        else:
            if current.edges[i] != None:
                current.edges[i].matched = True


def compare_letter_at_edge(edge,j,pattern,string,remainder):
    """
    This function compares every letter at an edge based on a string with a pattern
    :param edge: edge that we want to compare the letters with
    :param j: position in the pattern we are currently comparing
    :param pattern: pattern we want to check is on the edge
    :param string: string that we built the tree with
    :param remainder: remaining number of characters we have to compare

    :return: returns the remainder OR a 0 indicating every character has been matched OR a -1 indicating there
             was a mismatch somewhere along the edge. Also returns the total number of characters
             that has been compared and j value to tell us where in the pattern we are
    """
    total_compared = 0

    # goes through all the characters in the edge
    for i in range(edge.get_edge_length()):

        # if the character is a wildcard OR is equivalent to the string at the edge, we count it as a match
        if pattern[j] == string[edge.start + i] or pattern[j] == "?":
            remainder -= 1
            j += 1
            total_compared += 1
            # we have finished comparing every letter at the edge, and there are no more letters to compare
            if j > len(pattern)-1:
                return  0, total_compared,j
        else:
            # if we have mismatched on a letter, we return -1. the pattern does not exist along this edge
            return -1,total_compared,j

    # if we have matched with every character on the edge and need to move to the next one.
    return remainder,total_compared,j

def traverse_compare(curr_node,j,remainder,pattern,string):
    """
    This function is a recursive function that recursively traverses throughout all the edges
    from a node when we come accross a wild card.
    :param curr_node: current node we are at
    :param j: j is the indicator of where we are in the pattern
    :param remainder: remaining number of characters we have to compare
    :param pattern: pattern we are comparing with
    :param string: string we used to build the tree
    :return:
    """
    for i in range(256):
        if curr_node != None and curr_node.edges[i] != None:
            # we check to see if the edge we are at matches the pattern
            r, total_compared,x = compare_letter_at_edge(curr_node.edges[i],j,pattern,string,remainder)

            # if it doesnt match, we go to the next edge
            if r == -1:
                continue
            # if it matches, we will traverse the edges below it if its not a leaf to mark the edges as matched as well
            elif r == 0:
                # makes all the edges after the current one matched as well.
                curr_node.edges[i].matched = True
                if curr_node.edges[i].isLeaf == False:
                    nextNode = curr_node.next_nodes[ord(string[curr_node.edges[i].start])]
                    in_order_traversal(nextNode)
            # if we matched all the characters at an edge, but we still have a remainder,we need to go to the next node.
            else:
                edge = curr_node.edges[i]
                traverse_compare(curr_node.next_nodes[ord(string[curr_node.edges[i].start])],j+edge.get_edge_length(),remainder-edge.get_edge_length(),pattern,string)
                continue

def wildcard_search(string,pattern):
    """
    This function is used for searching a pattern with wildcards in the string. It returns
    all the occurences.
    :param pattern: pattern to search for in the tree
    :param string: string that we are going to find the pattern in
    :return: returns all the occurences of pattern in the string
    """

    # first we build a suffic tree with the string
    st = Suffix_tree(string)
    st.build_suffix_tree()
    n = len(pattern)-1
    j = 0
    remaining = n+1

    # initializing a pointer
    p = wildcardPointer()
    p.current_node = st.root # sets the current node to the root

    while j <= n:
        ori_j = j

        # if our pattern at position j is not a wildcard, we know we have only one edge that we can follow
        if pattern[j] != '?':
            current_edge = p.current_node.edges[ord(pattern[j])]

            # if we dont have that edge, it means we dont have a match
            if current_edge == None:
                break
            else:
                # compares all the letters on that edge
                remaining,tc,j = compare_letter_at_edge(current_edge,j,pattern,string,remaining)

            # if our remaining = -1, we mismatched somewhere, it breaks the loop
            if remaining == -1:
                break

            # if remaining = 0, we matched everything on the edge
            elif remaining == 0:
                current_edge.matched = True

            # if we still have remaining characters to compare,we go to the next node
            else:
                p.current_node = p.current_node.next_nodes[ord(pattern[ori_j])]
                p.potential_nodes = p.current_node.next_nodes
                p.potential_edges =p.current_node.edges
        else:
            traverse_compare(p.current_node, j, remaining, pattern, string)
            break

    occurences = []
    # gets all the suffix id's of the matched edges that will give us all the occurences of the pattern in text
    in_order_matched(occurences,st.root)
    for i in range(len(occurences)):
        occurences[i] = occurences[i] + 1
    return occurences


if __name__ == '__main__':
    argument_0 = sys.argv[0]

    argument_1 = sys.argv[1]
    argument_2 = sys.argv[2]

    text_file = open(argument_1,'r')
    pat_file = open(argument_2, 'r')
    output_file = open('output_wildcard_matching.txt','w')

    for line in text_file:
        text = line

    for line in pat_file:
        pattern = line

    text = text + "$"

    occurences = wildcard_search(text,pattern)
    for i in range(len(occurences)):
        output_file.write(occurences[i].__str__()+"\n")

    text_file.close()
    pat_file.close()
    output_file.close()


