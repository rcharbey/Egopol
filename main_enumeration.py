# -*- coding: utf-8 -*-
import enumerate

def main(graph, options):
    if 'k' in options:
        k = options['k']
    else:
        k = 5
        
    if 'method' in options:
        method = options['method']
    else:
        method = 'degree'
    
    return enumerate.characterize_with_patterns(graph, k, method)