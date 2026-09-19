import cv2
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from new_model import EMOTIONS

if __name__ == '__main__':
    # Use haar cascade classifier to detect faces
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    classifier = load_model('emotion_model.h5')

    # create a video capture object
    vid = cv2.VideoCapture(0)

    frames = 0
    everyXFrames = 5
    label = ""
    label_position = (0, 0)

    while True:
        frames = frames + 1
        # Capture the video per frame from the camera
        ret, frame = vid.read()

        # Convert the captured frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame and store the pixel coordinates in faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            # Mark the face with a rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (181, 215, 14), thickness=3)

            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if frames % everyXFrames == 0:
                frames = 0
                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    preds = classifier.predict(roi)[0]
                    pred_index = preds.argmax()
                    label = EMOTIONS[pred_index] + " %.2f%%" % float(preds[pred_index] * 100)
                    
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.imwrite(label+"_.jpg", frame)

        # Display the resulting frame
        cv2.imshow('Emotion Detection - (press q to quit)', frame)

        # If q is hit the window will close
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object and destroy window objects
    vid.release()
    cv2.destroyAllWindows()

"""
References:
    1) Face detection in OpenCV
        - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
    2) Haar feature-based cascade classifier by Paul Viola and Michael Jones in OpenCV
        - https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
"""
