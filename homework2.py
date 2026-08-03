import time


def read_file(filename):
    with open(filename, "r") as file:
        return [int(line.strip()) for line in file]


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    middle = len(arr) // 2
    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])

    return merge(left, right)


def merge_three(a, b, c):
    result = []
    i = j = k = 0

    while i < len(a) or j < len(b) or k < len(c):
        candidates = []

        if i < len(a):
            candidates.append((a[i], "a"))
        if j < len(b):
            candidates.append((b[j], "b"))
        if k < len(c):
            candidates.append((c[k], "c"))

        value, source = min(candidates)
        result.append(value)

        if source == "a":
            i += 1
        elif source == "b":
            j += 1
        else:
            k += 1

    return result


def merge_sort_three(arr):
    if len(arr) <= 1:
        return arr

    third = len(arr) // 3

    first = arr[:third]
    second = arr[third:2 * third]
    third_part = arr[2 * third:]

    first = merge_sort_three(first)
    second = merge_sort_three(second)
    third_part = merge_sort_three(third_part)

    return merge_three(first, second, third_part)


def merge_count(left, right):
    merged = []
    i = j = 0
    inversions = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged, inversions


def count_inversions(arr):
    if len(arr) <= 1:
        return arr, 0

    middle = len(arr) // 2

    left, inv_left = count_inversions(arr[:middle])
    right, inv_right = count_inversions(arr[middle:])

    merged, inv_merge = merge_count(left, right)

    return merged, inv_left + inv_right + inv_merge


def test_sort(name, sort_function, data):
    copy = data[:]

    start = time.perf_counter()
    result = sort_function(copy)
    end = time.perf_counter()

    correct = (result == sorted(data))

    print(name)
    print(f"Correct: {correct}")
    print(f"Time: {end - start:.6f} seconds")
    print()


def main():
    file1 = "testfile1.txt"
    file2 = "testfile2.txt"

    data1 = read_file(file1)
    data2 = read_file(file2)

    test_sort("2-Way MergeSort", merge_sort, data1)
    test_sort("3-Way MergeSort", merge_sort_three, data1)

    _, inversions = count_inversions(data1)
    print("Inversions:", inversions)

    test_sort("2-Way MergeSort", merge_sort, data2)
    test_sort("3-Way MergeSort", merge_sort_three, data2)

    _, inversions = count_inversions(data2)
    print("Inversions:", inversions)

    sorted_array = list(range(1, 9))
    reverse_array = list(range(8, 0, -1))

    _, inv_sorted = count_inversions(sorted_array)
    _, inv_reverse = count_inversions(reverse_array)

    print("Sorted array inversions:", inv_sorted)
    print("Reverse array inversions:", inv_reverse)


if __name__ == "__main__":
    main()