from django.shortcuts import render, redirect
from tanach.models import Word
from tanach.misc import get_csv, calculate_line_number
# Create your views here.
def showline(request, book=1, chapter=1, line=1):
    if request.method=='POST':
        p=request.POST
        return redirect('/%s/%s/%s/'%(p['book'],p['chapter'],p['line']))
    context = {'current': {'book':book, 'chapter':chapter, 'line':line}}
    # context['words']=Word.objects.filter(book=book,chapter=chapter, line=line)
    
    lineno = calculate_line_number(book,chapter,line)-1 # since index starts with zero
    context['lineno']=lineno+1
    for t in ['words','en_lines','en_words']:
        words_list = get_csv(t)
        context[t]=words_list[lineno] #' '.join(words_list[lineno])
    context['total_words']=len(context['words'])
    return render(request,'line.html',context)