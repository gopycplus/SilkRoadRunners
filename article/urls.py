from django.urls import path
from article.views import(
    create_article_view,
    detail_article_view,
    edit_article_view,
)

app_name = 'article'

urlpatterns = [
    path('create/', create_article_view, name="create"),
    path('<slug>/', detail_article_view, name="detail"),
    path('<slug>/edit', edit_article_view, name="edit"),
]
