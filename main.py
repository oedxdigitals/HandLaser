import cv2
import mediapipe as mp
import numpy as np
import time


# ==========================================
# CONFIG
# ==========================================

SAVE_VIDEO = "hand_laser_output.mp4"

WIDTH = 1280
HEIGHT = 720
FPS = 30

NUM_BEAMS = 10
GLOW_THICKNESS = 14
CORE_THICKNESS = 2
GLOW_STRENGTH = 0.45


RAINBOW = [
    (255,0,255),
    (255,0,170),
    (255,0,85),
    (255,51,0),
    (0,255,0),
    (0,255,210),
    (0,180,255),
    (0,90,255),
    (255,220,0),
    (255,120,0)
]


BRIDGE_PAIRS = [
    (0,0),
    (4,4),
    (8,8),
    (12,12),
    (16,16),
    (20,20),
    (5,9),
    (9,13),
    (13,17)
]


mp_hands = mp.solutions.hands
HAND_CONN = mp_hands.HAND_CONNECTIONS


# ==========================================
# HELPERS
# ==========================================

def draw_skeleton(frame, glow, pts):

    for i, (a,b) in enumerate(HAND_CONN):

        color = RAINBOW[i % len(RAINBOW)]

        cv2.line(
            glow,
            tuple(pts[a]),
            tuple(pts[b]),
            color,
            GLOW_THICKNESS,
            cv2.LINE_AA
        )

        cv2.line(
            frame,
            tuple(pts[a]),
            tuple(pts[b]),
            color,
            CORE_THICKNESS,
            cv2.LINE_AA
        )


    for p in pts:
        cv2.circle(
            frame,
            tuple(p),
            4,
            (255,255,255),
            -1
        )


def draw_prism(frame, glow, left, right):

    for idx, (la, ra) in enumerate(BRIDGE_PAIRS):

        p1 = left[la]
        p2 = right[ra]


        dx, dy = p2 - p1

        length = np.hypot(dx, dy) + 1e-6

        nx = -dy / length
        ny = dx / length


        for beam in range(NUM_BEAMS):

            t = (
                (beam - (NUM_BEAMS-1)/2)
                /
                max(NUM_BEAMS//2,1)
            ) * 18


            off_x = int(nx * t)
            off_y = int(ny * t)


            A = (
                p1[0] + off_x,
                p1[1] + off_y
            )

            B = (
                p2[0] + off_x,
                p2[1] + off_y
            )


            color = RAINBOW[
                (idx + beam)
                %
                len(RAINBOW)
            ]


            cv2.line(
                glow,
                A,
                B,
                color,
                GLOW_THICKNESS,
                cv2.LINE_AA
            )


            cv2.line(
                frame,
                A,
                B,
                color,
                CORE_THICKNESS+1,
                cv2.LINE_AA
            )


# ==========================================
# MEDIAPIPE
# ==========================================

hands = mp_hands.Hands(

    static_image_mode=False,

    max_num_hands=2,

    min_detection_confidence=0.75,

    min_tracking_confidence=0.6
)



cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)



fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(
    SAVE_VIDEO,
    fourcc,
    FPS,
    (WIDTH, HEIGHT)
)



prev = time.time()
spread = 0



# ==========================================
# MAIN LOOP
# ==========================================

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break


    frame = cv2.flip(frame, 1)

    H, W, _ = frame.shape


    glow = np.zeros_like(frame)


    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    results = hands.process(rgb)


    hand_points = []


    if results.multi_hand_landmarks:


        for hand in results.multi_hand_landmarks:


            pts = np.array([

                (
                    int(lm.x*W),
                    int(lm.y*H)

                )

                for lm in hand.landmark

            ])


            hand_points.append(pts)


            draw_skeleton(
                frame,
                glow,
                pts
            )



        if len(hand_points) == 2:


            left = hand_points[0]
            right = hand_points[1]


            spread = int(

                np.clip(

                    np.linalg.norm(
                        left[0]-right[0]
                    )

                    *100/W,

                    0,

                    100

                )

            )


            draw_prism(

                frame,

                glow,

                left,

                right

            )


    glow = cv2.GaussianBlur(

        glow,

        (31,31),

        0

    )


    frame = cv2.addWeighted(

        frame,

        1.0,

        glow,

        GLOW_STRENGTH,

        0

    )


    now = time.time()

    fps = int(

        1/max(

            now-prev,

            1e-6

        )

    )

    prev = now


    detected = len(hand_points)


    cv2.rectangle(

        frame,

        (10,10),

        (240,110),

        (0,0,0),

        -1

    )


    cv2.putText(
        frame,
        f"Hands: {detected}",
        (20,35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,255,0),
        2
    )


    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20,60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,255,0),
        2
    )


    cv2.putText(
        frame,
        "Gesture: 2H_BEAM",
        (20,85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255,255,0),
        2
    )


    cv2.putText(
        frame,
        f"Spread: {spread}%",
        (20,105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255,255,0),
        2
    )


    cv2.imshow(
        "Laser Hand Prism",
        frame
    )



    out.write(frame)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



cap.release()
out.release()

hands.close()

cv2.destroyAllWindows()


print(f"Saved: {SAVE_VIDEO}")
