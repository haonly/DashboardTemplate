from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
'''
class ImagePost(models.Model):
    image = ProcessedImageField(
        upload_to = generate_upload_path,
        processors=[ResizeToFill(1000, 800)],
        format='JPEG',
        #options = {'quality': 60}
    )
'''