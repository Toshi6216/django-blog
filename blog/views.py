from multiprocessing import get_context
from django.shortcuts import render,  redirect
from django.views.generic import View, TemplateView, CreateView, UpdateView, ListView, DeleteView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

#TopページのIndexページのview
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.order_by('-created')
    context_object_name = 'post_data'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        card = ContentCard.objects.all
        print("card")
        print(card)
        ctx['blog_card'] = card
        
        print(ctx['blog_card'])
        return ctx

#記事詳細画面のview
class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk']) #pkで記事を特定してデータ取得
        return render(request, 'blog/post_detail.html',{
            'post_data': post_data
        })

#記事投稿のview
class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def get_success_url(self): 
        return reverse("index") #入力フォーム内容がセーブできた時の遷移先

    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs) #オーバーライド前のget_context_dataで返されるオブジェクトを格納

        if self.request.method=="POST": #"POST"が呼び出されたときの処理
            post_formset = self.request.POST.copy() #request.POSTをコピーして変数に格納
            files = self.request.FILES  #FILESを変数に格納
            post_formset['contentcard-TOTAL_FORMS']=1 #フォームの数 formsetを使う場合必須
            post_formset['contentcard-INITIAL_FORMS']=0 #formsetを使う場合必須
            ctx["blog_formset"] = CardFormset(post_formset, files) #変数をフォームセットに渡す
        else:
            ctx["blog_formset"] = CardFormset()
            CardFormset.extra=1

        return ctx
   

    def form_valid(self, form):
        ctx = self.get_context_data()
        blog_formset = ctx["blog_formset"]

        if blog_formset.is_valid():
            self.object=form.save(commit=False)
            self.object.author=self.request.user
            self.object.save()
            blog_formset.instance = self.object
            blog_formset.save()
            return redirect(self.get_success_url())

        else:
            ctx["form"] = form
            return self.render_to_response(ctx)

#編集画面のview
class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm
    
    def get_success_url(self): 
        return reverse("index") #入力フォーム内容がセーブできた時の遷移先

    def get_context_data(self, **kwargs):
        post_data = Post.objects.get(pk=self.kwargs['pk'])
        if not self.request.user == post_data.author:
            raise Http404 #編集する記事のauthorとrequest.userが違うとエラー表示
            
        ctx=super(PostEditView, self).get_context_data(**kwargs) #オーバーライド前のget_context_dataで返されるオブジェクトを格納
        
        if self.request.method=="POST": #"POST"が呼び出されたときの処理
            files = self.request.FILES  #FILESを変数に格納
            ctx.update(dict(blog_formset=CardFormset(self.request.POST or None, files = files,  instance=self.object)))

        else: 
            ctx.update(dict(blog_formset=CardFormset(self.request.POST or None, instance=self.object)))
            CardFormset.extra=0
        
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        blog_formset = ctx["blog_formset"]

        if blog_formset.is_valid():
            self.object=form.save(commit=False)
            self.object.save()  
            blog_formset.save()
            return redirect(self.get_success_url())

        else:
            ctx["form"] = form
            return self.render_to_response(ctx)

#カテゴリ追加フォーム 
@login_required
def categoryFormView(request):
    category_list = Category.objects.all()
    form = CategoryForm(request.POST or None)
    context = {
        'category_list':category_list,
        'form':form,
    }
    if request.method == 'POST':
        if form.is_valid():
            Category.objects.create(**form.cleaned_data)
            return render(request, 'blog/category_form.html', context)
    return render(request, 'blog/category_form.html', context)

#カテゴリ削除のview
class CategoryDeleteView(LoginRequiredMixin, View):
    
    model = Category

    def get(self, request, *args, **kwargs):
        
        return render(request, 'blog/category_delete.html')

    def post(self, request):
        category_pks = request.POST.getlist('delete')  # <input type="checkbox" name="delete"のnameに対応
        Category.objects.filter(pk__in=category_pks).delete()
        return redirect('index')  # 一覧ページにリダイレクト




#投稿削除のview
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
 



#カテゴリごとに記事をまとめたview
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(
            name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(
            category=category_data)
        return render(request, 'blog/index.html', {
            'post_data' : post_data
        })


# ___ここから下はお試し用____

class TestDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'test_detail.html',{
            'post_data': post_data
        })

class BlogTestView(TemplateView):
    template_name = "test.html"

    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'test.html',{
            'post_data': post_data
        })


def lists(request):
    sample_list = Category.objects.all()
    form = CategoryForm(request.POST or None)
    context = {
        'sample_list':sample_list,
        'form':form,
    }
    if request.method == 'POST':
        if form.is_valid():

            # create()の場合
            Category.objects.create(**form.cleaned_data)

           
            return render(request, 'lists.html', context)
    return render(request, 'lists.html', context)



