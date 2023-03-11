import secrets
import string
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def get_key(length: int) -> str:
    """
    key Generator:
    length - key length
    """
    character_set = string.digits + string.ascii_letters
    return ''.join(secrets.choice(character_set) for _ in range(length))

def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    return render(request, 'core/404.html', {'path': request.path}, status=404)

def csrf_failure(request: HttpRequest, reason='') -> HttpResponse:
    return render(request, 'core/403csrf.html')
