import random
import itertools

# Green, Red, Yellow, Orange, White, Black
COLORS = ['G', 'R', 'Y', 'O', 'W', 'B']


def generate_all_codes():
    """
    Generates all possible 4-color codes.
    """
    return list(itertools.product(COLORS, repeat=4))


def feedback(code, guess):
    """
    Given a secret code and a guess, returns (black_pegs, white_pegs).
    """
    black_pegs = sum(c == g for c, g in zip(code, guess))

    # Count colors in code and guess
    code_color_count = {color: code.count(color) for color in COLORS}
    guess_color_count = {color: guess.count(color) for color in COLORS}

    # Count common colors ignoring positions
    common_colors = sum(
        min(code_color_count[c], guess_color_count[c]) for c in COLORS)

    white_pegs = common_colors - black_pegs

    return black_pegs, white_pegs


def parse_code_input(code_str):
    """
    Parses the user's input into a tuple of colors.
    """
    code = code_str.upper().strip().split()
    if len(code) != 4 or any(c not in COLORS for c in code):
        raise ValueError(
            "Invalid code. Use exactly 4 colors: G R Y O W B (separated by spaces).")
    return tuple(code)


def format_guess(guess):
    """
    Formats a guess tuple into a string for displaying.
    """
    return ' '.join(guess)


def mastermind_game():
    """
    Runs the Mastermind game where the user sets a secret code.
    """
    print("\n🎮 Welcome to Mastermind! 🎮")
    print("Colors: G=Green, R=Red, Y=Yellow, O=Orange, W=White, B=Black")
    print("Please think of a secret code and enter it.")
    print("Example input: G R Y B")
    print("-----------------------------------------------------------\n")

    while True:
        try:
            user_code_input = input("Enter your secret code (G R Y B): ")
            secret_code = parse_code_input(user_code_input)
            break
        except ValueError as e:
            print(e)

    possible_codes = generate_all_codes()
    round_number = 1

    while True:
        if not possible_codes:
            print("No possible codes left! There might have been an error.")
            break

        guess = random.choice(possible_codes)
        print(f"\nRound {round_number}: AI guesses --> {format_guess(guess)}")

        black_pegs, white_pegs = feedback(secret_code, guess)
        print(
            f"Feedback: {black_pegs} black peg(s), {white_pegs} white peg(s)")

        if black_pegs == 4:
            print(f"\n✅ AI has cracked your code in {round_number} rounds! 🎉")
            break

        # Belief Revision: filter possible codes
        new_possible = []
        for code in possible_codes:
            b, w = feedback(code, guess)
            if (b, w) == (black_pegs, white_pegs):
                new_possible.append(code)

        possible_codes = new_possible
        round_number += 1


if __name__ == "__main__":
    mastermind_game()
