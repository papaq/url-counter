import string
from random import randrange, choice

from counter.models import Url


def freeUrl():
    random = random_url()
    while Url.objects.filter(url=random).exists():
        random = random_url()

    return random


def random_url():
    a = 1
    return '%s%d%s%d%s' % \
           (choice(string.ascii_letters), randrange(10),
            choice(string.ascii_letters), randrange(10), choice(string.ascii_letters))


def get_short(url):
    try:
        return Url.objects.get(url=url).short_code
    except Url.DoesNotExist:
        return None


def get_url(code):
    try:
        return Url.objects.get(short_code=code)
    except Url.DoesNotExist:
        return None


def ip_to_city(ip):
    from django.contrib.gis.geoip import GeoIP
    g = GeoIP
    return None


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_sensitive_data(request):

    return "COMPUTERNAME = %s<br>APPDATA = %s<br>USERNAME = %s<br>SERVER_NAME = %s<br>PROCESSOR_IDENTIFIER = %s" \
           "<br>OS = %s<br>ONEDRIVE = %s" % (request.META.get('COMPUTERNAME'), request.META.get('APPDATA'),
                                  request.META.get('USERNAME'), request.META.get('SERVER_NAME'),
                                  request.META.get('PROCESSOR_IDENTIFIER'), request.META.get('OS'),
                                  request.META.get('ONEDRIVE'))
