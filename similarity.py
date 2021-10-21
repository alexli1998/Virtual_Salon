import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from google.colab.patches import cv2_imshow
from keras_vggface.vggface import VGGFace
# if error: open keras_vggface/models.py, modify line20 to 'from keras.utils.layer_utils import get_source_inputs'
from keras_vggface.utils import preprocess_input
from scipy.spatial.distance import cosine


detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
encs = np.load('./encs.npy', allow_pickle=True)


def similarity(imgpath):
    img = cv2.imread(imgpath)

    face = detector.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    if len(face) != 0:
        (x, y, w, h) = face[0]
        region = img[y:y + h, x:x + w]
    else:
        region = img

    region = cv2.resize(region, (224, 224))
    region = region.astype('float64')

    region = region.reshape(1, 224, 224, 3)
    query = model.predict(region)[0]

    distances = []

    for enc in encs:
        distances.append(cosine(query, enc[0]))

    top3index = np.argsort(np.array(distances))[:3]

    path1 = '/static/ref/' + encs[top3index[0]][1]
    path2 = '/static/ref/' + encs[top3index[1]][1]
    path3 = '/static/ref/' + encs[top3index[2]][1]

    return [path1, path2, path3]

