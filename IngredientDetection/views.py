from django.shortcuts import render
from rest_framework.decorators import api_view
import cv2
import numpy as np
from ultralytics import YOLO
from django.http import JsonResponse

model = YOLO("IngredientDetection/yolo/best.pt")

@api_view(['POST'])
def detectIngredients(request):
    # Process the uploaded image for object detection
    image_bytes = request.FILES.get('image').read()
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    # Perform object detection with YOLOv8
    results = model.predict(image)
    names = model.names
    
    detections = [names[int(c)] for r in results for c in r.boxes.cls]
    
    return JsonResponse({"detections": detections})