import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

while cap.isOpened():
  success, frame = cap.read()
  if not success:
    print("ویب کیم تک رسائی نہیں ہو سکی۔")
    break
  frame = cv2.flip(frame, 1)
  rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

  # ہینڈ پروسیسنگ
  result = hands.process(rgb_frame)
  gesture_text = "Searching..."

  if result.multi_hand_landmarks:
    for hand_landmarks in result.multi_hand_landmarks:
      mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

      landmarks = hand_landmarks.landmark
      tip_ids = [8, 12, 16, 20]
      mcp_ids = [5, 9, 13, 17]

      fingers_up = 0
      for i in range(4):
        if landmarks[tip_ids[i]].y < landmarks[mcp_ids[i]].y:
          fingers_up += 1
      if fingers_up >= 4:
        gesture_text = "Open Palm"
      elif fingers_up == 0:
        gesture_text = "Fist"
      else:
        gesture_text = "Gesture Detected"
  cv2.putText(
      frame,
      f"Gesture: {gesture_text}",
      (30, 50),
      cv2.FONT_HERSHEY_SIMPLEX,
      1,
      (0, 255, 0),
      2,
  )

  cv2.imshow("Syntecxhub - Hand Gesture Recognition", frame)
  if cv2.waitKey(1) & 0xFF == ord("q"):
    break

cap.release()
cv2.destroyAllWindows()