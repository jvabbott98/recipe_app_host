from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, default = 'No last name...')

    def __str__(self):
        return str(self.name)

