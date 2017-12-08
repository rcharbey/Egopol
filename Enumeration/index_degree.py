LONG_DICT_PATTERNS = [
        [1, 1],
        [1, 1, 2],
        [2, 2, 2],
        [1, 1, 2, 2],
        [1, 1, 1, 3],
        [1, 2, 2, 3],
        [2, 2, 2, 2],
        [2, 2, 3, 3],
        [3, 3, 3, 3],
        [1, 1, 2, 2, 2],
        [1, 1, 1, 1, 4],
        [1, 1, 1, 2, 3],
        [1, 2, 2, 2, 3],
        [1, 1, 2, 3, 3],
        [1, 1, 2, 2, 4],
        [2, 2, 2, 2, 2],
        [1, 2, 2, 2, 3],
        [1, 2, 3, 3, 3],
        [1, 2, 2, 3, 4],
        [2, 2, 2, 2, 4],
        [2, 2, 2, 3, 3],
        [2, 2, 2, 3, 3],
        [1, 3, 3, 3, 4],
        [2, 2, 3, 3, 4],
        [2, 2, 2, 4, 4],
        [2, 3, 3, 3, 3],
        [3, 3, 3, 3, 4],
        [2, 3, 3, 4, 4],
        [3, 3, 4, 4, 4],
        [4, 4, 4, 4, 4]
    ]

DICT_PATTERNS,i = {}, 1
for pattern in LONG_DICT_PATTERNS:
    id_pat = 0
    for deg in pattern:
        id_pat += 1 << (deg * 4)
    if i in [13, 17]:
        DICT_PATTERNS[id_pat] = (1, 2, (13,17))
    elif i in [21, 22]:
        DICT_PATTERNS[id_pat] = (3, 3, (21,22))
    else:
        DICT_PATTERNS[id_pat] = i
    i += 1
    
DICT_POSITIONS = [
    {1 : 1}, #1
    {1 : 2, 2 : 3}, #2
    {2 : 4}, #3
    {1 : 5, 2: 6}, #4
    {1 : 7, 3 : 8}, #5
    {1 : 9, 2 : 10, 3 : 11}, #6
    {2 : 12},#7
    {2 : 13, 3 : 14},#8
    {3 : 15},#9
    {1 : 16, 2 : (1,(17,18))},#10
    {1 : 19, 4 : 20},#11
    {1 : (2,(21,22)), 2 : 23, 3 : 24},#12
    {1 : 25, 2 : (1,(26,27)), 3 : 28},#13
    {1 : 29, 2 : 30, 3 : 31},#14
    {1 : 32, 2 : 33, 4 : 34},#15
    {2 : 35},#16
    {1 : 36, 2 : (3,(38,37)), 3 : 39},#17
    {1 : 40, 2 : 41, 3 : (1,(42,43))},#18
    {1 : 44, 2 : 45, 3 : 46, 4 : 47},#19
    {2 : 48, 4 : 49},#20
    {2 : (2,(50, 51)), 3 : 52},#21
    {2 : 53, 3 : 54},#22
    {1 : 55, 3 : 56, 4 : 57},#23
    {2 : 58, 3 : 59, 4 : 60},#24
    {2 : 61, 4 : 62},#25
    {2 : 63, 3 : (2,(64,65))},#26
    {3 : 66, 4 : 67},#27
    {2 : 68, 3 : 69, 4 : 70},#28
    {3 : 71, 4 : 72},#29
    {4 : 73}#30
]
                
def disambiguate_pattern(graph_sub, new_pattern):
    for v in graph_sub.vs:
        if v.degree() == new_pattern[0]:
            for n in v.neighbors():
                if n.degree() == new_pattern[1]:
                    return new_pattern[2][0]
    return new_pattern[2][1]

def disambiguate_position(graph_sub, v, new_position):
    for n in v.neighbors():
        if n.degree() == new_position[0]:
            return new_position[1][0]
    return new_position[1][1]
    
def degree_distribution(graph):
    result = 0
    for v in graph.vs:
        result += 1 << (4 * v.degree())
    return result

def index_pattern(graph_sub, pt, ps):
    try:
        new_pattern = DICT_PATTERNS[degree_distribution(graph_sub)]
    except:
        print graph_sub
        print DICT_PATTERNS
    if type(new_pattern) != int :
        new_pattern = disambiguate_pattern(graph_sub, new_pattern)
    pt[new_pattern - 1] += 1
    new_positions = DICT_POSITIONS[new_pattern - 1]
    if new_pattern in [10, 12, 13, 17, 18, 21, 26] :
        for v in graph_sub.vs:
            new_position = new_positions[v.degree()]
            if type(new_position) != int:
                new_position = disambiguate_position(graph_sub, v, new_positions[v.degree()])
            ps[v['id_principal']][new_position - 1] += 1
    else:
        for v in graph_sub.vs:
            ps[v['id_principal']][new_positions[v.degree()] - 1] += 1