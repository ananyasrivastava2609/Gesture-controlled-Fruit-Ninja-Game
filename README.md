# 🍉 Gesture-Controlled Fruit Ninja
A real-time computer vision game built with OpenCV and MediaPipe. Slice fruits using your index finger via webcam — no touch screen or external hardware required.

---

## 📌 Overview

This project replicates the core mechanics of Fruit Ninja using hand gesture recognition. The webcam captures your hand in real time, MediaPipe tracks your fingertip, and OpenCV renders fruits flying across the screen. Slice fruits to score points — but hit a bomb and it's game over.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| OpenCV (`cv2`) | Frame capture, rendering, HUD |
| MediaPipe | Real-time hand landmark detection |
| Python `random` | Fruit spawn randomization |
| Python `math` | Euclidean distance collision detection |

---

## 📁 Project Structure

```
fruit-ninja-cv/
│
├── main.py               # Game loop and orchestrator
├── fruit.py              # Fruit object (physics, drawing)
├── bomb.py               # Bomb object (physics, drawing)
├── hand_tracker.py       # MediaPipe hand tracking wrapper
│
└── assets/
    ├── fruits/
    │   ├── apple.png
    │   ├── banana.png
    │   ├── orange.png
    │   ├── grapes.png
    │   ├── avocado.png
    │   ├── dragonfruit.png
    │   ├── pineapple.png
    │   ├── kiwi.png
    │   └── blueberry.png
    └── bombs/
        └── bomb.png
```

---

## ⚙️ How It Works

### Game Loop (main.py)
Every frame runs this cycle:
1. Capture webcam frame
2. Flip frame horizontally (mirror effect)
3. Detect fingertip position via MediaPipe
4. Spawn fruits/bombs on a timer
5. Move and draw all active objects
6. Check collisions between fingertip and objects
7. Update score/missed count
8. Render HUD and display frame

### Physics Engine
Each fruit and bomb follows projectile motion:
```
x += vx
y += vy
vy += gravity
```
This produces a natural parabolic arc — fruits launch upward from below the screen and fall back down.

### Collision Detection
Uses Euclidean distance between the fingertip and object center:
```
distance = √((fx - obj.x)² + (fy - obj.y)²)
if distance < obj.radius → slice!
```

### Alpha Blending (Transparent PNGs)
Fruits and bombs are PNG images with transparency. They are blended onto the webcam frame using per-pixel alpha compositing:
```
output = (1 - alpha) × background + alpha × fruit_pixel
```

---

## 🎮 Features

### ✅ Implemented
- **Hand Tracking** — MediaPipe detects index fingertip in real time
- **Fruit System** — 9 fruit types, random spawn position and velocity
- **Projectile Physics** — Parabolic arc with gravity simulation
- **Collision Detection** — Distance-based slicing
- **Slash Trail** — Visual trail follows fingertip movement
- **Bomb System** — ~5–10% spawn chance, game over on hit
- **Scoring System** — Score on slice, missed count on drop
- **Game Over Screen** — Displays final score, press R to restart
- **Modular Architecture** — Separate files for each object type

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/fruit-ninja-cv.git
cd fruit-ninja-cv
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install opencv-python mediapipe
```

### 4. Add fruit assets
Place PNG images (with transparency) inside `assets/fruits/` and `assets/bombs/` following the filenames listed in the project structure above.

### 5. Run the game
```bash
python main.py
```

---

## 🎯 Controls

| Action | Control |
|---|---|
| Slice a fruit | Move index finger through it |
| Avoid bomb | Don't touch the bomb |
| Restart after game over | Press `R` |
| Quit | Press `Esc` |

---

## 🔧 Tuning Parameters

| Parameter | File | Variable | Effect |
|---|---|---|---|
| Spawn frequency | `main.py` | `frame_count % 45` | Lower = more frequent |
| Max objects on screen | `main.py` | `< 8` | Higher = more crowded |
| Fruit speed | `fruit.py` | `self.vy = random.randint(-35, -25)` | More negative = faster |
| Bomb probability | `main.py` | `random.random() < 0.05` | Higher = more bombs |
| Bomb size | `bomb.py` | `cv2.resize(self.image, (80, 80))` | Adjust dimensions |
| Collision sensitivity | `fruit.py` / `bomb.py` | `self.radius` | Higher = easier to hit |

---

## 🐛 Key Bugs Fixed

**Fruits appearing mid-screen instead of rising from bottom**
- Cause: `draw()` skipped rendering when `y1 < 0`, blocking visibility while fruit entered from below
- Fix: Only skip rendering when object is completely outside frame; clip image for partial visibility

**Crash on double fruit removal**
- Cause: A sliced fruit could be removed again by the off-screen check in the same loop iteration
- Fix: Added `continue` after slicing to skip the off-screen check for that fruit

**Windows path SyntaxError**
- Cause: Backslashes in file paths interpreted as Unicode escape sequences
- Fix: Use relative paths (`assets/bombs/bomb.png`) consistent across all files


---

## 👩‍💻 Author

Built as a Computer Vision project using Python, OpenCV, and MediaPipe.