import sys


def read_tree(filename):


    weights = {}
    children = {}

    section = None

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.lower() == "nodes":
                section = "nodes"
                continue

            if line.lower() == "edges":
                section = "edges"
                continue

            parts = line.split()

            if section == "nodes":
                node = int(parts[0])
                value = int(parts[1])

                weights[node] = value
                children[node] = []

            elif section == "edges":
                parent = int(parts[0])
                child = int(parts[1])

                children[parent].append(child)

    return weights, children


def tree_mwis(weights, children, root=1):

    include = {}
    exclude = {}

    def dfs(node):
        include[node] = weights[node]
        exclude[node] = 0

        for child in children[node]:
            dfs(child)

            include[node] += exclude[child]

            exclude[node] += max(include[child], exclude[child])

    dfs(root)

    return max(include[root], exclude[root])


def main():
    if len(sys.argv) != 2:
        print("Usage: python mwis_tree.py <data_file>")
        return

    filename = sys.argv[1]

    try:
        weights, children = read_tree(filename)
        answer = tree_mwis(weights, children)

        print("MWIS value:", answer)

    except FileNotFoundError:
        print("Error: file not found:", filename)

    except (ValueError, IndexError):
        print("Error: the input file is not formatted correctly.")


if __name__ == "__main__":
    main()