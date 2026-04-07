import cv2
import mediapipe as mp

class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils


    def get_finger_position(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.hands.process(rgb)

        h, w, _ = frame.shape

        if result.multi_hand_landmarks:

            for hand in result.multi_hand_landmarks:

                index_tip = hand.landmark[8]

                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                self.mp_draw.draw_landmarks(
                    frame, hand, self.mp_hands.HAND_CONNECTIONS
                )

                return x, y

        return None