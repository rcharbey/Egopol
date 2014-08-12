from igraph import *

PATTERNS = [
    [
        Graph.Full(1) #0  
    ],
    [
        Graph.Full(2),#1
    ],
    [
        Graph.Star(3),#2
        Graph.Full(3),#3
    ],
    [
        Graph.Formula("0-1,1-2,2-3"),#4
        Graph.Star(4),#5
        Graph.Formula("0-1,0-2,1-2,2-3"),#6
        Graph.Formula("0-1,0-2,1-3,2-3"),#7
        Graph.Formula("0-1,0-2,1-2,1-3,2-3"),#8
        Graph.Full(4),#9
    ],
    [
        Graph.Formula("0-1,1-2,2-3,3-4"),#10
        Graph.Star(5),#11
        Graph.Formula("0-1,0-2,0-3,3-4"),#12
        Graph.Formula("0-1,0-2,1-2,2-3,3-4"),#13
        Graph.Formula("0-1,1-2,1-3,2-3,3-4"),#14
        Graph.Formula("0-1,0-2,1-2,2-3,2-4"),#15
        Graph.Formula("0-1,1-2,2-3,3-4,4-0"),#16
        Graph.Formula("0-1,1-2,2-3,3-4,4-1"),#17
        Graph.Formula("0-1,0-2,0-3,1-2,2-3,3-4"),#18
        Graph.Formula("0-1,1-2,1-3,1-4,2-3,3-4"),#19
        Graph.Formula("0-1,0-2,1-2,2-3,2-4,3-4"),#20
        Graph.Formula("0-1,0-2,1-3,2-3,2-4,3-4"),#21
        Graph.Formula("0-1,0-2,1-3,1-4,2-3,2-4"),#22
        Graph.Formula("0-1,0-2,0-3,1-2,1-3,2-3,3-4"),#23
        Graph.Formula("0-1,0-2,1-2,1-3,2-3,2-4,3-4"),#24
        Graph.Formula("0-1,0-2,0-3,0-4,1-2,2-3,2-4"),#25
        Graph.Formula("0-1,0-2,0-3,1-2,1-4,2-3,3-4"),#26
        Graph.Formula("0-1,0-2,0-3,1-2,1-4,2-3,2-4,3-4"),#27
        Graph.Formula("0-1,0-2,0-3,1-2,1-3,1-4,2-3,3-4"),#28
        Graph.Formula("0-1,0-2,0-3,1-2,1-3,1-4,2-3,2-4,3-4"),#29
        Graph.Full(5)
    ]
]    