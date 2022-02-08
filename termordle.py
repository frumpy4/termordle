import argparse
import datetime
import random
from collections import Counter

parser = argparse.ArgumentParser(description="A terminal based wordle clone")
parser.add_argument("--colorblind", "-cb", action="store_true",
                    help="colorblind mode (green -> orange, yellow -> blue)")
parser.add_argument("--daily", "-d", action="store_true",
                    help="try the daily wordle")
parser.add_argument("--hard", action="store_true",
                    help="hard mode, selects a word from all valid words instead of just daily words. can be combined with daily")
parser.add_argument("--allow-all", "-a", action="store_true",
                    help="allow any 5 character string for guesses")
parser.add_argument("--no-emoji", "-q", action="store_true",
                    help="don't print emoji summary at the end")
parser.add_argument("--tries", "-t", type=int, default=6,
                    help="number of tries. default 6")
parser.add_argument("--word", "-w", type=str,
                    help="select the word, must be 5 characters. overrides daily/hard mode")

args = parser.parse_args()

cb = args.colorblind

# GREEN  = f"\x1b[{97 if cb else 30};1;{45 if cb else 102}m"
# YELLOW = f"\x1b[{30 if cb else 30};1;{103 if cb else 103}m"
# GRAY   = f"\x1b[{30 if cb else 30};1;{47 if cb else 47}m"

# https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
#              bold   foreground    background
GREEN  = f"\x1b[1m\x1b[38;5;232m\x1b[48;5;{208 if cb else 2}m"
YELLOW = f"\x1b[1m\x1b[38;5;232m\x1b[48;5;{45 if cb else 220}m"
GRAY   = f"\x1b[1m\x1b[38;5;232m\x1b[48;5;251m"

RESET  = "\x1b[0m"

EMOJI_GREEN  = "🟧" if cb else "🟩"
EMOJI_YELLOW = "🟦" if cb else "🟨"
EMOJI_GRAY   = "⬜"

WORDLE_BEGIN = datetime.date(2021, 6, 19)
day = (datetime.date.today() - WORDLE_BEGIN).days

with open("daily.txt", "r") as f:
    daily_words = f.read().split(" ")
with open("dictionary.txt", "r") as f:
    dictionary = f.read().split(" ")

all_words = daily_words + dictionary

random.seed(727)
random.shuffle(all_words)
random.seed()

# return a list of color codes for each letter
def check_word(word, guess):
    letters = Counter()
    w = [GRAY for _ in range(5)]

    # do one pass for green letters first
    for i, c in enumerate(guess):
        if c == word[i]:
            w[i] = GREEN
            letters[c] += 1

    # then check yellow letters and make sure not to overcount
    for i, c in enumerate(guess):
        if w[i] != GRAY:
            continue
        if c in word and letters[c] < word.count(c):
            w[i] = YELLOW
            letters[c] += 1

    return w

words = daily_words
if args.hard:
    words = all_words

if args.word:
    if len(args.word) != 5:
        print("word must be 5 characters")
        exit(1)

    word = args.word
    all_words.append(word)

else:
    if args.daily:
        word = words[day % len(words)]
    else:
        word = random.choice(words)

guesses = []

_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters = {c: "" for c in _letters}
def print_letters():
    # pretty keyboard
    for c in "QWERTYUIOP":
        print(f"{letters[c]} {c} {RESET}", end="")

    print("\n ", end="")
    for c in "ASDFGHJKL":
        print(f"{letters[c]} {c} {RESET}", end="")

    print("\n  ", end="")
    for c in "ZXCVBNM":
        print(f"{letters[c]} {c} {RESET}", end="")

print("type a word, press ctrl+c to give up")
print()

print_letters()
print()
print()

for i in range(args.tries):
    try:
        guess = input()

        while ( # topkek
            (len(guess) != 5) if args.allow_all
            else (guess.lower() not in all_words)
        ):
            # F = move one line up
            # G = move to beginning of line
            guess = input(f"\x1b[F{' ' * 5} '{guess}' is not a valid word\x1b[G")

        # clears invalid word message
        # since input() goes to next line, go up and 5 to the right
        # then K = clear from cursor to end of line
        print(f"\x1b[F\x1b[5C\x1b[K")

        colors = check_word(word, guess.lower())
        # guess.upper() for style i guess
        word_colors = zip(guess.upper(), colors)
        guesses.append(guess)

        # print word
        print("\x1b[F", end="")
        for c, color in word_colors:
            print(f"{color}{c}", end="")
        print(RESET)

        # update letter tracker
        for c, color in sorted(zip(guess.upper(), colors)):
            if color == GRAY:
                if letters[c] == "":
                    letters[c] = color
            elif letters[c]!= GREEN:
                letters[c] = color

        print(f"\x1b[{i + 5}F", end="")
        print_letters()
        print(f"\x1b[{i + 5}E", end=RESET)

        if colors == [GREEN] * 5:
            print(f"guessed correctly in {i + 1} word{'s' if i + 1 != 1 else ''}")
            i = str(i + 1)
            break

    except KeyboardInterrupt:
        print()
        print(f"the word was {word.upper()}")
        i = "X"
        break

else:
    print(f"the word was {word.upper()}")
    i = "X"

if not args.no_emoji:
    print()
    print(f"{'Daily ' if args.daily else ''}Termordle {'Hard mode ' if args.hard else ''}{str(day) + ' ' if args.daily else ''}{i}/{args.tries}")
    for guess in guesses:
        # slightly redundant i suppose
        colors = check_word(word, guess)
        for c in colors:
            if c == GREEN:
                print(EMOJI_GREEN, end="")
            if c == YELLOW:
                print(EMOJI_YELLOW, end="")
            if c == GRAY:
                print(EMOJI_GRAY, end="")

        print(f" ||`{guess.upper()}`||")
    print("<https://github.com/frumpy4/termordle>")
