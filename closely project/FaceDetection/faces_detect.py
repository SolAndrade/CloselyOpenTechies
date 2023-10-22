import cv2
import dlib
import numpy as np

# Inicializa el detector de caras de dlib
face_detector = dlib.get_frontal_face_detector()

# Inicializa el predictor de puntos faciales de dlib
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Inicializa la cámara
cap = cv2.VideoCapture(0)  # 0 para la cámara por defecto

# Carga los modelos pre-entrenados para la detección de edad y género
age_net = cv2.dnn.readNetFromCaffe("deploy_age2.prototxt", "age_net.caffemodel")
gender_net = cv2.dnn.readNetFromCaffe("deploy_gender2.prototxt", "gender_net.caffemodel")

while True:
    # Captura un fotograma de la cámara
    ret, frame = cap.read()

    # Convierte el fotograma a escala de grises para la detección de caras
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta caras en el fotograma
    faces = face_detector(gray)

    for face in faces:
        # Utiliza el predictor de puntos faciales para obtener las coordenadas faciales
        shape = predictor(frame, face)
        shape = np.array([(p.x, p.y) for p in shape.parts()])

        # Dibuja un trazado de rayos en la cara conectando los puntos faciales
        for i in range(1, len(shape)):
            cv2.line(frame, tuple(shape[i - 1]), tuple(shape[i]), (0, 255, 0), 2)

        # Estima la edad y el género de la persona en la cara
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        face_img = frame[y:y+h, x:x+w].copy()

        # Añade la comprobación para verificar si la región de la cara es válida
        if face_img is not None and not face_img.size == 0:
            # Preprocesa la imagen de la cara para la detección de edad y género
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

            # Realiza la detección de edad
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = int(age_preds.mean())

            # Realiza la detección de género
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = "Female" if gender_preds[0][0] > gender_preds[0][1] else "Male"

            # Dibuja la estimación de edad y género en la imagen
            cv2.putText(frame, f"Age: {age}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Gender: {gender}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            # Si no se detectó una cara válida, puedes mostrar un mensaje o realizar una acción adecuada.
            print("No se detectó una cara válida en este fotograma")

    # Muestra la imagen con las caras detectadas, el trazado de rayos y la estimación de edad y género
    cv2.imshow('Detección de caras', frame)

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
