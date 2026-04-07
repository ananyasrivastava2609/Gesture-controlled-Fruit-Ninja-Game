import random
import cv2


class Fruit:
    def __init__(self, width, height):
        self.x = random.randint(50, width - 50) # start somewhere in the middle
        self.y = height + 50 # start at bottom (0 for top)
        self.radius = 30 # for collision detection
        self.vx = random.randint(-4, 4)   # horizontal velocity
        self.vy = random.randint(-22, -16)  # initial upward speed throw
        self.gravity = 0.6

        # load fruit images
        self.images = [
            cv2.imread("assets/fruits/apple.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/banana.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/orange.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/grapes.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/avocado.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/dragonfruit.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/pineapple.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/kiwi.png", cv2.IMREAD_UNCHANGED),
            cv2.imread("assets/fruits/blueberry.png", cv2.IMREAD_UNCHANGED)
        ]
        
        # remove images that failed to load
        self.images = [img for img in self.images if img is not None]
        
        self.image = random.choice(self.images)

         # resize for display
        self.image = cv2.resize(self.image, (250, 250))

    def move(self): # update position based on velocity and gravity
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity 

    def draw(self, frame): 
        h, w, _ = self.image.shape

        x1 = int(self.x - w / 2)
        y1 = int(self.y - h / 2)
        x2 = x1 + w
        y2 = y1 + h


        frame_h, frame_w = frame.shape[:2]
        if x2 < 0 or x1 > frame_w or y2 < 0 or y1 > frame_h:
            return 
        
        # clip coordinates to frame boundaries
        rx1, ry1 = max(x1, 0), max(y1, 0)
        rx2, ry2 = min(x2, frame_w), min(y2, frame_h)

        # corresponding crop on the fruit image
        ix1 = rx1 - x1
        iy1 = ry1 - y1
        ix2 = ix1 + (rx2 - rx1)
        iy2 = iy1 + (ry2 - ry1)

        roi = frame[ry1:ry2, rx1:rx2]
        fruit_rgb = self.image[iy1:iy2, ix1:ix2, :3]
        alpha = self.image[iy1:iy2, ix1:ix2, 3] / 255.0

        for c in range(3):
            roi[:, :, c] = (1 - alpha) * roi[:, :, c] + alpha * fruit_rgb[:, :, c]