import heapq

class Node:
    def __init__(self, city, cost, parent=None):
        self.city = city
        self.cost = cost  # Total distance from start
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost  # Priority based on total distance

def astar_search(graph, start_city, goal_city):
    open_set = []  # Priority queue of nodes to explore
    closed_set = set()  # Set of visited cities
    start_node = Node(start_city, 0)

    heapq.heappush(open_set, start_node)
    while open_set:
        current_node = heapq.heappop(open_set)
        if current_node.city == goal_city:
            path = []
            while current_node:  # Reconstruct path from goal to start
                path.append(current_node.city)
                current_node = current_node.parent
            return path[::-1]  # Reverse path for start to goal order

        closed_set.add(current_node.city)
        for neighbor, distance in graph[current_node.city].items():
            if neighbor in closed_set:
                continue
            new_cost = current_node.cost + distance
            new_node = Node(neighbor, new_cost, current_node)
            heapq.heappush(open_set, new_node)  # Add neighbor with updated cost

    return None  # No path found

# Romania map data
romania_map = {
    'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Pitesti': 97, 'Craiova': 146},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# Example usage
start_city = 'Arad'
goal_city = 'Bucharest'

print("A* Search Algorithm")
print(f'Source {start_city}: Destination: {goal_city}')
path = astar_search(romania_map, start_city, goal_city)
if path:
    print("Optimal Path found:", path)
else:
    print("No path found")
