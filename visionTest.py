import io
import os
from google.cloud import vision

"""
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('/Users/andalval/Desktop/Foto prueba.jpeg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
"""
"""Detects faces in an image."""

client = vision.ImageAnnotatorClient()
path = os.path.abspath('/Users/andalval/Desktop/Expresiones prueba.jpg')

with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.face_detection(image=image)
faces = response.face_annotations

# Names of likelihood from google.cloud.vision.enums
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
print('Faces:')
i=1
for face in faces:
    mensaje = "Cara "+str(i)
    print(mensaje)
    print('Anger: {}'.format(likelihood_name[face.anger_likelihood]))
    print('Joy: {}'.format(likelihood_name[face.joy_likelihood]))
    print('Surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
    print('Sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
    print('Exposed: {}'.format(likelihood_name[face.under_exposed_likelihood]))
    print('Blurred: {}'.format(likelihood_name[face.blurred_likelihood]))
    print('Headwear: {}'.format(likelihood_name[face.headwear_likelihood]))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in face.bounding_poly.vertices])

    print('face bounds: {}'.format(','.join(vertices)))
    i=i+1