import sys

digit = int(sys.argv[1])

for i in range (digit,0,-1):
    empty = ' '*(i-1)
    tree = '#'*(digit+1-i)
    print('{}{}'.format(empty, tree))