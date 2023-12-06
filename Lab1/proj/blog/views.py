from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Category, Tag
from .forms import ArticleForm, CommentForm
from .forms import ArticleForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

def article_list(request):
    articles = Article.objects.all()
    all_categories = Category.objects.all()
    all_tags = Tag.objects.all()

    selected_tags = request.GET.getlist('tag')
    selected_category = request.GET.get('category')

    if selected_tags:
        articles = articles.filter(tags__name__in=selected_tags)
    if selected_category:
        articles = articles.filter(category__name=selected_category)

    return render(request, 'blog/article_list.html', {'articles': articles, 'all_categories': all_categories, 'all_tags': all_tags, 'selected_tags': selected_tags, 'selected_category': selected_category})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/article_detail.html', {'article': article, 'comments': comments, 'comment_form': comment_form})

def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_edit.html', {'form': form})

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            form.save_m2m()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_edit.html', {'form': form})

def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect('article_list')
    return render(request, 'blog/article_delete_confirm.html', {'article': article})
