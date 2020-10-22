# Import - Please check the requirements for every library that is used. Thank you
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar

import pandas as pd
import numpy as np
# sklear used to train our "model"
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import ImageTk, Image
import time


###### helper functions. Use them when needed #######
def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


# This is a secondary window that will serve as a loading screen - Just for an appealing design
display = Tk()
# place the title
display.title("Loading Screen")
# Configure
display.configure()
# specify the path of the image
path = "images/myPic.png"
# open the image
img = ImageTk.PhotoImage(Image.open(path))
# Create a label for that image as content
my = Label(display, image=img)
# the image of tha label will be the desired image
my.image = img
# Place the image in the window
my.place(x=0, y=0)
# Display the window
Frame(display, height=516, width=5, bg='black').place(x=520, y=0)
# Put a label with an overiview information
lbl1 = Label(display, text="Recommendation System", font='Timesnewroman 20 ', fg='blue')
lbl1.config(anchor=CENTER)
# Put the label on the window
lbl1.pack(padx=100, pady=100)


# A function to be called after some time (after loading screen have to go)
def call_display():
    display.destroy()


# Call the destroy function after 3 seconds
display.after(3000, call_display)
display.mainloop()

# Create Window object - this will be our main window
window = Tk(className=' Music Recommendation System')

# define four labels Title Author Year ISBN
l1 = Label(window, text='Music Recommendation System', bg='black', fg='white', pady=20, padx=20)
l1.grid(row=1, column=2)

# define four labels Title Author Year ISBN
l1 = Label(window, text='Title', pady=10)
l1.grid(row=2, column=1)

# Another label
l1 = Label(window, text='Author', pady=10)
l1.grid(row=4, column=1)

# Another label
l1 = Label(window, text='Year', pady=10)
l1.grid(row=6, column=1)

# Another label
l1 = Label(window, text='ISBN', pady=10)
l1.grid(row=8, column=1)

# define Entries - textfields to enter information
title_text = StringVar()
e1 = Entry(window, textvariable=title_text, width=30)
e1.grid(row=2, column=2)

author_text = StringVar()
e2 = Entry(window, textvariable=author_text, width=30)
e2.grid(row=4, column=2)

year_text = StringVar()
e3 = Entry(window, textvariable=year_text, width=30)
e3.grid(row=6, column=2)

isbn_text = StringVar()
e4 = Entry(window, textvariable=isbn_text, width=30)
e4.grid(row=8, column=2)

# define ListBox - a placeholder to store the result of our search
list1 = Listbox(window, height=12, width=55)
list1.grid(row=20, column=1, rowspan=50, columnspan=60)

# Attach scrollbar to the list - easily explore the list
sb1 = Scrollbar(window)
sb1.grid(row=20, column=3, rowspan=60)

# Configure that scroll bar to our list box
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

##################################################

# Read the data from the file
# Step 1: Read CSV File
df = pd.read_csv("movie_dataset.csv")
# print df.columns

# Step 2: Select Features
features = ['keywords', 'cast', 'genres', 'director']

# Step 3: Create a column in DF which combines all selected features
for feature in features:
    df[feature] = df[feature].fillna('')


def combine_features(row):
    try:
        return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]
    except:
        print("Error:", row)


df["combined_features"] = df.apply(combine_features, axis=1)
# print("Combined Features:", df["combined_features"].head())

# define a progress bar
var = IntVar()
var.set(0)
pgbar = Progressbar(
    window,
    orient=HORIZONTAL,
    mode='determinate',
    maximum=100,
    length=200,
    variable=var
)
pgbar.grid(row=71, column=2)

val = 0

'''
    # A recommended function to display the list in GUI
    :return none
'''


def recommend():
    # Clear the previous result
    list1.delete(0, END)
    load_text.set('Loading...')
    global val
    val = 0
    var.set(val)
    for i in range(101):
        if val < 100:
            val += 1
            var.set(val)
            time.sleep(0.01)
        else:
            messagebox.showwarning("Warning", "Please check our list! \nThank you!")

    # Read data from CSV - insert new result
    try:
        # Step 4: Create count matrix from this new combined column
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df["combined_features"])

        # Step 5: Compute the Cosine Similarity based on the count_matrix
        cosine_sim = cosine_similarity(count_matrix)

        movie_user_likes = title_text.get()

        # Step 6: Get index of this movie from its title
        movie_index = get_index_from_title(movie_user_likes)

        similar_movies = list(enumerate(cosine_sim[movie_index]))

        # Step 7: Get a list of similar movies in descending order of similarity score
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        # Reset the value so we can clear it afterwards
        val = 0
        load_text.set('35 Results were found')

        # Step 8: Print titles of first 50 movies
        i = 0
        for element in sorted_similar_movies:
            print(get_title_from_index(element[0]))
            list1.insert(i, str(i) + ". " + get_title_from_index(element[0]))
            i = i + 1
            if i > 35:
                break

    except:
        # Change the text
        load_text.set('Google failed search. Please come back later!')
        # Insert the information to the listbox
        list1.insert(END, str(title_text.get()) + ": Requested movie does not exist in our database!")
        # warning the user what to do next
        messagebox.showwarning("Warning", "Please type another movie or complete all the fields! \nThank you!")


# define a label
load_text = StringVar()
load_text.set("Press Key")
load_label = Label(window, textvariable=load_text, pady=10, padx=10)
load_label.grid(row=70, column=2)

'''
    # This function will print all the information we have in database for a specific movie title
    :returns none
'''


def onclick():
    try:
        '''
        Trying to make a load screen
        from tqdm.auto import tqdm

        for i in tqdm(range(100001)):
            load_text.set(" ", end='\r')
        '''
        # Get the information from the text fields and manipulate them
        load_text.set('Search clicked')
        print("Button is clicked")
        print('Author : ' + author_text.get())
        print('Author : ' + isbn_text.get())
        print('Author : ' + year_text.get())
        author = "" + author_text.get()
        title = "" + title_text.get()
        string_to_display = title + " by " + author

        # Insert the necessary information to the listbox for the specific movie title
        list1.insert(END, string_to_display)
        list1.insert(END, df[df.title == title]["index"].values[0])
        list1.insert(END, " ")
        list1.insert(END, "Budget: ", (df[df.title == title]["budget"].values[0]))
        list1.insert(END, " ")
        list1.insert(END, "Genre: ", (df[df.title == title]["genres"].values[0]))
        list1.insert(END, " ")
        list1.insert(END, "production_companies: ", (df[df.title == title]["production_companies"].values[0]))
        list1.insert(END, " ")
        list1.insert(END, "overview: ", (df[df.title == title]["overview"].values[0]))
        list1.insert(END, " ")
        list1.insert(END, "release_date: ", (df[df.title == title]["release_date"].values[0]))
        list1.insert(END, " ")
        list1.insert(END, "revenue: ", (df[df.title == title]["revenue"].values[0]))
        list1.insert(END, " ")
        list1.insert(END, "director: ", (df[df.title == title]["director"].values[0]))
        list1.insert(END, " ")
    except:
        # Delete the previous information
        list1.delete(0, END)
        # Enter the new information
        list1.insert(END, "This movie does not exists")
        # Alert the user what to do next
        messagebox.showwarning("Warning", "Please type another movie! \nThank you!")


# A function to clear the previous information on the screen
def clear():
    load_text.set('Clear the results!')
    # Clear the list box and setting the progress bar to 0
    global val
    val = 0
    var.set(val)
    list1.delete(0, END)


# Setting icons to the buttons
# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
# from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

# Define buttons
# Creating a photoimage object to use image
photo = PhotoImage(file="images/green.png")
b1 = Button(window, text='Google', width=15, command=recommend)
b1.grid(row=10, column=1)

# Define the search button
photo = PhotoImage(file="images/search_icon.png")
b1 = Button(window, text='Search Entry', width=15, command=onclick)
b1.grid(row=10, column=2)

# Define buttons
photo = PhotoImage(file="images/clear.png")
b1 = Button(window, text='Clear', width=85, command=clear, image=photo, compound=LEFT)
b1.grid(row=10, column=3)

# Set an icon to our main background
path = "images/search.png"
img = ImageTk.PhotoImage(Image.open(path))
my = Label(window, image=img)
my.image = img
my.grid(row=1, column=1)

# set window size
window.geometry("430x510")

# Enter the main loop never to return
window.mainloop()
