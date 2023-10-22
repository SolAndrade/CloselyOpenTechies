import cv2
import dlib
import numpy as np

face_detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0)  # 0 para la cámara por defecto

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector(gray)

    for face in faces:
        shape = predictor(frame, face)
        shape = np.array([(p.x, p.y) for p in shape.parts()])

        for i in range(1, len(shape)):
            cv2.line(frame, tuple(shape[i - 1]), tuple(shape[i]), (0, 255, 0), 2)

        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.putText(frame, "Age: 20", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, "Gender: Male", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, "Emotion: Normal", (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Detección de caras', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
