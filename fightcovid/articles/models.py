from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager

from django.utils.translation import ugettext_lazy as _


class Article(models.Model) :
    # Title for the article
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(5, "Title must be greater than 5 characters")]
    )
    # Author
    author = models.TextField()

    # Content for the article
    content = MarkdownxField()

    # Owner - who post this article (could not be the author)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='article_owned')

    # Comments to the article (Many to many)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='article_comments')

    # Related image
    image = models.ImageField(
        _("Featured image"), upload_to="articles_pictures/%Y/%m/%d/"
    )

    # Tag
    tags = TaggableManager()

    # Have been edited or not
    edited = models.BooleanField(default=False)

    # Time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


# reference
# https://github.com/vitorfs/bootcamp/tree/master/bootcamp
