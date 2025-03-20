from django.shortcuts import render, redirect
from tanach.models import Word
# Create your views here.
def showline(request, book=1, chapter=1, line=1):
    if request.method=='POST':
        p=request.POST
        return redirect('/%s/%s/%s/'%(p['book'],p['chapter'],p['line']))
    context = {'current': {'book':book, 'chapter':chapter, 'line':line}}
    context['words']=Word.objects.filter(book=book,chapter=chapter, line=line)
    return render(request,'line.html',context)