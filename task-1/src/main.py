"""Runner for the logistics max-flow model.

This script builds the graph, runs Edmonds-Karp with verbose step-by-step
output, and prints a concise report plus a CSV-friendly table of flows on each
original edge.
"""
from edmonds_karp import build_logistics_graph, edmonds_karp, min_cut_from_residual


def pretty_print_flow(edges, flow):
    print("\nFinal flows on original edges:")
    print(f"{'From':<6} {'To':<6} {'Cap':>5} {'Flow':>6}")
    print('-' * 30)
    for u, v, c in edges:
        f = flow.get(u, {}).get(v, 0)
        print(f"{u:<6} {v:<6} {c:5d} {f:6d}")


if __name__ == '__main__':
    nodes, edges = build_logistics_graph()
    SRC = 'SRC'
    SNK = 'SNK'
    augmented_nodes = nodes + [SRC, SNK]

    aug_edges = edges.copy()
    aug_edges += [(SRC, 'T1', 25 + 20 + 15), (SRC, 'T2', 15 + 30 + 10)]
    for i in range(1, 15):
        incoming = sum(c for (u, v, c) in edges if v == f"S{i}")
        aug_edges.append((f"S{i}", SNK, incoming))

    print("Running Edmonds-Karp on the logistics network (verbose steps)\n")
    maxf, flow, history = edmonds_karp(augmented_nodes, aug_edges, SRC, SNK, verbose=True)
    print('\n' + '='*60)
    print(f"RESULT: maximum flow from terminals to shops = {maxf} units")


    residual = history[-1]['residual_snapshot']
    S, T, cut_edges, cut_cap = min_cut_from_residual(augmented_nodes, aug_edges, SRC, residual)
    print(f"Min-cut capacity = {cut_cap} (should equal max flow)")
    print(f"S-side (reachable from SRC): {sorted(list(S))}")
    print(f"T-side (non-reachable): {sorted(list(T))}\n")
    pretty_print_flow(edges, flow)
    print('\nEdges in min-cut:')
    for u, v, c in cut_edges:
        print(f"  {u} -> {v} (cap={c})")
