import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

mpl.rcParams["font.family"] = "Segoe UI Emoji"

text1 = """
  🧁🧯  🤇🥌🦟  🤇🤫🥌😼🤫  🤇🤟  🦘🦊🥾
🤯🤯🧛😎😼  🥌🥦🤇🤇🦟😒  🧁🧛🧁🦊🧯  🦘😎🦘🦟🤯🦺  🥾🥾🥑🥑🥌
🤟🧁🥦  🥦😼🦊🥾🦺🤇  🧯🦟🦘🤶🦺🦟🥷🧯  😎🦟🦊🤟
🧁😎🦺🦊🤫🥌🧯  🦺😎  🦘😼🥦😎🥑  🤯🦘🦘🦺🦺  😼🤟🥾🤯🥾🤶🥦🦘
🦟😎🤟🦺😼🤶🤟  🧁🦟😎🤯🧛🤇🤟  🧯🤟  😎🦘🥌🧁🦘🤶🦺🦊  🤶🤶🤫🤟🦺
🤇🥌😎🥌🤟🤇  🥦🦺🦘🤇🥾🥷  🤯🦘🦺😒  🧯🦟🦊  🤇🧯🥌  🦟🤇🧛🧛🤟🤯🧛
🤫🦟  🥦🤶🥑🤇🥑  🥦🦊🥦  😼🤇🦟😎🥑  🧁🦊🤯🤫🦘🥾🦊
😎😼  🧛😎🧛🦊🤇🦊🦺🥷  🤯🦘🤶🧁🧁🧁🥌  🥷🤶🦊🦊😒🧛  😼😎🤫🧁"""


text2 = """
  🦺🤶🦺🦟  🦘🧯  🧛🥑🤯  🤶🥌🤇🥷😒
🧁🦘🥾  😎🤯  🤫🧁🤟🦺🤟🧯  🦺🤟🦟🤫😼
🤶😒🦺🥾  🧁🤶🥷🧛🧛🤫🧛  🤇🥾🤫🤇😒🦟🦟  🤇🥦🥷🧁🥑
😎🧯🦘🦟  🧛🦟🤇🧛🤫  😼🤟🦘  😎🦟🤯
🥷🤯🤟🧯🧁  🧁🤶🧁🧛🦘  🧁🤶🧯🥑🤯😒  🥦🥾🤶🤫😎  😎😎🤯😼🤶🧁🥷🦟
🧛😼🤟  🥑🤇🥾  🥾😒🤫  🧁😎🧛🤟🦺🥑🤯🤇  🦟🧯🥷  🥾🤇🥾
🥦🧁🦊😎🧁😒  😎🤇😼🤯🦊🥾🥷  😎🥌🤯🦟🧛🧁🧛  🦘🧁  😎😒🦊🧛  🥾🥾🤶🤯
😎😒🧛🤯🧁  🤟🦺🤯🧛  🦊🤶🥾🥑🥷🦘🦺  🦟😼🦘  🦘🤶😼🤫  🦟🦘😼🤯🤯"""


text3 = """
  🧯🧛🦟🤫🥦🤇🦟  😎🥑🤟🥷🧯🤫🤫  🥷🧯🦺🦺  🧛🥑🥾🦺🧁
🤇🦟🧁🥌🤇🥾🤶🥑  🥾🤫  😼🥑🦺  🤶🦺🦟  🤫🦺  🥦😼🧯🤫🦺🤶
🤟🥾🦺🤇  🤯🥦🤫🦟🤯🤟🤟🤶  🧛🥦🧁  🦘🧯🥾🧛🧯  🥑🤶😼
😎😎🥾🧛🧛  🦘🥑🧁😼🥌🤫🤟  🤟🤇🤶🦊🥾  🤫😼🤫🥾🦟🧁  🤇🦘🦺🧛😼  🥾🤇🥌🧁🤫🥷🦟🤫
🥑🧁🧁🤫🥑🦟🤟🥑  🧛🥌🥾  😼😼🤶🤟🦘  🤟🦺🤇🦘🧛🤯🥌  🧁🦟🤯🥾
🦘🥑  😼🥦🦟🧛🥑🧯🥌  🤇😼  😼🤫
🥾🦊🥷  🦘🤟  🦊🥑🤯🤫🥌🧛  🤇🤫😎🦺🥌  🥾🥦🥑🦊🧁  🥌😼😎🤫🤯
🥦🤶🧛🤟😒🦟🧁🧯  🤇🤫🧛🥦🦺🤟  🥦🤶🥑🦟  🦺🧛🦘🥦🧯🦺"""


text4 = """
  😎🧁🥦🦊🦟🥦  🤶🧯🥌🧯🤟  🧯🦺🧯😒🧁🧛  🦊🧁🥑🤫🤶  🤶🧁🦺🦊😎🤫🧛🥷  😒🤇🥌🤯🤇🤶🤶🥾
🦊😼🦟🦘😎🧛🤟  😎🤇🤯🧛🤇🦘🦘😼  🥑🥷🥑🤇🤟🤇  🦊🥑🥌😼🦘🤇  😼🤟  🦺🦟🥷😒🥦🤯
🤇🦟  🧛🤟🥾🤯🥦  🥦😒😎🥑🥷🤟🥾  🥑🤶  🦺🤫🥷😒🦺🤟  🥦😒🧛🧯🤇🥑🤶🥾
😎🤟🦺😒🥾🤇🤯🤶  🥦🦟🥦🤟🤫🤯🥑🤇  🤟🦊🥾🤟🤶🧯  😼🤯😒  🥦🤇🧁
😒🤟🥌🥌🤫🧛😼  🤯🦟🥑🤇🥑  🥑🦟😎😼😎  🦘🦟🥦🤇🦘
🤯😎🥦🦊😼😎🤶🤇  😼🤯🤯😎🥾😼🥷  🤯🥑🦟😼  🥷😎🤇🥌  🦺🦺🦺🥌🦘🧛🤫🤇
🥷🧁🥦😎  🧁🤇😒🦊🤯🤯😎😼  🧯🧁🥦  😎🤯  🦟🤫🥑🤟🤫🦟  😼🧁🦺😒😒🦺🤫🥦
🧛🥦🦟😼😒😒🦘  🤇🥾  🥌🥦🧛🤯🤶  🦟🥷🤇🥌😒🤶  🦟🤯😼😼"""


text5 = """
  🥌🦊🥾🦊🧁🧯🧛🤯  🧛😎🦟🥌🦘🥾🤯  😎🤶🧁🥌🦘🤇  🧛🦟🤯  🦊🦘🤶🦘🦊🥌  🥷🦊🧛
🧯😒🤫  😼🥌🧛🥾😼😎🤶  🧁🤫🧛🥾🤫  🦊🦟🦘🤶🥌😼
🧛🦊🤯🥾  🥑🦟🥑🤇😼  😒🦟  🦘🧛😎  🤟😼
😒🥾🤶😒🥾  🤇🦘  🥾😼  🥦🦊🥌🦘🦟
🤶🦘🦟  🧁🧯  🤫🤟😒😒🥦  🥦🧁🥌🦘😼🤟🤶
🤫🥑🦘🤇🥷🧁  🥑🧁  🤶🧛😒  🥷🥦
🧯🦊🧛  😼🤯🥑🤟  🧯😼🧯🦊😒🥦  🥾😒🦘🤫🦺🤟🧯  🧛😎🧛🧛😼🤯  🧁😒🦺🦺😒🦺
🧯😼🤯🧁🥌🤇🧛🦘  🧯🤯  😒🤟😼🥾🤟🤫  😎🤫"""

sequence = "😎😎🥦🦊🦺🥑🤇🧛🥦🦟🦘😼🥾🥦🤇🥌🦺🤶🦊😎🦟🥷🥷🥌😒🥑🦟🦺🤶🤶🥾🥾😼🥑😎🤫😎🦘🥷🦘🤯🤯🦟🤟🤯😎🥷🦊🥾🦟"


def clean_text(text):
    """
    **TODO**:
    Clean the text by removing all white spaces and new line character (\\\\n)

    :param text: The text to clean
    :return: The same text witout white spaces and new line characters
    """
    pass


def character_propabilities(text, all_chars):
    """
    **TODO**:
    Given a text, calculate the empirical observation propability of
    all characters from the "all_chars" list.

    The observation propability for character c
    is given as the number of occurrences of that character divided by the total
    number of characters in the string.

    :param text: The text for which character observation propabilities are to be calculated
    :param all_chars: A set of unique characters. The propability for each such character is to be calcualted.
    :return: A dictionary mapping all characters within the all_chars parameter to its respective observation propability.
    """
    pass


def get_emmision_propabilities(all_texts):
    """
    **TODO**:
    Return the emmision propabilities for each character in all the sets.
    This is essentially a list of dictionaries provided by :py:meth:`forward.character_propabilities`

    * Join all the texts together and clean the result (call :py:meth:`clean_text`).
    * Convert the joined string into a set to retrieve the unique characters (call `set <https://www.w3schools.com/python/python_sets.asp>`_)
    * Return a list of emmision propabilities dictionaries for all the texts (call :py:meth:`forward.character_propabilities`)

    :param all_texts: A list of texts
    :return: A list of dictionaries with emmision propabilities for each text
    """
    # TODO: Join all texts and clean them

    # TODO: Get a unique list of all characters across all five texts

    # TODO: Now get the character emmision propabilities for each text
    pass


def get_initial_alpha():
    """
    **TODO**:
    Return the initial alpha vector for the forward algorithm.

    Hint: In the beginning, all states are equally likely

    :return: np.array of shape 5x1 with the initial (equally likely) alpha values.
    """
    # In the begining, we don´t know which text our colleague choose
    # to start with, so all texts are equally likely
    pass


def get_state_transition_matrix():
    """
    **TODO**:
    Return the state transition matrix for the forward algorithm.

    Hint: With 90% chance the state stays the same while the remaining 10% shall be equally divided between the four other states.

    :return: np.array of shape 5x5 with the correct state transition propabilities
    """
    pass


def forward(alpha, character, state_transition_matrix, emmision_propabilities):
    """
    **TODO**: Implement one step of the forward algorithm.

    * Given the past alpha-values and the newly read character, use the state_transition_matrix
    to first predict the new state propabilities (new alpha values) according to the script.

    * Then multiply the state propabilities with the emmision propabilities of the observed character
    for each alphabet to retrieve the new alpha values.

    * Normalize the alpha vector after each step by diving by its sum. This helps to achieve numerically more stable results
    and allows for better interpretation of the results.

    :param alpha: np.array of shape (5,1) holding the past alpha values
    :param character: Observed character in this step
    :param state_transition_matrix: np.array of shape (5,5) holding the state transition propabilities
    :param emmision_propabilities: List of dictionaries holding the character emmision propabilities for each alphabet.
    :return: New alpha-vector after state transition and observation update (np.array of shape 5,1)
    """
    # TODO: Implement state transition and update the alpha vector accordingly

    # TODO: Retrieve symbol emmision propabilties for the given character and update the alpha vector

    # TODO: Normalize alpha for better visualization (divide by sum)

    # TODO: Return alpha
    pass


if __name__ == "__main__":
    # Get initial alpha values
    alpha = get_initial_alpha()

    # Estimate the emmision propabilities for the five texts
    emmision_propabilities = get_emmision_propabilities(
        [text1, text2, text3, text4, text5]
    )

    # Build the state transition matrix
    state_transition_matrix = get_state_transition_matrix()

    alpha_matrix = np.zeros((50, 5))  # shape: (T, num_states)

    # Clean the sequence
    sequence = clean_text(sequence)

    # Iterate over whole sequence
    for t, character in enumerate(sequence):
        # Run forward algorithm
        alpha = forward(
            alpha, character, state_transition_matrix, emmision_propabilities
        )

        # Store current alpha for later
        alpha_matrix[t, :] = alpha

    # Visualize alpha vectors as heat map
    states = ["Text 1", "Text 2", "Text 3", "Text 4", "Text 5"]
    df = pd.DataFrame(
        alpha_matrix.T, index=states, columns=[f"t{t+1}" for t in range(len(sequence))]
    )

    plt.ioff()
    plt.figure(figsize=(10, 4))
    sns.heatmap(df, annot=False, cmap="YlGnBu", cbar=True)
    plt.title("Alpha-Werte pro Zustand über die Zeit")
    plt.xlabel("Zeit (Position in Sequenz)")
    plt.ylabel("Zustand")
    plt.tight_layout()
    plt.show()
