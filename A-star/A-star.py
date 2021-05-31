import pygame
import numpy as np

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption("A* Algorithm")
win = pygame.display.set_mode([800, 700])
font = pygame.font.Font('freesansbold.ttf', 32)
exit = False

grid = [[0 for j in range(39)] for i in range(34)]
x = []
y = []

for i in range(10, 800, 20):
    x.append(i)
for i in range(10, 700, 20):
    y.append(i)

mx = 0
my = 0
success = False
s = [-1, -1]
e = [-1, -1]
w = []
w_s = [-1, -1]
w_e = [-1, -1]
nxt = 0
pos = []
stop = False
way = []


def optimal_node(n):
    f = 2*((abs(s[0]-e[0]) + abs(s[1]-e[1])))
    node = []
    for i in n:
        if ((i.g+i.h) < f):
            node = i
            f = i.g+i.h

    return node


def neighbours(n):

    nodes = []
    skipx = False
    skipy = False
    if n[0] < 1:
        skipx = True
    if n[1] < 1:
        skipy = True

    if (not skipx) and (not skipy):
        try:
            d = grid[n[0]-1][n[1]-1]
            if d != -1:
                nodes.append([n[0]-1, n[1]-1])
        except IndexError:
            pass

    if not skipx:
        try:
            d = grid[n[0]-1][n[1]]
            if d != -1:
                nodes.append([n[0]-1, n[1]])
        except IndexError:
            pass
        try:
            d = grid[n[0]-1][n[1]+1]
            if d != -1:
                nodes.append([n[0]-1, n[1]+1])
        except IndexError:
            pass

    if not skipy:
        try:
            d = grid[n[0]][n[1]-1]
            if d != -1:
                nodes.append([n[0], n[1]-1])
        except IndexError:
            pass

    try:
        d = grid[n[0]][n[1]+1]
        if d != -1:
            nodes.append([n[0], n[1]+1])
    except IndexError:
        pass

    try:
        d = grid[n[0]+1][n[1]]
        if d != -1:
            nodes.append([n[0]+1, n[1]])
    except IndexError:
        pass

    if not skipy:
        try:
            d = grid[n[0]+1][n[1]-1]
            if d != -1:
                nodes.append([n[0]+1, n[1]-1])
        except IndexError:
            pass

    try:
        d = grid[n[0]+1][n[1]+1]
        if d != -1:
            nodes.append([n[0]+1, n[1]+1])
    except IndexError:
        pass

    return nodes


class Node:

    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    # def __eq__(self, other):
    # 	return self.position == other.position


def path(current_node):

    p = []
    r, c = np.shape(grid)

    result = [[-1 for j in range(c)] for i in range(r)]
    current = current_node

    while current is not None:
        p.append(current.position)
        current = current.parent

    p = p[::-1]

    return p


def Astar():

    global win
    # max_iteration = (len(grid[0]) * len(grid) // 2)**5

    # infinite = 0

    open_list = []      # YET TO VISIT
    closed_list = []    # VISITED
    inf = 0
    start_Node = Node(parent=None, position=s)
    end_Node = Node(parent=None, position=e)

    open_list.append(start_Node)

    while len(open_list) != 0:

        current_node = optimal_node(open_list)
        open_list.pop(open_list.index(current_node))
        closed_list.append(current_node)
        # inf+=1
        # print(inf)
        for i in closed_list:
            pygame.draw.rect(win, (51, 255, 154),
                             (x[i.position[1]]+1, y[i.position[0]]+1, 19, 19))
        pygame.display.update()

        if current_node.position == end_Node.position:
            p = path(current_node)
            return True, p

        neigh = neighbours(current_node.position)

        successors = []

        for n in neigh:

            new_node = Node(parent=current_node, position=n)
            successors.append(new_node)

        for successor in successors:

            if len([visited for visited in closed_list if visited.position == successor.position]) > 0:
                continue

            successor.g = current_node.g+1
            successor.h = abs(successor.position[0]-end_Node.position[0])+abs(
                successor.position[1]-end_Node.position[1])
            successor.f = successor.g+successor.h

            if len([visited for visited in open_list if visited.position == successor.position and successor.g > visited.g]) > 0:
                continue

            open_list.append(successor)

    return False, None


success = False


while not exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit = True

        if event.type == pygame.MOUSEBUTTONDOWN and nxt != 2:
            mx, my = pygame.mouse.get_pos()

            if nxt == 0:

                grid[s[1]][s[0]] = 0
                temp = s[:]
                for i in range(1, len(x)):
                    if mx > x[i-1] and mx < x[i]:
                        s[1] = i-1
                        break
                for i in range(1, len(y)):
                    if my > y[i-1] and my < y[i]:
                        s[0] = i-1
                        break

                if s == e and s != [-1, -1]:
                    s = temp[:]
                grid[s[0]][s[1]] = 1

            elif nxt == 1:

                temp = e[:]
                grid[e[0]][e[1]] = 0

                for i in range(1, len(x)):
                    if mx > x[i-1] and mx < x[i]:
                        e[1] = i-1
                        break
                for i in range(1, len(y)):
                    if my > y[i-1] and my < y[i]:
                        e[0] = i-1
                        break

                if e == s:
                    e = temp[:]
                grid[e[0]][e[1]] = 2

        if event.type == pygame.MOUSEBUTTONUP and nxt == 2:
            for [mx, my] in pos:
                t = [-1, -1]
                for i in range(1, len(x)):
                    if mx > x[i-1] and mx < x[i]:
                        t[1] = i-1
                        break
                for i in range(1, len(y)):
                    if my > y[i-1] and my < y[i]:
                        t[0] = i-1
                        break

                if t != [-1, -1] and t != s and t != e:
                    w.append(t)
                    grid[t[0]][t[1]] = -1

            pos = []

        if event.type == pygame.MOUSEMOTION and nxt == 2:
            if event.buttons[0] == 1:
                mx, my = pygame.mouse.get_pos()
                pos.append([mx, my])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                nxt += 1
            if event.key == pygame.K_LEFT and nxt > 0:
                nxt -= 1
            if event.key == pygame.K_0 and nxt == 2:
                for i in w:
                    grid[i[0]][i[1]] = 0
                w = []

    if exit:
        break

    win.fill((239, 248, 250))

    for i in range(10, 800, 20):
        pygame.draw.line(win, (0, 0, 0), (i, 10), (i, 690), 2)

    for i in range(10, 700, 20):
        pygame.draw.line(win, (0, 0, 0), (10, i), (790, i), 2)

    if s != [-1, -1]:
        pygame.draw.rect(win, (34, 139, 34), (x[s[1]]+4, y[s[0]]+4, 14, 14))
    if e != [-1, -1]:
        pygame.draw.rect(win, (229, 0, 61), (x[e[1]]+4, y[e[0]]+4, 14, 14))

    for i in w:
        if x[i[1]] < 790 and y[i[0]] < 690:
            pygame.draw.rect(win, (18, 142, 230),
                             (x[i[1]]+1, y[i[0]]+1, 19, 19))

    if nxt == 3 and not stop:
        stop = True
        print("Searching.....")

        success, way = Astar()
        if success:
            print("Found Solution!!")
            tracking = True
        if not success:
            print("Destination is Unreachable")
            way = []
            cl = []

    for i in way:
        pygame.draw.rect(win, (254, 0, 79), (x[i[1]]+1, y[i[0]]+1, 19, 19))

    pygame.display.update()
