import math

'''
This min heap class was taken from Assignment 1. Portions of its code are also from FIT 1008.
However, it has been modified to suit the requirements of the assignments accordingly.
'''
class minheap():
    def __init__(self):
        self.heap = [0]
        self.positions =[None]

    def set_positions(self,vertices):
        # initializes the positions list
        self.positions = self.positions*(vertices+1)

    def getsize(self):
        return len(self.heap)

    def swap(self,i, j):
        """
        :param i: first item to swap
        :param j: second item to swap
        :param input_list: list of items to swap
        """
        self.positions[self.heap[i][0].vertex] = j
        self.positions[self.heap[j][0].vertex] = i
        temp = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = temp



    def rise(self,k):
        """
        This function maintains the min heap by swapping the parent and child if the frequency is lesser than the parent
        the item with the lower index
        :param k: index of item to rise
        Time complexity: O(log V)
        """
        while k > 1 and self.heap[k][0].distance < self.heap[k // 2][0].distance:
            self.swap(k, k // 2)
            k //= 2
        return k

    def smallest_child(self,k):
        """
        Gets the position of the child with the smaller distance
        Time complexity: O(1)
        :param k: index of parent
        :return: returns the position of the smaller child with the smaller distance
        """
        if 2 * k == len(self.heap) - 1 or self.heap[2 * k][0].distance < self.heap[2 * k + 1][0].distance:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self,k):
        """
        This function sinks the root by checking the frequency and indexes of both children and swapping
        when neccessary to maintain the properties of a min heap (parent should have a smaller distance
        than child)
        Time Complexity: O(log V)
        :param k: index of root
        """
        while 2 * k + 1 <= len(self.heap):
            child = self.smallest_child(k)
            if self.heap[k][0].distance <= self.heap[child][0].distance:
                break
            self.swap(child, k)
            k = child

    def decrease_distance(self, new_distance, vertex):
        """
        This function is to update the distance if there is a lesser one.
        :param new_distance: distance to be updated
        :param vertex: vertex of distance to be updated
        :return: Does not return anything
        Time Complexity: O(log V)
        """
        index = self.positions[vertex.vertex]
        self.heap[index][1] = new_distance
        vertex.distance = new_distance
        self.rise(index)

    def pop_minVal(self):
        """
        :param input_list: list of items to pop
        :return: returns the root
        """
        minimum = self.heap[1]  # minimum value is always at the root
        self.swap(len(self.heap) - 1, 1)  # swap the min value with the last node
        self.heap.pop()  # remove the last node
        self.sink(1)  # put the root value at the place it should be
        return minimum

    def append(self,items):
        """
        Time Complexity: O(log V)
        This function is to build a min heap based on a list given
        :param input_list: list to build a min heap from
        :return: returns the min heap
        """
        self.heap.append(items)
        pos = self.rise(self.getsize()-1)
        self.positions[items[0].vertex] = pos
        return pos

"""
Portions of the code on how to implement Djikstra is from the lecture slides. The algorithm behind it
is also based on the lecture slides.
"""
class Vertex():
    # Vertex class to keep track of edges and other payloads / properties of a vertex node
    def __init__(self,vertex):
        self.vertex = vertex
        self.edges = []
        self.predecessor = None
        self.visited = False
        self.discovered = False
        self.distance = math.inf
        self.is_redlightcam = False
        self.is_service = False
        self.distance_forward = -1
        self.distance_backward = -1

class Edge():
    # Edge class to keep track of the edge.
    def __init__(self,u,v,w):
        self.u = u
        self.v = v
        self.w = w
        self.is_toll = False

class reverseGraph():
    """
    This is a new class for the reverse graph needed for Task 3. It has the exact same methods as the
    Graph class.
    """
    def __init__(self):
        self.vertices = [None]
        self.size = 0

    def clear(self, source):
        """
            This function is to make the distance of the source be 0 and the rest of the vertices
            to be infinity.
            Time Complexity: O(V)
            :param source: source to initialize distance to 0
            :return: Does not return anything
                """
        for i in range(len(self.vertices)):
            if self.vertices[i] is not None:
                self.vertices[i].visited = False
                self.vertices[i].discovered = False
                if i != source:
                    self.vertices[i].distance = math.inf
        self.vertices[source].distance = 0


    def build_reverse_graph(self,filename):
        """
            Functionality: build the graph and reverse graph using the file.
            Time Complexity: O(E+V) where E is the total number of edges and V is the total number of vertices
            Space Complexity: O(E+V)
            Precondition: the file must be an appropriate file
            :param filename_roads: filename to build the graph with
            :return: Does not return anything
                """
        file = open(filename, 'r')
        file_graph = []
        for item in file:
            item = item.strip()
            item = item.split(' ')
            file_graph.append(item)

        for i in range(len(file_graph)):
            file_graph[i][0] = int(file_graph[i][0])
            file_graph[i][1] = int(file_graph[i][1])
            file_graph[i][2] = float(file_graph[i][2])

        new_file = []
        for i in range(len(file_graph)):
            new_file.append([file_graph[i][0], file_graph[i][1]])

        # gets the vertex with the highest value
        max_vertex = max(new_file[0])
        for i in range(1, len(new_file)):
            cur_max = max(new_file[i])
            if cur_max > max_vertex:
                max_vertex = cur_max
        max_vertex += 1

        self.vertices = self.vertices * max_vertex
        for i in range(max_vertex):
            self.vertices[i] = Vertex(i)
            self.size += 1

        # adds the edges
        for i in range(len(file_graph)):
            self.add_edge(self.vertices[file_graph[i][1]], self.vertices[file_graph[i][0]], file_graph[i][2])

    def add_edge(self, source, destination, weight):
        edge = Edge(source, destination, weight)
        source.edges.append(edge)

    def addService(self,filename_service):
        file = open(filename_service,'r')
        services = []
        for item in file:
            services.append(int(item))

        for item in services:
            self.vertices[item].is_service = True

    def Djikstra(self, source,graph,flag=False):
        """
        Functionality: To find the quickest path from a source that goes through all the nodes. This function uses Djikstra
        to find the shortest path.

        Time Complexity: O(E log V). Where E is the total number of edges and V is the total
                        number of vertices. It is O(E log V) as our heap size is size V and its operations
                        are log(V). We are also relaxing the edges and only going through each edge once
                        so it is O(E log V).
        Space Complexity: The space complexity is O(E+V).Where E is the total number of edges and V is the total
                        number of edges
        Pre condition: source are valid vertices
        :param source: source of node to start from
        :return: Does not return anything
               """
        source = int(source)
        graph.clear(source)
        source_vertex = self.vertices[source]
        result = []

        # building the min heap : O(log v)

        min_heap = minheap()
        min_heap.set_positions(len(self.vertices))
        min_heap.append([source_vertex,source_vertex.distance]) # adds the source to the min heap

        while len(min_heap.heap) > 1:
            # print('source', graph.vertices[source])

            current = min_heap.pop_minVal()[0]
            if current.visited is not True:
               total_distance = current.distance
               if current.is_service is True :
                   total_distance = current.distance
                   if flag == False:
                       current.distance_forward = total_distance
                   else:
                       current.distance_backward = total_distance
            current.visited = True
            # this for loop runs O(VlogV) times
            if len(current.edges) != 0:
                for vertex in current.edges:
                    if vertex.v.visited is True:
                        pass
                    else:
                        if vertex.v.discovered is False:
                            vertex.v.distance = current.distance + vertex.w
                            vertex.v.predecessor = current
                            min_heap.append([vertex.v, vertex.v.distance])
                            vertex.v.discovered = True
                        elif vertex.v.distance > current.distance + vertex.w:
                                if vertex.v.visited is False:
                                    vertex.v.predecessor = current
                                    min_heap.decrease_distance(current.distance + vertex.w, vertex.v)

    def getPath(self,source,target):
        """
        Functionality: To get the path given a source and target vertex
        Time Complexity: O(V) where V is the total number of vertices
        Space Complexity: O(E+V) Where E is the total number of edges and V is the total
                        number of vertices
        Pre condition: source and target must be valid vertices
        :param source: source node
        :param target: target node
        :return:
               """
        source = int(source)

        source_vertex = self.vertices[source]

        target = int(target)
        target_vertex = self.vertices[target]

        result = []
        current_vertex = target_vertex
        while current_vertex != source_vertex:
            result.append(current_vertex.vertex)

            current_vertex = current_vertex.predecessor
        result.append(current_vertex.vertex)

        result = result[::-1]
        return result



class Graph:
    def __init__(self):
        self.vertices = [None]
        self.size = 0
        self.reverse_graph = reverseGraph()     #reverse graph needed for task 3
        self.services = []

    def clear(self,source):
        """
        This function is to make the distance of the source be 0 and the rest of the vertices
        to be infinity.
        Time Complexity: O(V)
        :param source: source to initialize distance to 0
        :return: Does not return anything
        """
        for i in range(len(self.vertices)):
            self.vertices[i].visited = False
            self.vertices[i].discovered = False
            if i != source:
                self.vertices[i].distance = math.inf
        self.vertices[source].distance = 0

    def buildGraph(self,filename_roads):
        """
        Functionality: build the graph and reverse graph using the file.
        Time Complexity: O(E+V) where E is the total number of edges and V is the total number of vertices
        Space Complexity: O(E+V)
        Precondition: the file must be an appropriate file
        :param filename_roads: filename to build the graph with
        :return: Does not return anything
        """
        file = open(filename_roads,'r')
        file_graph = []
        for item in file:
            item = item.strip()
            item = item.split(' ')
            file_graph.append(item)

        # makes the weightage to a float
        for i in range(len(file_graph)):
            file_graph[i][0] = int(file_graph[i][0])
            file_graph[i][1] = int(file_graph[i][1])
            file_graph[i][2] = float(file_graph[i][2])

        new_file = []
        for i in range(len(file_graph)):
            new_file.append([file_graph[i][0], file_graph[i][1]])

        # gets the vertex with the highest value
        max_vertex = max(new_file[0])
        for i in range(1,len(new_file)):
            cur_max = max(new_file[i])
            if cur_max > max_vertex:
                max_vertex = cur_max
        max_vertex += 1

        # populates the vertex list
        self.vertices = self.vertices * max_vertex
        for i in range(max_vertex):
            self.vertices[i] = Vertex(i)
            self.size += 1

        # adds the edges
        for i in range(len(file_graph)):
            self.add_edge(self.vertices[file_graph[i][0]],self.vertices[file_graph[i][1]],file_graph[i][2])

        # building the reverse graph
        self.reverse_graph.build_reverse_graph(filename_roads)

    def add_edge(self,source,destination,weight):
        """
        Adds the edges to the vertexes.
        :param source: source vertex
        :param destination: destination vertex
        :param weight: weight of the edge
        :return: Does not return anything
        """
        edge = Edge(source,destination,weight)
        source.edges.append(edge)

    def quickestPath(self, source, target):
        """
        Functionality: To find the quickest path from a source to a target. This function uses Djikstra
        to find the shortest path.

        Time Complexity: O(E log V). Where E is the total number of edges and V is the total
                        number of vertices. It is O(E log V) as our heap size is size V and its operations
                        are log(V). We are also relaxing the edges and only going through each edge once
                        so it is O(E log V).
        Space Complexity: The space complexity is O(E+V).Where E is the total number of edges and V is the total
                        number of edges
        Pre condition: source and target are valid vertices
        :param source: source of node to start from
        :param target: target node which is the destination
        :return: returns [[],-1] if there is no path between source and vertex. Returns the path with the shortest distance
                 if there exists a path
        """
        source = int(source)
        target = int(target)
        self.clear(source)
        result = []
        source_vertex = self.vertices[source]
        target_vertex = self.vertices[target]

        # building the min heap : O(log v)
        min_heap = minheap()
        min_heap.set_positions(len(self.vertices))
        min_heap.append([source_vertex,source_vertex.distance]) # adds the source to the min heap

        # this while loop runs (E log V) times
        while target_vertex.visited is not True and len(min_heap.heap) > 1:
            current = min_heap.pop_minVal()[0]

            if current.visited is not True:
                # adds node to the heap if it hasnt already been added
                result.append(current.vertex)
                total_distance = current.distance
            current.visited = True

            if len(current.edges) != 0:
                for vertex in current.edges:
                    # if vertex is already visited, we dont go through it again
                    if vertex.v.visited is True:
                        pass
                    else:
                        if vertex.v.discovered is False:
                            vertex.v.distance = current.distance + vertex.w
                            vertex.v.predecessor = current
                            # puts vertex in the heap if it isnt already inside
                            min_heap.append([vertex.v, vertex.v.distance])
                            vertex.v.discovered = True
                        elif vertex.v.distance > current.distance + vertex.w:
                                if vertex.v.visited is False:
                                    vertex.v.predecessor = current
                                    # updates the distance
                                    min_heap.decrease_distance(current.distance + vertex.w, vertex.v)

        if target_vertex.visited is not True:
            # returns this if there is no path
            return [[],-1]
        else:
            # uses the predecessor to get the shortest path
            result = []
            current_vertex = target_vertex
            while current_vertex != source_vertex:
                result.append(current_vertex.vertex)
                current_vertex = current_vertex.predecessor
            result.append(current_vertex.vertex)
            result = result[::-1]

        return (result,total_distance)

    def augmentGraph(self,filename_camera,filename_toll):
        """
        Functionality: to modify the vertices and edges to check if its a camera or toll
        Time Complexity: O(EV) where E is the total number of edges and V is the total number of vertices
        Space Complexity: O(E+V) where E is the total number of edges and V is the total number of vertices
        Pre condition: file names are valid
        :param filename_camera: file that contains the red light cameras
        :param filename_toll: file that contains the tolls
        :return: Does not return anything
        """
        camera = open(filename_camera,'r')
        tolls = open(filename_toll,'r')

        cam_list =[]
        toll_list =[]
        for item in camera:
            item = item.strip()
            item = int(item)
            cam_list.append(item)

        for item in tolls:
            item = item.strip()
            item = item.split()
            item[0] = int(item[0])
            item[1] = int(item[1])
            toll_list.append(item)

        for item in cam_list:
            self.vertices[item].is_redlightcam = True

        for item in toll_list:
            edges = self.vertices[item[0]].edges
            for edge in edges:
                if edge.u.vertex == item[0] and edge.v.vertex == item[1]:
                    edge.is_toll = True

    def quickestSafePath(self, source, target):
        """
        Functionality: To find the quickest safe path from a source to a target that does not consist.
                       of red light cameras and tolls. This function uses Djikstra to find the shortest path.

        Time Complexity: O(E log V). Where E is the total number of edges and V is the total
                        number of edges. It is O(E log V) as our heap size is size V and its operations
                        are log(V). We are also relaxing the edges and only going through each edge once
                        so it is O(E log V).
        Space Complexity: The space complexity is O(E+V).Where E is the total number of edges and V is the total
                        number of vertices
        Pre condition: source and target are valid vertices
        :param source: source of node to start from
        :param target: target node which is the destination
        :return: returns [[],-1] if there is no path between source and vertex. Returns the path with the shortest distance
                 going through no cameras and tolls if there exists a path
        """
        source = int(source)
        target = int(target)
        self.clear(source)
        result = []
        source_vertex = self.vertices[source]
        target_vertex = self.vertices[target]

        # building the min heap : O(log v)

        min_heap = minheap()
        min_heap.set_positions(len(self.vertices))
        min_heap.append([source_vertex, source_vertex.distance])  # adds the source to the min heap

        # this while loop runs (E log V) times
        while target_vertex.visited is not True and len(min_heap.heap) > 1:
            current = min_heap.pop_minVal()[0]

            # checks if vertex is a red light camera, if it is, goes back to the beginning of the loop
            if current.is_redlightcam is True:
                continue

            if current.visited is not True and current.is_redlightcam is False:
                # adds node to the heap if it hasnt already been added
                result.append(current.vertex)
                total_distance = current.distance
            current.visited = True

            if len(current.edges) != 0:
                for edge in current.edges:
                    # checks if the edge is a toll
                    if edge.v.visited is True or edge.is_toll is True:
                        pass
                    else:
                        if edge.v.discovered is False:
                            edge.v.distance = current.distance + edge.w
                            edge.v.predecessor = current
                            min_heap.append([edge.v, edge.v.distance])
                            edge.v.discovered = True
                        elif edge.v.distance > current.distance + edge.w:
                            if edge.v.visited is False:
                                edge.v.predecessor = current
                                min_heap.decrease_distance(current.distance + edge.w, edge.v)

        if target_vertex.visited is not True:
            # returns this is there is no path
            return [[], -1]

        else:
            # uses the predecessor to get the previous nodes to get the path
            result = []
            current_vertex = target_vertex
            while current_vertex != source_vertex:
                result.append(current_vertex.vertex)
                current_vertex = current_vertex.predecessor
            result.append(current_vertex.vertex)
            result = result[::-1]

        return(result, total_distance)

    def addService(self, filename_service):
        """
        Functionality: To modify the vertices if they are a service
        Time Complexity: O(V) where V is the total number of vertices
        Space Complexity: O(E+V)
        Pre condition: file must be a valid file
        :param filename_service:
        :return: Does not return anything
        """
        file = open(filename_service, 'r')
        services = []
        for item in file:
            services.append(int(item))

        for item in services:
            self.services.append(item)
            self.vertices[item].is_service = True

        for item in services:
            self.reverse_graph.vertices[item].is_service = True

    ## modified version of Djikstra to run only from the source.
    def Djikstra(self, source, graph, flag=False):
        """
        Functionality: To find the quickest path from a source that goes through all the nodes. This function uses Djikstra
        to find the shortest path.

        Time Complexity: O(E log V). Where E is the total number of edges and V is the total
                        number of vertices. It is O(E log V) as our heap size is size V and its operations
                        are log(V). We are also relaxing the edges and only going through each edge once
                        so it is O(E log V).
        Space Complexity: The space complexity is O(E+V).Where E is the total number of edges and V is the total
                        number of edges
        Pre condition: source are valid vertices
        :param source: source of node to start from
        :return: Does not return anything
        """
        source = int(source)
        graph.clear(source)
        source_vertex = self.vertices[source]
        result = []

        # building the min heap : O(log v)
        min_heap = minheap()
        min_heap.set_positions(len(self.vertices))
        min_heap.append([source_vertex, source_vertex.distance])  # adds the source to the min heap

        while len(min_heap.heap) > 1:
            current = min_heap.pop_minVal()[0]
            if current.visited is not True:
                total_distance = current.distance
                # checks if it is a service. if it is, gets the current distance forward / backwards
                if current.is_service is True:
                    total_distance = current.distance
                    if flag == False:
                        current.distance_forward = total_distance
                    else:
                        current.distance_backward = total_distance
            current.visited = True
            if len(current.edges) != 0:
                for vertex in current.edges:
                    if vertex.v.visited is True:
                        pass
                    else:
                        if vertex.v.discovered is False:
                            vertex.v.distance = current.distance + vertex.w
                            vertex.v.predecessor = current
                            min_heap.append([vertex.v, vertex.v.distance])
                            vertex.v.discovered = True
                        elif vertex.v.distance > current.distance + vertex.w:
                            if vertex.v.visited is False:
                                vertex.v.predecessor = current
                                min_heap.decrease_distance(current.distance + vertex.w, vertex.v)

    def getPath(self, source, target):
        """
        Functionality: To get the path given a source and target vertex
        Time Complexity: O(V) where V is the total number of vertices
        Space Complexity: O(E+V) Where E is the total number of edges and V is the total
                        number of vertices
        Pre condition: source and target must be valid vertices
        :param source: source node
        :param target: target node
        :return:
        """
        source = int(source)
        source_vertex = self.vertices[source]

        target = int(target)
        target_vertex = self.vertices[target]

        result = []
        current_vertex = target_vertex
        while current_vertex != source_vertex:
            result.append(current_vertex.vertex)
            current_vertex = current_vertex.predecessor
        result.append(current_vertex.vertex)

        result = result[::-1]
        return result

    def quickestDetourPath(self,source,target):
        """
        Functionality: To find the quickest detour path from the source to the target passing
        through atleast one of the service vertices.

        Time Complexity: O(2E log V) = O(E log V).Where E is the total number of edges and V is the total
                        number of vertices. It is so because we are running Djikstra twice. First on our
                        original graph and the second time on the reversed graph.
        Space Complexity: O(E+V) Where E is the total number of edges and V is the total
                        number of vertices
        Pre condition: source and target have to be valid vertices.
        :param source: source to start from
        :param target: target to end.
        :return: returns [[],-1] if theres no valid path. Returns a path and distance otherwise.
        """
        source = int(source)
        target = int(target)

        # This is O(2E log V). We run Djikstra for both the original graph and the reversed graph.
        self.Djikstra(source,self)
        self.reverse_graph.Djikstra(target,self.reverse_graph,True)

        possibilites_list =[]

        # gets the distances of going to the service node from the source and going to the target from service node
        for i in range(len(self.services)):
            if self.vertices[self.services[i]].distance_forward == -1 or self.reverse_graph.vertices[self.services[i]].distance_backward == -1:
                pass
            else:
                dist = [self.vertices[self.services[i]].distance_forward + self.reverse_graph.vertices[self.services[i]].distance_backward,
                self.services[i]]
                possibilites_list.append(dist)

        if len(possibilites_list) != 0:
            # gets the minmum value (shortest distance)
            minimum = min(possibilites_list)
            print(minimum)
            # gets the paths to combine them
            path1 = self.getPath(source,minimum[1])
            path2 = self.reverse_graph.getPath(target,minimum[1])
            path2 = path2[::-1]
            path2 = path2[1::]
            combined_paths = path1 + path2
            print([combined_paths,minimum[0]])
            return (combined_paths,minimum[0])
        else:
            return [[],-1]



if __name__ == '__main__':
    print('-----------------------------------------------------')
    graph = input("Enter the file name for the graph: ")
    camera_nodes = input("Enter the file name for the camera nodes: ")
    toll_roads = input("Enter the file name for the toll roads: ")
    service_nodes = input("Enter the file name for the service nodes: ")

    print('-----------------------------------------------------')
    source = input("Source node: ")
    sink_node = input("Sink node: ")
    print('-----------------------------------------------------')

    new_graph = Graph()
    new_graph.buildGraph(graph)
    quickest_path = new_graph.quickestPath(source,sink_node)
    result_str1 = ''
    arrow = ''
    for v in (quickest_path[0]):
        result_str1 += arrow + str(v)
        arrow = ' --> '
    print('-----------------------------------------------------')
    print('Quickest path:')
    print(result_str1)
    print('Time taken: '+ str(quickest_path[1]) + ' minute(s)')


    new_graph.augmentGraph(camera_nodes,toll_roads)
    safe_quickest_path = new_graph.quickestSafePath(source,sink_node)
    result_str2 = ''
    arrow = ''
    for v in (safe_quickest_path[0]):
        result_str2 += arrow + str(v)
        arrow = ' --> '
    print('-----------------------------------------------------')
    print('Safe quickest path:')
    print(result_str2)
    print('Time taken: '+ str(safe_quickest_path[1]) + ' minute(s)')

    new_graph.addService(service_nodes)
    quickest_detour = new_graph.quickestDetourPath(source,sink_node)
    result_str3 = ''
    arrow = ''
    for v in (quickest_detour[0]):
        result_str3 += arrow + str(v)
        arrow = ' ---> '
    print('-----------------------------------------------------')
    print('Quickest detour path:')
    print(result_str3)
    print('Time taken: ' + str(quickest_detour[1]) + ' minute(s)')


