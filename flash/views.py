from django.shortcuts import render

def flash_list(request):
    return render(request, 'flash/flash_list.html')