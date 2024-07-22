from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from article.models import Article
from article.forms import CreateArticle, UpdateArticleForm
from account.models import Account

def create_article_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    
    form = CreateArticle(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateArticle()

    context['form'] = form 

    return render(request, "article/create_article.html", {})

def detail_article_view(request, slug):
    context = {}

    article = get_object_or_404(Article, slug=slug)
    context['article'] = article

    return render(request, 'article/detail_article.html', context)

def edit_article_view(request, slug):
    context = {}
    
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    article = get_object_or_404(Article, slug=slug)

    if article.author != user:
        return HttpResponse("You are not allowed to edit this post!")

    if request.POST:
        form = UpdateArticleForm(request.POST or None, request.FILES or None, instance=article)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            article = obj
    form = UpdateArticleForm(
        initial = {
            "title": article.title,
            "body": article.body,
            "image": article.image,
        }
    )

    context['form'] = form
    return render(request, 'article/edit_article.html', context)

def get_article_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        articles = Article.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for article in articles:
            queryset.append(article)
    
    return list(set(queryset))