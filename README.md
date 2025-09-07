# 🦖 Dino Game

A **Chrome Dino-style** game developed in **Python**, with support for running both via script and as a compiled `.exe` for Windows.  
This project was created for learning and fun, using **Pygame** and custom graphic resources.

---

## 🚀 Technologies Used
- **Python 3.12+**
- **Pygame** (for graphics and game logic)
- **cx_Freeze** (to generate the `.exe`)
- **Spritesheets** for animations

---

## 📂 Project Structure

dino/
├── dino.py # Main game script
├── dino2.py # Alternative version of the game
├── setup.py # Setup script for build
├── build/ # Folder containing compiled version
│ ├── exe.win-amd64-3.12/
│ │ ├── dino.exe # Windows executable
│ │ └── imagem/ # Game sprites
└── assets/ (future place to organize images if needed)

yaml
Copiar código

---

## 🕹️ How to Play

### 🔹 Running with Python
1. Make sure you have **Python 3.12+** installed.  
2. Install dependencies:
   ```bash
   pip install pygame
   ```
Run the game:


 ```bash
python dino.py
 ```
🔹 Running on Windows (compiled version)
Go to the folder:

```bash
build/exe.win-amd64-3.12/
```
Double-click dino.exe.


Enjoy the game 🦖!

🎮 Controls
Spacebar → Jump

Arrow Down → Duck

ESC → Exit the game

📸 Demo
👉 Here you can add screenshots or even a GIF of gameplay.
Example of adding a GIF to the README:

markdown
Copiar código
![Dino Game Demo](path/to/your_gif.gif)

🛠️ Build the Executable
If you want to recreate the .exe yourself:

```bash
Copiar código
python setup.py build
The executable will be generated inside the build/ folder.
```

👤 Author
Victor Miranda

🌐 LinkedIn: https://www.linkedin.com/in/victor-miranda-5005ab304

💻 GitHub: @victor-kauan-coder
