from __future__ import annotations

'''
Created on 24.06.2019

@author: Thomas Siegmund Heidenreich
@copyright: MIT license
@summary: Defines the data structure of an directed, weighed multigraph
as well as multiple algorithms for analysis.
'''

import csv
from typing import List, Iterable, Set, Dict, Hashable


class Edge:
    '''A directed, weighted edge.'''    
    source_node: Hashable
    target_node: Hashable
    weight: float
    
    def __init__(self, source_node: Hashable, target_node: Hashable, weight: float=0):
        self.source_node = source_node
        self.target_node = target_node
        self.weight = weight
            
                
class Graph:
    '''
    A directed, weighted multigraph
    
    Allows multiple crossed_edges between arbitrary source - and - target-nodes, 
    nodes are indexed from 0 upwards incrementally.
    '''
    nodes: Set[Hashable]
    edges: Set[Edge]
    outgoing_edges: Dict[Hashable : Set[Edge]]
    entering_edges: Dict[Hashable : Set[Edge]]
       
    def __init__(self, nodes: Iterable[Hashable]=[], edges: Iterable[Edge]=[], **kwargs):
        # If parameters for copying are given
        if('outgoing_edges' in kwargs and
           'entering_edges' in kwargs):
            self.nodes = nodes
            self.edges = edges
            self.outgoing_edges = kwargs['outgoing_edges']
            self.entering_edges = kwargs['entering_edges']
        else:
            self.nodes = set()
            self.edges = set()
            self.outgoing_edges = dict()
            self.entering_edges = dict()
            self.add_nodes(nodes)
            self.add_edges(edges)
    
    def node_count(self) -> int:
        '''Returns the number of nodes in the graph'''
        return len(self.nodes)
    
    def edge_count(self) -> int:
        '''Returns the number of edges in the graph'''
        return len(self.edges)
        
    def add_nodes(self, nodes: Iterable[Hashable]):
        '''Adds the given nodes to the graph'''
        for node in nodes:
            self.add_node(node)
        
    def add_node(self, node: Hashable):
        '''Adds the given node to the graph'''
        if node in self.nodes:
            raise ValueError('Node cannot be added to graph, already contained')
        self.nodes.add(node)
        self.outgoing_edges[node] = set()
        self.entering_edges[node] = set()
    
    def add_edges(self, edges: Iterable[Edge]):
        '''Adds the given crossed_edges to the graph'''
        for edge in edges:
            self.add_edge(edge)
    
    def add_edge(self, edge: Edge):
        '''Adds the given edge to the graph'''
        # Make sure that both the source_node
        if not (edge.source_node in self.nodes and 
            edge.target_node in self.nodes):
            # as well as the target_node are contained in the graph.
            raise ValueError('source - or - target-node of given edge not in graph')      
        self.edges.add(edge)
        self.outgoing_edges[edge.source_node].add(edge)
        self.entering_edges[edge.target_node].add(edge)          
        
    def delete_edges(self, edges: Iterable[Edge]):
        '''Deletes the given edges from the graph'''
        for edge in edges:
            self.delete_edge(edge)    
    
    def delete_edge(self, edge):
        '''Deletes the given edge from the graph'''
        if edge not in self.edges:
            raise ValueError('edge not contained in graph, cannot be deleted')
        self.edges.remove(edge)
        self.outgoing_edges[edge.source_node].remove(edge)
        self.entering_edges[edge.target_node].remove(edge)
        
    def delete_node(self, node):
        '''Deletes the given node with all corresponding edges from the graph'''
        if node not in self.nodes:
            raise ValueError('node not contained in graph, cannot be deleted')
        self.delete_edges(self.outgoing_edges[node].copy())
        self.delete_edges(self.entering_edges[node].copy())
        self.nodes.remove(node)
    
    def copy(self) -> Graph:
        '''Returns a copy of the graph, with the nodes and edges being shallow copies'''
        outgoing_edges_copy = dict()
        entering_edges_copy = dict()
        for node in self.nodes:
            outgoing_edges_copy[node] = self.outgoing_edges[node].copy()
            entering_edges_copy[node] = self.entering_edges[node].copy()
        return Graph(self.nodes.copy(), self.edges.copy(),
                     outgoing_edges=outgoing_edges_copy, entering_edges=entering_edges_copy)

                
class Path:
    '''A directed, weighted path'''    
    graph: Graph
    start_node: Hashable
    visited_nodes: Set[Hashable]
    crossed_edges: List[Edge]
    total_weight: float    
    
    def __init__(self, graph: Graph, start_node: Hashable, crossed_edges : Iterable[Edge]=[], **kwargs):
        self.graph = graph
        self.start_node = start_node  
        if ('visited_nodes' in kwargs and 
            'total_weight' in kwargs):
            self.crossed_edges = crossed_edges  
            self.visited_nodes = kwargs['visited_nodes']
            self.total_weight = kwargs['total_weight']
        else:
            self.crossed_edges = []
            self.visited_nodes = {start_node}
            self.total_weight = 0       
            self.add_edges(crossed_edges)

    def add_edges(self, edges: Iterable[Edge]):
        for edge in edges:
            self.add_edge(edge) 
                
    def add_edge(self, edge: Edge):
        # Check whether the edge is in the graph and follows the path
        if edge not in self.graph.edges or edge.source_node != self.goal_node():
            raise ValueError('Given edge not in graph or not following the path') 
        self.crossed_edges.append(edge)
        self.visited_nodes.add(edge.target_node)
        self.total_weight += edge.weight
        
    def length(self) -> int:
        '''Returns the number of edges crossed'''
        return len(self.crossed_edges)
    
    def goal_node(self) -> Hashable:
        '''Returns the final visited node'''
        if(any(self.crossed_edges)):
            return self.crossed_edges[-1].target_node
        else:
            return self.start_node
        
    def visited_nodes_ordered(self) -> List[Hashable]:
        '''
        Returns a list of all visited nodes 
        in order of visit from start to finish.
        '''        
        visited_nodes_ordered = [self.start_node]
        for edge in self.crossed_edges:
            visited_nodes_ordered.append(edge.target_node)
        return visited_nodes_ordered
    
    def following_edges(self) -> Set[Edge]:
        '''Returns a list of the outgoing crossed_edges of the goal_node.'''   
        return self.graph.outgoing_edges[self.goal_node()]
            
    def copy(self) -> Path:
        '''Copy of the path, with all edges and nodes being shallow copied'''
        return Path(self.graph, self.start_node, self.crossed_edges.copy(),
                    visited_nodes=self.visited_nodes.copy(), total_weight=self.total_weight)


def average_length(paths: Iterable[Path]) -> float:
    '''Returns the average length over all given paths'''
    return length_sum(paths) / len(paths)


def average_total_weight(paths: Iterable[Path]) -> float:
    '''Returns the average total_weight over all given paths'''
    return total_weight_sum(paths) / len(paths)


def length_sum(paths: Iterable[Path]) -> int:
    '''Returns the sum of all lengths of the given paths'''
    length_sum = 0
    for path in paths:
        length_sum += path.length()
    return length_sum


def total_weight_sum(paths: Iterable[Path]) -> float:
    '''Returns the sum of the total_weight of all given paths'''    
    total_weight_sum = 0
    for path in paths:
        total_weight_sum += path.total_weight
    return total_weight_sum 


def shortest_path(paths: Iterable[Path]) -> Path:
    '''Returns the path with minimal total_weight of all given paths'''    
    shortest_path = None
    for path in paths:
        if shortest_path is None or shortest_path.total_weight > path.total_weight :
            shortest_path = path
    return shortest_path 


def longest_path(paths: Iterable[Path]) -> Path:
    '''Returns the path with maximal total_weight of all given paths'''    
    longest_path = None
    for path in paths:
        if longest_path is None or longest_path.total_weight < path.total_weight :
            longest_path = path
    return longest_path 


def all_distinct_cycles(graph: Graph) -> List[Path]:
    '''
    Returns all distinct cycles in the graph
    
    Every returned cycle only contains one cycle total,
    and is unique no matter which starting-node in the
    cycle is chosen.
    '''
    graph_copy = graph.copy()
    all_distinct_cycles = []
    for node in graph.nodes:
        # For all preceding nodes
        for entering_edge in graph_copy.entering_edges[node]:
            # Get all acyclic paths from the node to its preceding nodes
            new_cycles = all_acyclic_paths(graph_copy, node, entering_edge.source_node)
            for cycle in new_cycles:
                # Then add the corresponding entering edge
                cycle.add_edge(entering_edge)
            all_distinct_cycles += new_cycles
        # Delete that node in order to avoid adding the same cycle twice
        graph_copy.delete_node(node)
    return all_distinct_cycles


def all_acyclic_paths(graph: Graph, start_node: Hashable, goal_node: Hashable) -> List[Path]:
    '''Returns all acyclic paths from the start_node to the goal_node'''
    # Check whether start - and - goal-node are contained in graph
    if not (start_node in graph.nodes and goal_node in graph.nodes):
        raise ValueError('Given start - or - goal-node not contained in given graph')
    all_acyclic_paths = []
    current_paths = [Path(graph, start_node)]
    new_paths = []
    # While not all paths converged to the goal_node
    while any(current_paths):
        # Check whether any paths remain
        for current_path in current_paths:
            # If the path reached the goal node,          
            if current_path.goal_node() == goal_node:
                all_acyclic_paths.append(current_path)
            else:
                for following_edge in current_path.following_edges():
                    # If the following edge does not cause any cycles to occur
                    if following_edge.target_node not in current_path.visited_nodes:
                        # Keep the extended path for the next iteration
                        new_path = current_path.copy()
                        new_path.add_edge(following_edge)
                        new_paths.append(new_path)
        current_paths = new_paths
        new_paths = []
    return all_acyclic_paths


def import_graph() -> Graph:
    '''
    Returns the graph created from the "LabyrinthEdges.csv"-file
    
    The metadata in the csv-file is transformed from a undirected network
    in a directed, weighted multigraph.  The returned graph contains 76 
    nodes and 166 crossed_edges.
    '''   
    imported_graph = Graph()
    # Add all nodes
    for i in range(38):
            imported_graph.add_node(str(i) + 'a')
            imported_graph.add_node(str(i) + 'b')
    with open ('resources/LabyrinthEdges.csv') as csvfile:
        crossed_edges = csv.reader(csvfile)
        edges_iter = iter(crossed_edges)
        next(edges_iter, None)
        for edge in edges_iter:
            # Import edge data
            node_1 = str(edge[0])
            node_2 = str(edge[1])
            weight = float(edge[2])
            direction_1 = edge[3]
            direction_2 = edge[4]
            # Add transformed directed edges
            if direction_1 in {'u', 'r'}:
                source_node_a = node_1 + 'a'
                target_node_b = node_1 + 'b'
            else:
                source_node_a = node_1 + 'b'
                target_node_b = node_1 + 'a'
            if direction_2 in {'d', 'l'}:
                target_node_a = node_2 + 'a'
                source_node_b = node_2 + 'b'
            else:
                target_node_a = node_2 + 'b'
                source_node_b = node_2 + 'a'
            imported_graph.add_edge(Edge(source_node_a, target_node_a, weight))
            imported_graph.add_edge(Edge(source_node_b, target_node_b, weight))
    return imported_graph

