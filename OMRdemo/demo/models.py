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

class SubmitImage(models.Model):
    '''
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    body = models.TextField()
    '''
    image = models.ImageField(blank=True, upload_to="image", null=True)

    def __str__(self):
        return self.title
    def summary(self):
        return self.body[:100]