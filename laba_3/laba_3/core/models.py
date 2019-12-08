from django.db import models


class File(models.Model):
    """
    file - файл базы знаний в формате kdb
    name - имя файла для отображения на фронте
    """
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=50)
