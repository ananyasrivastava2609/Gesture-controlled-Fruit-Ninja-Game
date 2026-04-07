import cv2
import random

class Bomb:
    def __init__(self, width, height):
        self.x = random.randint(50, width - 50)
        self.y = height + 50
        self.radius = 20
        self.vx = random.randint(-4, 4)
        self.vy = random.randint(-28, -20)
        self.gravity = 0.6

        self.image = cv2.imread("assets/bombs/bomb.png", cv2.IMREAD_UNCHANGED)

        if self.image is not None:
            self.image = cv2.resize(self.image, (100, 100))

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity

    def draw(self, frame):
        if self.image is None:
            return

        h, w, _ = self.image.shape

        x1 = int(self.x - w / 2)
        y1 = int(self.y - h / 2)
        x2 = x1 + w
        y2 = y1 + h

        frame_h, frame_w = frame.shape[:2]

        if x2 < 0 or x1 > frame_w or y2 < 0 or y1 > frame_h:
            return

        # clip to frame boundaries
        rx1, ry1 = max(x1, 0), max(y1, 0)
        rx2, ry2 = min(x2, frame_w), min(y2, frame_h)

        ix1 = rx1 - x1
        iy1 = ry1 - y1
        ix2 = ix1 + (rx2 - rx1)
        iy2 = iy1 + (ry2 - ry1)

        roi = frame[ry1:ry2, rx1:rx2]
        bomb_rgb = self.image[iy1:iy2, ix1:ix2, :3]
        alpha = self.image[iy1:iy2, ix1:ix2, 3] / 255.0

        for c in range(3):
            roi[:, :, c] = (1 - alpha) * roi[:, :, c] + alpha * bomb_rgb[:, :, c]