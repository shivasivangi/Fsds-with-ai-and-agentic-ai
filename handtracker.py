import cv2
import mediapipe as mp
import math
from collections import deque

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Simple utility: distance between two normalized landmarks
def landmark_distance(lm1, lm2, image_width, image_height):
    x1, y1 = int(lm1.x * image_width), int(lm1.y * image_height)
    x2, y2 = int(lm2.x * image_width), int(lm2.y * image_height)
    return math.hypot(x2 - x1, y2 - y1)

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5
) as hands:

    # For smoothing a simple "index up" gesture over frames
    index_up_history = deque(maxlen=8)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # draw landmarks + connections
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
                )

                # Example: determine if index finger is up (simple heuristic)
                # Landmark indices: 5 = index_finger_mcp, 6 = index_finger_pip, 7 = dip, 8 = tip
                lm = hand_landmarks.landmark
                index_tip = lm[8]
                index_pip = lm[6]
                wrist = lm[0]

                # Compare y (remember: origin top-left, so smaller y is higher)
                index_up = index_tip.y < index_pip.y and index_tip.y < lm[5].y
                index_up_history.append(index_up)

                # If majority of recent frames show index up -> gesture detected
                if sum(index_up_history) > len(index_up_history) * 0.6:
                    cv2.putText(frame, 'INDEX UP', (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 2, cv2.LINE_AA)

                # Small example: compute distance between thumb tip (4) and index tip (8)
                d = landmark_distance(lm[4], lm[8], w, h)
                cv2.putText(frame, f'D:{int(d)}', (10,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200,200,0), 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC to quit
            break

cap.release()
cv2.destroyAllWindows()
