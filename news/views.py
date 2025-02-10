from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import NewsModelForm, CommentaryModelForm
from news.models import News, Commentaries, Likes 
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse

def index(request, *args, **kwargs):
    qs = News.objects.all()
    context = {'news_list': qs}
    return render(request, 'index.html', context)

def detail_view(request, *args, **kwargs):
    liked = False
    try:
        obj = News.objects.get(id=kwargs['pk'])
    except News.DoesNotExist:
        raise Http404
    
    if request.user.is_authenticated and obj.likes.filter(user=request.user):
        liked = True
    context = {'single_object': obj, 'liked':liked}   
    
    return render(request, 'news.html', context)

def about(request, *args, **kwargs):
    return render(request, 'about.html')

def anekdot(request, *args, **kwargs):
    return render(request, 'anekdot.html')

def test_view(request, *args, **kwargs):
    data = dict(request.GET)
    print(data)
    obj = News.objects.get(id=data['pk'][0])
    return HttpResponse(f'<b>{obj.article}</b>')

@login_required
@permission_required('user.is_staff', raise_exception=True)
def create_view(request, *args, **kwargs):
    form = NewsModelForm(request.POST or None, request.FILES)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        return redirect('/')
    return render(request, 'forms.html', {'form': form})

@login_required
def edit_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = NewsModelForm(request.POST, instance=obj)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.save()
            return redirect(f"/news/{pk}/")
    else:
        form = NewsModelForm(instance=obj)
    return render(request, 'edit_news_form.html', {'single_object': obj, 'form': form})

@login_required
def delete_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    obj.delete()
    return HttpResponseRedirect(reverse('index'))

def art(request, *args, **kwargs):
    return render(request, 'art.html')

@login_required
def commentary_view(request, pk):
    form = CommentaryModelForm(request.POST or None)
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    
    if form.is_valid():
        text = form.cleaned_data.get('text')
        user = request.user
        commentary_obj = Commentaries(user=user, text=text)
        commentary_obj.save()
        obj.commentary.add(commentary_obj)
        obj.save()
        return redirect(f'/news/{pk}')

    return render(request, 'commentary.html', {'single_object': obj, 'form': form})
    
@login_required
def commentary_edit_view(request, pk, pk2):
    try:
        obj = Commentaries.objects.get(id=pk2)
    except Commentaries.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = CommentaryModelForm(request.POST, instance=obj)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.save()
            return redirect(f"/news/{pk}/")
    else:
        form = CommentaryModelForm(instance=obj)
    return render(request, 'edit_commentary_form.html', {'single_object': obj, 'form': form})

@login_required
def commentary_delete_view(request, pk, pk2):
    try:
        obj = Commentaries.objects.get(id=pk2)
    except Commentaries.DoesNotExist:
        raise Http404
    obj.delete()
    return redirect(f"/news/{pk}/")

@login_required
def likes_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        user = request.user
        if not obj.likes.filter(user=user):
            like_obj = Likes(user=user, like=True)
            like_obj.save()
            obj.likes.add(like_obj)
            obj.save()
        else:
            obj.likes.filter(user=user).delete()
    return redirect(f"/news/{pk}/")

def contact(request, *args, **kwargs):
    return render(request, 'contact.html')