# Quiz-Game
My Python Quiz-Game project
Quiz Game 🎓💻
Welcome to Quiz Game, an academic project developed with passion and dedication! 🎉 This interactive application, crafted in Python using tkinter for the graphical interface, offers users an engaging platform to test and expand their knowledge across various topics. 🧠 Designed as part of my academic journey, this project reflects my commitment to applying theoretical concepts to practical, real-world solutions. Below, I’ll provide a comprehensive overview of the project, its development, functionality, and technical details.

![Image](https://github.com/user-attachments/assets/7c90f283-e72a-48be-ade7-a7b9845657c6)

About the Project 📚
I am Dalia Adriana, a second-year student at the Faculty of Automation, Computers, and Electronics in Craiova, Romania, pursuing a degree in Multimedia Systems Engineering. 🎓 This project was undertaken for the Algorithm Design course, a key component of my curriculum, under the guidance of my esteemed professors. The course focuses on designing efficient algorithms and implementing them in software, and this game serves as a hands-on application of those principles. 🚀 The project was inspired by the need for an educational tool that blends entertainment with learning, aiming to reinforce my skills in programming, algorithm optimization, and user interface design.
The development process spanned several weeks and involved multiple stages:

Planning: I began by defining the game’s objectives, including a category-based question system, dynamic scoring, and user profiles. I sketched the workflow, identifying key algorithms for question randomization and score tracking.
Implementation: Using Python, I built the game’s core logic with the QuizGame class in quiz.py, integrated the GUI with tkinter, and added sound effects using pygame and numpy. The json module was employed to manage user data dynamically.
Testing: I conducted rigorous testing to ensure stability, addressing issues such as question duplication and interface lag. This involved running the game with various inputs and monitoring the quiz_game.log file for errors.
Refinement: Feedback from peers and self-assessment led to enhancements like hint options and a statistics tracker, improving user experience and educational value.

This project not only honed my technical skills but also deepened my understanding of algorithm efficiency and software design, making it a significant milestone in my academic portfolio. 📈
Project Details and Functionality 🌟
How the Game Works
Quiz Game is designed to engage users in a question-and-answer format, with the following core mechanics:

Categories: The game supports multiple categories (e.g., General Knowledge, Countries and Cities), with questions stored in text files within the categories directory. If no files are present, the game simulates questions to maintain functionality.
Gameplay: Users log in or register, select a category and difficulty level, and answer a set number of questions. Each correct answer earns points, while hints (e.g., "Half Letters," "First Letter") can be used at a point cost.
Scoring and Levels: Points accumulate based on correct answers, with levels increasing as thresholds are met (e.g., Level 4 at 60/100 XP). This gamification encourages continuous play.
Statistics and Highscores: The game tracks performance metrics (e.g., average score, time per game) and maintains a highscore list, saved dynamically in generated JSON files.
Exit and Restart: Users can exit to the menu or restart, with all progress saved for logged-in users.

Technical Implementation
The game’s architecture is built around the following components:

Main Script (main.py): Initializes the GUI window, sets the background, and launches the QuizGame instance. It uses a main event loop to handle user interactions.
Game Logic (quiz.py): Contains the QuizGame class, which manages question loading, user input validation, scoring, and hint logic. Key methods include:
load_questions(): Reads questions from categories files or generates random ones.
check_answer(): Compares user input with the correct answer, updating the score.
save_data(): Serializes user data and highscores to JSON files.


Libraries:
tkinter: Provides the graphical interface, including buttons, entry fields, and labels.
pygame and numpy: Enable sound effects, processed as NumPy arrays for compatibility.
Pillow (PIL): Handles image resizing (e.g., background to 800x600 pixels).
json: Manages persistent data storage.


Algorithms: The game employs a random selection algorithm for questions, optimized with a shuffle function to avoid repetition, and a linear search for highscore updates.

Commands and Usage
To set up and run the game locally, follow these steps:

Install Python: Ensure Python 3.x is installed. Verify with:python --version

orpython3 --version


Install Dependencies: Install required libraries using pip:pip install pygame numpy pillow

Check installation with:pip show pygame
pip show numpy
pip show pillow


Run the Game: Navigate to the project directory in your terminal or command prompt:cd path/to/Quiz-Game

Then start the game:python main.py


Manage Data Files: The game generates users.json, last_login.json, and highscores.json on first run. To reset them (if needed), delete these files manually and restart the game.
Add Questions: Create text files in the categories directory (e.g., general_easy.txt) with questions in the format:Question: What is the capital of France?
Answer: Paris

Save and rerun the game to load new questions.

Educational Value
Quiz Game transcends entertainment, serving as a robust learning tool. It encourages users to explore diverse topics, reinforces memory through repeated engagement, and fosters strategic thinking via hint usage. For me, the project was a practical exercise in applying data structures (e.g., lists for questions), control flow (e.g., game loops), and file I/O (e.g., JSON handling), aligning with the Algorithm Design curriculum. It also enhanced my problem-solving skills and introduced me to multimedia integration, a cornerstone of my specialization.
Requirements ⚙️
To run the game, you need:

Python 3.x 🐍
tkinter (included with Python)
pygame (for sounds) 🎵
numpy (for sound generation)
Pillow (PIL) (for images) 🖼️
json (included with Python)

Install the required libraries with the command:
pip install pygame numpy pillow

How to Run ▶️

Ensure you have installed the required libraries (see above).
Navigate to the project directory:cd path/to/Quiz-Game


Run the main file:python main.py



File Structure 📂

main.py: The main script that launches the game. 🚀
quiz.py: Contains the QuizGame class with the game logic. 🧩
back.jpg: The game background. 🖼️
quiz_game.log: Log file for debugging. 📜

Notes 📝

The game automatically generates files such as users.json, last_login.json, and highscores.json on the first run to store user data and scores. These are not included locally for confidentiality reasons. 🔒 To reset, delete these files and restart.
For full functionality, add question files to the categories directory (e.g., general_easy.txt). If none exist, the game simulates questions. ❓
![Image](https://github.com/user-attachments/assets/4963f886-48fb-496d-949d-e0f8d6d14d31)
![Image](https://github.com/user-attachments/assets/db93e39d-76ba-4551-b6af-3c33bd9ece98)
![Image](https://github.com/user-attachments/assets/587a5f82-7b1d-4e35-a6a1-c00c116693ae)
![Image](https://github.com/user-attachments/assets/48e23c6e-2a48-444e-848a-efdb0ae8e023)
![Image](https://github.com/user-attachments/assets/fd528f59-00f0-427b-9060-a9e7c4b5ca9e)

Thank you for exploring my project! I hope you enjoy Quiz Game! 😊 I welcome any feedback or suggestions to further enhance this academic endeavor. 💬
