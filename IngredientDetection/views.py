from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
import cv2
import numpy as np
from ultralytics import YOLO
from django.http import JsonResponse
import boto3
from django.conf import settings
import uuid

from Inventory.models import Ingredient
from Inventory.serializers import IngredientSerializer

model = YOLO("IngredientDetection/yolo/best.pt")

@api_view(['POST'])
@parser_classes([MultiPartParser])
def detectIngredients(request):
    try:
        image_bytes = request.FILES.get('image')
        image_type = request.POST.get('imageType').split("/")[-1]
        image = np.frombuffer(image_bytes.read(), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.SECRET_ACCESS_KEY)
        s3.upload_fileobj(image_bytes, 'my-fridge', f'{uuid.uuid4()}.{image_type}')
        
        # Perform object detection with YOLOv8
        results = model.predict(image)
        names = model.names
        
        detections = [names[int(c)] for r in results for c in r.boxes.cls]
        
        # Remove duplicate detections
        unique_detections = list(map(lambda x: x.lower(), set(detections)))
        ingredients = Ingredient.objects.filter(name__in=unique_detections)
        
        return JsonResponse({"detections": list(ingredients.values())})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=415)