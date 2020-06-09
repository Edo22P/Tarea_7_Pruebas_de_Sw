import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def normalizar(entrada):
    entrada=entrada.lower()
    entrada=entrada.replace("(","")
    entrada=entrada.replace(")","")
    entrada=entrada.replace("{","")
    entrada=entrada.replace("}","")
    entrada=entrada.replace("[","")
    entrada=entrada.replace("]","")
    entrada=entrada.replace(",","")
    entrada=entrada.replace(".","")
    entrada=entrada.replace(":","")
    entrada=entrada.replace(";","")
    entrada=entrada.replace("=","")
    entrada=entrada.replace("/","")
    entrada=entrada.replace(" ","")
    entrada=entrada.replace("?","")
    entrada=entrada.replace("¿","")
    entrada=entrada.replace("!","")
    entrada=entrada.replace("¡","")
    entrada=entrada.replace("-","")
    entrada=entrada.replace("_","")
    entrada=entrada.replace("#","")
    entrada=entrada.replace("$","")
    entrada=entrada.replace("%","")
    entrada=entrada.replace("&","")
    entrada=entrada.replace("|","")
    entrada=entrada.replace("°","")
    entrada=entrada.replace("¬","")
    entrada=entrada.replace("+","")
    entrada=entrada.replace("*","")
    entrada=entrada.replace("~","")
    entrada=entrada.replace("á","a")
    entrada=entrada.replace("é","e")
    entrada=entrada.replace("í","i")
    entrada=entrada.replace("ó","o")
    entrada=entrada.replace("ú","u")
    entrada=entrada.replace("'","")
    entrada=entrada.replace("@","")
    return entrada

def detect_text(photo, bucket):

    client=boto3.client('rekognition')
    control=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':"Control.png"}}) #cambiar nombre de imagen de control
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections_control=control['TextDetections']
    aux=""
    palabras_control=""
    print ('Detected text\n----------')
    for text in textDetections_control:
        print ('Detected text:' + text['DetectedText'])
        print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        print ('Id: {}'.format(text['Id']))
        if 'ParentId' in text:
            print ('Parent Id: {}'.format(text['ParentId']))
        print ('Type:' + text['Type'])
        if(text["Type"]=="WORD"):
        	#if(int(text['Confidence'])<=97):
        	#return False
            if(int(text['Confidence'])<97):
                continue
            aux=normalizar(text['DetectedText'])
            palabras_control += aux
        print()

    textDetections=response['TextDetections']
    palabras=""
    print ('Detected text\n----------')
    for text in textDetections:
        print ('Detected text:' + text['DetectedText'])
        print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        print ('Id: {}'.format(text['Id']))
        if 'ParentId' in text:
            print ('Parent Id: {}'.format(text['ParentId']))
        print ('Type:' + text['Type'])
        if(text["Type"]=="WORD"):
        	#if(int(text['Confidence'])<=97):
        	#return False
            if(int(text['Confidence'])<97):
                continue
            aux=normalizar(text['DetectedText'])
            palabras += aux
        print()
    print("palabras_control: "+ palabras_control)
    print("palabras: "+ palabras)
    if(palabras.find(palabras_control)==-1):
        return False
    else:
        return True
def main():
    foto=input("Introducir nombre de imagen: ")
    bucket='bucketedo'
    photo=foto
    text_comparison=detect_text(photo,bucket)
    file = open("log.txt", "a")
    now = datetime.now()
    file.write("Imagen de control: " + "Control.png\n")
    file.write("Imagen de prueba: " + foto+ "\n")
    file.write("Resultado: " + str(text_comparison)+ "\n")
    file.write("Fecha: " + str(now)+ "\n")
    file.write("\n")
    return text_comparison



if __name__ == "__main__":
    A=main()
    print(A)
