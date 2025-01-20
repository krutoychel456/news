from django import forms
from .models import News, Commentaries

# class NewsForm(forms.Form):
#     article = forms.CharField()
#     body = forms.CharField(widget=form.Textarea)

class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'article',
            'body',
            'image'
        ]

    def clean_article(self):
        data = self.cleaned_data.get('article')
        if len(data) < 5:
            raise forms.ValidationError('чотa как то чуть-чуть')
        return data
    
class CommentaryModelForm(forms.ModelForm):
    class Meta:
        model = Commentaries
        fields = [
            'text'
        ]