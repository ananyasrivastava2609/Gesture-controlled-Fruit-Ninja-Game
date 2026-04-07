import cv2
import math
import random
from hand_tracker import HandTracker
from fruit import Fruit
from bomb import Bomb

cap = cv2.VideoCapture(0)

tracker = HandTracker()

def reset_game():
    return {
        "fruits": [],
        "bombs": [],
        "score": 0,
        "missed": 0,
        "frame_count": 0,
        "trail_points": [],
        "game_over": False
    }

state = reset_game()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # --- GAME OVER SCREEN ---
    if state["game_over"]:
        cv2.putText(frame, "GAME OVER", (width // 2 - 160, height // 2 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.putText(frame, f"Final Score: {state['score']}", (width // 2 - 140, height // 2 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(frame, "Press R to Restart", (width // 2 - 140, height // 2 + 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 200, 200), 2)
        cv2.imshow("Fruit Ninja", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            state = reset_game()
        elif key == 27:
            break
        continue  # skip all game logic below

    # --- SPAWN ---
    state["frame_count"] += 1
    if state["frame_count"] % 17 == 0 and len(state["fruits"]) + len(state["bombs"]) < 5:
        if random.random() < 0.10:
            state["bombs"].append(Bomb(width, height))
        else:
            state["fruits"].append(Fruit(width, height))

    # --- HAND TRACKING ---
    finger = tracker.get_finger_position(frame)

    if finger:
        state["trail_points"].append(finger)
        if len(state["trail_points"]) > 10:
            state["trail_points"].pop(0)
    else:
        state["trail_points"].clear()

    for i in range(1, len(state["trail_points"])):
        cv2.line(frame, state["trail_points"][i-1], state["trail_points"][i], (255, 0, 0), 5)

    # --- FRUITS ---
    for fruit in state["fruits"][:]:
        fruit.move()
        fruit.draw(frame)

        if finger:
            fx, fy = finger
            distance = math.hypot(fx - fruit.x, fy - fruit.y)
            if distance < fruit.radius:
                state["fruits"].remove(fruit)
                state["score"] += 1
                continue  # skip the off-screen check for this fruit

        if fruit.y > height + 80:
            state["fruits"].remove(fruit)
            state["missed"] += 1

    # --- BOMBS ---
    for bomb in state["bombs"][:]:
        bomb.move()
        bomb.draw(frame)

        if finger:
            fx, fy = finger
            distance = math.hypot(fx - bomb.x, fy - bomb.y)
            if distance < bomb.radius:
                state["game_over"] = True
                break  # no need to check other bombs

        if bomb.y > height + 80:
            state["bombs"].remove(bomb)

    # --- HUD ---
    cv2.putText(frame, f"Score: {state['score']}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Missed: {state['missed']}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Fruit Ninja", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()