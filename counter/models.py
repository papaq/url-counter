from django.db import models


class Url(models.Model):
    url = models.CharField(null=False, blank=False, max_length=200)
    short_code = models.CharField(editable=False, max_length=5)
    counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            from counter import utils
            self.short_code = utils.freeUrl()
        super(Url, self).save(*args, **kwargs)

    def increase_counter(self):
        self.counter += 1
        self.save()


class Redirection(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=20, null=True)
    sensitive = models.CharField(null=True, max_length=500)

    def save(self, *args, **kwargs):
        self.url.increase_counter()
        super(Redirection, self).save(*args, **kwargs)

    def get_city(self):
        return None
