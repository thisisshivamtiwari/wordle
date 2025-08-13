import time
import random

def give_colors(true_word, guess):
    """Compares guess to true_word and returns color feedback for each letter."""
    ans = []
    for i in range(10):
        if guess[i] not in true_word:
            ans.append(0)  # gray
        elif guess[i] == true_word[i]:
            ans.append(2)  # green
        else:
            ans.append(1)  # yellow
    return ans

def nextGuess(current_guesses, current_colors, legal_words):
    """
    Returns a legal word not yet guessed.
    (For demo, picks randomly from remaining legal words.)
    """
    used = set(current_guesses)
    choices = [w for w in legal_words if w not in used]
    if choices:
        return random.choice(choices)
    else:
        return random.choice(legal_words)

# Example setup
true_word = "ABVCDGERQOShivam"
legal_word_list = ["ABVCDGERQOmavihs", "ABVCDZXBNOhiamvs", "YUISCZXBNOvamshi"]
guess_list = []
colors_list = []
num_guesses = 0

while True:
    curr_guess = nextGuess(guess_list, colors_list, legal_word_list)
    num_guesses += 1
    curr_colors = give_colors(true_word, curr_guess)
    guess_list.append(curr_guess)
    colors_list.append(curr_colors)
    print(f"Guess {num_guesses}: {curr_guess} -> {curr_colors}")
    if sum(curr_colors) == 20:  # all green
        print(f"Solved in {num_guesses} guesses!")
        break
    time.sleep(0.5)