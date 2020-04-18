from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

import os, json
JSON_FOLDER = os.path.join(settings.BASE_DIR, 'torah', 'json')

class ChapterView(View):
    def get_line(self, lang,l='total'):
        fp = os.path.join(JSON_FOLDER, lang, f"{self.context['title']}.json")
        data = json.loads(open(fp).read())
        lines = data['text'][self.context['chapter']-1]
        return len(lines) if l=='total' else lines[l]

    def get_segment(self, line):
        """ For mp3"""
        try:
            fp = open(os.path.join(JSON_FOLDER, 'g_mp3', f"{self.context['chapter']}.txt"))
            lines = fp.readlines()
            return [lines[line], lines[line+1]]
        except (FileNotFoundError, IndexError) as error:
            # if file or line doesn't exist, dummy
            return ['1','2']

    def get_translations(self, line):
        return {
            'paleo': self.get_line('paleo',line)[::-1],
            # 'english_mtt': self.get_line('english_mtt',line),
            'english': self.get_line('english',line),
            # 'hebrew': self.get_line('hebrew',line),
            # 'malayalam': self.get_line('malayalam',line),
            'segment':self.get_segment(line)
        }

    def get(self, request, title='genesis', chapter=1):
        self.context = {'title':title, 'chapter':chapter, 'lines': []}
        total_lines = self.get_line('paleo')
        for line in range(total_lines):
            self.context['lines'].append(self.get_translations(line))
        return render(request,'home.html',self.context)


def showoutline(request, title='genesis'):
    fp = os.path.join(JSON_FOLDER, 'outline', f"{title}.json")
    data = json.loads(open(fp).read())
    return render(request,'outline.html', {'outline': data, 'title': title})
