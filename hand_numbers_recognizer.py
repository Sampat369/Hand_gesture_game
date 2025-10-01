import cv2
import mediapipe as mp
import random
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Finger indices and their corresponding landmarks
FINGERS = {
    "Thumb": (mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.THUMB_CMC),
    "Index": (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.INDEX_FINGER_MCP),
    "Middle": (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP),
    "Ring": (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_MCP),
    "Pinky": (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP, mp_hands.HandLandmark.PINKY_MCP)
}

# Start webcam
cap = cv2.VideoCapture(0)
play=True
repeated=False
u_score=0
c_score=0
result=""
start_time=time.time()
while cap.isOpened():
    
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    if play==True:
        period=time.time()-start_time
        if period>0 and period<4:
            cv2.putText(frame, 'Rock', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if period>2 and period<4:
            cv2.putText(frame, 'Paper....', (100+50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if period>4:
            play=False
            do=True
            random_number=random.randint(0,2)
            if random_number==0:
                c_sign="Rock"
            elif random_number==1:
                c_sign="Scissors"   
            else:
                c_sign="Paper"
            start_time=time.time()

    if play==False and time.time()-start_time>1.5:
        
        cv2.putText(frame,c_sign, (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
        if sign =="Invalid" or repeated:
                cv2.putText(frame,"Make a move!!!,try again", (110, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                repeated=True
                if time.time()-start_time>3:
                  start_time=time.time()-0.1
                  play=True
                  repeated=False
        
        elif time.time()-start_time>3:
            if c_sign==sign and do:
                result="It's a Tie"
                do=False

            elif ((c_sign=="Rock" and sign=="Scissors") or (c_sign=="Scissors" and sign=="Paper") or (c_sign=="Paper" and sign=="Rock")) and do:
                result="Ha Ha!,I Win"
                c_score+=1
                do=False

            elif do and ((sign=="Rock" and c_sign=="Scissors") or (sign=="Scissors" and c_sign=="Paper") or (sign=="Paper" and c_sign=="Rock")):
                result="You Win!"
                u_score+=1
                do=False
            
            cv2.putText(frame,result, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
            

        if time.time()-start_time>5:
            start_time=time.time()-0.1
            play=True
        
    
    # Flip the frame horizontally for a mirror effect
    
    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe
    results = hands.process(rgb_frame)
    
    sign="Invalid"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determine finger states
            finger_states = []
            for finger, (tip, pip, mcp) in FINGERS.items():
                if finger =="Thumb":
                    #Thumb in x-axis
                    tip_x=hand_landmarks.landmark[tip].x
                    ip_x=hand_landmarks.landmark[pip].x
                    cmc_x=hand_landmarks.landmark[mcp].x
                    state="Up" if tip_x<ip_x  else "Folded"
                else:    
                    tip_y = hand_landmarks.landmark[tip].y
                    pip_y = hand_landmarks.landmark[pip].y
                    mcp_y = hand_landmarks.landmark[mcp].y

                    # Finger is considered "up" if tip is above PIP and MCP, else "folded"
                    state = "Up" if tip_y < pip_y and tip_y<mcp_y  else "Folded"
                finger_states.append(f"{finger}: {state}")

        
            print(finger_states)
            if finger_states==['Thumb: Up', 'Index: Up', 'Middle: Up', 'Ring: Up', 'Pinky: Up']:
                number="5"
            elif finger_states==['Thumb: Folded', 'Index: Up', 'Middle: Up', 'Ring: Up', 'Pinky: Up']:
                number="4" 
            elif finger_states==['Thumb: Folded', 'Index: Up', 'Middle: Up', 'Ring: Folded', 'Pinky: Folded']:
                number="2"
            elif finger_states==['Thumb: Folded', 'Index: Up', 'Middle: Up', 'Ring: Up', 'Pinky: Folded']:
                number="3"
            elif finger_states==['Thumb: Folded', 'Index: Up', 'Middle: Up', 'Ring: Up', 'Pinky: Folded']:
                number="3"
            elif finger_states==['Thumb: Folded', 'Index: Folded', 'Middle: Folded', 'Ring: Folded', 'Pinky: Folded']:
                number="0"
            elif finger_states==['Thumb: Up', 'Index: Folded', 'Middle: Folded', 'Ring: Folded', 'Pinky: Folded']:
                number="6"
            elif finger_states==['Thumb: Up', 'Index: Up', 'Middle: Folded', 'Ring: Folded', 'Pinky: Folded']:
                number="7"
            elif finger_states==['Thumb: Up', 'Index: Up', 'Middle: Up', 'Ring: Folded', 'Pinky: Folded']:
                number="8"
            elif finger_states==['Thumb: Up', 'Index: Up', 'Middle: Up', 'Ring: Up', 'Pinky: Folded']:
                number="9"
            else:
                number="?"

            #Show sign
            if number=="2":
                sign="Scissors"
            elif number=="5":
                sign="Paper"        
            elif number=="0":
                sign="Rock"
            else:
                sign="Invalid"

            cv2.putText(frame, f'Sign: {sign}', (50, 6*30+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            #/cv2.putText(frame, f'Number: {number}', (50, 50+5*30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Display finger states on the frame
            #for i, state in enumerate(finger_states):
            #      cv2.putText(frame, state, (50, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if "Up" in state else (0, 0, 255), 2)
            #show score
            cv2.putText(frame, f'Computer: {c_score}', (50,30*7+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
            cv2.putText(frame, f'You: {u_score}', (50,30*8+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
    # Display the frame
    cv2.imshow('Finger State Detection', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
#python hand_numbers_recognizer.py