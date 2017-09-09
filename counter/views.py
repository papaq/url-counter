from django.shortcuts import render, redirect
from django.urls import reverse

from counter.forms import UrlForm
from counter.models import Url, Redirection
from counter.utils import get_short, get_url, get_ip, get_sensitive_data


def shorten_url(request):
    form = UrlForm(request.POST or None)

    saved = ''
    short_url = ''
    list_url_address = reverse('counter:list_url')

    if form.is_valid():
        url = form.clean_url()
        short_code = get_short(url)

        if not short_code:
            recorded_url = Url(url=url)
            recorded_url.save()
            short_code = recorded_url.short_code

        saved = url
        short_url = "%s/%s" % (request.META['HTTP_HOST'], short_code)

    context = {
        'saved': saved,
        'short_url': short_url,
        'list_url_address': list_url_address,
        'form': form,
    }
    return render(request, 'counter/shorten_url.html', context)


def history_of_url(request, short_code):
    url = get_url(short_code)
    if not url:
        return redirect(reverse("counter:list_url"))

    records = Redirection.objects.filter(url=url).order_by('datetime')

    context = {
        'records': records,
        'url': url,
    }
    return render(request, 'counter/history_of_url.html', context)


def redirect_url(request, short_code):
    url = get_url(short_code)
    if not url:
        return redirect("http://crit.org.ua")

    # was found
    redirection = Redirection(url=url, ip=get_ip(request), sensitive=get_sensitive_data(request))
    redirection.save()
    print(get_sensitive_data(request))

    address = 'http://' + url.url
    return redirect(address)


def list_url(request):
    context = {
        'urls': Url.objects.all(),
    }
    return render(request, 'counter/list_url.html', context)


def redirect_to_shorten(request):
    return redirect(reverse('counter:shorten_url'))


def redirection_info(request, short_code, redirection_pk):
    if not Redirection.objects.filter(pk=redirection_pk).exists() \
            or Redirection.objects.filter(pk=redirection_pk).first().url.short_code != short_code:
        return redirect(reverse('counter:list_url'))

    context = {
        'redirection': Redirection.objects.filter(pk=redirection_pk).first(),
    }
    return render(request, 'counter/redirection_info.html', context)
