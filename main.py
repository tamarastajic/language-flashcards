from tkinter import *
import pandas
from random import choice

# ------------------ Constants  ------------------
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
PATH_TO_ORIGINAL = "data/Bulgarian Words (~8000).csv"
PATH_TO_DATA = "data/Bulgarian Words - Personal Track.csv"

ran_card = {}


# ------------------ Functions  ------------------
def get_new_word():
    """A function that switches the flashcard to a new word."""
    global ran_card, timer
    window.after_cancel(timer)
    ran_card = choice(data_dict)
    flash_card.itemconfig(current_side, image=card_front)
    flash_card.itemconfig(language_txt, text="Bulgarian", fill="black")
    flash_card.itemconfig(word_txt, text=ran_card['Bulgarian'], fill="black")
    timer = window.after(3000, func=flip_card)


def flip_card():
    """A function that flips the card."""
    flash_card.itemconfig(current_side, image=card_back)
    flash_card.itemconfig(language_txt, fill="white", text="English")
    flash_card.itemconfig(word_txt, fill="white", text=ran_card['English'])


def remove_data():
    """A function that removes a specific piece of data."""
    data_dict.remove(ran_card)
    new_data = pandas.DataFrame(data_dict)
    new_data.to_csv(PATH_TO_DATA, index=False)
    get_new_word()


# ------------------ Word Data  ------------------
try:
    data = pandas.read_csv(PATH_TO_DATA)
except FileNotFoundError:
    data = pandas.read_csv(PATH_TO_ORIGINAL)
data_dict = data.to_dict(orient="records")

# ------------------ Window  ------------------
window = Tk()
window.title("Flash Cards - Bulgarian Edition")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ------------------ Timer  ------------------
timer = window.after(3000, func=flip_card)

# ------------------ Flashcard Canvas ------------------
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

flash_card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
current_side = flash_card.create_image(400, 263, image=card_front)
language_txt = flash_card.create_text(400, 150, text="", fill="black", font=LANGUAGE_FONT)
word_txt = flash_card.create_text(400, 263, text="", fill="black", font=WORD_FONT)
flash_card.grid(row=0, column=0, columnspan=2)

# ------------------ Button Widgets------------------
wrong_image = PhotoImage(file="images/wrong.png")
right_image = PhotoImage(file="images/right.png")

wrong_button = Button(image=wrong_image, highlightthickness=0, command=get_new_word)
wrong_button.grid(row=1, column=0)
right_button = Button(image=right_image, highlightthickness=0, command=remove_data)
right_button.grid(row=1, column=1)

# ------------------ Loop ------------------
get_new_word()
window.mainloop()
