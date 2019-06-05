'''
Created on 03.06.2019

@author: Thomas Siegmund Heidenreich
'''

import csv


def main():
    '''
    edges = [
        Edge(0, 1),
        Edge(0, 3),
        Edge(1, 2),
        Edge(1, 2),
        Edge(1, 3),
        Edge(2, 0),
        Edge(2, 3),
        Edge(3, 0)
        ]
    graph = Graph(4)
    graph.add_edges(edges)
    print(len(all_distinct_cycles(graph)))    
    '''    
    '''
    graph = import_graph()
    all_paths = all_acyclic_paths(graph, 0, 37)
    sp = shortest_path(all_paths)
    lp = longest_path(all_paths)
    print(len(all_paths))
    print(lp.visited_nodes_in_order())
    '''
    exit()


def average_total_weight(paths):
    '''Returns the average total_weight over all given paths'''
    return total_weight_sum(paths) / len(paths)


def total_weight_sum(paths):
    '''Returns the sum of the total_weight of all given paths'''
    
    total_weight_sum = 0
    for path in paths:
        total_weight_sum += path.total_weight
    return total_weight


def shortest_path(paths):
    '''Returns the path with minimal total_weight of all given paths'''
    
    shortest_path = None
    for path in paths:
        if shortest_path is None or shortest_path.total_weight > path.total_weight :
            shortest_path = path
    return shortest_path 


def longest_path(paths):
    '''Returns the path with maximal total_weight of all given paths'''
    
    longest_path = None
    for path in paths:
        if longest_path is None or longest_path.total_weight < path.total_weight :
            longest_path = path
    return longest_path 


def all_acyclic_paths(graph, start_node, goal_node):
    '''
    Returns a set of all acyclic paths in the graph 
    leading from the start_node to the goal_node.
    '''
    
    current_paths = [Path(graph, start_node)]
    new_paths = []
    all_paths_converged = False
    # While some paths have not reached the goal_node or 
    # got stuck in a cycle or impasse.
    while not all_paths_converged:
        # Check whether any paths remain
        all_paths_converged = any(current_paths)
        for current_path in current_paths:
            # If the current_path has not reached the goal_node jet
            if current_path.final_node() != goal_node:                
                for following_edge in current_path.following_edges():
                    # If following_edge does not lead into a cycle
                    if following_edge.target_node not in current_path.visited_nodes:
                        # Add extended path to next iteration
                        new_path = current_path.copy()
                        new_path.add_edge(following_edge)                      
                        new_paths.append(new_path)
                        all_paths_converged = False
            # Otherwise simply keep the current_path
            else:
                new_paths.append(current_path)
        current_paths = new_paths
        new_paths = []
    return current_paths

                
def all_distinct_cycles(graph):
    '''
    Returns all cycles in the graph which are pairwise distinct to each other.
    
    A cycle is distinct to another when it is not contained or 
    a rotation of the other cycle.  The cycles always have 
    the smallest indexed node as the starting-node.
    '''
    
    all_distinct_cycles = []    
    for start_node in range(graph.node_count):        
        current_paths = [Path(graph, start_node)]
        new_paths = []
        all_paths_cycled = False        
        while not all_paths_cycled:
            # Check whether the graph contains any cycles
            all_paths_cycled = any(current_paths)
            for current_path in current_paths:
                # If current_path has no edges and thus cannot be a cycle                
                if (current_path.length() == 0 or 
                    current_path.final_node() != start_node):
                    # or has not jet cycled back to the starting-node
                    for following_edge in current_path.following_edges():
                        following_node = following_edge.target_node 
                        # If the following_node is the start_node
                        if (following_node == start_node or 
                           (following_node > start_node and 
                            following_node not in current_path.visited_nodes)):
                            # Or is not contained as a start_node in earlier cycles and 
                            # does not create additional cycles.
                            new_path = current_path.copy()
                            new_path.add_edge(following_edge)
                            # Add extended path to next iteration
                            new_paths.append(new_path)
                            all_paths_cycled = False
                else:
                    # Otherwise simply add cycle to the next iteration
                    new_paths.append(current_path)
            current_paths = new_paths
            new_paths = []
        # Add all cycles containing the current start_node to
        # the set of all distinct cycles.
        all_distinct_cycles.extend(current_paths)
    return all_distinct_cycles


def import_graph():
    '''
    Returns the graph created from the data of the labyrinth of theseus stored as a .csv file.
    
    Graph contains 76 nodes and 166 edges.
    '''
    
    imported_graph = Graph(76)
    with open ('LabyrinthEdges.csv') as csvfile:
        edges = csv.reader(csvfile)
        edges_iter = iter(edges)
        next(edges_iter, None)
        for edge in edges_iter:
            # import edge data
            node_1 = int(edge[0])
            node_2 = int(edge[1])
            weight = float(edge[2])
            direction_1 = edge[3]
            direction_2 = edge[4]
            # add transformed edges
            imported_graph.add_edge(directed_edge
                (node_1, node_2, weight, direction_1, direction_2))
            imported_graph.add_edge(directed_edge
                (node_2, node_1, weight, direction_2, direction_1))
        return imported_graph

            
def _directed_edge(source_node, target_node, weight, source_direction, target_direction):
    '''
    TODO
    '''
    
    if source_direction in {'d', 'l'}:
        source_node += 38
    if target_direction in {'u', 'r'}:
        target_node += 38
    return Edge(source_node, target_node, weight)

        
class Path:
    '''A directed, weighted path'''    

    def __init__(self, graph, start_node, **kwargs):
        self.graph = graph
        self.start_node = start_node     
        if ('edges' in kwargs and
            'visited_nodes' in kwargs and 
            'total_weight' in kwargs):
            self.visited_nodes = kwargs['visited_nodes']
            self.total_weight = kwargs['total_weight']
            self.edges = kwargs['edges']
        else:
            self.visited_nodes = {start_node}
            self.edges = []
            self.total_weight = 0
        
    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge) 
                
    def add_edge(self, edge):
        self.edges.append(edge)
        self.visited_nodes.add(edge.target_node)
        self.total_weight += edge.weight
    
    def length(self):
        return len(self.edges)
    
    def final_node(self):
        if(any(self.edges)):
            return self.edges[-1].target_node
        else:
            return self.start_node
        
    def visited_nodes_in_order(self):
        '''
        Returns a list of all visited nodes 
        in order of visit from start to finish.
        '''
        
        visited_nodes = [self.start_node]
        for edge in self.edges:
            visited_nodes.append(edge.target_node)
        return visited_nodes
    
    def following_edges(self):
        '''Returns a list of the outgoing edges of the final_node.'''
        
        return self.graph.outgoing_edges[self.final_node()]
            
    def copy(self):
        '''Copy of the path.'''
        return Path(self.graph, self.start_node, edges=self.edges.copy(), visited_nodes=self.visited_nodes.copy(), total_weight=self.total_weight)

    
class Graph:
    '''
    A directed, weighted multigraph.
    
    Allows multiple edges between arbitrary source - and - target-nodes, 
    nodes are indexed from 0 upwards incrementally.
    '''
    
    def __init__(self, node_count, edges=None):
        self.node_count = node_count
        self.outgoing_edges = []
        for i in range(node_count):
            self.outgoing_edges.append([])
        self.all_edges = {}
        if edges is not None:
            self.add_edges(edges)
    
    def add_edges(self, edges):
        '''Adds the given edges to the graph.'''
        for edge in edges:
            self.add_edge(edge)
    
    def add_edge(self, edge):
        '''Adds the given edge to the graph.'''
        # Make sure that both the source_node
        if (self.node_in_graph(edge.source_node) and 
            self.node_in_graph(edge.target_node)):
            # as well as the target_node are contained in the graph.
            self.outgoing_edges[edge.source_node].append(edge)
            self.all_edges.add(edge)
        else:
            raise ValueError('source - or - target-node of given edge not in graph')
        
    def edge_count(self):
        '''Returns the amount of edges in the graph.'''
        return len(self.all_edges)
    
    def node_in_graph(self, node):
        '''Returns whether the given node is contained in the graph.'''
        return 0 <= node < self.node_count

    def edge_in_graph(self, edge):
        '''Returns whether the given edge is contained in the graph.'''
        return edge in self.all_edges

                
class Edge:
    '''A directed, weighted edge.'''
    
    def __init__(self, source_node, target_node, weight=0):
        self.source_node = source_node
        self.target_node = target_node
        self.weight = weight

        
if __name__ == '__main__':
    main()
