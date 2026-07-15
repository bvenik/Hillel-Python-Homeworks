from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Hello, world!")

def main_page_view(request):
    return HttpResponse('Welcome to the main page!')