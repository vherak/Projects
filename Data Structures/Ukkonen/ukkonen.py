class Node:
    """
    This is a class to store the nodes
    """
    def __init__(self, root = None):
        self.link = root
        self.prev_node = None
        self.next_nodes = [None]*256    # to store the next nodes
        self.edges = [None]*256

class End:
    """
    This is a class to store the Ends of the edges
    """
    def __init__(self):
        self.end_counter = 0

    # this function will incremenet the counter
    def increment_endcounter(self):
        self.end_counter += 1

class Edge:
    """
    This class is an edge class that stores the start and end of each edge, and if it has a leaf value
    """
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.edge_length = self.get_edge_length()
        self.isLeaf = True
        self.leaf_value = None
        self.matched = False

    # if there is an edge object there, we will get the length of the edge
    # with the end counter. Otherwise, we will just get the length of the edge with the start and end value
    def get_edge_length(self):
        # gets the length of the edge
        try:
            self.end.end_counter
        except:
            return self.end - self.start + 1
        else:
            return self.end.end_counter - self.start

class Pointer:
    def __init__(self):
        self.active_node = None
        self.active_edge = None
        self.length = 1

class Suffix_tree:
    """
    This class is to build a suffix tree. When the build suffix tree method is called, a suffix
    tree is made from the string.
    """
    def __init__(self,string):
        self.root = Node()
        self.root.link = self.root
        self.string = string


    def build_suffix_tree(self):
        """
        This function builds a suffix tree without using suffix links. It follows Ukkonnen's algorithm
        along with the tricks and rules.
        :return:
        """
        i = 0
        j = 0
        string = self.string
        n = len(string)-1
        root = self.root
        e = End()

        # setting pointer to the root initially
        pointer = Pointer()
        pointer.active_node = self.root
        edge_only = False

        # we will have n phases
        while i <= n:
            current_letter = string[j]
            pointer.active_edge = pointer.active_node.edges[ord(current_letter)]

            # if letter is not in the tree yet, insert it by making a new edge from the root
            if pointer.active_node.edges[ord(current_letter)] == None:
                pointer.active_node.edges[ord(current_letter)] = Edge(i,e)
                pointer.active_node.edges[ord(current_letter)].leaf_value = j
                pointer.active_node.edges[ord(current_letter)].isLeaf = True

                # we will also start a new phase
                i += 1
                j += 1
                e.increment_endcounter()
            else:
            # if it is already in the tree, It is Rule 3 and Show stopper. We will start a new phase
            # and maintain the value of j
                i += 1
                if i > n:
                    continue
                e.increment_endcounter()
                pointer.active_edge = pointer.active_node.edges[ord(string[j])]
                pointer.length = 1

                while j != i:
                    current_letter = string[i]
                   # if our edge length is less than the length of substring we are looking at, we traverse the nodes using skip count
                    if pointer.active_edge.get_edge_length() < i - j + 1:
                        prev_edge,total_skips,remainder,edge_only = self.skip_count_traverse(i,j,pointer,string)
                        str_compare = string[pointer.active_edge.start+remainder]

                        # if we only need to branch and not create a new node
                        if edge_only == True:
                            current_node = pointer.active_node

                            # creating a new egde and assigning a leaf value
                            new_edge = Edge(i, e)
                            current_node.edges[ord(string[i])] = new_edge
                            new_edge.leaf_value = j
                            new_edge.isLeaf = True

                            self.reset_pointer(pointer, current_node, j + 1, string, i)
                            edge_only = False
                            j += 1
                            continue


                    # otherwise, we are already on the right edge. we dont need to traverse
                    else:

                        str_compare = string[pointer.active_edge.start + pointer.length]

                    # if its rule 3 again, we start a new phase by incrementing i and going to the next letter
                    # by increasing the pointer length
                    if str_compare == current_letter and pointer.length != -1:
                        i += 1
                        if i > n:
                            break
                        e.increment_endcounter()
                        pointer.length += 1

                    # if its not rule 3 again, its rule 2: branching
                    else:
                        current_edge = pointer.active_edge
                        current_node = pointer.active_node


                        # if the current edge is not a leaf, branching is different. One edge will have a fixed end value
                        if current_edge.isLeaf == False:
                            end = current_edge.get_edge_length()

                            # updating edge of current edges end
                            current_edge.end = current_edge.start + pointer.length - 1
                            current_edge.isLeaf = False
                            current_edge.leaf_value = None

                            current_next_node = current_node.next_nodes[ord(string[current_edge.start])]

                            # creating a new node, with a link to root
                            new_node = Node(self.root)

                            starting = pointer.length + current_edge.start
                            # creating 2 new edges. The edge we have had originally will now have a fixed end value
                            new_edge1 = Edge(pointer.length + current_edge.start, end-pointer.length+starting-1)
                            new_edge1.isLeaf = False
                            new_edge1.leaf_value = None

                            new_edge2 = Edge(i, e)
                            new_edge2.leaf_value = j
                            new_edge2.isLeaf = True

                            # adding the edges to the newly created node
                            new_node.edges[ord(string[pointer.length + current_edge.start])] = new_edge1
                            new_node.edges[ord(string[i])] = new_edge2

                            if current_next_node!= None:
                                new_node.next_nodes[ord(string[pointer.length + current_edge.start])] = current_next_node

                            # assigning the values so that we know by following the edge, we can go to the next node from the current one
                            current_node.next_nodes[ord(string[current_edge.start])]= None
                            current_node.next_nodes[ord(string[current_edge.start])] = new_node



                        else:
                            # changes active node to the next one if needed
                            current_edge.end = current_edge.start+pointer.length-1
                            current_edge.isLeaf = False
                            prev_leaf_value = current_edge.leaf_value
                            current_edge.leaf_value = None

                            # creates two new edges and a new node
                            new_node = Node(self.root)
                            new_edge1 = Edge(pointer.length+current_edge.start, e)
                            new_edge1.isLeaf = True
                            new_edge1.leaf_value = prev_leaf_value

                            new_edge2 = Edge(i,e)
                            new_edge2.leaf_value = j
                            new_edge2.isLeaf = True
                            new_node.edges[ord(string[pointer.length+current_edge.start])] = new_edge1
                            new_node.edges[ord(string[i])] = new_edge2

                            current_node.next_nodes[ord(string[current_edge.start])] = new_node



                        j += 1
                        # just resets pointer to root because not using suffix links
                        self.reset_pointer(pointer, current_node, j, string,i)


    def reset_pointer(self,p,current_active_node,j,string,i):
        # resets pointer to start again from the root.
        p.active_node = current_active_node.link
        p.active_edge = p.active_node.edges[ord(string[j])]
        p.length = i-j

    def skip_count_traverse(self,i,j,pointer,string):
        """
        This function performs the traversal when we need to traverse the nodes.
        It will place the pointer at the right edge and node we are supposed to be looking at.
        Since I didnt implement suffix links, it will always traverse from the root
        :param i: current position of i
        :param j: current position of j
        :param pointer: pointer
        :param string: string we are building suffix tree on
        :return:
        """

        # initializes some variables that we need for the traversal
        pointer.active_node = self.root
        pointer.active_edge = pointer.active_node.edges[ord(string[j])]
        previous_edge = pointer.active_edge
        current_node = pointer.active_node
        current_edge = pointer.active_edge
        total = 0   # total stores the total characters we have already compared
        remainder = i-j+1   # remainder stores the characters we have not yet compared
        skips = j
        edge_only = False   # this variable stores the value whether we need to just branch with and edge only if we already have a node there
        while total < i-j+1 and remainder > current_edge.get_edge_length():
            # if we have an edge from that node
            if current_node.edges[ord(string[current_edge.start])] != None and current_node.next_nodes[ord(string[current_edge.start])] != None:
                total += current_edge.get_edge_length()
                remainder -= current_edge.get_edge_length()
                current_node = current_node.next_nodes[ord(string[current_edge.start])]

                # if we already have a node there and we just need an edge
                if current_node.edges[ord(string[j+total])] == None and current_node != None:
                    edge_only = True
                    break
                # if we cant traverse anymore
                elif current_node == None:
                    break
                else:
                    current_edge = current_node.edges[ord(string[j+total])]
            else:
                break

        # updates pointer values after traversing
        pointer.active_node = current_node
        pointer.active_edge = current_edge
        pointer.length = remainder-1
        return previous_edge, total,remainder-1,edge_only


