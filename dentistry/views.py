from django.shortcuts import render
from .model import update_model_weights
from . import prediction
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def home(request):
    return render(request,'index.html')

update_model_weights()
prediction.load_model()

@csrf_exempt
def predict(request):
    data = {"success": False}
    if request.method == "POST":

        # Ensure an image was properly uploaded to our endpoint
        if request.FILES.get("image"):

            # Convert the image
            image = request.FILES["image"].read()

            probs, original, heatmap = prediction.predict_image(image)

            # Fill the response
            data["success"] = True
            data["id"] = random.randint(0, 100)
            data["probs"] = probs
            data["original"] = original
            data["heatmap"] = heatmap

    # return the data dictionary as a JSON response
    return JsonResponse(data)
