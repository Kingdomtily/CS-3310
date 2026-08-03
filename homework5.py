from array import array
from heapq import nlargest
import sys


def build_graphs(filename, number_of_vertices):
    outgoing_count = array("I", [0]) * (number_of_vertices + 1)
    incoming_count = array("I", [0]) * (number_of_vertices + 1)

    # First pass: count outgoing and incoming edges for each vertex.
    with open(filename, "r", buffering=1024 * 1024) as file:
        for line in file:
            tail_string, head_string = line.split()
            tail = int(tail_string)
            head = int(head_string)
            outgoing_count[tail] += 1
            incoming_count[head] += 1

    # start[v] gives the starting position of vertex v's neighbors.
    outgoing_start = array("I", [0]) * (number_of_vertices + 2)
    incoming_start = array("I", [0]) * (number_of_vertices + 2)

    for vertex in range(1, number_of_vertices + 1):
        outgoing_start[vertex + 1] = (
            outgoing_start[vertex] + outgoing_count[vertex]
        )
        incoming_start[vertex + 1] = (
            incoming_start[vertex] + incoming_count[vertex]
        )

    number_of_edges = outgoing_start[number_of_vertices + 1]
    outgoing_edges = array("I", [0]) * number_of_edges
    incoming_edges = array("I", [0]) * number_of_edges

    # Keep track of the next available position for each vertex.
    outgoing_next = array("I", outgoing_start)
    incoming_next = array("I", incoming_start)

    # Second pass: store the actual edges.
    with open(filename, "r", buffering=1024 * 1024) as file:
        for line in file:
            tail_string, head_string = line.split()
            tail = int(tail_string)
            head = int(head_string)

            position = outgoing_next[tail]
            outgoing_edges[position] = head
            outgoing_next[tail] += 1

            position = incoming_next[head]
            incoming_edges[position] = tail
            incoming_next[head] += 1

    original_graph = (outgoing_start, outgoing_edges)
    reverse_graph = (incoming_start, incoming_edges)

    return original_graph, reverse_graph


def calculate_finishing_order(start, edges, number_of_vertices):
    visited = bytearray(number_of_vertices + 1)
    finishing_order = array("I")

    for starting_vertex in range(number_of_vertices, 0, -1):
        if visited[starting_vertex]:
            continue

        visited[starting_vertex] = 1
        stack_vertices = [starting_vertex]
        stack_positions = [start[starting_vertex]]

        while stack_vertices:
            vertex = stack_vertices[-1]
            position = stack_positions[-1]
            ending_position = start[vertex + 1]

            while (
                position < ending_position
                and visited[edges[position]]
            ):
                position += 1

            if position < ending_position:
                neighbor = edges[position]
                stack_positions[-1] = position + 1
                visited[neighbor] = 1
                stack_vertices.append(neighbor)
                stack_positions.append(start[neighbor])
            else:
                stack_vertices.pop()
                stack_positions.pop()
                finishing_order.append(vertex)

    return finishing_order


def calculate_scc_sizes(
    start,
    edges,
    finishing_order,
    number_of_vertices
):
    visited = bytearray(number_of_vertices + 1)
    component_sizes = []

    for index in range(len(finishing_order) - 1, -1, -1):
        starting_vertex = finishing_order[index]

        if visited[starting_vertex]:
            continue

        visited[starting_vertex] = 1
        stack = [starting_vertex]
        component_size = 0

        while stack:
            vertex = stack.pop()
            component_size += 1

            for position in range(start[vertex], start[vertex + 1]):
                neighbor = edges[position]

                if not visited[neighbor]:
                    visited[neighbor] = 1
                    stack.append(neighbor)

        component_sizes.append(component_size)

    return component_sizes


def kosaraju(filename, number_of_vertices):
    original_graph, reverse_graph = build_graphs(
        filename,
        number_of_vertices
    )

    reverse_start, reverse_edges = reverse_graph

    finishing_order = calculate_finishing_order(
        reverse_start,
        reverse_edges,
        number_of_vertices
    )

    original_start, original_edges = original_graph

    component_sizes = calculate_scc_sizes(
        original_start,
        original_edges,
        finishing_order,
        number_of_vertices
    )

    five_largest = nlargest(5, component_sizes)
    five_largest.extend([0] * (5 - len(five_largest)))

    return five_largest


def main():
    if len(sys.argv) not in (2, 3):
        print(
            f"Usage: {sys.argv[0]} edge_file "
            "[number_of_vertices]"
        )
        sys.exit(1)

    filename = sys.argv[1]

    if len(sys.argv) == 3:
        number_of_vertices = int(sys.argv[2])
    else:
        number_of_vertices = 875714

    five_largest = kosaraju(filename, number_of_vertices)

    print("Five largest SCC sizes:")
    print(",".join(str(size) for size in five_largest))


if __name__ == "__main__":
    main()