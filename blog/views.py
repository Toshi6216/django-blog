from django.shortcuts import render,  redirect
from django.views.generic import View, TemplateView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'blog/index.html',{
            'post_data': post_data
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_detail.html',{
            'post_data': post_data
        })

class CreatePostView(View,LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'blog/post_form.html',{
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
#        category = Category(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
#            post_data.category = request.category
            #post_data.nickname = request.nickname
            post_data.save()
            return redirect('post_detail', post_data.id)


        return render(request, 'blog/post_form.html',{
            'form': form
        })

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial = {
                'title' : post_data.title,
                'content' : post_data.content
#                'category' : post_data.category
            }
        )
        
        return render(request, 'blog/post_form.html',{
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
#        category = Category(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
#            post_data.category = request.category
            #post_data.nickname = request.nickname
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])


        return render(request, 'blog/post_form.html',{
            'form': form
        })

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_delete.html',{
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')


class BlogTestView(TemplateView):
    template_name = "test.html"

    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'test.html',{
            'post_data': post_data
        })


class SampleChoiceAddView(View):
    def get(self, request):
        form_1 = forms.SampleChoiceAddForm()

        form_1.fields['choice_1'].choices =[
            ('hokkaido', '北海道'),
            ('touhoku', '東北'),
            ('kantou', '関東'),
            ('hokuriku','北陸'),
            ('toukai', '東海'),
        ]
        context = {
            'form': form_1
        }
        return render(request, 'choice_sample.html', context)
sample_choice_add_view = SampleChoiceAddView.as_view()
