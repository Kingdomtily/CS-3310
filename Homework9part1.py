from math import isqrt

def minimum_squares(n):
    if n < 0:
        raise ValueError("n must be nonnegative")
    dp = [float("inf")] * (n + 1)
    chosen_square = [0] * (n + 1)
    dp[0] = 0
    for current_number in range(1, n + 1):
        for root in range(1, isqrt(current_number) + 1):
            square = root * root
            remaining = current_number - square
            candidate_count = dp[remaining] + 1
            if candidate_count < dp[current_number]:
                dp[current_number] = candidate_count
                chosen_square[current_number] = square
    squares_used = []
    remaining = n
    while remaining > 0:
        square = chosen_square[remaining]
        squares_used.append(square)
        remaining -= square
    return dp[n], squares_used


def print_numbers_requiring_four_squares():
    print("Numbers from 1 through 50 requiring at least four squares:")
    for number in range(1, 51):
        count, squares = minimum_squares(number)
        if count >= 4:
            expression = " + ".join(str(square) for square in squares)
            print(f"{number} = {expression}")

def main():
    for number in [12, 13]:
        count, squares = minimum_squares(number)
        expression = " + ".join(str(square) for square in squares)
        print(f"{number} = {expression}")
        print(f"Minimum number of squares: {count}")
        print()
    print_numbers_requiring_four_squares()
if __name__ == "__main__":
    main()