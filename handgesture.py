import cv2
import mediapipe as mp
import pyautogui
from math import sqrt

# Mediapipe Hands setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Global flag for gesture control
gesture_control_active = False

def stop_gesture_control():
    """Stops the hand gesture control."""
    global gesture_control_active
    gesture_control_active = False
    print("Hand gesture control stopped.")

def hand_gesture_control():
    """Controls the mouse using hand gestures."""
    global gesture_control_active
    gesture_control_active = True

    cap = cv2.VideoCapture(0)

    try:
        while gesture_control_active:
            success, frame = cap.read()
            if not success:
                break

            # Flip the frame horizontally for a mirror-like view
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape

            # Convert the frame color to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks on the hand
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Get coordinates for index finger (tip) and thumb (tip)
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                    # Convert normalized coordinates to pixel values
                    ix, iy = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)
                    tx, ty = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)

                    # Map index finger coordinates to screen dimensions
                    screen_x = int(index_finger_tip.x * screen_width)
                    screen_y = int(index_finger_tip.y * screen_height)

                    # Move mouse pointer
                    pyautogui.moveTo(screen_x, screen_y)

                    # Check distance between index finger and thumb
                    distance = sqrt((ix - tx) ** 2 + (iy - ty) ** 2)

                    # Perform a click if fingers are close enough
                    if distance < 30:  # Adjust threshold as needed
                        pyautogui.click()

            # Display the video feed with landmarks
            cv2.imshow("Hand Gesture Control", frame)

            # Break the loop on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_gesture_control()
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
