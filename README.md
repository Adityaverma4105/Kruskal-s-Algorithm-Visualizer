# Kruskal-s-Algorithm-Visualizer
Algorithm (Kruskal’s Algorithm)
Step-by-Step Algorithm:
1.	Sort all edges in non-decreasing order of their weight.
2.	Initialize an empty set MST to store the edges of the minimum spanning tree.
3.	For each edge in the sorted list:
o	If including the edge does not form a cycle, include it in the MST.
o	Else, skip it.
4.	Repeat until V - 1 edges are added to the MST.
5.	Output the edges in the MST and their total weight.
________________________________________
5. Pseudocode
KRUSKAL(G):
    A = ∅
    sort edges of G in increasing order by weight
    for each edge (u, v) in sorted edges:
        if u and v are in different sets:
            add (u, v) to A
            union(u, v)
    return A
