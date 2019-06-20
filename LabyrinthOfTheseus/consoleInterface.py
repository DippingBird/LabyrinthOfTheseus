'''
Created on 06.06.2019

@author: Thomas Siegmund Heidenreich
'''

import graphAnalysis
from typing import Collection


def main():
    display_labyrinth_graph_analysis()
    exit()


def display_labyrinth_graph_analysis():
    '''
    Displays the analysis of the Labyrinth of Theseus
    as a graph in the console.
    '''
    print('Building graph ...')
    graph = graphAnalysis.import_graph()
    print('Done!')
    # All acyclic paths from the entry to the exit of the labyrinth
    print('Analysing graph ...')
    acyclic_paths = graphAnalysis.all_acyclic_paths(graph, 0, 37)
    cyclic_paths = graphAnalysis.all_distinct_cycles(graph)
    print('Done!')
    print(f'''
----------Labyrinth of Theseus graph analysis----------

Node count : {graph.node_count}
Edge count : {graph.edge_count()}

-----------Acyclic paths from entry to exit------------
{written_paths_analysis(acyclic_paths)}
-------------------Distinct cycles---------------------
{written_paths_analysis(cyclic_paths)}
''')
    

def written_paths_analysis(paths: Collection[graphAnalysis.Path]) -> str:
    '''Returns a string containing analysis of the given paths.'''
    shortest_path = graphAnalysis.shortest_path(paths)
    longest_path = graphAnalysis.longest_path(paths)
    written_paths_analysis = f'''    
----------General Paths----------
    
Path count     : {len(paths)}
Average length : {graphAnalysis.average_length(paths):.3f}
Average weight : {graphAnalysis.average_total_weight(paths):.3f}

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


def written_path(path: graphAnalysis.Path, max_line_length: int=80) -> str:
    '''
    Returns a string showing the visited nodes of the given path in order
    with the corresponding edge-weights.
    '''
    # Make sure that at least two nodes with on edge
    # fit in one line.
    if(max_line_length <= 16):
        raise ValueError('Given maximal line-length is to short')
    char_count = 0
    written_path = f'({path.start_node})'
    for edge in path.edges:
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
    
    