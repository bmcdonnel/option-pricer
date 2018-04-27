from django.http import HttpResponse

def index(request):
    print("pricer index")

    return HttpResponse("Hello, world.")
