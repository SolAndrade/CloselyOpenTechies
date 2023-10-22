import cv2
import face_recognition
import numpy as np

# Inicializa la cámara
cap = cv2.VideoCapture(0)  # 0 para la cámara por defecto

while True:
    # Captura un fotograma de la cámara
    ret, frame = cap.read()

    # Detecta caras en el fotograma
    face_locations = face_recognition.face_locations(frame)

    for face_location in face_locations:
        top, right, bottom, left = face_location

        # Recorta la región de la cara
        face_image = frame[top:bottom, left:right]

        # Utiliza el modelo VGGFace para estimar el género y la edad
        # Nota: Asegúrate de que tienes el modelo VGGFace pre-entrenado descargado y accesible
        # desde https://github.com/rcmalli/keras-vggface
        # Debes proporcionar la ruta al modelo en la siguiente línea.
        # Aquí se asume que el modelo se encuentra en la misma carpeta que el script.
        model_path = "vggface_weights.h5"
        # Carga el modelo VGGFace
        gender_age_model = load_model(model_path)

        # Preprocesa la imagen de la cara para el modelo VGGFace
        face_image = cv2.resize(face_image, (224, 224))
        face_image = np.expand_dims(face_image, axis=0)
        face_image = preprocess_input(face_image)

        # Realiza la estimación de género y edad
        gender, age = gender_age_model.predict(face_image)

        # Convierte las predicciones en etiquetas
        gender_label = "Female" if gender[0][0] > 0.5 else "Male"
        age_label = int(age[0][0])

        # Dibuja un rectángulo alrededor de la cara y muestra el género y la edad estimados
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"Gender: {gender_label}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Age: {age_label}", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Muestra la imagen con las caras detectadas, género y edad estimados
    cv2.imshow('Detección de caras', frame)

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
