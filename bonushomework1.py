import heapq
import math
import sys


def read_case(filename):

    with open(filename, "r") as file:
        numbers = list(map(int, file.read().split()))

    if len(numbers) < 2:
        raise ValueError("The input file is missing the target or item count.")

    target = numbers[0]
    number_of_items = numbers[1]

    expected_numbers = 2 + 2 * number_of_items

    if len(numbers) != expected_numbers:
        raise ValueError(
            f"Expected {number_of_items} items, but the file contains "
            f"{(len(numbers) - 2) // 2} item pairs."
        )

    values = []
    costs = []

    position = 2

    for _ in range(number_of_items):
        values.append(numbers[position])
        costs.append(numbers[position + 1])
        position += 2

    return values, costs, target


def state_id(item_index, current_value, target):
    return item_index * (target + 1) + current_value


def decode_state(vertex, target):
    return divmod(vertex, target + 1)


def minimum_cost_subset(values, costs, target):
    number_of_items = len(values)
    values_per_layer = target + 1

    number_of_vertices = (number_of_items + 1) * values_per_layer

    source = state_id(0, 0, target)
    destination = state_id(number_of_items, target, target)

    distances = [math.inf] * number_of_vertices
    previous = [None] * number_of_vertices

    distances[source] = 0

    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance != distances[current_vertex]:
            continue

        if current_vertex == destination:
            break

        item_index, current_value = decode_state(
            current_vertex,
            target
        )

        if item_index == number_of_items:
            continue

        next_item_index = item_index + 1

        skipped_vertex = state_id(
            next_item_index,
            current_value,
            target
        )

        if current_distance < distances[skipped_vertex]:
            distances[skipped_vertex] = current_distance

            previous[skipped_vertex] = (
                current_vertex,
                False
            )

            heapq.heappush(
                priority_queue,
                (current_distance, skipped_vertex)
            )

        new_value = min(
            target,
            current_value + values[item_index]
        )

        chosen_vertex = state_id(
            next_item_index,
            new_value,
            target
        )

        new_distance = current_distance + costs[item_index]

        if new_distance < distances[chosen_vertex]:
            distances[chosen_vertex] = new_distance

            previous[chosen_vertex] = (
                current_vertex,
                True
            )

            heapq.heappush(
                priority_queue,
                (new_distance, chosen_vertex)
            )

    if distances[destination] == math.inf:
        return None

    selected_items = []
    current_vertex = destination

    while current_vertex != source:
        previous_information = previous[current_vertex]

        if previous_information is None:
            raise RuntimeError("Could not reconstruct the shortest path.")

        previous_vertex, item_was_selected = previous_information

        current_layer, _ = decode_state(
            current_vertex,
            target
        )

        if item_was_selected:
            selected_items.append(current_layer)

        current_vertex = previous_vertex

    selected_items.reverse()

    total_value = sum(
        values[item_number - 1]
        for item_number in selected_items
    )

    total_cost = sum(
        costs[item_number - 1]
        for item_number in selected_items
    )

    return selected_items, total_value, total_cost


def print_result(values, costs, target):
    result = minimum_cost_subset(values, costs, target)

    if result is None:
        print("No subset reaches the target value.")
        return

    selected_items, total_value, total_cost = result

    print(f"Target value: {target}")
    print(f"Selected items: {selected_items}")
    print()

    print("Item details:")

    for item_number in selected_items:
        index = item_number - 1

        print(
            f"  Item {item_number}: "
            f"value = {values[index]}, "
            f"cost = {costs[index]}"
        )

    print()
    print(f"Total value: {total_value}")
    print(f"Total cost: {total_cost}")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} input_file.txt")
        return

    filename = sys.argv[1]

    try:
        values, costs, target = read_case(filename)
        print_result(values, costs, target)
    except (OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()