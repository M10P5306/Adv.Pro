test_cases = int(input())
mazes = []
nodes_in_mazes = []
number_of_nodes_in_maze = []
for i in range(test_cases):
    maze = []
    rows = int(input().split()[1])
    start = ()
    aliens = []
    for r in range(rows):
        input_row = input()
        if 'S' in input_row:
            start = (r, input_row.index('S'))
        if 'A' in input_row:
            for char_index, char in enumerate(input_row):
                if char == 'A':
                    aliens.append((r, char_index))
        maze.append(input_row)
    mazes.append(maze)
    nodes_found = [start]
    for alien in aliens:
        nodes_found.append(alien)
    nodes_in_mazes.append(nodes_found)
    number_of_nodes_in_maze.append(len(nodes_found))

offsets = [[-1, 0], [0, -1], [1, 0], [0, 1]]
w_and_d_for_mazes = []


def bfs(origin, maze_nbr, alien_nodes):
    queue = [(origin[0], origin[1])]
    weight_and_distance = []
    visited_nodes = [(origin[0], origin[1])]
    in_queue = len(queue)
    weight = 1
    alien_counter = 0

    while not len(queue) == 0:
        current_square = queue.pop(0)
        for off in offsets:
            i = current_square[0] + off[0]
            j = current_square[1] + off[1]
            square = mazes[maze_nbr][i][j]
            if square != '#' and (i, j) not in visited_nodes:
                queue.append((i, j))
                visited_nodes.append((i, j))
                if (i, j) in alien_nodes:
                    weight_and_distance.append((weight, nodes_in_mazes[maze_nbr].index((origin[0], origin[1])),
                                                nodes_in_mazes[maze_nbr].index((i, j))))
                    alien_counter += 1
                    if alien_counter == number_of_nodes_in_maze[maze_nbr] - 1:
                        return weight_and_distance
        in_queue -= 1
        if in_queue == 0:
            weight += 1
            in_queue = len(queue)
    return weight_and_distance


for i in range(len(nodes_in_mazes)):
    alien_nodes = nodes_in_mazes[i].copy()
    alien_nodes.pop(0)
    maze_w_and_d = []
    for tupp in bfs(nodes_in_mazes[i][0], i, alien_nodes):
        maze_w_and_d.append(tupp)
    aliens_to_be_found = len(alien_nodes)
    while len(alien_nodes) != 0:
        for tupp in bfs(alien_nodes.pop(0), i, alien_nodes):
            maze_w_and_d.append(tupp)
    maze_w_and_d.sort()
    w_and_d_for_mazes.append(maze_w_and_d)


def find(p, i_find):
    if p[i_find] != i_find:
        p[i_find] = find(p, p[i_find])
    return p[i_find]


def union(p, ra, x, y):
    if ra[x] < ra[y]:
        p[x] = y
    elif ra[x] > ra[y]:
        p[y] = x
    else:
        p[y] = x
        ra[x] += 1


def kruskal(nodes, length):
    result = []
    ind = 0
    e = 0

    p = []
    rank = []
    minimum = 0

    for node in range(number_of_nodes_in_maze[length]):
        p.append(node)
        rank.append(0)

    while e < len(p) - 1:

        w, u, v = nodes[ind]
        ind = ind + 1
        x = find(p, u)
        y = find(p, v)

        if x != y:
            e = e + 1
            result.append([w, u, v])
            union(p, rank, x, y)
            minimum += w

    print(minimum)


for index, m in enumerate(w_and_d_for_mazes):
    kruskal(m, index)