import os
import random
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import time
import hashlib
import unicodedata
import logging
import platform
import numpy as np
import pygame
from PIL import Image, ImageTk

class QuizGame:
    def __init__(self, root):
        logging.basicConfig(
            filename="quiz_game.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info("Joc inițializat")

        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Setează imaginea ca fundal cu fallback
        self.bg_label = None
        try:
            self.bg_image = Image.open("back.jpg")
            self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            logging.info("Fundalul imaginii setat cu succes")
        except FileNotFoundError as e:
            logging.error(f"Fișierul back.jpg nu a fost găsit: {e}")
            self.root.configure(bg="#F5F5F5")  # Culoare fallback crem deschis
            messagebox.showerror("Eroare", "Fișierul back.jpg nu a fost găsit. Verifică calea!")
            self.bg_label = None
        except Exception as e:
            logging.error(f"Eroare la încărcarea imaginii de fundal: {e}")
            self.root.configure(bg="#F5F5F5")  # Culoare fallback crem deschis
            messagebox.showwarning("Atenție", f"Imaginea de fundal nu a putut fi încărcată: {e}")
            self.bg_label = None

        # Adaugă gestionarea redimensionării ferestrei
        self.root.bind("<Configure>", self.resize_background)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.correct_sound = self.generate_correct_sound()
            self.incorrect_sound = self.generate_incorrect_sound()
            self.hint_sound = self.generate_hint_sound()
            self.game_over_sound = self.generate_game_over_sound()
            logging.info("Sunete inițializate cu succes")
        except Exception as e:
            logging.error(f"Eroare la inițializarea sunetelor: {e}")
            self.correct_sound = None
            self.incorrect_sound = None
            self.hint_sound = None
            self.game_over_sound = None
            messagebox.showwarning("Atenție", f"Sunetele nu au putut fi inițializate: {e}")

        self.colors = {
            "primary": "#94A3B8",      # Albastru-gri pastel pentru elemente principale
            "secondary": "#A7F3D0",    # Verde mentă deschis pentru butoane
            "accent": "#FECACA",       # Piersică pală pentru accente
            "success": "#6EE7B7",      # Verde pastel pentru răspunsuri corecte
            "error": "#FCA5A5",        # Coral pastel pentru erori
            "background": "#F5F5F5",   # Crem deschis pentru fundal fallback
            "text": "#1F2937"          # Gri închis pentru text clar
        }

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TEntry",
                        fieldbackground=self.colors["background"],
                        background=self.colors["background"],
                        foreground=self.colors["text"],
                        borderwidth=0,
                        relief="flat",
                        padding=5,
                        font=('Helvetica', 14))
        style.configure("Selected.TEntry",
                        fieldbackground="#E2E8F0",  # Gri deschis pentru selecție
                        background="#E2E8F0",
                        foreground=self.colors["text"],
                        borderwidth=0,
                        relief="solid")
        style.configure("Custom.Treeview",
                        font=('Helvetica', 12),
                        background=self.colors["background"],
                        fieldbackground=self.colors["background"],
                        foreground=self.colors["text"])
        style.configure("Custom.Treeview.Heading",
                        font=('Helvetica', 12, 'bold'),
                        background=self.colors["primary"],
                        foreground=self.colors["text"])
        style.configure("TScale",
                        background=self.colors["background"],
                        troughcolor=self.colors["secondary"],
                        foreground=self.colors["text"])

        self.categories = {
            "general": "Cunoștințe Generale",
            "țări_orașe": "Țări și Orașe",
            "scenariu": "Scenariu Separat"
        }
        self.difficulties = ["ușor", "mediu", "greu"]
        self.questions = {}
        self.current_questions = []
        self.deferred_questions = []
        self.score = 0
        self.current_question_index = 0
        self.total_questions = 10
        self.difficulty = "mediu"
        self.category = "general"
        self.player_name = ""
        self.hints_used = 0
        self.max_hints = 3
        self.hint_indices = []
        self.start_time = 0
        self.end_time = 0
        self.highscores_file = "highscores.json"
        self.users_file = "users.json"
        self.last_login_file = "last_login.json"
        self.incorrect_answers = []
        self.is_fast_quiz = False
        self.fast_quiz_duration = 300
        self.time_left = 0
        self.timer_id = None
        self.status_label = None
        self.answer_label = None
        self.player_label = None
        self.menu_buttons = []
        self.selected_menu_index = 0
        self.login_elements = []
        self.selected_login_index = 0
        self.level = 1
        self.experience = 0
        self.level_threshold = 100

        if not os.path.exists("categories"):
            try:
                os.makedirs("categories")
                logging.info("Director 'categories' creat")
            except Exception as e:
                logging.error(f"Eroare la crearea directorului 'categories': {e}")
                messagebox.showerror("Eroare", f"Nu s-a putut crea directorul 'categories': {e}")

        self.load_users()
        self.load_highscores()
        self.create_login_screen()

    def resize_background(self, event=None):
        """Redimensionează imaginea de fundal în funcție de dimensiunea ferestrei."""
        if self.bg_label and self.bg_image:
            new_width = self.root.winfo_width()
            new_height = self.root.winfo_height()
            try:
                resized_image = self.bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(resized_image)
                self.bg_label.configure(image=self.bg_photo)
                self.bg_label.image = self.bg_photo
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                logging.debug("Imagine de fundal redimensionată")
            except Exception as e:
                logging.error(f"Eroare la redimensionarea imaginii de fundal: {e}")
                self.root.configure(bg=self.colors["background"])

    def on_closing(self):
        if messagebox.askokcancel("Ieșire", "Vrei să închizi jocul?"):
            try:
                pygame.mixer.quit()
                self.save_users()
                self.root.quit()
                self.root.destroy()
                logging.info("Joc închis de utilizator")
            except Exception as e:
                logging.error(f"Eroare la închiderea jocului: {e}")

    def generate_correct_sound(self):
        sample_rate = 44100
        duration = 0.5
        freq = 1000
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        sound_data = 0.5 * np.sin(2 * np.pi * freq * t)
        sound_data = np.column_stack((sound_data, sound_data))
        sound_data = (sound_data * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(sound_data)
        return sound

    def generate_incorrect_sound(self):
        sample_rate = 44100
        duration = 0.5
        freq = 200
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        sound_data = 0.5 * np.sin(2 * np.pi * freq * t)
        sound_data = np.column_stack((sound_data, sound_data))
        sound_data = (sound_data * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(sound_data)
        return sound

    def generate_hint_sound(self):
        sample_rate = 44100
        duration = 0.1
        freq = 800
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        sound_data = 0.3 * np.sin(2 * np.pi * freq * t)
        sound_data = np.column_stack((sound_data, sound_data))
        sound_data = (sound_data * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(sound_data)
        return sound

    def generate_game_over_sound(self):
        sample_rate = 44100
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        sound_data = (0.4 * np.sin(2 * np.pi * 600 * t) +
                      0.3 * np.sin(2 * np.pi * 800 * t) +
                      0.2 * np.sin(2 * np.pi * 1000 * t))
        sound_data = np.column_stack((sound_data, sound_data))
        sound_data = (sound_data * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(sound_data)
        return sound

    def play_sound(self, sound):
        if sound:
            try:
                sound.play()
                logging.info("Sunet redat")
            except Exception as e:
                logging.error(f"Eroare la redarea sunetului: {e}")

    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
                if self.player_name and self.player_name in self.users:
                    user_data = self.users[self.player_name]
                    self.level = user_data.get("level", 1)
                    self.experience = user_data.get("experience", 0)
                    self.max_hints = user_data.get("max_hints", 3)
                logging.info("Utilizatori încărcați cu succes")
            except Exception as e:
                logging.error(f"Eroare la încărcarea utilizatorilor: {e}")
                self.users = {}
                if self.status_label:
                    self.status_label.config(text="Eroare la încărcarea utilizatorilor!", fg=self.colors["error"])
                else:
                    messagebox.showerror("Eroare", f"Nu s-au putut încărca utilizatorii: {e}")
        else:
            self.users = {}
            logging.info("Fișierul users.json nu există, inițializat cu dicționar gol")

    def save_users(self):
        try:
            if self.player_name:
                self.users[self.player_name] = {
                    "password": self.users.get(self.player_name, {}).get("password", ""),
                    "level": self.level,
                    "experience": self.experience,
                    "max_hints": self.max_hints
                }
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
            logging.info(f"Utilizatori salvați: {self.player_name}")
        except Exception as e:
            logging.error(f"Eroare la salvarea utilizatorilor: {e}")
            if self.status_label:
                self.status_label.config(text="Eroare la salvarea utilizatorilor!", fg=self.colors["error"])
            else:
                messagebox.showerror("Eroare", f"Nu s-a putut salva users.json: {e}")

    def load_last_login(self):
        if os.path.exists(self.last_login_file):
            try:
                with open(self.last_login_file, "r", encoding="utf-8") as f:
                    last_login = json.load(f).get("username", "")
                logging.info(f"Ultimul login încărcat: {last_login}")
                return last_login
            except Exception as e:
                logging.error(f"Eroare la încărcarea ultimului login: {e}")
                if self.status_label:
                    self.status_label.config(text="Eroare la încărcarea ultimului login!", fg=self.colors["error"])
                else:
                    messagebox.showerror("Eroare", f"Nu s-a putut încărca last_login.json: {e}")
                return ""
        logging.info("Fișierul last_login.json nu există")
        return ""

    def save_last_login(self, username):
        try:
            with open(self.last_login_file, "w", encoding="utf-8") as f:
                json.dump({"username": username}, f, indent=4, ensure_ascii=False)
            logging.info(f"Ultimul login salvat: {username}")
        except Exception as e:
            logging.error(f"Eroare la salvarea ultimului login: {e}")
            if self.status_label:
                self.status_label.config(text="Eroare la salvarea ultimului login!", fg=self.colors["error"])
            else:
                messagebox.showerror("Eroare", f"Nu s-a putut salva last_login.json: {e}")

    def hash_password(self, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        logging.info("Parolă hash-uită")
        return hashed

    def update_login_selection(self):
        for i, element in enumerate(self.login_elements):
            if isinstance(element, ttk.Entry):
                if i == self.selected_login_index:
                    element.focus_set()
                    element.configure(style="Selected.TEntry")
                else:
                    element.configure(style="TEntry")
            elif isinstance(element, tk.Button):
                if i == self.selected_login_index:
                    element.config(bg=self.colors["success"], relief="sunken")
                else:
                    element.config(bg=self.colors["secondary"], relief="raised")

    def create_login_screen(self):
        self.clear_frame()
        if self.bg_label:
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title_label = tk.Label(self.root, text="Quiz Game Login", font=('Helvetica', 24, 'bold'), bg=self.colors["background"], fg=self.colors["text"])
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        login_frame = tk.Frame(self.root, bg=self.colors["background"])
        login_frame.place(relx=0.5, rely=0.3, anchor="center")

        tk.Label(login_frame, text="Username:", font=('Helvetica', 14), bg=self.colors["background"], fg=self.colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(login_frame, width=25, font=('Helvetica', 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.username_entry.insert(0, self.load_last_login())

        tk.Label(login_frame, text="Password:", font=('Helvetica', 14), bg=self.colors["background"], fg=self.colors["text"]).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(login_frame, width=25, show="*", font=('Helvetica', 12))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.remember_var = tk.BooleanVar(value=True)
        checkbutton = tk.Checkbutton(login_frame, text="Remember Me", variable=self.remember_var, font=('Helvetica', 12), bg=self.colors["background"], fg=self.colors["text"], activebackground=self.colors["background"], activeforeground=self.colors["text"])
        checkbutton.grid(row=2, column=1, columnspan=2, pady=10, sticky="w")

        btn_frame = tk.Frame(self.root, bg=self.colors["background"])
        btn_frame.place(relx=0.5, rely=0.5, anchor="center")

        login_button = tk.Button(btn_frame, text="Login", font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"], activebackground=self.colors["success"], activeforeground=self.colors["text"], command=self.login, relief="flat", cursor="hand2")
        login_button.pack(side="left", padx=10, fill="x", expand=True)

        register_button = tk.Button(btn_frame, text="Register", font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"], activebackground=self.colors["success"], activeforeground=self.colors["text"], command=self.register, relief="flat", cursor="hand2")
        register_button.pack(side="left", padx=10, fill="x", expand=True)

        self.status_label = tk.Label(self.root, text="", font=('Helvetica', 12), bg=self.colors["background"], fg=self.colors["error"])
        self.status_label.place(relx=0.5, rely=0.6, anchor="center")

        self.login_elements = [self.username_entry, self.password_entry, login_button, register_button]
        self.selected_login_index = 0

        def move_up(event):
            self.selected_login_index = (self.selected_login_index - 1) % len(self.login_elements)
            self.update_login_selection()

        def move_down(event):
            self.selected_login_index = (self.selected_login_index + 1) % len(self.login_elements)
            self.update_login_selection()

        def move_left(event):
            if isinstance(self.login_elements[self.selected_login_index], ttk.Entry):
                entry = self.login_elements[self.selected_login_index]
                cursor_pos = entry.index(tk.INSERT)
                if cursor_pos > 0:
                    entry.icursor(cursor_pos - 1)
            else:
                self.selected_login_index = (self.selected_login_index - 1) % len(self.login_elements)
                self.update_login_selection()

        def move_right(event):
            if isinstance(self.login_elements[self.selected_login_index], ttk.Entry):
                entry = self.login_elements[self.selected_login_index]
                cursor_pos = entry.index(tk.INSERT)
                if cursor_pos < len(entry.get()):
                    entry.icursor(cursor_pos + 1)
            else:
                self.selected_login_index = (self.selected_login_index + 1) % len(self.login_elements)
                self.update_menu_selection()

        def select_option(event):
            element = self.login_elements[self.selected_login_index]
            if isinstance(element, ttk.Entry):
                if element == self.username_entry:
                    self.selected_login_index = 1
                elif element == self.password_entry:
                    self.selected_login_index = 2
                self.update_login_selection()
            elif isinstance(element, tk.Button):
                element.invoke()

        self.update_login_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)
        logging.info("Ecran de login creat")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.status_label.config(text="Completează toate câmpurile!")
            logging.warning("Încercare de login cu câmpuri goale")
            return
        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username]["password"] == hashed_password:
            self.player_name = username
            self.level = self.users[username].get("level", 1)
            self.experience = self.users[username].get("experience", 0)
            self.max_hints = self.users[username].get("max_hints", 3)
            if self.remember_var.get():
                self.save_last_login(username)
            else:
                self.save_last_login("")
            self.create_main_menu()
            logging.info(f"Login reușit pentru utilizator: {username}")
        else:
            self.status_label.config(text="Nume utilizator sau parolă incorecte!")
            logging.warning(f"Login eșuat pentru utilizator: {username}")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.status_label.config(text="Completează toate câmpurile!")
            logging.warning("Încercare de înregistrare cu câmpuri goale")
            return
        if username in self.users:
            self.status_label.config(text="Numele de utilizator există deja!")
            logging.warning(f"Încercare de înregistrare cu utilizator existent: {username}")
            return
        self.users[username] = {
            "password": self.hash_password(password),
            "level": 1,
            "experience": 0,
            "max_hints": 3
        }
        self.save_users()
        self.status_label.config(text="Cont creat cu succes! Conectează-te acum.", fg=self.colors["success"])
        logging.info(f"Utilizator înregistrat: {username}")

    def load_highscores(self):
        if os.path.exists(self.highscores_file):
            try:
                with open(self.highscores_file, "r", encoding="utf-8") as f:
                    self.highscores = json.load(f)
                logging.info(f"Scoruri încărcate: {len(self.highscores)} intrări")
            except Exception as e:
                logging.error(f"Eroare la încărcarea scorurilor: {e}")
                self.highscores = []
                if self.status_label:
                    self.status_label.config(text="Eroare la încărcarea scorurilor!", fg=self.colors["error"])
                else:
                    messagebox.showerror("Eroare", f"Nu s-au putut încărca scorurile: {e}")
        else:
            self.highscores = []
            logging.info("Fișierul highscores.json nu există, inițializat cu listă goală")

    def save_highscore(self):
        if not self.player_name:
            logging.warning("Numele jucătorului lipsește, scorul nu a fost salvat")
            return
        time_taken = self.end_time - self.start_time
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        score_entry = {
            "name": self.player_name,
            "score": self.score,
            "date": current_date,
            "category": self.category,
            "difficulty": self.difficulty,
            "questions": len(self.current_questions) if self.is_fast_quiz else self.total_questions,
            "time": round(time_taken, 2),
            "hints_used": self.hints_used
        }
        self.highscores.append(score_entry)
        self.highscores.sort(key=lambda x: (-x["score"], x["time"]))
        try:
            with open(self.highscores_file, "w", encoding="utf-8") as f:
                json.dump(self.highscores, f, indent=4, ensure_ascii=False)
            logging.info(f"Scor salvat: {score_entry}")
        except Exception as e:
            logging.error(f"Eroare la salvarea scorurilor: {e}")
            if self.status_label:
                self.status_label.config(text="Eroare la salvarea scorului!", fg=self.colors["error"])
            else:
                messagebox.showerror("Eroare", f"Nu s-a putut salva highscores.json: {e}")

    def normalize_text(self, text):
        text = text.lower()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        return text

    def load_questions_from_file(self, category, difficulty):
        file_path = f"categories/{category}_{difficulty}.txt"
        questions = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for i in range(0, len(lines), 2):
                    if i + 1 < len(lines):
                        question = lines[i].strip()
                        answer = lines[i + 1].strip()
                        if question and answer and len(answer) > 0:
                            questions.append({"question": question, "answer": answer, "category": category, "difficulty": difficulty})
                logging.info(f"Încărcate {len(questions)} întrebări din {file_path}")
            except Exception as e:
                logging.error(f"Eroare la încărcarea întrebărilor din {file_path}: {e}")
                if self.status_label:
                    self.status_label.config(text="Eroare la încărcarea întrebărilor!", fg=self.colors["error"])
                else:
                    messagebox.showerror("Eroare", f"Nu s-au putut încărca întrebările: {e}")
        else:
            logging.info(f"Fișierul {file_path} nu există")
        return questions

    def download_questions(self, category, difficulty):
        if self.status_label:
            self.status_label.config(text=f"Se încarcă întrebări pentru {self.categories.get(category, category)} ({difficulty})...")
        self.root.update()

        questions = []
        if category == "general":
            if difficulty == "ușor":
                questions = [
                    {"question": "Ce animal este cunoscut pentru dungile sale alb-negru?", "answer": "zebră", "category": "general", "difficulty": "ușor"},
                    {"question": "Câte zile are luna februarie într-un an normal?", "answer": "28", "category": "general", "difficulty": "ușor"},
                    {"question": "Ce culoare are cerul într-o zi senină?", "answer": "albastru", "category": "general", "difficulty": "ușor"},
                ]
            elif difficulty == "mediu":
                questions = [
                    {"question": "Ce limbă se vorbește în Brazilia?", "answer": "portugheză", "category": "general", "difficulty": "mediu"},
                    {"question": "Cine a fost autorul romanului 'Pe aripile vântului'?", "answer": "Margaret Mitchell", "category": "general", "difficulty": "mediu"},
                    {"question": "Ce instrument muzical are clape albe și negre?", "answer": "pian", "category": "general", "difficulty": "mediu"},
                ] + [{"question": f"Întrebare medie generală {i}?", "answer": f"răspuns{i}", "category": "general", "difficulty": "mediu"} for i in range(200)]
            elif difficulty == "greu":
                questions = [
                    {"question": "Ce filozof a scris lucrarea 'Critica rațiunii pure'?", "answer": "Immanuel Kant", "category": "general", "difficulty": "greu"},
                    {"question": "Care este capitala statului Bhutan?", "answer": "Thimphu", "category": "general", "difficulty": "greu"},
                    {"question": "Ce artist a pictat 'Cina cea de Taină'?", "answer": "Leonardo da Vinci", "category": "general", "difficulty": "greu"},
                ] + [{"question": f"Întrebare grea generală {i}?", "answer": f"răspuns{i}", "category": "general", "difficulty": "greu"} for i in range(200)]
        elif category == "țări_orașe":
            if difficulty == "ușor":
                questions = [
                    {"question": "Care este capitala Franței?", "answer": "Paris", "category": "țări_orașe", "difficulty": "ușor"},
                    {"question": "Ce țară are capitala București?", "answer": "România", "category": "țări_orașe", "difficulty": "ușor"},
                ]
            elif difficulty == "mediu":
                questions = [
                    {"question": "Care este capitala Australiei?", "answer": "Canberra", "category": "țări_orașe", "difficulty": "mediu"},
                    {"question": "Ce oraș este cunoscut pentru Colosseum?", "answer": "Roma", "category": "țări_orașe", "difficulty": "mediu"},
                ]
            elif difficulty == "greu":
                questions = [
                    {"question": "Care este capitala insulei Kiribati?", "answer": "Tarawa", "category": "țări_orașe", "difficulty": "greu"},
                    {"question": "Care este cel mai mic stat independent din lume?", "answer": "Vatican", "category": "țări_orașe", "difficulty": "greu"},
                ]
        elif category == "scenariu":
            if difficulty == "ușor":
                questions = [
                    {"question": "Ești un detectiv. Unde cauți mai întâi indicii în castel?", "answer": "bibliotecă", "category": "scenariu", "difficulty": "ușor"},
                    {"question": "Ce obiect găsești pe biroul din castel?", "answer": "o scrisoare", "category": "scenariu", "difficulty": "ușor"},
                ]
            elif difficulty == "mediu":
                questions = [
                    {"question": "Ce mesaj este scris pe scrisoarea găsită?", "answer": "Întâlnire la miezul nopții", "category": "scenariu", "difficulty": "mediu"},
                    {"question": "Unde se află cheia secretă a castelului?", "answer": "sub covor", "category": "scenariu", "difficulty": "mediu"},
                ]
            elif difficulty == "greu":
                questions = [
                    {"question": "Ce oră indică ceasul din turn când auzi țipătul?", "answer": "2 dimineața", "category": "scenariu", "difficulty": "greu"},
                    {"question": "Ce simbol este gravat pe cheia secretă?", "answer": "o lună plină", "category": "scenariu", "difficulty": "greu"},
                ]

        file_path = f"categories/{category}_{difficulty}.txt"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for q in questions:
                    f.write(f"{q['question']}\n{q['answer']}\n")
            logging.info(f"Întrebări salvate în {file_path}")
        except Exception as e:
            logging.error(f"Eroare la salvarea întrebărilor în {file_path}: {e}")
            if self.status_label:
                self.status_label.config(text="Eroare la salvarea întrebărilor!", fg=self.colors["error"])
            else:
                messagebox.showerror("Eroare", f"Nu s-au putut salva întrebările: {e}")

        if self.status_label:
            self.status_label.config(text="Întrebări încărcate cu succes!", fg=self.colors["success"])
        self.root.update()
        time.sleep(1)

        logging.info(f"Întrebări simulate descărcate: {len(questions)} pentru {category}/{difficulty}")
        return questions

    def select_random_questions(self):
        key = f"{self.category}_{self.difficulty}"
        if key not in self.questions or not self.questions[key]:
            questions = self.load_questions_from_file(self.category, self.difficulty)
            if not questions:
                questions = self.download_questions(self.category, self.difficulty)
            self.questions[key] = questions

        available_questions = self.questions[key]
        if not available_questions:
            messagebox.showerror("Eroare", "Nu există întrebări disponibile pentru această categorie și dificultate!")
            logging.error(f"Nu există întrebări pentru {key}")
            self.create_main_menu()
            return

        if self.is_fast_quiz:
            self.current_questions = random.sample(available_questions, min(200, len(available_questions)))
        elif len(available_questions) <= self.total_questions:
            self.current_questions = available_questions.copy()
        else:
            self.current_questions = random.sample(available_questions, self.total_questions)
        logging.info(f"Selectate {len(self.current_questions)} întrebări pentru joc")

    def display_hidden_answer(self, answer=None, revealed_indices=None):
        if answer is None:
            answer = self.current_questions[self.current_question_index]["answer"]
        hidden = ""
        if revealed_indices is None:
            revealed_indices = []
        for i, char in enumerate(answer):
            if char == " ":
                hidden += " "
            elif i in revealed_indices or not char.isalnum():
                hidden += char
            else:
                hidden += "_"
        return hidden

    def reveal_half_letters(self, answer):
        length = len(answer)
        num_to_reveal = max(1, length // 2)
        valid_indices = [i for i, char in enumerate(answer) if char.isalnum() and i not in self.hint_indices]
        if not valid_indices:
            return self.display_hidden_answer(answer, self.hint_indices)
        num_to_reveal = min(num_to_reveal, len(valid_indices))
        new_indices = random.sample(valid_indices, num_to_reveal)
        self.hint_indices.extend(new_indices)
        return self.display_hidden_answer(answer, self.hint_indices)

    def reveal_first_letter(self, answer):
        for i, char in enumerate(answer):
            if char.isalnum() and i not in self.hint_indices:
                self.hint_indices.append(i)
                break
        return self.display_hidden_answer(answer, self.hint_indices)

    def clear_frame(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()
        if self.bg_label:
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.status_label = None
        self.answer_label = None
        self.player_label = None
        self.menu_buttons = []
        self.selected_menu_index = 0
        self.login_elements = []
        self.selected_login_index = 0
        self.root.unbind('<Return>')
        self.root.unbind('<Up>')
        self.root.unbind('<Down>')
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        logging.info("Interfață curățată")

    def update_menu_selection(self):
        for i, element in enumerate(self.menu_buttons):
            if isinstance(element, ttk.Entry):
                if i == self.selected_menu_index:
                    element.focus_set()
                    element.configure(style="Selected.TEntry")
                else:
                    element.configure(style="TEntry")
            elif isinstance(element, tk.Button):
                if i == self.selected_menu_index:
                    element.config(bg=self.colors["success"], relief="sunken")
                else:
                    element.config(bg=self.colors["secondary"], relief="raised")

    def create_main_menu(self):
        self.clear_frame()
        title_label = tk.Label(self.root, text="QUIZ GAME", font=('Helvetica', 28, 'bold'),
                               bg=self.colors["background"], fg=self.colors["text"])
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        menu_options = [
            ("Start Game", self.start_game),
            ("Select Category", self.show_category_menu),
            ("Select Difficulty", self.show_difficulty_menu),
            ("Set Questions", self.show_total_questions_menu),
            ("Fast Quiz (5 min)", lambda: self.start_fast_quiz(300)),
            ("Fast Quiz (10 min)", lambda: self.start_fast_quiz(600)),
            ("Fast Quiz (15 min)", lambda: self.start_fast_quiz(900)),
            ("Statistics", self.show_stats),
            ("Highscores", self.show_highscores),
            ("Exit", self.on_closing)
        ]

        self.menu_buttons = []
        for i, (text, command) in enumerate(menu_options):
            btn = tk.Button(self.root, text=text, font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"],
                            fg=self.colors["text"],
                            activebackground=self.colors["success"], activeforeground=self.colors["text"],
                            relief="flat", cursor="hand2", command=command)
            btn.place(relx=0.5, rely=0.25 + i * 0.07, anchor="center", width=200)
            self.menu_buttons.append(btn)

        current_settings = f"Category: {self.categories[self.category]} | Difficulty: {self.difficulty} | Questions: {self.total_questions}"
        settings_label = tk.Label(self.root, text=current_settings, font=('Helvetica', 10),
                                  bg=self.colors["background"], fg=self.colors["text"])
        settings_label.place(relx=0.5, rely=0.94, anchor="s")  # Mutat mai jos la rely=0.94

        level_label = tk.Label(self.root, text=f"Level: {self.level} | XP: {self.experience}/{self.level_threshold}",
                               font=('Helvetica', 10), bg=self.colors["background"], fg=self.colors["text"])
        level_label.place(relx=0.5, rely=0.99, anchor="s")  # Mutat mai jos la rely=0.99

        def move_up(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_down(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_left(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_right(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def select_option(event):
            if 0 <= self.selected_menu_index < len(menu_options):
                menu_options[self.selected_menu_index][1]()

        self.selected_menu_index = 0
        self.update_menu_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)
        logging.info("Meniu principal creat")

    def show_stats(self):
        self.clear_frame()
        title_label = tk.Label(self.root, text="Statistics", font=('Helvetica', 24, 'bold'), bg=self.colors["background"], fg=self.colors["text"])
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        player_scores = [s for s in self.highscores if s["name"] == self.player_name]
        if not player_scores:
            stats_label = tk.Label(self.root, text="No statistics available. Play a game to see your stats!", font=('Helvetica', 14), bg=self.colors["background"], fg=self.colors["text"])
            stats_label.place(relx=0.5, rely=0.3, anchor="center")
        else:
            total_games = len(player_scores)
            total_questions = sum(s["questions"] for s in player_scores)
            total_correct = sum(s["score"] for s in player_scores)
            correct_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
            avg_score = total_correct / total_games
            avg_time = sum(s["time"] for s in player_scores) / total_games
            total_hints = sum(s["hints_used"] for s in player_scores)

            category_stats = {}
            for cat in self.categories:
                cat_scores = [s for s in player_scores if s["category"] == cat]
                if cat_scores:
                    cat_questions = sum(s["questions"] for s in cat_scores)
                    cat_correct = sum(s["score"] for s in cat_scores)
                    cat_percentage = (cat_correct / cat_questions * 100) if cat_questions > 0 else 0
                    category_stats[cat] = f"{cat_percentage:.2f}% ({cat_correct}/{cat_questions})"

            difficulty_stats = {}
            for diff in self.difficulties:
                diff_scores = [s for s in player_scores if s["difficulty"] == diff]
                if diff_scores:
                    diff_questions = sum(s["questions"] for s in diff_scores)
                    diff_correct = sum(s["score"] for s in diff_scores)
                    diff_percentage = (diff_correct / diff_questions * 100) if diff_questions > 0 else 0
                    difficulty_stats[diff] = f"{diff_percentage:.2f}% ({diff_correct}/{diff_questions})"

            stats_text = (
                f"Player: {self.player_name}\n"
                f"Current Level: {self.level} | XP: {self.experience}/{self.level_threshold}\n"
                f"Games Played: {total_games}\n"
                f"Correct Answers: {correct_percentage:.2f}% ({total_correct}/{total_questions})\n"
                f"Average Score: {avg_score:.2f}\n"
                f"Average Time per Game: {avg_time:.2f} seconds\n"
                f"Hints Used: {total_hints}\n"
                f"\nCategory Performance:\n"
            )
            for cat, stat in category_stats.items():
                stats_text += f"  - {self.categories[cat]}: {stat}\n"
            stats_text += "\nDifficulty Performance:\n"
            for diff, stat in difficulty_stats.items():
                stats_text += f"  - {diff.capitalize()}: {stat}\n"

            stats_label = tk.Label(self.root, text=stats_text, font=('Helvetica', 12), bg=self.colors["background"], fg=self.colors["text"], justify="left")
            stats_label.place(relx=0.5, rely=0.5, anchor="center")

        back_button = tk.Button(self.root, text="Back to Menu", font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"],
                                activebackground=self.colors["success"], activeforeground=self.colors["text"], relief="flat", cursor="hand2", command=self.create_main_menu)
        back_button.place(relx=0.5, rely=0.9, anchor="center", width=200)

        self.menu_buttons = [back_button]

        def move_up(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_down(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_left(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_right(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def select_option(event):
            if 0 <= self.selected_menu_index < len(self.menu_buttons):
                self.menu_buttons[self.selected_menu_index].invoke()

        self.selected_menu_index = 0
        self.update_menu_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)
        logging.info(f"Statistici afișate pentru jucător: {self.player_name}")

    def show_category_menu(self):
        self.clear_frame()
        title_label = tk.Label(self.root, text="SELECT CATEGORY", font=('Helvetica', 24, 'bold'), bg=self.colors["background"], fg=self.colors["text"])
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        category_list = list(self.categories.items())
        menu_options = [(name, lambda k=key: self.set_category(k)) for key, name in category_list]
        menu_options.append(("Back to Menu", self.create_main_menu))

        self.menu_buttons = []
        for i, (text, command) in enumerate(menu_options):
            btn = tk.Button(self.root, text=text, font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"],
                            activebackground=self.colors["success"], activeforeground=self.colors["text"], relief="flat", cursor="hand2", command=command)
            btn.place(relx=0.5, rely=0.25 + i * 0.07, anchor="center", width=200)
            self.menu_buttons.append(btn)

        self.status_label = tk.Label(self.root, text="", font=('Helvetica', 12), bg=self.colors["background"], fg=self.colors["error"])
        self.status_label.place(relx=0.5, rely=0.9, anchor="center")

        def move_up(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_down(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_left(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_right(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def select_option(event):
            if 0 <= self.selected_menu_index < len(menu_options):
                menu_options[self.selected_menu_index][1]()

        self.selected_menu_index = 0
        self.update_menu_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)
        logging.info("Meniu de categorii creat")

    def set_category(self, category):
        self.category = category
        self.create_main_menu()
        if self.status_label:
            self.status_label.config(text=f"Category set to: {self.categories[category]}", fg=self.colors["success"])
        self.root.update()
        time.sleep(1)
        logging.info(f"Categorie setată: {category}")

    def show_difficulty_menu(self):
        self.clear_frame()
        title_label = tk.Label(self.root, text="SELECT DIFFICULTY", font=('Helvetica', 24, 'bold'), bg=self.colors["background"], fg=self.colors["text"])
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        menu_options = [(diff, lambda d=diff: self.set_difficulty(d)) for diff in self.difficulties]
        menu_options.append(("Back to Menu", self.create_main_menu))

        self.menu_buttons = []
        for i, (text, command) in enumerate(menu_options):
            btn = tk.Button(self.root, text=text.capitalize(), font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"],
                            activebackground=self.colors["success"], activeforeground=self.colors["text"], relief="flat", cursor="hand2", command=command)
            btn.place(relx=0.5, rely=0.25 + i * 0.07, anchor="center", width=200)
            self.menu_buttons.append(btn)

        self.status_label = tk.Label(self.root, text="", font=('Helvetica', 12), bg=self.colors["background"], fg=self.colors["error"])
        self.status_label.place(relx=0.5, rely=0.9, anchor="center")

        def move_up(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_down(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_left(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_right(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def select_option(event):
            if 0 <= self.selected_menu_index < len(menu_options):
                menu_options[self.selected_menu_index][1]()

        self.selected_menu_index = 0
        self.update_menu_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)
        logging.info("Meniu de dificultate creat")

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.create_main_menu()
        if self.status_label:
            self.status_label.config(text=f"Difficulty set to: {difficulty.capitalize()}", fg=self.colors["success"])
        self.root.update()
        time.sleep(1)
        logging.info(f"Dificultate setată: {difficulty}")

    def show_total_questions_menu(self):
        self.clear_frame()
        style = ttk.Style()
        style.configure("TScale", background=self.colors["background"], troughcolor=self.colors["secondary"],
                        foreground=self.colors["text"])

        title_label = tk.Label(self.root, text="SET NUMBER OF QUESTIONS", font=('Helvetica', 24, 'bold'),
                               bg=self.colors["background"], fg=self.colors["text"])
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        slider_label = tk.Label(self.root, text=f"Number of Questions: {self.total_questions}", font=('Helvetica', 14),
                                bg=self.colors["background"], fg=self.colors["text"])
        slider_label.place(relx=0.5, rely=0.3, anchor="center")

        slider = ttk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL, length=300,
                           value=self.total_questions, style="TScale")
        slider.place(relx=0.5, rely=0.4, anchor="center")

        def update_slider_label(event=None):
            value = int(slider.get())
            slider_label.config(text=f"Number of Questions: {value}")
            self.total_questions = value

        slider.bind("<B1-Motion>", update_slider_label)
        slider.bind("<ButtonRelease-1>", update_slider_label)

        menu_options = [
            ("Set", lambda: (update_slider_label(), self.set_total_questions(self.total_questions))),
            ("Back to Menu", self.create_main_menu)
        ]

        self.menu_buttons = []
        for i, (text, command) in enumerate(menu_options):
            btn = tk.Button(self.root, text=text, font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"],
                            fg=self.colors["text"],
                            activebackground=self.colors["success"], activeforeground=self.colors["text"], relief="flat",
                            cursor="hand2", command=command)
            btn.place(relx=0.5, rely=0.5 + i * 0.07, anchor="center", width=200)
            self.menu_buttons.append(btn)

        self.status_label = tk.Label(self.root, text="", font=('Helvetica', 12), bg=self.colors["background"], fg=self.colors["error"])
        self.status_label.place(relx=0.5, rely=0.9, anchor="center")

        def move_up(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_down(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_left(event):
            if slider.get() > 1:
                slider.set(slider.get() - 1)
                update_slider_label()
            else:
                self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
                self.update_menu_selection()

        def move_right(event):
            if slider.get() < 20:
                slider.set(slider.get() + 1)
                update_slider_label()
            else:
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
                self.update_menu_selection()

        def select_option(event):
            if 0 <= self.selected_menu_index < len(menu_options):
                menu_options[self.selected_menu_index][1]()

        self.selected_menu_index = 0
        self.update_menu_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)

        logging.info("Meniu pentru setarea numărului de întrebări creat")

    def set_total_questions(self, value):
        self.total_questions = value
        self.create_main_menu()
        if self.status_label:
            self.status_label.config(text=f"Number of questions set to: {value}", fg=self.colors["success"])
        self.root.update()
        time.sleep(1)
        logging.info(f"Număr de întrebări setat: {value}")

    def start_fast_quiz(self, duration):
        self.is_fast_quiz = True
        self.fast_quiz_duration = duration
        self.start_game()
        logging.info(f"Fast quiz început cu durata: {duration} secunde")

    def start_game(self):
        self.score = 0
        self.current_question_index = 0
        self.hints_used = 0
        self.hint_indices = []
        self.incorrect_answers = []
        self.deferred_questions = []
        self.select_random_questions()
        if not self.current_questions:
            return
        self.start_time = time.time()
        self.show_question_screen()
        logging.info(f"Joc început: {self.category}, {self.difficulty}, {self.total_questions} întrebări")

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.time_left = max(0, self.fast_quiz_duration - elapsed_time)
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        self.timer_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")
        if self.time_left > 0:
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.end_game()
        logging.debug(f"Timer actualizat: {self.time_left} secunde rămase")

    def show_question_screen(self):
        if self.is_fast_quiz and (time.time() - self.start_time) >= self.fast_quiz_duration:
            self.end_game()
            return
        if not self.is_fast_quiz and self.current_question_index >= len(self.current_questions):
            self.end_game()
            return
        if self.is_fast_quiz and self.current_question_index >= len(self.current_questions):
            self.select_random_questions()
            self.current_question_index = 0
        self.clear_frame()

        current_q = self.current_questions[self.current_question_index]
        question = current_q["question"]
        answer = current_q["answer"]
        hidden_answer = self.display_hidden_answer(revealed_indices=self.hint_indices)

        player_info = f"{self.player_name} | Score: {self.score} | Hints: {self.max_hints - self.hints_used} | Level: {self.level}"
        self.player_label = tk.Label(self.root, text=player_info, font=('Helvetica', 14), bg=self.colors["background"], fg=self.colors["text"])
        self.player_label.place(relx=0.02, rely=0.02, anchor="nw")

        question_info = f"Question {self.current_question_index + 1}" + (f"/{len(self.current_questions)}" if not self.is_fast_quiz else "")
        question_label = tk.Label(self.root, text=question_info, font=('Helvetica', 14), bg=self.colors["background"], fg=self.colors["text"])
        question_label.place(relx=0.98, rely=0.02, anchor="ne")

        progress = (self.current_question_index + 1) / len(self.current_questions) * 100 if not self.is_fast_quiz else (self.fast_quiz_duration - self.time_left) / self.fast_quiz_duration * 100
        progress_bar = ttk.Progressbar(self.root, length=600, mode='determinate', maximum=100, value=progress)
        progress_bar.place(relx=0.5, rely=0.1, anchor="center")

        question_label = tk.Label(self.root, text=f"{question}", font=('Helvetica', 16), bg=self.colors["background"], fg=self.colors["text"], wraplength=650, justify="center")
        question_label.place(relx=0.5, rely=0.2, anchor="center")

        answer_text = f"Answer ({len(answer)} letters): {hidden_answer}"
        self.answer_label = tk.Label(self.root, text=answer_text, font=('Helvetica', 18), bg=self.colors["background"], fg=self.colors["text"])
        self.answer_label.place(relx=0.5, rely=0.35, anchor="center")

        input_frame = tk.Frame(self.root, bg=self.colors["background"])
        input_frame.place(relx=0.5, rely=0.45, anchor="center")

        input_label = tk.Label(input_frame, text="Your Answer:", font=('Helvetica', 14), bg=self.colors["background"], fg=self.colors["text"])
        input_label.pack(side="left", padx=(0, 10))

        self.answer_entry = ttk.Entry(input_frame, font=('Helvetica', 14), width=25)
        self.answer_entry.pack(side="left", fill="x", expand=True)

        button_frame = tk.Frame(self.root, bg=self.colors["background"])
        button_frame.place(relx=0.5, rely=0.55, anchor="center")

        check_button = tk.Button(button_frame, text="Check Answer", font=('Helvetica', 12, 'bold'), bg=self.colors["success"], fg=self.colors["text"],
                                 activebackground=self.colors["secondary"], activeforeground=self.colors["text"], command=self.check_answer, relief="flat", cursor="hand2")
        check_button.pack(side="left", fill="x", expand=True, padx=5)

        skip_button = tk.Button(button_frame, text="Skip Question", font=('Helvetica', 12, 'bold'), bg=self.colors["accent"], fg=self.colors["text"],
                                activebackground=self.colors["secondary"], activeforeground=self.colors["text"], command=self.skip_question, relief="flat", cursor="hand2")
        skip_button.pack(side="left", fill="x", expand=True, padx=5)

        back_button = tk.Button(button_frame, text="Back to Menu", font=('Helvetica', 12, 'bold'), bg=self.colors["error"], fg=self.colors["text"],
                                activebackground=self.colors["secondary"], activeforeground=self.colors["text"], command=self.create_main_menu, relief="flat", cursor="hand2")
        back_button.pack(side="left", fill="x", expand=True, padx=5)

        hint_frame = tk.Frame(self.root, bg=self.colors["background"])
        hint_frame.place(relx=0.5, rely=0.65, anchor="center")

        hint1_button = tk.Button(hint_frame, text="Hint: Half Letters", font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"],
                                 activebackground=self.colors["success"], activeforeground=self.colors["text"], command=lambda: self.show_hint(1), relief="flat", cursor="hand2")
        hint1_button.pack(side="left", fill="x", expand=True, padx=5)

        hint2_button = tk.Button(hint_frame, text="Hint: First Letter", font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"],
                                 activebackground=self.colors["success"], activeforeground=self.colors["text"], command=lambda: self.show_hint(2), relief="flat", cursor="hand2")
        hint2_button.pack(side="left", fill="x", expand=True, padx=5)

        clear_button = tk.Button(hint_frame, text="Clear Answer", font=('Helvetica', 12, 'bold'), bg=self.colors["error"], fg=self.colors["text"],
                                 activebackground=self.colors["secondary"], activeforeground=self.colors["text"], command=lambda: self.answer_entry.delete(0, tk.END), relief="flat", cursor="hand2")
        clear_button.pack(side="left", fill="x", expand=True, padx=5)

        if self.is_fast_quiz:
            self.timer_label = tk.Label(self.root, text="Time Left: 00:00", font=('Helvetica', 14), bg=self.colors["background"], fg=self.colors["error"])
            self.timer_label.place(relx=0.5, rely=0.9, anchor="center")
            self.update_timer()

        self.menu_buttons = [self.answer_entry, check_button, skip_button, back_button, hint1_button, hint2_button, clear_button]

        def move_up(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_down(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_left(event):
            if self.menu_buttons[self.selected_menu_index] == self.answer_entry:
                cursor_pos = self.answer_entry.index(tk.INSERT)
                if cursor_pos > 0:
                    self.answer_entry.icursor(cursor_pos - 1)
            else:
                self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
                self.update_menu_selection()

        def move_right(event):
            if self.menu_buttons[self.selected_menu_index] == self.answer_entry:
                cursor_pos = self.answer_entry.index(tk.INSERT)
                if cursor_pos < len(self.answer_entry.get()):
                    self.answer_entry.icursor(cursor_pos + 1)
            else:
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
                self.update_menu_selection()

        def select_option(event):
            element = self.menu_buttons[self.selected_menu_index]
            if isinstance(element, ttk.Entry):
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
                self.update_menu_selection()
            elif isinstance(element, tk.Button):
                element.invoke()

        self.selected_menu_index = 0
        self.update_menu_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)
        logging.info(f"Ecran întrebare afișat: Întrebarea {self.current_question_index + 1}")

    def skip_question(self):
        if self.hints_used >= self.max_hints:
            messagebox.showwarning("Warning", "You have used all available hints!")
            logging.warning("Attempt to skip question without available hints")
            return
        current_q = self.current_questions[self.current_question_index]
        self.deferred_questions.append(current_q)
        self.hints_used += 1
        if self.player_label:
            self.player_label.config(text=f"{self.player_name} | Score: {self.score} | Hints: {self.max_hints - self.hints_used} | Level: {self.level}")
        messagebox.showinfo("Skipped", "Question skipped. You will answer it at the end.")
        self.current_question_index += 1
        self.hint_indices = []
        self.show_question_screen()
        logging.info(f"Question skipped: {current_q['question']}")

    def check_answer(self):
        current_q = self.current_questions[self.current_question_index]
        user_answer = self.answer_entry.get().strip()
        if not user_answer:
            messagebox.showwarning("Warning", "Please enter an answer!")
            logging.warning("Attempt to check answer without input")
            return
        correct_answer = current_q["answer"]
        normalized_user_answer = self.normalize_text(user_answer)
        normalized_correct_answer = self.normalize_text(correct_answer)
        logging.info(f"User answer: {normalized_user_answer}, Correct answer: {normalized_correct_answer}")
        if normalized_user_answer == normalized_correct_answer:
            self.score += 1
            xp_earned = 10
            if self.difficulty == "mediu":
                xp_earned += 5
            elif self.difficulty == "greu":
                xp_earned += 10
            if self.is_fast_quiz:
                xp_earned += 5
            self.experience += xp_earned
            messagebox.showinfo("Correct!", f"Correct answer! You earned {xp_earned} XP!")
            self.play_sound(self.correct_sound)
            while self.experience >= self.level_threshold:
                self.level += 1
                self.experience -= self.level_threshold
                self.level_threshold = int(self.level_threshold * 1.5)
                self.max_hints += 1
                messagebox.showinfo("New Level!", f"You reached Level {self.level}! Reward: +1 hint (total: {self.max_hints})")
                self.save_users()
            logging.info(f"Correct answer: {current_q['question']}, XP earned: {xp_earned}")
        else:
            messagebox.showerror("Incorrect!", f"Wrong answer! The correct answer was: {correct_answer}")
            self.play_sound(self.incorrect_sound)
            self.incorrect_answers.append(current_q)
            logging.info(f"Incorrect answer: {current_q['question']}, Answer given: {user_answer}")
        self.current_question_index += 1
        self.hint_indices = []
        self.show_question_screen()

    def end_game(self):
        self.end_time = time.time()
        time_taken = round(self.end_time - self.start_time, 2)
        self.save_highscore()
        self.save_users()
        self.play_sound(self.game_over_sound)
        if self.deferred_questions and (not self.is_fast_quiz or self.time_left > 0):
            messagebox.showinfo("Deferred Questions", "You will now answer the skipped questions.")
            self.current_questions = self.deferred_questions
            self.deferred_questions = []
            self.current_question_index = 0
            self.is_fast_quiz = False
            self.show_question_screen()
            logging.info("Switching to deferred questions")
            return
        result_message = (
            f"Congratulations, {self.player_name}!\n"
            f"Final Score: {self.score}/{self.current_question_index}\n"
            f"Total Time: {time_taken} seconds\n"
            f"Hints Used: {self.hints_used}\n"
            f"Level: {self.level} | XP: {self.experience}/{self.level_threshold}\n"
        )
        if self.incorrect_answers:
            result_message += "\nYou got some questions wrong. Press OK to review them."
            messagebox.showinfo("Final Result", result_message)
            self.start_review_incorrect_answers()
            logging.info("Game ended, proceeding to review incorrect answers")
        else:
            messagebox.showinfo("Final Result", result_message)
            self.create_main_menu()
            logging.info("Game ended, returning to menu")

    def start_review_incorrect_answers(self):
        self.current_questions = self.incorrect_answers
        self.incorrect_answers = []
        self.current_question_index = 0
        self.is_fast_quiz = False
        self.show_question_screen()
        logging.info("Started reviewing incorrect answers")

    def show_hint(self, hint_type):
        if self.hints_used >= self.max_hints:
            messagebox.showwarning("Warning", "You have used all available hints!")
            logging.warning("Attempt to use hint without available hints")
            return
        current_q = self.current_questions[self.current_question_index]
        answer = current_q["answer"]
        if hint_type == 1:
            hidden_answer = self.reveal_half_letters(answer)
        elif hint_type == 2:
            hidden_answer = self.reveal_first_letter(answer)
        else:
            messagebox.showerror("Error", "Invalid hint type!")
            logging.error(f"Invalid hint requested: {hint_type}")
            return
        self.hints_used += 1
        self.answer_label.config(text=f"Answer ({len(answer)} letters): {hidden_answer}")
        if self.player_label:
            self.player_label.config(text=f"{self.player_name} | Score: {self.score} | Hints: {self.max_hints - self.hints_used} | Level: {self.level}")
        self.play_sound(self.hint_sound)
        logging.info(f"Hint used: type {hint_type} for question {current_q['question']}")

    def show_highscores(self, show_player_only=False):
        self.clear_frame()
        title_label = tk.Label(self.root, text=f"{'MY HIGHSCORES' if show_player_only else 'ALL HIGHSCORES'}",
                               font=('Helvetica', 24, 'bold'), bg=self.colors["background"],
                               fg=self.colors["text"])
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        columns = ("Name", "Score", "Time", "Category", "Difficulty", "Date")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8,
                            style="Custom.Treeview")  # Redus height la 8 pentru a face loc butoanelor
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        scores_to_show = [score for score in self.highscores if
                          score['name'] == self.player_name] if show_player_only else self.highscores
        for i, score in enumerate(scores_to_show, 1):
            category_name = self.categories.get(score['category'], score['category'])
            tree.insert("", "end", values=(
                score['name'],
                score['score'],
                f"{score['time']} sec",
                category_name,
                score['difficulty'],
                score['date']
            ))
        tree.place(relx=0.5, rely=0.45, anchor="center")  # Mutat mai sus la rely=0.45

        btn_frame = tk.Frame(self.root, bg=self.colors["background"], highlightthickness=0)
        btn_frame.place(relx=0.5, rely=0.75, anchor="center")  # Mutat mai sus la rely=0.75

        toggle_button = tk.Button(btn_frame, text="Show Only My Scores" if not show_player_only else "Show All Scores",
                                  font=('Helvetica', 12, 'bold'), bg=self.colors["secondary"], fg=self.colors["text"],
                                  activebackground=self.colors["success"], activeforeground=self.colors["text"],
                                  command=lambda: self.show_highscores(not show_player_only), relief="flat",
                                  cursor="hand2",
                                  width=20)
        toggle_button.pack(side="left", padx=10)

        back_button = tk.Button(btn_frame, text="Back to Menu", font=('Helvetica', 12, 'bold'),
                                bg=self.colors["secondary"],
                                fg=self.colors["text"], activebackground=self.colors["success"],
                                activeforeground=self.colors["text"],
                                command=self.create_main_menu, relief="flat", cursor="hand2", width=20)
        back_button.pack(side="left", padx=10)

        self.menu_buttons = [toggle_button, back_button]

        def move_up(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_down(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_left(event):
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def move_right(event):
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_buttons)
            self.update_menu_selection()

        def select_option(event):
            if 0 <= self.selected_menu_index < len(self.menu_buttons):
                self.menu_buttons[self.selected_menu_index].invoke()

        self.selected_menu_index = 0
        self.update_menu_selection()
        self.root.bind('<Up>', move_up)
        self.root.bind('<Down>', move_down)
        self.root.bind('<Left>', move_left)
        self.root.bind('<Right>', move_right)
        self.root.bind('<Return>', select_option)
        logging.info(f"Highscores displayed: {'player only' if show_player_only else 'all scores'}")

if __name__ == "__main__":
    if platform.system() == "Emscripten":
        import asyncio
        async def main():
            root = tk.Tk()
            app = QuizGame(root)
            while True:
                root.update()
                await asyncio.sleep(1.0 / 60)
        asyncio.ensure_future(main())
    else:
        root = tk.Tk()
        app = QuizGame(root)
        root.mainloop()  # Add this line
