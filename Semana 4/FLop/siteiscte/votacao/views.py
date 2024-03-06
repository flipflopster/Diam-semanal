from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Pagina de entrada da appvotacao.")

