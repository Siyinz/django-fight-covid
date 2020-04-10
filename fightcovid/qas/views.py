from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from qas.models import Tag, Question, Answer
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from qas.owner import OwnerListView, OwnerDetailView, OwnerUpdateView, OwnerDeleteView
from qas.forms import QuestionForm

class QuestionList(OwnerListView):
	model = Question
	template_name = 'qas/question_list.html'
	#paginate_by = 20
	#context_object_name = 'questions'
	# success_url = reverse_lazy(‘qas:all')

class QuestionDetail(OwnerDetailView):
	model = Question
	template_name = 'qas/question_detail.html'
	#fields = '__all__'
	#success_url = reverse_lazy(‘qas:all')
	#def get_context_data(self, *args, **kwargs):
	#	context = super().get_context_data(*args, **kwargs)
	#	return context
	def get(self, request, pk):
		question = Question.objects.get(id=pk)
		tags = Tag.objects.filter(question=question)
		answers = Answer.objects.filter(question=question)
		context = {'question': question, 'tags': tags, 'answers': answers}
		return render(request, self.template_name, context)

class QuestionCreate(LoginRequiredMixin, CreateView):
#    form_class = QuestionForm
#    template_name = "qas/question_form.html"
#    def form_valid(self, form):
#        object = form.save(commit = False)
#        object.owner = self.request.user
#        object.save()
#        return super(QuestionCreate, self).form_valid(form)
#	success_url = reverse_lazy('qas:all')
#    def get_success_url(self):
#        return reverse('qas:all')
    template = 'qas/question_form.html'
    success_url = reverse_lazy('qas:all')
    def get(self, request, pk=None) :
        form = QuestionForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)
    def post(self, request, pk=None) :
        form = QuestionForm(request.POST)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)
        # Add owner to the model before saving
        question = form.save(commit=False)
        question.owner = self.request.user
        question.save()
        return redirect(self.success_url)


class AnswerCreate(LoginRequiredMixin, CreateView):
	model = Answer
	fields = ['content']
#	message = _('Thank you')
#	success_url = reverse_lazy('qas:all')
	# required relationship between answer and question
	def form_valid(self, form):
		form.instance.solver = self.request.user
		form.instance.question_id = self.kwargs['question_id']
		return super(AnswerCreate, self).form_valid(form)
	def get_success_url(self):
#		messages.success(self.request, self.message)
		return reverse("qas:question_detail", kwargs={"pk": self.kwargs["question_id"]})

#  reference: https://github.com/swappsco/django-qa/blob/master/qa/views.py



# something similar to comment
class TagCreate(LoginRequiredMixin, View):
#	model = Tag
#	fields = ['name']
	def post(self, request, pk):
		q = get_object_or_404(Question, id = pk)
		tag =Tag(name = request.POST['tag'], owner = request.user, question = q)
		tag.save()
		return redirect(reverse('qas:question_detail', args = [pk]))
