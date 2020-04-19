from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from django.utils.translation import ugettext_lazy as _


class Article(models.Model) :
    # Title for the article
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(5, "Title must be greater than 5 characters")]
    )
    # Author
    author = models.CharField(
            max_length=100,
            validators=[MinLengthValidator(5, "Author name must be greater than 5 characters")]
    )
    source = models.CharField(max_length=200, default='Source URL')
    # Content for the article
    content = MarkdownxField()
    # Abstract of the article
    abstract = models.CharField(max_length=250, default='Abstract of the article')
    # Owner - who post this article (could not be the author)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='article_owned')
    # Comments to the article (Many to many)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='article_comments')
    # Related picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    # Tag
    tags = TaggableManager()
    # Time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_markdown(self):
        return markdownify(self.content)

    # Shows up in the admin list
    def __str__(self):
        return self.title

class Comment(models.Model) :
    # Comment content
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    # Many-to-one relationship
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Hit(models.Model):
    date = models.DateTimeField(auto_now = True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#    session = models.CharField(max_length=40, default='session')
#    ip = models.CharField(max_length=40, default='ip')
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')



# reference
# https://github.com/vitorfs/bootcamp/tree/master/bootcamp
