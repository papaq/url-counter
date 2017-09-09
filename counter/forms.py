from django import forms

from counter.models import Url


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ('url',)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        return url
