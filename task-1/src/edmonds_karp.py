"""Edmonds-Karp implementation with detailed step-by-step debugging output.

Graph nodes are arbitrary hashable labels (strings). The implementation supports
multiple sources/sinks by using an auxiliary super-source/super-sink when
requested by the caller (these are not part of the user's 20-node model — they
are virtual and used only for computation).

Functions:
- edmonds_karp(graph, source, sink, verbose=False): returns (max_flow, flow_dict, history)
- build_logistics_graph(): builds the specific 20-node logistics graph from the task
- min_cut_from_residual(residual_graph, source): returns (S_set, T_set, cut_edges)

The implementation intentionally prints each augmenting path, its bottleneck
and cumulative flow when `verbose=True` to satisfy the step-by-step requirement.
"""
from collections import deque, defaultdict
from typing import Dict, Tuple, List, Any

def _bfs_capacity(parent, capacity, adj, source, sink):
    for k in parent:
        parent[k] = None
    q = deque([source])
    parent[source] = source
    while q:
        u = q.popleft()
        for v in adj[u]:
            if parent[v] is None and capacity[u][v] > 0:
                parent[v] = u
                if v == sink:
                    return True
                q.append(v)
    return False


def edmonds_karp(nodes: List[Any], edges: List[Tuple[Any, Any, int]], source, sink, verbose: bool = False):
    """Compute max flow with Edmonds-Karp.

    nodes: list of node labels
    edges: list of (u, v, cap)
    source, sink: node labels in the (possibly augmented) graph

    Returns: (max_flow, flow, history)
      - flow: dict-of-dict with flow[u][v]
      - history: list of dicts describing each augmentation (path, path_flow, cumulative)
    """
    adj = {n: set() for n in nodes}
    capacity = {u: defaultdict(int) for u in nodes}
    for u, v, c in edges:
        adj[u].add(v)
        adj[v].add(u) 
        capacity[u][v] += c
        capacity[v][u] += 0

    parent = {n: None for n in nodes}
    max_flow = 0
    flow = {u: defaultdict(int) for u in nodes}
    history = []

    step = 0
    while _bfs_capacity(parent, capacity, adj, source, sink):
        path = []
        v = sink
        bottleneck = float('inf')
        while v != source:
            u = parent[v]
            path.append((u, v))
            bottleneck = min(bottleneck, capacity[u][v])
            v = u
        path.reverse()

        step += 1
        for u, v in path:
            capacity[u][v] -= bottleneck
            capacity[v][u] += bottleneck
            flow[u][v] += bottleneck
            flow[v][u] -= bottleneck
        max_flow += bottleneck
        history.append({'step': step, 'path': [u for u, _ in path] + [sink], 'path_edges': path, 'bottleneck': bottleneck, 'cumulative_flow': max_flow, 'residual_snapshot': {u: dict(capacity[u]) for u in nodes}})

        if verbose:
            print(f"Step {step}: found augmenting path: {[n for n in history[-1]['path']]} \n  bottleneck = {bottleneck}\n  cumulative max flow = {max_flow}\n")

    return max_flow, flow, history


def min_cut_from_residual(nodes: List[Any], edges: List[Tuple[Any, Any, int]], source, residual_capacity: Dict[Any, Dict[Any, int]]):
    """Given residual capacities (after max-flow), return S and T sets and the cut edges.

    residual_capacity should be a mapping residual_capacity[u][v] -> remaining cap
    """
    visited = set()
    q = deque([source])
    while q:
        u = q.popleft()
        if u in visited:
            continue
        visited.add(u)
        for v in residual_capacity[u]:
            if residual_capacity[u][v] > 0 and v not in visited:
                q.append(v)
    S = visited
    T = set(nodes) - S
    cut_edges = []
    cap_sum = 0
    original_caps = {(u, v): c for (u, v, c) in edges}
    for u in S:
        for v in T:
            if (u, v) in original_caps:
                cut_edges.append((u, v, original_caps[(u, v)]))
                cap_sum += original_caps[(u, v)]
    return S, T, cut_edges, cap_sum


def build_logistics_graph():
    """Constructs the 20-node logistics graph as specified in the assignment.

    Node naming:
      - Terminals: T1, T2
      - Warehouses: W1..W4 ("Склад 1..4")
      - Shops: S1..S14 ("Магазин 1..14")

    Returns (nodes, edges) where edges is list of (u, v, cap).
    """
    nodes = []
    nodes += [f"T{i}" for i in (1, 2)]
    nodes += [f"W{i}" for i in range(1, 5)]
    nodes += [f"S{i}" for i in range(1, 15)]

    edges = [
        ("T1", "W1", 25),
        ("T1", "W2", 20),
        ("T1", "W3", 15),
        ("T2", "W3", 15),
        ("T2", "W4", 30),
        ("T2", "W2", 10),

        ("W1", "S1", 15),
        ("W1", "S2", 10),
        ("W1", "S3", 20),

        ("W2", "S4", 15),
        ("W2", "S5", 10),
        ("W2", "S6", 25),

        ("W3", "S7", 20),
        ("W3", "S8", 15),
        ("W3", "S9", 10),

        ("W4", "S10", 20),
        ("W4", "S11", 10),
        ("W4", "S12", 15),
        ("W4", "S13", 5),
        ("W4", "S14", 10),
    ]
    return nodes, edges


if __name__ == "__main__":
    nodes, edges = build_logistics_graph()

    SRC = "SRC"
    SNK = "SNK"
    augmented_nodes = nodes + [SRC, SNK]
    total_cap = sum(c for _, _, c in edges)
    aug_edges = edges.copy()

    aug_edges += [(SRC, "T1", 25 + 20 + 15), (SRC, "T2", 15 + 30 + 10)]

    for i in range(1, 15):
        incoming = sum(c for (u, v, c) in edges if v == f"S{i}")
        aug_edges.append((f"S{i}", SNK, incoming))

    maxf, flow, history = edmonds_karp(augmented_nodes, aug_edges, SRC, SNK, verbose=True)
    print(f"\nComputed max flow = {maxf}")

    residual = history[-1]['residual_snapshot'] if history else {n: {} for n in augmented_nodes}
    S, T, cut_edges, cut_cap = min_cut_from_residual(augmented_nodes, aug_edges, SRC, residual)
    print(f"Min cut capacity = {cut_cap}; edges in cut: {cut_edges}")
