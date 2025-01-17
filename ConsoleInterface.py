'''
Created on 24.06.2019

@author: Thomas Siegmund Heidenreich
@copyright: MIT license
@summary: Contains Methods to present the results of the graph analysis
in the console.
'''

import GraphAnalysis
from typing import Collection
import time

def main():
    display_labyrinth_graph_analysis()
    exit()
    


def display_labyrinth_graph_analysis():
    '''
    Displays the analysis of the Labyrinth of Theseus
    as a graph in the console.
    '''
    begin = time.time()
    print('Building graph ...')
    graph = GraphAnalysis.import_graph()
    print('Done!')
    # All acyclic paths from the entry to the exit of the labyrinth
    print('Analysing graph ...')
    acyclic_paths = GraphAnalysis.all_acyclic_paths(graph, '0a', '37a')
    cyclic_paths = GraphAnalysis.all_distinct_cycles(graph)
    print('Done!')
    end = time.time()
    print(f'Time passed: {end - begin: .2f} seconds')
    print(f'''
----------Labyrinth of Theseus graph analysis----------

Node count : {graph.node_count()}
Edge count : {graph.edge_count()}

-----------Acyclic paths from entry to exit------------
{written_paths_analysis(acyclic_paths)}
-------------------Distinct cycles---------------------
{written_paths_analysis(cyclic_paths)}
''')    

    
def written_paths_analysis(paths: Collection[GraphAnalysis.Path]) -> str:
    '''Returns a string containing analysis of the given paths.'''
    shortest_path = GraphAnalysis.shortest_path(paths)
    longest_path = GraphAnalysis.longest_path(paths)
    written_paths_analysis = f'''    
----------General Paths----------
    
Path count     : {len(paths)}
Average length : {GraphAnalysis.average_length(paths):.3f}
Average weight : {GraphAnalysis.average_total_weight(paths):.3f}

----------Shortest Path----------

Length         : {shortest_path.length()}
Weight         : {shortest_path.total_weight:.1f}

{written_path(shortest_path)}

----------Longest Path-----------

Length         : {longest_path.length()}
Weight         : {longest_path.total_weight:.1f}

{written_path(longest_path)}    
'''
    return written_paths_analysis


def written_path(path: GraphAnalysis.Path, max_line_length: int=80) -> str:
    '''
    Returns a string showing the visited nodes of the given path in order
    with the corresponding edge-weights.
    '''
    # Make sure that at least two nodes with on edge
    # fit in one line.
    if(max_line_length <= 18):
        raise ValueError('Given maximal line-length is to short')
    char_count = 0
    written_path = f'({path.start_node})'
    for edge in path.crossed_edges:
        next_node = f'-[{edge.weight:.1f}]->({edge.target_node})'
        # If the current line is longer than the given line-length,
        # cut it off
        if(max_line_length <= (len(written_path)-char_count)+len(next_node)):
            # Account for line-break character
            char_count = len(written_path) + 1
            written_path += f'\n({edge.source_node})'
        written_path += next_node
    return written_path


if __name__ == '__main__':
    main()
    
    
