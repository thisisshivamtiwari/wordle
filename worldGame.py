
# ===============================
# IMPORTS: Bringing in Python Libraries
# ===============================
# In Python, we use 'import' to bring in external modules (libraries) that provide extra functionality.
# For example, 'import math' gives us access to mathematical functions like sqrt, log, etc.
#
# Here, we import several modules:
# - time: for working with time and measuring durations (not used in this code, but often useful)
# - random: for generating random numbers or selecting random items
# - math: for advanced mathematical operations (like logarithms)
# - nltk: Natural Language Toolkit, a library for working with human language data
# - words: a corpus (collection) of English words provided by NLTK
#
# Example: If you want to use the square root function, you would write:
# import math
# print(math.sqrt(16))  # Output: 4.0

import time  # Provides time-related functions (e.g., sleep, time)
import random  # Used for random selection, shuffling, etc.
import math  # Advanced math functions (e.g., log2, sqrt)
import nltk  # Natural Language Toolkit for language processing
from nltk.corpus import words  # Import the list of English words from NLTK

# ===============================
# NLTK DATA DOWNLOAD: Ensuring Required Data is Available
# ===============================
# NLTK comes with many datasets, but they are not always downloaded by default.
# The following code checks if the 'words' corpus is available. If not, it downloads it.
#
# 'try' and 'except' are used for error handling in Python. If the code in 'try' fails, 'except' runs.
#
# Example:
# try:
#     # Code that might fail
#     x = 1 / 0
# except ZeroDivisionError:
#     print("You can't divide by zero!")

try:
    nltk.data.find('corpora/words')  # Check if the 'words' corpus is already downloaded
except LookupError:
    nltk.download('words')  # If not found, download it

# ===============================
# FUNCTION: get_5_letter_words
# ===============================
# Functions in Python are defined using 'def'.
# This function gets all valid 5-letter English words from the NLTK corpus.
#
# Example of a simple function:
# def add(a, b):
#     return a + b
# print(add(2, 3))  # Output: 5

def get_5_letter_words():
    """Get list of valid 5-letter words from NLTK corpus"""
    word_list = words.words()  # Get all words from the NLTK corpus
    # Filter for 5-letter words, uppercase, alphabetic only
    five_letter_words = []  # Create an empty list to store 5-letter words
    for word in word_list:
        if len(word) == 5 and word.isalpha():
            five_letter_words.append(word.upper())  # Add the word in uppercase if it is 5 letters and alphabetic
    
    # Remove duplicates and sort
    five_letter_words = list(set(five_letter_words))  # Convert to set to remove duplicates, then back to list
    five_letter_words.sort()  # Sort the list alphabetically
    
    return five_letter_words  # Return the final list of 5-letter words

# Download required NLTK data
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

def get_5_letter_words():
    """Get list of valid 5-letter words from NLTK corpus"""
    word_list = words.words()
    # Filter for 5-letter words, uppercase, alphabetic only
    five_letter_words = []
    for word in word_list:
        if len(word) == 5 and word.isalpha():
            five_letter_words.append(word.upper())
    
    # Remove duplicates and sort
    five_letter_words = list(set(five_letter_words))
    five_letter_words.sort()
    
    return five_letter_words

def give_colors(true_word, guess):
    """takes two strings of length 5.
    returns a list of length 5 with values 0,1 or 2."""
    ans = []
    true_word_chars = list(true_word)
    guess_chars = list(guess)
    
    # First pass: mark exact matches (green)
    for i in range(5):
        if guess_chars[i] == true_word_chars[i]:
            ans.append(2)  # Green
            true_word_chars[i] = None  # Mark as used
            guess_chars[i] = None  # Mark as used
        else:
            ans.append(-1)  # Placeholder
    
    # Second pass: mark present but wrong position (yellow) and absent (gray)
    for i in range(5):
        if ans[i] == -1:  # Not yet determined
            if guess_chars[i] in true_word_chars:
                ans[i] = 1  # Yellow
                # Remove one instance of this character from true_word_chars
                true_word_chars[true_word_chars.index(guess_chars[i])] = None
            else:
                ans[i] = 0  # Gray
    
    return ans

def is_word_consistent(word, guesses, colors):
    """Check if a word is consistent with all previous guesses and their colors."""
    for guess, color_feedback in zip(guesses, colors):
        # Simulate what colors this word would give for the previous guess
        simulated_colors = give_colors(word, guess)
        
        # If the simulated colors don't match the actual colors, word is not consistent
        if simulated_colors != color_feedback:
            return False
    
    return True

def calculate_word_score(candidate, consistent_words):
    """Calculate information gain score for a candidate word"""
    if len(consistent_words) <= 1:
        return 0
    
    color_pattern_groups = {}
    
    # Group consistent words by the color pattern they would produce
    for true_word_candidate in consistent_words:
        colors = tuple(give_colors(true_word_candidate, candidate))
        if colors not in color_pattern_groups:
            color_pattern_groups[colors] = []
        color_pattern_groups[colors].append(true_word_candidate)
    
    # Calculate entropy - prefer candidates that create more evenly distributed groups
    total_words = len(consistent_words)
    entropy = 0
    for group in color_pattern_groups.values():
        prob = len(group) / total_words
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

def nextGuess(current_guesses, current_colors, legal_words):
    """Strategic word selection for Wordle solver"""
    
    # If no previous guesses, use a good starting word
    if len(current_guesses) == 0:
        # Common good starting words with diverse letters
        good_starters = ['ADIEU', 'AUDIO', 'AROSE', 'RAISE', 'STARE', 'SLATE', 'CRATE', 'TEARS']
        for starter in good_starters:
            if starter in legal_words:
                return starter
        return legal_words[0]  # Fallback
    
    # Filter legal words to only those consistent with previous feedback
    consistent_words = []
    for word in legal_words:
        if is_word_consistent(word, current_guesses, current_colors):
            consistent_words.append(word)
    
    # If no consistent words found, return first legal word (shouldn't happen)
    if not consistent_words:
        return legal_words[0]
    
    # If only one consistent word left, return it
    if len(consistent_words) == 1:
        return consistent_words[0]
    
    # If few words left, just pick the first one
    if len(consistent_words) <= 2:
        return consistent_words[0]
    
    # Strategy: Choose word that maximizes information gain
    best_word = None
    best_score = -1
    
    # Consider both consistent words and other legal words as potential guesses
    candidate_guesses = list(set(consistent_words + legal_words[:1000]))  # Limit for performance
    
    for candidate in candidate_guesses:
        score = calculate_word_score(candidate, consistent_words)
        
        # Slight preference for words that are actually possible answers
        if candidate in consistent_words:
            score += 0.1
        
        if score > best_score:
            best_score = score
            best_word = candidate
    
    return best_word if best_word else consistent_words[0]

# Main game execution
def play_wordle_solver(true_word, legal_word_list):
    """Play the Wordle solver game"""
    guess_list = []
    colors_list = []
    num_guesses = 0
    print(f"True word: {true_word}")
    print(f"Dictionary size: {len(legal_word_list)} words")
    print("Starting game...")
    print()

    while True:
        curr_guess = nextGuess(guess_list, colors_list, legal_word_list)
        num_guesses += 1
        curr_colors = give_colors(true_word, curr_guess)
        guess_list.append(curr_guess)
        colors_list.append(curr_colors)

        # Print current guess and colors
        print(f"Guess {num_guesses}: {curr_guess}")
        color_str = ""
        for c in curr_colors:
            if c == 0:
                color_str += "⬜"  # Gray
            elif c == 1:
                color_str += "🟨"  # Yellow  
            else:
                color_str += "🟩"  # Green
        print(f"Colors: {color_str}")

        # Count remaining possible words
        consistent_words = [word for word in legal_word_list 
                          if is_word_consistent(word, guess_list, colors_list)]
        print(f"Remaining possibilities: {len(consistent_words)}")
        if len(consistent_words) <= 10:
            print(f"Possible words: {consistent_words}")
        print()

        if sum(curr_colors) == 10:  # All green (2 * 5 = 10)
            print(f"✅ Solved in {num_guesses} guesses!")
            return True

# Example usage
if __name__ == "__main__":
    # Get 5-letter words from NLTK
    print("Loading 5-letter words from NLTK...")
    legal_word_list = get_5_letter_words()
    print(f"Loaded {len(legal_word_list)} words")
    
    # Example with a word from the list
    if legal_word_list:
        # Choose a random word from the list as the true word
        true_word = random.choice(legal_word_list)
        
        # Or set a specific word
        # true_word = "HOUSE"  # Make sure it's in the list
        
        success = play_wordle_solver(true_word, legal_word_list)
    else:
        print("No 5-letter words found in NLTK corpus!")