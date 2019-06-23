# The Labyrinth of Theseus
A hobby project analysing a puzzle about the labyrinth of theseus by David Well republished by Heinrich Hemme on [spektrum.de](https://www.spektrum.de/).

---
## Table of Contents
1. **Motivation**
2. **Graph Generation**
3. **Algorithms**
4. **Usage**
5. **License**
---
## Motivation
The idea to make this project began with the solving of the current puzzle from the column "[Mathematische Rätsel](https://www.spektrum.de/raetsel/)" titled "[Hemmes mathematische Rätsel: Das Labyrinth](https://www.spektrum.de/raetsel/das-labyrinth/1577642)" written by Heinrich Hemme and published online by the "[Spektrum der Wissenschaft Verlagsgesellschaft mbH](https://www.spektrumverlag.de/impressum/)" on the 25th October of 2018, a german version of the [Scientific American](https://www.scientificamerican.com/). Hemmes short summary of the puzzle translated into englisch:

> Theseus enters the labyrinth, in which Minotaurus lurks on him, through the 
> southern entrance and wants to leave it through the northern, where Ariadne waits
> on him. In order to confuse the beast, Theseus leaves no romm in which he enters 
> through the opposite exit, but rather taking a turn to the right or left. Which is
> the shortest path of this kind through the labyrinth? It should be assumed that 
> Theseus always walks parallel or cross to the walls of the rooms.

![Image of the labyrinth](/LabyrinthOfTheseus/resources/labyrinth.png)
All rights reserved to Heinrich Hemme

Hemme showed that the shortest path Theseus could take is 30 units long assuming that a small quadratic room has a sidelength of 1 unit. He also mentioned that Markus Götz from Maihingen analyzed the problem 1998 and found that there were a total of 624 acyclic paths for Theseus to take.

![Image of shortest path in labyrinth](/LabyrinthOfTheseus/resources/shortestPath.png)
All rights reserved to Heinrich Hemme

My approach was converting the labyrinth into a graph and applying [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) in order to find the shortest path. A few months passed until i wanted to learn how to program in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) after learning C# and Java. I figured writing a program analysing this puzzle as a graph would be a good first challenge, hopefully finding the same amount of acyclic paths that Markus found.

However i found quite the opposite, that there were 8256 acyclic paths, more than 13-times the amount that Markus found! After a lot of pondering and double-checking i believe my awnser is the correct one, however i cant be absolutely sure, a third person solving the problem through programing would certainly help deciding which the correct awnser is.
## Graph Generation
In order to convert the labyrinth into a graph i placed a node into transit from one romm in another, as well from the start in the first room and from the last room to the goal. Edges are added between nodes respecting the rule of always turning right or left, and the weight being the length assuming the same units as Hemme. This placement of the nodes has the advantage of treating every romm equally, meaning that the edges are similar for similar rooms.

However each node has two states, for nodes connecting horizontal adjacent rooms entering from the left or right, and for vertical adjacent rooms entering from up or down. Thus each node actually represents two nodes in an ordinary directed weighted graph, but since these two nodes are highly symmetrical they can often be treated just as one.

Since the puzzle is only concerned with paths from the start to the finish one can simplify the graph by deleting nodes which have only outgoing or ingoing edge, resulting in the folowing graph.

![Image of the labyrinth graph](/LabyrinthOfTheseus/resources/graph.png)
Transformed image using the work of Heinrich Hemme

The nodes are arbitrary indexed in a raster-fashion from the bottom upwards and left-to-right. One can easily see that this simplification does not alter the amount of paths between the start-and-goal nodes nor the amount of cycles in the graph, since no choice is made when entering or leaving such nodes.

The last step is converting the presented graph into a proper directed weighted graph, which i did by assigning nodes that are entered from the left or bottom and left from the right or top the index shown in the graph, otherwise the index added with 38, assuring that all nodes are distinct and indexed consecutive.

The edges of the shown undirected are given to a program as a typed in [csv-file](/LabyrinthOfTheseus/resources/labyrinthEdges.csv). the directions specify where the edge is leading relative to the node, being shortened as follows:

Identifier | Direction
-----------|----------
u | up
d | down
l | left
r | right

The edges are written in an ascending order, according to the following order-relation:

```python
IsLesserThan(edge1, edge2):
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
The project implements twomain  algorithms for analysing the graph. One returning the set of all acyclic paths from a given start-node to a given goal-node, and another returning the set of all distinct cycles. A cycle is called distinct in this context if it doesnt contain another cycle and its start-node is unique, which is archieved by always choosing the smallest indexed node as the start-node.

Since the graph can have multiple edges bewtween two nodes it is a so called multigraph, and prevents the implementation of a weight-function with the source-and-target-node as inputs. A simplified but logically identical Python-Code is shown as follows, in the actual project these algorithms are implemented  as iterative not recursive ones to increase efficiency. One can further increase efficiency by using Hash-Sets to implement Path.visited_nodes, in order to check for containement in O(1) instead of O(n). A full implementation of the Graph, Edge or Path class is not given.

```python

class Edge:
'''A directed, weighted edge.''' 
   source_node: int
   target_node: int
   weight: float

class Grapg:
'''A directed, weighted multigraph.'''
   # Nodes are indexed from 0 to node_count-1 incremental
   node_count: int

class Path:
   # The node where the path starts
   start_node: int
   # The node where the path ends
   finish_node: int
   # Set of all nodes which are visited on the path
   visited_nodes: Collection[int]
   # Set of all outgoing edges from the finish-node
   following_edges: Collection[Edge]
   
   __init__(self, start_node):
      self.start_node = start_node
  
   add_edge(self, edge: Edge):
   '''Adds the edge to the path if it is a following edge.'''
      pass
   
   copy(self) -> Path:
   '''Returns a shallow copy of the path.'''
      pass
      
      
# Initialize the current_path parameter only containing the start-node
# and all_paths as an empty collection
GetAllAcyclicPaths(current_path: Path, goal_node: int, all_paths=[]: Collection[Path], ignore_nodes=0: int) -> Collection[Path]:
'''Returns a list of all acyclic paths leading from the given path to the goal-node.'''
   # If the path hasnt reached the goal yet
   if current_path.finish_node is not goal_node:
      # For all edges continuing the path
      for edge in path.following_edges:
         # which dont cause cycles
         if edge.target_node not in path.visited_nodes and edge.target_node >= ignore_nodes:
            # Recursively use method on the new path extended by the following edge
            new_path = current_path.copy()
            new_path.add_egde(edge)
            paths.extend(GetAllAcyclicPaths(goal_node, new_path, all_paths)   
   else:
      # If the path has reached the goal add it to the list of all acyclic paths
      all_paths.add(current_path)
   return all_paths

#TODO
GetAllDistinctCycles(graph: Graph) -> Collection[Path]:
'''Returns a list of all distinct cycles in the given graph.'''
   all_cycles = []: List[Path]
   for i in range(0, graph.node_count):
      all_cycles.extend(GetAllAcyclicPaths(Path(i), i,  [], i)
   return all_cycles 

```

Shortest and longest paths are found via linear search, as well as other data for example the arithmetic average of the length of all distinct cycles.

## Usage
