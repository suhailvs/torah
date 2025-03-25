from django.shortcuts import render, redirect

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
        try:
            context[t]=words_list[lineno] #' '.join(words_list[lineno])
        except IndexError:
            context[t]=[]
    context['total_words']=len(context['words'])
    return render(request,'tanach/line.html',context)




def show_word(request, word):
    words = Word.objects.filter(book=1,token=word)
    return render(request, "tanach/word.html", {"words": words})

from django.db.models import Max, Case, When, Value, CharField
from tanach.models import Word
from tanach.templatetags.torah_filters import KOREN
def word_list(request):
    # word list of genesis. words = 20629, unique_words=5007
    conditions = [When(token__startswith=l, then=Value(l)) for l in KOREN]
    letter_group = Case(*conditions, default=Value("Other"), output_field=CharField())
    words = Word.objects.filter(book=1).values("token").distinct().annotate(group=letter_group)
    word_group = {l: words.filter(group=l) for l in KOREN}
    return render(request, "tanach/word_list.html", {"words": word_group})
