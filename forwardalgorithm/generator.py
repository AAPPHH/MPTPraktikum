import numpy as np
import random


def create_characterset():
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    ]

    # Flatten the ranges into a list of visible code points
    emoji_codepoints = []
    for start, end in emoji_ranges:
        emoji_codepoints.extend(range(start, end + 1))

    # Randomly select visible emojis (change 10 to however many you want)
    random_emojis = random.sample(emoji_codepoints, 20)

    # Convert code points to characters
    emoji_chars = [chr(cp) for cp in random_emojis]

    return emoji_chars


def create_alphabet(characters):
    alphabet = [(c, 1.0 + np.power(np.random.uniform(), 1.1)) for c in characters]
    sum = np.array([w for c, w in alphabet]).sum()
    alphabet = [(c, w / sum) for c, w in alphabet]
    return alphabet


def pick_random_char_from_alphabet(alphabet):
    chars = [c for c, _ in alphabet]
    weights = [w for _, w in alphabet]
    return np.random.choice(chars, p=weights)


def write_random_word(alphabet):
    k = np.random.choice([2, 3, 4, 5, 6, 7, 8])
    st = ""
    for _ in range(k):
        st += pick_random_char_from_alphabet(alphabet)

    return st


characters = create_characterset()
A1 = create_alphabet(characters)
A2 = create_alphabet(characters)
A3 = create_alphabet(characters)
A4 = create_alphabet(characters)
A5 = create_alphabet(characters)

for alpha, name in zip(
    [A1, A2, A3, A4, A5], ["text1", "text2", "text3", "text4", "text5"]
):
    lines = []
    for _ in range(8):
        words = np.random.choice([4, 5, 6])
        line = "  ".join([write_random_word(alpha) for _ in range(words)])
        lines.append(line)

    paragraph = "\n".join(lines)
    paragraph = f"""
  {name} = \"\"\"
  {paragraph}\"\"\"
  """

    print(paragraph)

pWechsel = 0.1
cnt = 50
A = A4  # "randomly" start with alphabet 4"
s = ""
while cnt > 0:
    if np.random.uniform() <= pWechsel:
        validAlphabets = [A1, A2, A3, A4, A5]
        validAlphabets.remove(A)
        A = random.choice(validAlphabets)

    s += pick_random_char_from_alphabet(A)

    cnt -= 1

print(f'sequence = "{s}"')
if A == A1:
    print("Last Alphabet was A1")
if A == A2:
    print("Last Alphabet was A2")
if A == A3:
    print("Last Alphabet was A3")
if A == A4:
    print("Last Alphabet was A4")
if A == A5:
    print("Last Alphabet was A5")
