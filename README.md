Quiz Game 🎓💻

Welcome to Quiz Game, an intellectually enriching academic endeavor crafted with passion and precision! 🎉 This interactive Python application, developed using tkinter for its graphical interface, provides an engaging platform for users to test and broaden their knowledge across diverse topics. 🧠 Conceived as part of my academic pursuits, this project exemplifies my commitment to translating theoretical concepts into practical, real-world applications, serving as a cornerstone of my growth at the University of Craiova. Below, I offer a detailed exploration of its development, functionality, and technical underpinnings.

![Image](https://github.com/user-attachments/assets/7c90f283-e72a-48be-ade7-a7b9845657c6)

About the Project 📚

I am Dalia Adriana, a second-year student at the Faculty of Automation, Computers, and Electronics (FACE) in Craiova, Romania, specializing in Multimedia Systems Engineering. 🎓 This project was undertaken as a key assignment for the Algorithm Design course, a fundamental component of my curriculum, under the esteemed guidance of my professors. The course is dedicated to mastering the design and implementation of efficient algorithms, and Quiz Game stands as a practical manifestation of these principles. 🚀
The genesis of this project arose from a vision to create an educational tool that seamlessly blends entertainment with learning. Spanning several weeks, the development process encompassed meticulous planning, coding, testing, and refinement. I began by outlining objectives such as a category-based question system, dynamic scoring, and user profiles, sketching workflows to optimize algorithms for question randomization and score management. Implementation involved constructing the QuizGame class in quiz.py, integrating the GUI with tkinter, and enhancing the experience with pygame and numpy for sound effects, alongside json for data persistence. Rigorous testing addressed challenges like question duplication and interface lag, utilizing the quiz_game.log file for error tracking. Peer feedback and self-assessment drove refinements, including hint options and a statistics tracker, elevating both usability and educational impact. This journey not only sharpened my technical prowess but also deepened my insight into algorithmic efficiency and user-centered design, marking it as a significant milestone in my academic portfolio. 📈

🔑 Features

👤 User Registration and Login: Enables secure account creation and login, ensuring personalized progress tracking.
🔐 Secure Authentication: Employs password hashing and session management to safeguard user data.
🧩 Question Categories: Supports multiple categories (e.g., General Knowledge, Countries and Cities), with questions sourced from text files in the categories directory or simulated if absent.
🎮 Gameplay Mechanics: Allows users to select difficulty levels and answer questions, earning points with optional hints ("Half Letters" or "First Letter") at a cost.
📊 Scoring and Levels: Awards points for correct answers, unlocking levels (e.g., Level 4 at 60/100 XP) to foster continuous engagement.
📈 Statistics Tracker: Records performance metrics such as average score and game duration.
🏆 Highscores System: Maintains a dynamic leaderboard of top scores.
🚪 Exit and Navigation: Permits users to return to the menu or restart, with progress saved for logged-in users.

⚠ Known Issues and Limitations

Hint Logic: The hint system ("Half Letters," "First Letter") may occasionally offer suboptimal assistance due to random selection limitations.
Question Simulation: Simulated questions, used when category files are absent, lack depth and may repeat, necessitating manual file creation for a richer experience.
Performance Constraints: Local testing with SQLite may experience lag with a large user base, rendering it unsuitable for production-scale deployment.
Sound Compatibility: Audio effects via pygame are basic and may require additional configuration for consistent performance across systems.

🧪 Technologies Used

Backend: Python, with core logic in quiz.py and initialization in main.py.
Frontend: tkinter for graphical interface development.
Audio Processing: pygame and numpy for sound generation and playback.
Image Handling: Pillow (PIL) for background resizing.
Data Management: json for persistent storage of user data and highscores.
Development Tools: Native Python libraries and a local development environment.

📦 Requirements

To execute this project locally, ensure the following dependencies are installed:
Python 3.x 🐍
tkinter (included with Python)
pygame 🎵
numpy 📊
Pillow (PIL) 🖼️
json (included with Python)

Install the required libraries with the following command:
pip install pygame numpy pillow

🔧 Setup Instructions

Follow these detailed steps to set up and run the project on your laptop:
Verify Python Installation: Confirm your Python version is installed:
python --version
or
python3 --version
If not installed, download it from https://www.python.org/.
Install Dependencies: Navigate to your project directory and install the necessary libraries:
cd path/to/Quiz-Game
pip install pygame numpy pillow
Verify installation with:
pip show pygame
pip show numpy
pip show pillow

Run the Game: Launch the application from the project directory:

python main.py
The game will initialize, generating users.json, last_login.json, and highscores.json if they do not exist.
Manage Data Files: To reset user data or highscores, manually delete the generated JSON files and restart the game.
Add Questions: Enhance gameplay by creating text files in the categories directory (e.g., general_easy.txt). Use the following format:
Question: What is the capital of France?
Answer: Paris
Save the file and rerun the game to load the new questions.


📁 Project Structure

Quiz-Game/
main.py: The primary script that initializes the game interface and event loop. 🚀
quiz.py: Contains the QuizGame class, managing game logic, input validation, scoring, and data persistence. 🧩
back.jpg: The background image file utilized by the game. 🖼️
categories/: Directory for storing question text files (e.g., general_easy.txt).
quiz_game.log: Log file for debugging and error monitoring. 📜



📜 Educational Value and Disclaimer

Quiz Game transcends traditional entertainment, emerging as a potent educational tool. It inspires users to delve into varied subjects, strengthens memory through repeated engagement, and nurtures strategic thinking through hint utilization. For me, this project was a hands-on exploration of data structures (e.g., lists for questions), control flow (e.g., game loops), and file input/output (e.g., JSON management), perfectly aligning with the Algorithm Design curriculum. It also bolstered my problem-solving abilities and introduced me to multimedia integration, a pivotal aspect of my specialization.
Disclaimer: This project is the product of the Algorithm Design laboratory at the Faculty of Automation, Computers, and Electronics (FACE), University of Craiova (http://ace.ucv.ro/). It is intended for educational purposes and may include limitations or incomplete features. Use it at your own risk, and conduct thorough testing and configuration before considering any production deployment. 🔬

![image](https://github.com/user-attachments/assets/9de097c9-96b3-4fe3-87ff-965a366af987)
![Image](https://github.com/user-attachments/assets/4963f886-48fb-496d-949d-e0f8d6d14d31)
![Image](https://github.com/user-attachments/assets/db93e39d-76ba-4551-b6af-3c33bd9ece98)
![Image](https://github.com/user-attachments/assets/587a5f82-7b1d-4e35-a6a1-c00c116693ae)
![Image](https://github.com/user-attachments/assets/48e23c6e-2a48-444e-848a-efdb0ae8e023)
![Image](https://github.com/user-attachments/assets/fd528f59-00f0-427b-9060-a9e7c4b5ca9e)

Thank you for immersing yourself in my project! I hope you find Quiz Game both captivating and instructive! 😊 I warmly welcome your feedback or suggestions to further enrich this academic endeavor. 💬
