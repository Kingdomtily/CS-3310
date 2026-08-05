import sys
import argparse
from functools import lru_cache


def read_knapsack_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        first_line = file.readline().split()

        if len(first_line) != 2:
            raise ValueError(
                "The first line must contain capacity and item count."
            )

        capacity = int(first_line[0])
        expected_item_count = int(first_line[1])

        items = []

        for line_number, line in enumerate(file, start=2):
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) != 2:
                raise ValueError(
                    f"Invalid data on line {line_number}: {line}"
                )

            value = int(parts[0])
            weight = int(parts[1])

            if value <= 0 or weight <= 0:
                raise ValueError(
                    f"Values and weights must be positive. "
                    f"Error on line {line_number}."
                )

            items.append((value, weight))

    if len(items) != expected_item_count:
        print(
            f"Warning: expected {expected_item_count} items, "
            f"but read {len(items)}."
        )

    return capacity, items


def knapsack_iterative(capacity, items):
    best_value = [0] * (capacity + 1)

    for item_number, (value, weight) in enumerate(items, start=1):

        for current_capacity in range(capacity, weight - 1, -1):

            candidate = (
                best_value[current_capacity - weight] + value
            )

            if candidate > best_value[current_capacity]:
                best_value[current_capacity] = candidate

        if item_number % 100 == 0:
            print(
                f"Processed {item_number} of {len(items)} items."
            )

    return best_value[capacity]


def knapsack_recursive(capacity, items):
    sys.setrecursionlimit(max(10_000, len(items) + 100))

    @lru_cache(maxsize=None)
    def solve(item_index, remaining_capacity):

        if item_index < 0 or remaining_capacity <= 0:
            return 0

        value, weight = items[item_index]

        if weight > remaining_capacity:
            return solve(
                item_index - 1,
                remaining_capacity
            )

        skip_item = solve(
            item_index - 1,
            remaining_capacity
        )

        take_item = value + solve(
            item_index - 1,
            remaining_capacity - weight
        )

        return max(skip_item, take_item)

    optimal_value = solve(
        len(items) - 1,
        capacity
    )

    cache_data = solve.cache_info()

    print("Cached subproblems:", cache_data.currsize)
    print("Cache hits:", cache_data.hits)
    print("Cache misses:", cache_data.misses)

    return optimal_value


def main():
    parser = argparse.ArgumentParser(
        description="Solve a 0/1 knapsack problem."
    )

    parser.add_argument(
        "filename",
        help="Path to the knapsack data file"
    )

    parser.add_argument(
        "--method",
        choices=["iterative", "recursive"],
        default="recursive",
        help="Choose iterative or recursive dynamic programming"
    )

    arguments = parser.parse_args()

    try:
        capacity, items = read_knapsack_file(arguments.filename)

        print("Knapsack capacity:", capacity)
        print("Number of items:", len(items))
        print("Algorithm:", arguments.method)

        if arguments.method == "iterative":
            answer = knapsack_iterative(capacity, items)
        else:
            answer = knapsack_recursive(capacity, items)

        print("Optimal knapsack value:", answer)

    except FileNotFoundError:
        print(f"Could not find the file: {arguments.filename}")
        sys.exit(1)

    except ValueError as error:
        print("Input error:", error)
        sys.exit(1)

    except MemoryError:
        print("The program ran out of memory.")
        sys.exit(1)


if __name__ == "__main__":
    main()