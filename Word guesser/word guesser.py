import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame.mixer

# Initialize the pygame mixer
pygame.mixer.init()

class Character:
    def __init__(self, name, questions, info, image_path, audio_path):
        self.name = name
        self.questions = questions
        self.info = info
        self.image_path = image_path
        self.audio_path = audio_path

def guess_character(characters, first_letter):
    if not first_letter:
        show_info("Akinator", "Please enter a letter.")
        return

    # Convert to lowercase
    first_letter = first_letter.lower()

    # Filter characters based on the first letter
    filtered_characters = [char for char in characters if char.name.lower().startswith(first_letter)]

    if not filtered_characters:
        show_info("Akinator", "No characters found with the specified letter.")
        return

    # Perform BFS
    while filtered_characters:
        # Dequeue the character
        current = filtered_characters.pop(0)

        if guess_ask_question(current):
            # Ask if the guessed character is correct
            answer = ask_yes_no("Akinator", f"I guessed it! Your character is {current.name}.\nIs this correct?")
            if answer:
                show_character_info(current)
                return

    # If unable to guess the character
    show_info("Akinator", "Sorry, I couldn't guess your character.")

def guess_ask_question(character):
    """
    Function to ask questions about the character.
    """
    for q in character.questions:
        answer = ask_yes_no("Question", q)
        if not answer:
            return False
    return True

def show_character_info(character):
    dialog = tk.Toplevel()
    dialog.title(character.name)
    dialog.geometry("600x400")
    dialog.configure(bg="#FFD700")  # Gold
    
    # Load and display character image
    try:
        image = Image.open(character.image_path)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(dialog, image=photo)
        label.image = photo  # Keep a reference
        label.pack()
    except Exception as e:
        print("Error loading image:", e)

    # Display character information
    label_info = tk.Label(dialog, text=character.info, font=("Arial", 12), bg="#FFD700", fg="#2E8B57")  # SeaGreen
    label_info.pack(pady=10)

    ok_button = tk.Button(dialog, text="OK", command=lambda: on_ok_button_click(dialog), font=("Arial", 12, "bold", "italic"), bg="#2E8B57", fg="white")  # SeaGreen
    ok_button.pack(pady=5)

    # Play audio
    pygame.mixer.Sound(character.audio_path).play()

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

def on_ok_button_click(dialog):
    # Stop the currently playing music
    pygame.mixer.stop()
    dialog.destroy()

def show_info(title, message):
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("500x300")
    dialog.configure(bg="#FFD700")  # Gold
    label = tk.Label(dialog, text=message, font=("Arial", 12), bg="#FFD700", fg="#2E8B57")  # SeaGreen
    label.pack(pady=10)
    ok_button = tk.Button(dialog, text="OK", command=dialog.destroy, font=("Arial", 12, "bold", "italic"), bg="#2E8B57", fg="white")  # SeaGreen
    ok_button.pack(pady=5)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

def ask_yes_no(title, message):
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("600x400")
    dialog.configure(bg="#FFD700")  # Gold
    label = tk.Label(dialog, text=message, font=("Arial", 12), bg="#FFD700", fg="#2E8B57")  # SeaGreen
    label.pack(pady=5)
    yes_button = tk.Button(dialog, text="Yes", command=lambda: set_answer(dialog, True), font=("Arial", 12, "bold", "italic"), bg="#2E8B57", fg="white")  # SeaGreen
    yes_button.pack(side="left", padx=10)
    no_button = tk.Button(dialog, text="No", command=lambda: set_answer(dialog, False), font=("Arial", 12, "bold", "italic"), bg="#2E8B57", fg="white")  # SeaGreen
    no_button.pack(side="right", padx=10)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)
    return dialog.answer

def set_answer(dialog, value):
    dialog.answer = value
    dialog.destroy()

def akinator(characters):
    """
    Main function to play the Akinator game.
    """
    global root
    # Create Tkinter window
    root = tk.Tk()
    root.title("Akinator")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Styling
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg="#FFD700")  # Gold

    # Load and display image
    try:
        image = Image.open("C:/Users/Steady/Downloads/car_final.jpg")  # Change path accordingly
        image = image.resize((screen_width, screen_height))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.image = photo  # Keep a reference
        label.pack(fill="both", expand=True)

        # Create a frame for buttons and text fields
        frame = tk.Frame(root, bg="#FFD700", bd=5)
        frame.place(relx=0.5, rely=0.2, relwidth=0.6, relheight=0.2, anchor="n")

        # Create GUI elements
        label = tk.Label(frame, text="Welcome to Akinator!", font=("Arial", 18, "bold", "italic"), bg="#FFD700", fg="#2E8B57")  # SeaGreen
        label.pack(pady=10)

        entry_label = tk.Label(frame, text="Enter the first letter of the character: ", font=("Arial", 12, "bold", "italic"), bg="#FFD700", fg="#2E8B57")  # SeaGreen
        entry_label.pack()

        entry = tk.Entry(frame, font=("Arial", 12))
        entry.pack()

        def start_game():
            guess_character(characters, entry.get())

        # Button to start the game
        start_button = tk.Button(frame, text="Start", command=start_game, font=("Arial", 12, "bold", "italic"), bg="#2E8B57", fg="white")  # SeaGreen
        start_button.pack(pady=10)
        
    except Exception as e:
        print("Error loading image:", e)

    root.mainloop()

# Define characters and their questions
mario = Character("Mario", ["Does your character wear a hat?", "Is your character associated with Nintendo?"], "Mario is a fictional character in the Mario video game franchise, created by Nintendo.", "C:/amirdhasuba/sem4/AI/ai.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Super Mario Bros. Theme Song.mp3")
mickey_mouse = Character("Mickey Mouse", ["Does your character have big round ears?", "Is your character associated with Disney?"], "Mickey Mouse is an animated character created by Walt Disney and Ub Iwerks at The Walt Disney Company.", "C:/Users/Steady/OneDrive/Desktop/aiproj.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio\Mickey Mouse Clubhouse Theme Song  disneyjunior.mp3")
spongebob = Character("SpongeBob SquarePants", ["Is your character a sea creature?", "Is your character associated with Nickelodeon?"], "SpongeBob SquarePants is a fictional character and the titular character of the American animated television series of the same name.", "C:/amirdhasuba/sem4/AI/AIPROJECT/sponge.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/SpongeBob SquarePants Theme Song NEW HD Episode Opening Credits Nick Animation (1).mp3")
superman = Character("Superman", ["Does your character wear a cape?", "Is your character associated with DC Comics?"], "Superman is a fictional superhero appearing in American comic books published by DC Comics.","C:/amirdhasuba/sem4/AI/AIPROJECT/superman.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Superman March Original Cartoon Intro 2011 Remaster.mp3")
spiderman = Character("Spider-Man", ["Does your character shoot webs?", "Is your character associated with Marvel Comics?"], "Spider-Man is a fictional superhero created by writer Stan Lee and artist Steve Ditko for Marvel Comics.","C:/amirdhasuba/sem4/AI/AIPROJECT/spider.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Spider Man Song Original [Remastered].mp3")
scooby_doo = Character("Scooby-Doo", ["Is your character a talking dog?", "Does your character solve mysteries?"], "Scooby-Doo is a fictional character and the titular character of the animated television series of the same name.","C:/amirdhasuba/sem4/AI/AIPROJECT/scooby.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Scooby Doo Theme Song – Best Coast from Scoob The Album [Official Audio].mp3")
batman = Character("Batman", ["Does your character wear a mask?", "Is your character associated with DC Comics?"], "Batman is a fictional superhero appearing in American comic books published by DC Comics.","C:/amirdhasuba/sem4/AI/AIPROJECT/batman.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Batman Opening and Closing Theme 1966 - 1968 With Snippets.mp3")
ironman = Character("Iron Man", ["Does your character wear an armored suit?", "Is your character associated with Marvel Comics?"], "Iron Man is a fictional superhero appearing in American comic books published by Marvel Comics.","C:/amirdhasuba/sem4/AI/AIPROJECT/iron man.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/IRON MAN - Opening.mp3")
homer_simpson = Character("Homer Simpson", ["Is your character associated with The Simpsons?", "Does your character work at a nuclear power plant?"], "Homer Simpson is a fictional character and one of the main characters of the American animated sitcom The Simpsons.","C:/amirdhasuba/sem4/AI/AIPROJECT/homer simpson.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/The Simpsons Main Title Theme.mp3")
pikachu = Character("Pikachu", ["Is your character a yellow electric rodent?", "Is your character associated with Pokémon?"], "Pikachu is a species of Pokémon, fictional creatures that appear in an assortment of media of the Pokémon franchise by Nintendo and Game Freak.","C:/amirdhasuba/sem4/AI/AIPROJECT/pikachu.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Pikachu Song - Pokemon Go Dance   Pokemon Song Remix.mp3")
hello_kitty = Character("Hello Kitty", ["Is your character a white cat with a red bow?", "Is your character associated with Sanrio?"], "Hello Kitty is a fictional character produced by the Japanese company Sanrio.","C:/amirdhasuba/sem4/AI/AIPROJECT/hello kitty.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Hello Kitty Greatest Hits Song Medley.mp3")
scooby_dum = Character("Scooby-Dum", ["Is your character Scooby-Doo's cousin?", "Is your character less intelligent than Scooby-Doo?"], "Scooby-Dum is a fictional Great Dane created by Hanna-Barbera Productions.","C:/amirdhasuba/sem4/AI/AIPROJECT/scooby dum.gif", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Scooby Doo Theme Song – Best Coast from Scoob The Album [Official Audio].mp3")
spongegar = Character("SpongeGar", ["Is your character a prehistoric sponge?", "Is your character associated with SpongeBob SquarePants?"], "SpongeGar is a prehistoric ancestor of SpongeBob SquarePants.","C:/amirdhasuba/sem4/AI/AIPROJECT/spongegar.gif", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/SpongeBob SquarePants Theme Song NEW HD Episode Opening Credits Nick Animation (1).mp3")
tigger = Character("Tigger", ["Is your character a striped tiger?", "Is your character associated with Winnie the Pooh?"], "Tigger is a fictional tiger character originally introduced in the A. A. Milne book The House at Pooh Corner.","C:/amirdhasuba/sem4/AI/AIPROJECT/tigger.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/The Wonderful Thing About Tiggers Sing Along Songs.mp3")
popeye = Character("Popeye", ["Does your character love spinach?", "Is your character associated with Popeye the Sailor?"], "Popeye the Sailor is a fictional cartoon character created by Elzie Crisler Segar.","C:/amirdhasuba/sem4/AI/AIPROJECT/poppeye.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Popeye The Sailor Man Intro Theme Song.mp3")
daffy_duck = Character("Daffy Duck", ["Is your character associated with Looney Tunes?", "Is your character a black duck?"], "Daffy Duck is an animated cartoon character produced by Warner Bros. Animation studios.","C:/amirdhasuba/sem4/AI/AIPROJECT/duffy duck.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Duck Dodgers intro.mp3")
pikmin = Character("Pikmin", ["Is your character small and plant-like?", "Is your character associated with Nintendo?"], "Pikmin are fictional plant-like creatures in the Pikmin video game series created by Shigeru Miyamoto.","C:/amirdhasuba/sem4/AI/AIPROJECT/pimin.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Pikmin song cover.mp3")
kermit = Character("Kermit the Frog", ["Is your character associated with The Muppets?", "Is your character green?"], "Kermit the Frog is a Muppet character and the protagonist of the Muppet Show.","C:/amirdhasuba/sem4/AI/AIPROJECT/kermit.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Original Theme Song  The Muppet Show  Disney.mp3")
homer = Character("Homer Simpson", ["Is your character associated with The Simpsons?", "Is your character overweight?"], "Homer Simpson is a fictional character and one of the main characters of the American animated sitcom The Simpsons.","C:/amirdhasuba/sem4/AI/AIPROJECT/homer simpson.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/The Simpsons Main Title Theme.mp3")
bugs_bunny = Character("Bugs Bunny", ["Is your character associated with Looney Tunes?", "Is your character a gray rabbit?"], "Bugs Bunny is an animated cartoon character created in 1940 by Leon Schlesinger Productions.","C:/amirdhasuba/sem4/AI/AIPROJECT/bugs bunny.gif", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Bugs Bunny Theme - This Is It.mp3")
chhota_bheem = Character("Chhota Bheem", ["Is your character a young boy?", "Is your character associated with Pogo TV?"], "Chhota Bheem is an Indian animated comedy adventure television series created by Rajiv Chilaka.","C:/amirdhasuba/sem4/AI/AIPROJECT/Chhota-Bheem-GIF-Png.gif", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Chotta bheem title song in tamil (1).mp3")
shinchan = Character("Shinchan", ["Is your character a mischievous boy?", "Is your character associated with Japanese anime?"], "Shin Chan is a Japanese manga series written and illustrated by Yoshito Usui.","C:/amirdhasuba/sem4/AI/AIPROJECT/shinchan.gif", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Shin chan opening theme song in tamilTamil cartoon world.mp3")
chutki = Character("Chutki", ["Is your character a cheerful girl?", "Is your character associated with Chhota Bheem series?"], "Chutki is one of the main characters in the Indian animated television series Chhota Bheem.","C:/amirdhasuba/sem4/AI/AIPROJECT/chutki.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Chotta bheem title song in tamil (1).mp3")
raju = Character("Raju", ["Is your character a mischievous young boy?", "Is your character associated with Chhota Bheem series?"], "Raju is one of the main characters in the Indian animated television series Chhota Bheem.","C:/amirdhasuba/sem4/AI/AIPROJECT/raju.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Chotta bheem title song in tamil (1).mp3")
kalia = Character("Kalia", ["Is your character a strong and powerful boy?", "Is your character associated with Chhota Bheem series?"], "Kalia is one of the main characters in the Indian animated television series Chhota Bheem.","C:/amirdhasuba/sem4/AI/AIPROJECT/kalai.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Chotta bheem title song in tamil (1).mp3")
jaggu = Character("Jaggu", ["Is your character a talking monkey?", "Is your character associated with Chhota Bheem series?"], "Jaggu is one of the main characters in the Indian animated television series Chhota Bheem.","C:/amirdhasuba/sem4/AI/AIPROJECT/jaggu.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Chotta bheem title song in tamil (1).mp3")
doraemon = Character("Doraemon", ["Is your character a robot cat?", "Is your character associated with Japanese manga?"], "Doraemon is a Japanese manga series written and illustrated by Fujiko F. Fujio.","C:/amirdhasuba/sem4/AI/AIPROJECT/doreamon.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/Doraemon title song in tamil.mp3")
dora=Character("Dora", ["Is your character a young explorer?", "Is your character associated with Nickelodeon?"], "Dora the Explorer is an American educational animated TV series created by Chris Gifford.", "C:/amirdhasuba/sem4/AI/AIPROJECT/dora.jpg", "C:/amirdhasuba/sem4/AI/AIPROJECT/audio/dora song.mp3")
# List of characters
characters = [mario, mickey_mouse, spongebob, superman, spiderman, scooby_doo, batman, ironman, homer_simpson, pikachu,
              hello_kitty, scooby_dum, spongegar, tigger, popeye, daffy_duck, pikmin, kermit, homer, bugs_bunny,
              chhota_bheem, shinchan, chutki, raju, kalia, jaggu, doraemon,dora]  # Add more characters here

# Start the Akinator game
akinator(characters)


# List of characters
  # Add more characters here

# Start the Akinator game
akinator(characters)
