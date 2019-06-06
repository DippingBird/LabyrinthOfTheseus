'''
Created on 06.06.2019

@author: Thomas Siegmund Heidenreich
'''

import GraphAnalysis


def written_paths_analysis(paths):
    '''Returns a string containing analysis of the given paths.'''
    shortest_path = GraphAnalysis.shortest_path(paths)
    longest_path = GraphAnalysis.longest_path(paths)
    written_paths_analysis = f'''    
----------General Paths----------
    
Count          : {len(paths)}
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


def written_path(path, line_length=60):
    '''
    Returns a string showing the visited nodes of the given path in order
    with the corresponding edge-weights.
    '''
    line_count = 1
    written_path = f'({path.start_node})'
    for edge in path.edges:
        written_path += f'-[{edge.weight:.1f}]->'
        # If the current line is longer than the given line-length,
        # cut it off
        if(line_count*line_length < len(written_path)):
            written_path += '\n'
            line_count += 1
        written_path +=f'({edge.target_node})'
    return written_path


def written_path_nodes(path):
    '''Returns a string showing the visited nodes of the given path in order.'''
    written_path_nodes=''
    for visited_node in path.visited_nodes_ordered():
        written_path_nodes += f'({visited_node})->'
    return written_path_nodes[0:-2]
