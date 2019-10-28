import boto3
import os
import json
import base64

if __name__ == "__main__":

    sourceFile='/Users/andalval/Desktop/FotoLandaprueba.jpg'
    targetFile='/Users/andalval/Desktop/Fotogrupalprueba.jpg'
    client=boto3.client('rekognition')
   
    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')

    response = client.detect_faces(Image={'Bytes': imageSource.read()}, Attributes=['ALL'])

    print('Detected faces for ' + sourceFile)    
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
            + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))
    imageSource.close()
    imageTarget.close()  

    response=client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face at ' +
            str(position['Left']) + ' ' +
            str(position['Top']) +
            ' matches with ' + confidence + '% confidence')