from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from article.views import get_article_queryset
from article.models import Article

ARTICLES_PER_PAGE = 12

def home_screen_view(request, *args, **kwargs):
	
	context = {}

	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	articles = sorted(get_article_queryset(query), key=attrgetter('date_updated'), reverse=True)
	


	# Pagination
	page = request.GET.get('page', 1)
	articles_paginator = Paginator(articles, ARTICLES_PER_PAGE)
	try:
		articles = articles_paginator.page(page)
	except PageNotAnInteger:
		articles = articles_paginator.page(ARTICLES_PER_PAGE)
	except EmptyPage:
		articles = articles_paginator.page(articles_paginator.num_pages)

	context['articles'] = articles

	return render(request, "personal/home.html", context)


