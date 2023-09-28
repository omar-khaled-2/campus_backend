from django.db import models
from pathlib import Path
import uuid

class AutoNameFileField(models.FileField):
    def generate_filename(self, instance, filename):
        return f"{self.upload_to}/{uuid.uuid4().hex}{Path(filename).suffix}"



class AutoNameImageField(models.ImageField):
    def generate_filename(self, instance, filename):
      
        return f"{self.upload_to}/{uuid.uuid4().hex}{Path(filename).suffix}"
