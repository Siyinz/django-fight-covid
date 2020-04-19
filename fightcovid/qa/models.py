from django.db import models

# Create your models here.
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Question(models.Model):
	# title for question
	title = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Title must be greater than 1 character")])

    # content for questions
	#content = models.TextField()
	content = MarkdownxField()

	# user who asked the question  (many to one)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	# time
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# tags
	tags = TaggableManager()

	def __str__(self):
		return self.title

	def get_markdown(self):
	    return markdownify(self.content)




class Answer(models.Model):
	# answers
	content = models.CharField(max_length=500, validators=[MinLengthValidator(2, "Answers must be greater than 1 character")])

	# question
	question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)

	# user who answered the question
	solver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	total_votes = models.IntegerField(default=0)

	def __str__(self):
		return self.content


# votes for answers
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.BooleanField(default=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'answer')

