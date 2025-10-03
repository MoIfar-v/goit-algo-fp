import heapq


def dijkstra(graph, start):
    """Алгоритм Дейкстри для пошуку найкоротших шляхів від стартової вершини."""
    distances = {vertex: float('inf') for vertex in graph}
    prev = {vertex: None for vertex in graph}
    distances[start] = 0.0

    # heap elements are tuples (distance, vertex)
    heap = [(0.0, start)]

    while heap:
        dist_u, u = heapq.heappop(heap)

        # stale entry check
        if dist_u > distances[u]:
            continue

        for v, w in graph[u].items():
            alt = dist_u + w
            if alt < distances[v]:
                distances[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    return distances, prev


def reconstruct_path(prev, target):
    """Реконструює найкоротший шлях до цільової вершини."""
    path: list[str] = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path


if __name__ == '__main__':

    heap = [1, 3, 5, 7, 9, 11, 13]

    graph = {}
    n = len(heap)
    for i in range(n):
        node = str(i)
        graph[node] = {}

    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2
        for child in (left, right):
            if child < n:
                u = str(i)
                v = str(child)
                w = abs(heap[i] - heap[child])

                graph[u][v] = w
                graph[v][u] = w

    start = '0'   
    target = '6'  

    distances, prev = dijkstra(graph, start)
    print(f'Довжина шляху з вершини {start} (root heap):')
    for node in sorted(distances, key=lambda x: int(x)):
        print(f"  {node}: {distances[node]}")

    path = reconstruct_path(prev, target)
    print(f"Найкоротший шлях {start} -> {target}: {path}")