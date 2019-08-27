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
<sup>All rights reserved to Heinrich Hemme</sup>

Hemme showed that the shortest path Theseus could take is 30 units long assuming that a small quadratic room has a sidelength of 1 unit. He also mentioned that Markus Götz from Maihingen (who sadly passed away last year i was told by Hemme) analyzed the problem 1998 and found that there were a total of 624 acyclic paths for Theseus to take.

![Image of shortest path in labyrinth](/resources/images/shortestPath.png)
<sup>All rights reserved to Heinrich Hemme</sup>

My approach was converting the labyrinth into a graph and applying [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) in order to find the shortest path. A few months passed until i wanted to learn how to program in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) after learning C# and Java. I figured writing a program analysing this puzzle as a graph would be a good first challenge, hopefully finding the same amount of acyclic paths that Markus found.

However i found quite the opposite, that there were 8256 acyclic paths, which was later confirmed by a friend of Hemme, the mathematician Helmut Postl residing in Vienna, Austria.

## Graph Generation
In order to convert the labyrinth into a graph i placed nodes into each transit from one room in another, as well from the start in the first room and from the last room to the goal. Edges are added between nodes respecting the rule of always turning right or left, and the weight being the length assuming the same units as Hemme. This placement of the nodes has the advantage of treating every romm equally, meaning that the edges are similar for similar rooms.

However each node has two states, for nodes connecting horizontal adjacent rooms entering from the left or right, and for vertical adjacent rooms entering from up or down. Thus each node actually represents two nodes in an ordinary directed weighted graph, but since these two nodes are highly symmetrical they can often just be treated as one.

Since the puzzle is only concerned with paths from the start to the finish one can simplify the graph by deleting nodes which have only outgoing-or-ingoing edge, resulting in the folowing graph.

![Image of the labyrinth graph](/resources/images/graph.png)
<sup>Image using the transformed work of Heinrich Hemme</sup>

The nodes are arbitrary indexed in a raster-fashion from the bottom upwards and left-to-right. One can easily see that this simplification does not alter the amount of paths between the start-and-goal nodes nor the amount of cycles in the graph, since no choice is made when entering or leaving such nodes.

The last step is converting the presented graph into a proper directed weighted graph, which i did by adding to nodes that are entered from the left or bottom and left from the right or top the letter **a**, otherwise **b**.

The edges of the shown undirected graph are given to a program as a typed in [csv-file](/resources/labyrinthEdges.csv). The directions specify where the edge is leading relative to the node, being shortened as follows:

Identifier | Direction
-----------|----------
u          | up
d          | down
l          | left
r          | right

The edges are written in an ascending order, according to the following order-relation:

```python
is_lesser_than(edge_1, edge_2):
'''Returns wether edge_1 is behind edge_2 in an ascending order.'''

   # Smaller indexed nodes of both edges
   minnode_1 = min(edge_1.node_1, edge_1.node_2)
   minnode_2 = min(edge_2.node_1, edge_2.node_2)
   # Greater indexed nodes of both edges
   maxnode_1 = max(edge_1.node_1, edge_1.node_2)
   maxnode_2 = max(edge_2.node_1, edge_2.node_2)
   
   # Compare by the smaller indexed nodes
   if minnode_1 < minnode_2:
      return True
   # then the greater ones
   elif minnode_1 == minnode_2 and maxnode_1 < maxnode_2:
      return True
   else:
      # finally compare by weight
      return maxnode_1 == maxnode_2 and edge_1.weight < edge_2.weight
```

By default `node_1` is allready the smaller and `node_2` the bigger indexed node.

## Algorithms
The project implements two main  algorithms for analysing the graph. One returning the set of all acyclic paths from a given start-node to a given goal-node, and another returning the set of all distinct cycles. 
A cycle is called distinct in this context if it does not contain another cycle and its unique no matter which node is chosen as the starting node.

The algorithm for finding all acyclic paths simply visits the succeeding nodes from the current paths (starting with one path
only containing the starting-node) and creates a new, extended path to each visited node. 
If the visited node is the goal-node, it is added to the list of all acyclic paths. If not, and no cycle is created, i.e. the node has not been visited before, it is added to the next iteration as starting path, otherwise it is ignored. After that the current paths are also ignored, and the iteration starts again with the remaining extended paths.
This procedure repeats until no paths are added to the next iteration, i.e. all extended paths reach their goal or cause
a cycle to occur.

The algorithm for finding all distict cyclic paths uses the previous algorithm by choosing a random node from the graph and collecting all acyclic paths from this node to its preceeding nodes. After that the paths are extended by their edge to the node and added to the list of all distinct cycles. 
Then the node is deleted from the graph, including all entering and outgoing edges, and a random node is picked from the remaining set and the procedure is repeated, until no nodes remain.

Since the graph can have multiple edges bewtween two nodes it is a so called multigraph, and this prevents the implementation of a weight-function with the source-and-target-node as inputs. For the second algorithm, a copy of the graph can be used if the graph should not be modified.

Shortest and longest paths are found via linear search, as well as other data for example the arithmetic average of the length of all distinct cycles. This leads among other things to the following result, the longest acyclic path:

![Longest path](/resources/images/longestPath.png)
<sup>Image using the transformed work of Heinrich Hemme</sup>

## Usage

By running the module [`ConsoleInterface`](/ConsoleInterface.py) the graph is analysed and the results should returned as a console log similar as follows:

```
Building graph ...
Done!
Analysing graph ...
Done!
Time passed:  80.00 seconds

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

(0a)-[2.0]->(2a)-[1.0]->(4b)-[2.0]->(9a)-[2.0]->(15a)-[2.5]->(10a)-[2.5]->(6a)
(6a)-[4.0]->(8a)-[1.5]->(11b)-[2.5]->(16b)-[2.0]->(18b)-[2.5]->(20b)
(20b)-[2.5]->(27a)-[1.0]->(33a)-[2.0]->(37a)

----------Longest Path-----------

Length         : 51
Weight         : 104.0

(0a)-[2.0]->(2a)-[1.0]->(4b)-[1.0]->(1b)-[3.5]->(7a)-[1.5]->(9a)-[1.5]->(13b)
(13b)-[2.5]->(17a)-[2.5]->(20a)-[2.5]->(18a)-[2.0]->(16a)-[2.5]->(11a)
(11a)-[1.5]->(14a)-[3.5]->(12b)-[1.5]->(8b)-[4.0]->(6b)-[2.5]->(10b)
(10b)-[2.5]->(15b)-[2.0]->(17b)-[2.5]->(13a)-[1.5]->(9b)-[1.5]->(7b)
(7b)-[3.5]->(1a)-[1.0]->(4a)-[2.5]->(10a)-[2.5]->(5b)-[1.0]->(2b)-[2.0]->(3a)
(3a)-[1.0]->(6a)-[4.0]->(8a)-[1.5]->(12a)-[3.5]->(14b)-[1.5]->(11b)
(11b)-[2.5]->(16b)-[2.0]->(18b)-[2.5]->(20b)-[2.5]->(26b)-[3.0]->(32b)
(32b)-[1.0]->(27a)-[1.0]->(33a)-[2.0]->(34b)-[1.0]->(29a)-[1.0]->(24b)
(24b)-[1.5]->(22a)-[1.5]->(19b)-[3.5]->(23b)-[1.5]->(25a)-[1.0]->(31a)
(31a)-[3.0]->(36b)-[1.0]->(30b)-[1.0]->(35a)-[2.0]->(37a)    

-------------------Distinct cycles---------------------
    
----------General Paths----------
    
Path count     : 3538
Average length : 24.910
Average weight : 54.987

----------Shortest Path----------

Length         : 2
Weight         : 4.0

(3b)-[3.0]->(6b)-[1.0]->(3b)

----------Longest Path-----------

Length         : 39
Weight         : 85.0

(12a)-[3.5]->(14b)-[1.5]->(11b)-[2.5]->(16b)-[2.0]->(18b)-[2.0]->(15b)
(15b)-[2.0]->(9b)-[2.0]->(4a)-[1.0]->(2b)-[2.0]->(1a)-[1.5]->(7b)-[3.0]->(13a)
(13a)-[2.5]->(17b)-[4.0]->(26a)-[1.0]->(32a)-[2.0]->(33b)-[1.0]->(27b)
(27b)-[2.5]->(20a)-[2.5]->(18a)-[2.0]->(16a)-[2.5]->(11a)-[1.5]->(14a)
(14a)-[3.5]->(12b)-[1.5]->(8b)-[4.0]->(6b)-[2.5]->(10b)-[2.5]->(5a)-[1.0]->(3b)
(3b)-[2.0]->(2a)-[1.0]->(4b)-[1.0]->(1b)-[3.5]->(7a)-[1.5]->(9a)-[1.5]->(13b)
(13b)-[2.5]->(17a)-[2.0]->(15a)-[2.5]->(10a)-[2.5]->(6a)-[4.0]->(8a)
(8a)-[1.5]->(12a)
```

This task takes approximate 2 minutes on my Intel i5-7200U processor running Windows 10 and CPython. All the algorithms in the module [`GraphAnalysis`](/GraphAnalysis.py) should work with any arbitrary graph. However the module [`ConsoleInterface`](/ConsoleInterface.py) has some settings specific to the example, that being the check for minimal line length in line 84, assuming that the nodes never have an identifier-length greater than 3, and the weights are only displayed with one decimal of accuracy.

## License

This project is licensed under the terms of the MIT license.
