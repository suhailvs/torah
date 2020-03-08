from django.conf import settings
from django.shortcuts import render, redirect
import os, json
JSON_FOLDER = os.path.join(settings.BASE_DIR, 'torah', 'json')

def get_line(lang,c, l='total'):
    fp = os.path.join(JSON_FOLDER, lang, f"{c['title']}.json")
    data = json.loads(open(fp).read())
    lines = data['text'][c['chapter']-1]
    return len(lines) if l=='total' else lines[l]

def get_segment(c,line):
    fp = open(os.path.join(JSON_FOLDER, 'g_mp3', f"{c['chapter']}.txt"))
    lines = fp.readlines()
    try: 
        return [lines[line], lines[line+1]]
    except IndexError:
        return ['1','2']

def showline(c, line):
    return {
        'paleo': get_line('paleo',c, line)[::-1],
        'english_mtt': get_line('english_mtt',c, line),
        'english': get_line('english',c, line),
        'hebrew': get_line('hebrew',c, line),
        'malayalam': get_line('malayalam',c, line),
        'segment':get_segment(c, line)
    }
    

def showchapter(request, title='genesis', chapter=1):
    if request.method=='POST':
        return redirect(f"/{request.POST['title']}/{request.POST['chapter']}/")

    context = {'title':title, 'chapter':chapter, 'lines': []}
    total_lines = get_line('paleo', context)
    for line in range(total_lines):
        context['lines'].append(showline(context,line))
    return render(request,'home.html',context)

