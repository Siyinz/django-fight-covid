from django.db import models

# Create your models here.
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings


class Question(models.Model):
	# title for question 
	title = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Title must be greater than 1 character")])

    	# content for questions
	content = models.TextField()

	# user who asked the question  (many to one)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	# time
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# tags
	tags = models.ManyToManyField(settings.AUTH_USER_MODEL, through = 'Tag', related_name = 'tags_owned')
	def __str__(self):
		return self.title


# tags for questions
class Tag(models.Model):
	name = models.CharField(max_length=10, validators = [MinLengthValidator(2, "Tags must be greater than 1 character")])
	#name = TaggableManager()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Answer(models.Model):
	# answers
	content = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Answers must be greater than 1 character")])
        
	# question
	question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)

	# user who answered the question 
	solver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


	def __str__(self):
		return self.content
