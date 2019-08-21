# The Labyrinth of Theseus
A hobby project analysing a puzzle about the labyrinth of theseus invented by David Wells republished by Heinrich Hemme on [spektrum.de](https://www.spektrum.de/).

---
## Table of Contents
1. [**Motivation**](#motivation)
2. [**Graph Generation**](#graph-generation)
3. [**Algorithms**](#algorithms)
4. [**Usage**](#usage)
5. [**License**](#license)
---
## Motivation
The idea to create this project began with solving the current puzzle from the mathematical puzzle-column "[Mathematische Rätsel](https://www.spektrum.de/raetsel/)" titled "[Hemmes mathematische Rätsel: Das Labyrinth](https://www.spektrum.de/raetsel/das-labyrinth/1577642)" written by Heinrich Hemme and published online by the "[Spektrum der Wissenschaft Verlagsgesellschaft mbH](https://www.spektrumverlag.de/impressum/)" on the 25th October of 2018, a german version of the [Scientific American](https://www.scientificamerican.com/). Hemmes short summary of the puzzle translated into englisch:

> Theseus enters the labyrinth, in which Minotaurus lurks on him, through the 
> southern entrance and wants to leave it through the northern, where Ariadne waits
> on him. In order to confuse the beast, Theseus leaves no romm in which he enters 
> through the opposite exit, but rather taking a turn to the right or left. Which is
> the shortest path of this kind through the labyrinth? It should be assumed that 
> Theseus always walks parallel or cross to the walls of the rooms.

![Image of the labyrinth](/resources/images/labyrinth.png)
All rights reserved to Heinrich Hemme

Hemme showed that the shortest path Theseus could take is 30 units long assuming that a small quadratic room has a sidelength of 1 unit. He also mentioned that Markus Götz from Maihingen (who sadly passed away last year i was told by Hemme) analyzed the problem 1998 and found that there were a total of 624 acyclic paths for Theseus to take.

![Image of shortest path in labyrinth](/resources/images/shortestPath.png)
All rights reserved to Heinrich Hemme

My approach was converting the labyrinth into a graph and applying [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) in order to find the shortest path. A few months passed until i wanted to learn how to program in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) after learning C# and Java. I figured writing a program analysing this puzzle as a graph would be a good first challenge, hopefully finding the same amount of acyclic paths that Markus found.

However i found quite the opposite, that there were 8256 acyclic paths, more than 13-times the amount that Markus found! After a lot of pondering and double-checking i believe my awnser is the correct one, however i cannot be absolutely sure, a third person solving the problem through programing would certainly help deciding which the correct awnser is.
## Graph Generation
In order to convert the labyrinth into a graph i placed nodes into each transit from one romm in another, as well from the start in the first room and from the last room to the goal. Edges are added between nodes respecting the rule of always turning right or left, and the weight being the length assuming the same units as Hemme. This placement of the nodes has the advantage of treating every romm equally, meaning that the edges are similar for similar rooms.

However each node has two states, for nodes connecting horizontal adjacent rooms entering from the left or right, and for vertical adjacent rooms entering from up or down. Thus each node actually represents two nodes in an ordinary directed weighted graph, but since these two nodes are highly symmetrical they can often just be treated as one.

Since the puzzle is only concerned with paths from the start to the finish one can simplify the graph by deleting nodes which have only outgoing-or-ingoing edge, resulting in the folowing graph.

![Image of the labyrinth graph](/resources/images/graph.png)
Image using the transformed work of Heinrich Hemme

The nodes are arbitrary indexed in a raster-fashion from the bottom upwards and left-to-right. One can easily see that this simplification does not alter the amount of paths between the start-and-goal nodes nor the amount of cycles in the graph, since no choice is made when entering or leaving such nodes.

The last step is converting the presented graph into a proper directed weighted graph, which i did by assigning nodes that are entered from the left or bottom and left from the right or top the index shown in the graph, otherwise the index added with 38, assuring that all nodes are distinct and indexed consecutive.

The edges of the shown undirected graph are given to a program as a typed in [csv-file](/resources/labyrinthEdges.csv). The directions specify where the edge is leading relative to the node, being shortened as follows:

Identifier | Direction
-----------|----------
u          | up
d          | down
l          | left
r          | right

The edges are written in an ascending order, according to the following order-relation:

```python
is_lesser_than(edge1, edge2):
'''Returns wether edge1 is behind edge2 in an ascending order.'''

   # Smaller indexed nodes of both edges
   minnode1 = min(edge1.node1, edge1.node2)
   minnode2 = min(edge2.node1, edge2.node2)
   # Greater indexed nodes of both edges
   maxnode1 = max(edge1.node1, edge1.node2)
   maxnode2 = max(edge2.node1, edge2.node2)
   
   # Compare by the smaller indexed nodes
   if minnode1 < minnode2:
      return True
   # then the greater ones
   elif minnode1 == minnode2 and maxnode1 < maxnode2:
      return True
   else:
      # finally compare by weight
      return maxnode1 == maxnode2 and ede1.weight < edge2.weight
```

By default node1 is allready the smaller and node2 the bigger indexed node.
## Algorithms
The project implements two main  algorithms for analysing the graph. One returning the set of all acyclic paths from a given start-node to a given goal-node, and another returning the set of all distinct cycles. A cycle is called distinct in this context if it does not contain another cycle and its start-node is unique, which is archieved by always choosing the smallest indexed node as the start-node (in the following example it is the maximal indexed node).

Since the graph can have multiple edges bewtween two nodes it is a so called multigraph, and this prevents the implementation of a weight-function with the source-and-target-node as inputs. A simplified but logical identical Python-Code is shown as follows, in the actual project these algorithms are implemented  as iterative not recursive ones to increase efficiency. One can further increase efficiency by using Hash-Sets to implement Path.visited_nodes, in order to check for containement in O(1) instead of O(n). One could also when finding all distinct cycles simply delete the edges and nodes that are not needed anymore to avoid uneccesary edge-checking, however this was not done in this project because it increases the complexity of the graph-class, the "deleted" nodes are simply ignored. A full implementation of the Graph, Edge or Path class is not given.


```python
class Edge:
'''A directed, weighted edge.''' 
   source_node: int
   target_node: int
   weight: float


class Graph:
'''A directed, weighted multigraph.'''
   # Nodes are indexed from 0 to node_count-1 incremental
   node_count: int
   
   delete_maximal_node(self):
      '''
      Deletes the highest indexed node from the graph as well as 
      all in-and-outleading edges.
      '''
      pass
      
   copy(self):
      '''Returns a copy of the path with all attributes being a shallow copy.'''
      pass


class Path:
'''A directed, weighted path'''
   # The graph in which the path is contained
   graph: Graph
   # The node in the graph where the path starts
   start_node: int
   # The node in the graph where the path ends
   finish_node: int
   # Set of all nodes which are visited on the path
   visited_nodes: Collection[int]
   # Set of all outgoing edges from the finish-node
   following_edges: Collection[Edge]
   
   __init__(self, graph: Graph, start_node: int):
      self.graph = graph
      self.start_node = start_node     
  
   add_edge(self, edge: Edge):
   '''Adds the edge to the path if it is a following edge.'''
      pass
   
   copy(self):
   '''Returns a copy of the path with all attributes being a shallow copy.'''
      pass
      
      
# Initialize the current_path parameter only containing the start-node
# and all_paths as an empty collection.
GetAllAcyclicPaths(current_path: Path, goal_node: int, all_paths=[]: Collection[Path]):
'''Returns a list of all acyclic paths leading from the given path to the goal-node.'''
   # If the path has not reached the goal yet
   if current_path.finish_node is not goal_node:
      # For all edges continuing the path
      for edge in path.following_edges:
         # which dont cause cycles
         if edge.target_node not in path.visited_nodes:
            # Recursively use method on the new path extended by the following edge
            new_path = current_path.copy()
            new_path.add_egde(edge)
            paths.extend(GetAllAcyclicPaths(new_path, goal_node, all_paths)   
   else:
      # If the path has reached the goal add it to the list of all acyclic paths
      all_paths.add(current_path)
   return all_paths


GetAllDistinctCycles(graph: Graph):
'''Returns a list of all distinct cycles in the given graph.'''
   reduced_graph = graph.copy()
   all_cycles = []: List[Path]
   # For all possible maximal indexed start-nodes
   for i in range(graph.node_count-1, -1, -1):
      all_cycles.extend(GetAllAcyclicPaths(Path(reduced_graph, i), i))
      reduced_graph.delete_maximal_node()
   return all_cycles 
```

Shortest and longest paths are found via linear search, as well as other data for example the arithmetic average of the length of all distinct cycles. This leads among other things to the following result, the longest acyclic path:

![Longest path](/resources/images/longestPath.png)
Image using the transformed work of Heinrich Hemme

## Usage

By running the module [`consoleInterface`](/consoleInterface.py) the graph is analysed and the results should returned as a console log similar as follows:

```
Building graph ...
Done!
Analysing graph ...
Done!
Time passed:  132.64 seconds

----------Labyrinth of Theseus graph analysis----------

Node count : 76
Edge count : 166

-----------Acyclic paths from entry to exit------------
     
----------General Paths----------
    
Path count     : 8256
Average length : 35.047
Average weight : 70.516

----------Shortest Path----------

Length         : 14
Weight         : 30.0

(0)-[2.0]->(2)-[1.0]->(4)-[2.0]->(9)-[2.0]->(15)-[2.5]->(10)-[2.5]->(6)
(6)-[4.0]->(8)-[1.5]->(11)-[2.5]->(16)-[2.0]->(18)-[2.5]->(20)-[2.5]->(27)
(27)-[1.0]->(33)-[2.0]->(37)

----------Longest Path-----------

Length         : 51
Weight         : 104.0

(0)-[2.0]->(2)-[1.0]->(4)-[1.0]->(1)-[3.5]->(7)-[1.5]->(9)-[1.5]->(13)
(13)-[2.5]->(17)-[2.5]->(20)-[2.5]->(18)-[2.0]->(16)-[2.5]->(11)-[1.5]->(14)
(14)-[3.5]->(12)-[1.5]->(8)-[4.0]->(6)-[2.5]->(10)-[2.5]->(15)-[2.0]->(17)
(17)-[2.5]->(13)-[1.5]->(9)-[1.5]->(7)-[3.5]->(1)-[1.0]->(4)-[1.0]->(2)
(2)-[2.0]->(3)-[1.0]->(5)-[2.5]->(10)-[2.5]->(6)-[4.0]->(8)-[1.5]->(12)
(12)-[3.5]->(14)-[1.5]->(11)-[2.5]->(16)-[2.0]->(18)-[2.5]->(20)-[2.5]->(26)
(26)-[3.0]->(32)-[1.0]->(27)-[1.0]->(33)-[2.0]->(34)-[1.0]->(29)-[1.0]->(24)
(24)-[1.5]->(22)-[1.5]->(19)-[3.5]->(23)-[1.5]->(25)-[1.0]->(31)-[3.0]->(36)
(36)-[1.0]->(30)-[1.0]->(35)-[2.0]->(37)    

-------------------Distinct cycles---------------------
    
----------General Paths----------
    
Path count     : 3538
Average length : 24.910
Average weight : 54.987


----------Shortest Path----------

Length         : 3
Weight         : 4.0

(1)-[1.0]->(4)-[1.0]->(2)-[2.0]->(1)

----------Longest Path-----------
 
Length         : 39
Weight         : 85.0

(1)-[1.0]->(4)-[1.0]->(2)-[2.0]->(3)-[1.0]->(5)-[2.5]->(10)-[2.5]->(6)
(6)-[4.0]->(8)-[1.5]->(12)-[3.5]->(14)-[1.5]->(11)-[2.5]->(16)-[2.0]->(18)
(18)-[2.5]->(20)-[2.5]->(27)-[1.0]->(33)-[2.0]->(32)-[1.0]->(26)-[4.0]->(17)
(17)-[2.5]->(13)-[3.0]->(7)-[1.5]->(1)-[2.0]->(2)-[1.0]->(4)-[2.0]->(9)
(9)-[2.0]->(15)-[2.0]->(18)-[2.0]->(16)-[2.5]->(11)-[1.5]->(14)-[3.5]->(12)
(12)-[1.5]->(8)-[4.0]->(6)-[2.5]->(10)-[2.5]->(15)-[2.0]->(17)-[2.5]->(13)
(13)-[1.5]->(9)-[1.5]->(7)-[3.5]->(1)
```

This task takes approximate 2 minutes on my Intel i5-7200U processor running Windows 10 and CPython. All the algorithms in the module [`graphAnalysis`](graphAnalysis.py) should work with any arbitrary graph. However the module [`consoleInterface`](/consoleInterface.py) has some settings specific to the example, that being the check for minimal line length in line 77, assuming that the nodes are never indexed above 99, and the weights are only displayed with one decimal of accuracy. Also the nodes are displayed modulu 38 so they fit the [graph](/resources/images/graph.png) shown before.

## License

This project is licensed under the terms of the MIT license.
