from django import forms

from article.models import Article

class CreateArticle(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['title', 'body', 'image']

class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image']

    def save(self, commit=True):
        article = self.instance
        article.title = self.cleaned_data['title']
        article.body = self.cleaned_data['body']

        if self.cleaned_data['image']:
            article.image = self.cleaned_data['image']

        if commit:
            article.save()
        
        return article