import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    cost: int
    u: int
    v: int


class UnionFind:
    def __init__(self, number_of_vertices):
        # Vertices are numbered from 1 through number_of_vertices.
        self.parent = list(range(number_of_vertices + 1))
        self.rank = [0] * (number_of_vertices + 1)

    def find(self, vertex):
        # Path compression
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])

        return self.parent[vertex]

    def union(self, first, second):
        root_first = self.find(first)
        root_second = self.find(second)

        # Adding this edge would create a cycle.
        if root_first == root_second:
            return False

        # Union by rank
        if self.rank[root_first] < self.rank[root_second]:
            root_first, root_second = root_second, root_first

        self.parent[root_second] = root_first

        if self.rank[root_first] == self.rank[root_second]:
            self.rank[root_first] += 1

        return True


def read_graph(filename):
    edges = []

    with open(filename, "r") as graph_file:
        first_line = graph_file.readline().split()

        number_of_vertices = int(first_line[0])
        expected_number_of_edges = int(first_line[1])

        for line in graph_file:
            if not line.strip():
                continue

            u, v, cost = map(int, line.split())
            edges.append(Edge(cost, u, v))

    if len(edges) != expected_number_of_edges:
        raise ValueError(
            f"Expected {expected_number_of_edges} edges, "
            f"but read {len(edges)}."
        )

    return number_of_vertices, edges


def kruskal(number_of_vertices, edges):
    union_find = UnionFind(number_of_vertices)

    # Sorting places the lowest-cost edges first.
    edges.sort()

    mst_edges = []
    total_cost = 0

    for edge in edges:
        # Select the edge only when it connects two different components.
        if union_find.union(edge.u, edge.v):
            mst_edges.append(edge)
            total_cost += edge.cost

            # A spanning tree with n vertices contains n - 1 edges.
            if len(mst_edges) == number_of_vertices - 1:
                break

    if len(mst_edges) != number_of_vertices - 1:
        raise ValueError(
            "The graph is disconnected and does not have a spanning tree."
        )

    return total_cost, mst_edges


def main():
    if len(sys.argv) != 2:
        print("Usage: python kruskal_mst.py graph_file.txt")
        return

    filename = sys.argv[1]

    try:
        number_of_vertices, edges = read_graph(filename)
        total_cost, mst_edges = kruskal(number_of_vertices, edges)

        print("Edges selected for the minimum spanning tree:")

        for edge in mst_edges:
            print(edge.u, edge.v, edge.cost)

        print()
        print("Number of MST edges:", len(mst_edges))
        print("Total MST cost:", total_cost)

    except (OSError, ValueError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()