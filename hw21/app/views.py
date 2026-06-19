from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .forms import TaskForm
from .serializers import TaskSerializer


@csrf_exempt
def task_form_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            return JsonResponse({"message": "Form is valid!"}, status=200)
        return JsonResponse(form.errors, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@api_view(['POST'])
def task_serializer_view(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        return Response({"message": "Serializer is valid!"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)