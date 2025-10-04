import uuid
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color: str = "#EEEEEE"):
        self.left= None
        self.right= None
        self.val= key
        self.color= color
        self.id= str(uuid.uuid4())


def heap_to_tree(heap):
    if not heap:
        return None
    nodes = [Node(v) for v in heap]
    n = len(nodes)
    for i in range(n):
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n:
            nodes[i].left = nodes[l]
        if r < n:
            nodes[i].right = nodes[r]
    return nodes[0]


def traverse_bfs(root):
    if root is None:
        return []
    order = []
    q = deque([root])
    while q:
        n = q.popleft()
        order.append(n)
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)
    return order


def traverse_dfs(root):
    order = []
    if root is None:
        return order

    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


def collect_nodes(root):
    mapping = {}

    def _rec(n):
        if n is None:
            return
        mapping[n.id] = n
        _rec(n.left)
        _rec(n.right)

    _rec(root)
    return mapping


def hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)


def generate_palette(n, start_hex, end_hex):
    if n <= 0:
        return []
    s = hex_to_rgb(start_hex)
    e = hex_to_rgb(end_hex)
    pal = []
    for i in range(n):
        t = i / max(n - 1, 1)
        rgb = (int(s[0] + (e[0] - s[0]) * t), int(s[1] + (e[1] - s[1]) * t), int(s[2] + (e[2] - s[2]) * t))
        pal.append(rgb_to_hex(rgb))
    return pal


def add_edges(graph, node, pos, x=0.0, y=0.0, layer=1):
    if node is None:
        return graph
    graph.add_node(node.id, color=node.color, label=str(node.val))
    if node.left:
        graph.add_edge(node.id, node.left.id)
        l = x - 1 / (2 ** layer)
        pos[node.left.id] = (l, y - 1)
        add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
    if node.right:
        graph.add_edge(node.id, node.right.id)
        r = x + 1 / (2 ** layer)
        pos[node.right.id] = (r, y - 1)
        add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def build_graph_and_pos(root):
    G = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    add_edges(G, root, pos)
    return G, pos


def draw_tree(root):
    G, pos = build_graph_and_pos(root)
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in G.nodes(data=True)}
    plt.figure(figsize=(8, 5))
    nx.draw(G, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def draw_all_trees(root, bfs_order, dfs_order, start_hex='#0B3D91', end_hex='#D6E8FF'):
    G, pos = build_graph_and_pos(root)
    node_ids = list(G.nodes())
    labels = {node[0]: node[1]['label'] for node in G.nodes(data=True)}

    orig_colors = ['#EEEEEE' for _ in node_ids]

    # BFS палітра та кольори
    pal_bfs = generate_palette(len(bfs_order), start_hex=start_hex, end_hex=end_hex)
    id_to_color_bfs = {nid: '#EEEEEE' for nid in node_ids}
    for idx, n in enumerate(bfs_order):
        id_to_color_bfs[n.id] = pal_bfs[idx]
    bfs_colors = [id_to_color_bfs[nid] for nid in node_ids]

    # DFS палітра та кольори
    pal_dfs = generate_palette(len(dfs_order), start_hex=start_hex, end_hex=end_hex)
    id_to_color_dfs = {nid: '#EEEEEE' for nid in node_ids}
    for idx, n in enumerate(dfs_order):
        id_to_color_dfs[n.id] = pal_dfs[idx]
    dfs_colors = [id_to_color_dfs[nid] for nid in node_ids]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    # Original
    ax = axes[0]
    nx.draw(G, pos=pos, labels=labels, arrows=False, node_size=1800, node_color=orig_colors, font_weight='bold', ax=ax)
    ax.set_title('Original tree')

    # BFS
    ax = axes[1]
    nx.draw(G, pos=pos, labels=labels, arrows=False, node_size=1800, node_color=bfs_colors, font_weight='bold', ax=ax)
    ax.set_title('BFS final colors')

    # DFS
    ax = axes[2]
    nx.draw(G, pos=pos, labels=labels, arrows=False, node_size=1800, node_color=dfs_colors, font_weight='bold', ax=ax)
    ax.set_title('DFS final colors')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    heap = [1, 3, 5, 7, 9, 11, 13]
    root = heap_to_tree(heap)
    if root:
        bfs_order = traverse_bfs(root)
        dfs_order = traverse_dfs(root)
        draw_all_trees(root, bfs_order, dfs_order, start_hex='#0B3D91', end_hex='#D6E8FF')
