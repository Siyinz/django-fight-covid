from articles.models import Article, Comment
from articles.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile
from articles.forms import CreateForm,CommentForm

#from articles.hit import render_to_response_hit_count
from articles.models import Hit

class ArticleListView(OwnerListView):
    model = Article
    # By convention:
    template_name = "articles/article_list.html"

class ArticleDetailView(OwnerDetailView):
    model = Article
    template_name = "articles/article_detail.html"
    def get(self, request, pk) :
        x = Article.objects.get(id=pk)
        comments = Comment.objects.filter(article=x).order_by('-updated_at')
        comment_form = CommentForm()
#        Hit(content_object=x, ip=request.META['REMOTE_ADDR'], session=request.session.session_key).save()
        Hit(content_object=x).save()
        hit = Hit.objects.filter(object_id=pk).count()
#        hit = Hit.objects.count()
        context = { 'article' : x, 'comments': comments, 'comment_form': comment_form, 'hits': hit}
        return render(request, self.template_name, context)


class ArticleCreateView(LoginRequiredMixin, View):
    template = 'articles/article_form.html'
    success_url = reverse_lazy('articles:all')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

class ArticleUpdateView(LoginRequiredMixin, View):
    template = 'articles/article_form.html'
    success_url = reverse_lazy('articles:all')
    def get(self, request, pk) :
        pic = get_object_or_404(Article, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(Article, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)

class ArticleDeleteView(OwnerDeleteView):
    model = Article

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Article, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, article=f)
        comment.save()
        return redirect(reverse('articles:article_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "articles/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        article = self.object.article
        return reverse('articles:article_detail', args=[article.id])

def stream_file(request, pk) :
    article = get_object_or_404(Article, id=pk)
    response = HttpResponse()
    response['Content-Type'] = article.content_type
    response['Content-Length'] = len(article.picture)
    response.write(article.picture)
    return response

