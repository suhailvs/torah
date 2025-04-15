from django.shortcuts import render, redirect

from tanach.misc import get_csv, calculate_line_number


# Create your views here.
def showline(request, book=1, chapter=1, line=1):
    if request.method == "POST":
        p = request.POST
        return redirect("/%s/%s/%s/" % (p["book"], p["chapter"], p["line"]))
    context = {"current": {"book": book, "chapter": chapter, "line": line}}
    lineno = calculate_line_number(book, chapter, line) - 1
    context["lineno"] = lineno + 1
    for t in ["words", "en_lines", "en_words"]:
        words_list = get_csv(t)
        try:
            context[t] = words_list[lineno]
        except IndexError:
            context[t] = []
    context["total_words"] = len(context["words"])
    return render(request, "tanach/line.html", context)


def show_word(request, word):
    from tanach.models import Word

    words = Word.objects.filter(book=1, token=word)
    return render(request, "tanach/word.html", {"words": words})


def word_list(request):
    from tanach.models import Word
    from tanach.templatetags.torah_filters import KOREN

    # word list of genesis. words = 20629, unique_words=5007
    qs = Word.objects.filter(book=1).values("token").distinct()
    get_words_startswith = lambda l: qs.extra(
        where=["SUBSTR(token, 1, %s) = %s"], params=[1, l]
    ).order_by("token")
    word_group = {l: get_words_startswith(l) for l in KOREN}
    return render(request, "tanach/word_list.html", {"words": word_group})
