from tkinter import *
from PIL import ImageTk, Image
import random
import pandas

the_dict = {"English": ""}


def generate_random_word():
    global word, title, the_dict, flip_timer
    window.after_cancel(flip_timer)
    the_dict = random.choice(to_learn)
    canvas.delete(word)
    canvas.delete(title)
    title = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
    word = canvas.create_text(400, 263, text=f"{the_dict['French']}", font=("Ariel", 60, "bold"))


def flip_card():
    global the_dict
    canvas.itemconfig(title, text="English")
    canvas.itemconfig(word, text=the_dict["English"])
    window.after(3000, flip_card)


def is_known():
    to_learn.remove(the_dict)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_random_word()


BACKGROUND_COLOR = "black"

try:
    french_csv = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    french_csv = pandas.read_csv("data/french_words.csv")
to_learn = french_csv.to_dict(orient="records")

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

card_back = ImageTk.PhotoImage(Image.open("images/card_back.jpg"))
card_front = ImageTk.PhotoImage(Image.open("images/card_front.jpg"))
canvas_image = canvas.create_image(400, 263, image=card_front)

title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

x_image = ImageTk.PhotoImage(Image.open("images/wrong.jpg"))
x_button = Button(image=x_image, highlightthickness=0, command=generate_random_word)
x_button.grid(row=1, column=0)

correct_image = ImageTk.PhotoImage(Image.open("images/right.jpg"))
correct_button = Button(image=correct_image, highlightthickness=0, command=is_known)
correct_button.grid(row=1, column=1)

flip_timer = window.after(3000, flip_card)
generate_random_word()
window.mainloop()
