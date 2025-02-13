import cv2
import mediapipe as mp
import os
import time
import math


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


mp_drawing = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)


pinch_threshold = 0.3  
min_distance_for_zero_volume = 0.05  


cv2.namedWindow('Hand Tracking')
cv2.createTrackbar('Pinch Threshold', 'Hand Tracking', 30, 100, lambda x: None)  
cv2.createTrackbar('Detection Threshold', 'Hand Tracking', 5, 100, lambda x: None)  
cv2.createTrackbar('Max Distance', 'Hand Tracking', 50, 100, lambda x: None)  

def set_volume(volume_percentage):
    """Set the system volume based on the percentage (0-100)."""
    volume_percentage = max(0, min(100, volume_percentage))
    os.system(f"osascript -e 'set volume output volume {volume_percentage}'")

def skip_song(direction):
    """Simulate skipping or going back a song."""
    if direction == "next":
        print("Skipping to the next song...")
    elif direction == "previous":
        print("Going back to the previous song...")

def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def is_hand_open(hand_landmarks):
    """Check if the hand is open based on finger angles and distances."""
    
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    
    thumb_index_distance = euclidean_distance(thumb_tip, index_tip)
    index_middle_distance = euclidean_distance(index_tip, middle_tip)
    middle_ring_distance = euclidean_distance(middle_tip, ring_tip)
    ring_pinky_distance = euclidean_distance(ring_tip, pinky_tip)

    
    open_threshold = 0.1  

    
    return (thumb_index_distance > open_threshold and
            index_middle_distance > open_threshold and
            middle_ring_distance > open_threshold and
            ring_pinky_distance > open_threshold)

def is_pinch_between_hands(hand_landmarks1, hand_landmarks2):
    """Check if the hands are pinching and return pinch distance and points."""
    thumb_tip = hand_landmarks1.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks2.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    
    pinch_distance = euclidean_distance(thumb_tip, index_tip)
    return pinch_distance, thumb_tip, index_tip  

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    
    image = cv2.flip(image, 1)

    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    
    results_hands = hands.process(image_rgb)

    
    pinch_threshold = cv2.getTrackbarPos('Pinch Threshold', 'Hand Tracking') / 100.0  
    detection_threshold = cv2.getTrackbarPos('Detection Threshold', 'Hand Tracking') / 100.0  
    max_distance = cv2.getTrackbarPos('Max Distance', 'Hand Tracking') / 100.0  

    
    if results_hands.multi_hand_landmarks:
        hands_landmarks = results_hands.multi_hand_landmarks

        
        if len(hands_landmarks) >= 2:
        
                    
                    cv2.putText(image, f'Volume: {int(volume_percentage)}%', 
                                (int((thumb_x + index_x) / 2) - 50, int((thumb_y + index_y) / 2) - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        
        for hand_landmarks in hands_landmarks:    
            if is_hand_open(hands_landmarks[0]):
                print("Hand is open, disabling pinch gesture.")
                continue  

            pinch_distance, thumb_tip, index_tip = is_pinch_between_hands(hands_landmarks[0], hands_landmarks[1])

            
            if pinch_distance < detection_threshold:  
                
                if pinch_distance < min_distance_for_zero_volume:
                    volume_percentage = 0  
                else:
                    volume_percentage = max(0, min(100, ((pinch_distance - min_distance_for_zero_volume) / (pinch_threshold - min_distance_for_zero_volume)) * 100))  
                set_volume(volume_percentage)
                print(f"Volume set to: {volume_percentage}%")

                
                if pinch_distance < pinch_threshold:  
                    thumb_x, thumb_y = int(thumb_tip.x * image.shape[1]), int(thumb_tip.y * image.shape[0])
                    index_x, index_y = int(index_tip.x * image.shape[1]), int(index_tip.y * image.shape[0])
                    cv2.line(image, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 2)  

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    
    cv2.imshow('Hand Tracking', image)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break


cap.release()
cv2.destroyAllWindows()