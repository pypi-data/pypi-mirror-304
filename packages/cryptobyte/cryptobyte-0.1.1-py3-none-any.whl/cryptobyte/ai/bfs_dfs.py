graph = {
    'A': set(['B', 'C']),
    'B': set(['A', 'D', 'E']),
    'C': set(['A', 'F']),
    'D': set(['B']),
    'E': set(['B', 'F']),
    'F': set(['C', 'E'])
}


def bfs(graph, start, goal, visited=None):
    if visited is None:
        visited = set()
    if start == goal:
        return [goal]
    for neighbors in graph[start]:
        if neighbors not in visited:
            visited.add(neighbors)
            path = bfs(graph, neighbors, goal, visited)
            if path:
                return [start] + path
    return None


start_node = 'A'
goal_node = 'F'
print(bfs(graph, start_node, goal_node))

# Depth-First Search


def dfs(graph, node, visited=None):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n, visited)
    return visited


print("Depth-First search")
n = dfs(graph, 'A', [])
print(n)
