"""
Usage: 

$ ./manage.py shell
import site_generator
site_generator.generate()
"""

from django.template.loader import render_to_string
import os, json
from tanach.books import TANACH_BOOKS
from tanach.misc import get_csv, calculate_line_number

class GenerateHtml:
    def __init__(self):
        self.titles = [b['book'].lower() for b in TANACH_BOOKS[:5]] #['genesis','exodus','leviticus','numbers','deuteronomy']
        self.translations = ['paleo','english','english_line'] #'english_mtt', 'malayalam'] # 'english', 'malayalam']
        self.datas = self.get_datas_dict()

    def get_audio_segment(self, chapter,line):
        try:
            fp = open(os.path.join('tanach', 'json', 'g_mp3', f"{chapter}.txt"))
            lines = fp.readlines()
            return [lines[line], lines[line+1]]
        except (FileNotFoundError, IndexError) as error:
            # if file or line doesn't exist, dummy
            return ['1','2']

    def generate(self):
        for n_book,c_book in enumerate(TANACH_BOOKS[:5]): # only torah
            print(f'Loading book {c_book["book"]} ...')
            total_chapters = len(c_book['chapters'])
            for n_chapter,c_chapter in enumerate(c_book['chapters']):
                context = {'title':c_book["book"].lower(), 'chapter':n_chapter+1, 'lines': [], 'total_chapters':total_chapters}
                for line in range(c_chapter):
                    dict_line_trans = {'segment':self.get_audio_segment(n_chapter+1, line)}
                    for k in self.translations:
                        lineno = calculate_line_number(n_book+1, n_chapter+1,line+1)-1
                        try:
                            dict_line_trans[k] = self.datas[k][lineno] #[title][chapter][line]
                        except IndexError:
                            print(k, n_chapter, line)

                    context['lines'].append(dict_line_trans)
                self.create_html_file(context)

    def get_datas_dict(self):
        datas = {}
        for lang in self.translations:
            csv_names={'paleo':'words','english':'en_words','english_line':'en_lines'}
            datas[lang] = get_csv(csv_names[lang])
        return datas

    def create_outline_html_files(self,context):
        """Generate 5 Outline html files
        1.html, 2.html, 3.html, 4.html, 5.html"""
        for i, title in enumerate(self.titles):
            fp = os.path.join('tanach', 'json', 'outline', f"{title}.json")
            data = json.loads(open(fp).read())
            context_two = {'title': title, 'title_number': i+1,'outline':data }
            filedata = render_to_string('static_outline.html', dict(context, **context_two))
            fp = open(f'../docs/{i+1}.html','w')
            fp.write(filedata)  

    def create_html_file(self, context):
        context['static_url'] = '../static/'
        context['site_url'] = 'https://suhailvs.github.io/torah/'
        title = context['title']
        context['title_number'] = self.titles.index(title)+1
        chapter = context['chapter']
        html_dir = os.path.join('..', 'docs', str(context['title_number']))
        fname = '{0}/{1}.html'.format(html_dir,chapter)
        filedata = render_to_string('static.html', context)

        if not os.path.exists(html_dir):
            os.makedirs(html_dir)

        print('Book: {0}, Chapter: {1}'.format(title,chapter))
        fp = open(fname, 'w')
        fp.write(filedata)
        
        if title=='genesis' and chapter==1:
            context['static_url'] = 'static/'
            self.create_outline_html_files(context)
            filedata = render_to_string('static.html', context)
            fp = open('../docs/index.html','w')
            fp.write(filedata)  

def g():
    c=GenerateHtml()
    c.generate()

