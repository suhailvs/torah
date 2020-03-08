"""
Usage: 

$ ./manage.py shell
import site_generator
site_generator.generate()
"""

from django.template.loader import render_to_string
import os, json

class GenerateHtml:
    def __init__(self):
        self.titles = ['genesis','exodus','leviticus','numbers','deuteronomy']
        self.translations = ['paleo', 'english_mtt', 'malayalam'] # 'english', 'malayalam']
        self.datas = self.get_datas_dict()

    def generate(self):        
        for title in self.titles:
            paleo = self.datas['paleo'][title]
            total_chapters = len(paleo)
            for chapter in range(total_chapters):
                context = {'title':title, 'chapter':chapter+1, 'lines': [], 'total_chapters':total_chapters}
                # if chapter == 2: break
                total_lines = len(paleo[chapter])
                for line in range(total_lines):
                    dict_line_trans = {}
                    for k in self.translations:
                        try:
                            dict_line_trans[k] = paleo[chapter][line][::-1] if k=='paleo' else self.datas[k][title][chapter][line]
                        except IndexError:
                            print(k, chapter, line)

                    context['lines'].append(dict_line_trans)
                
                self.create_html_file(context)

    def load_json(self, lang='paleo', title='genesis'):
        fp = os.path.join('torah', 'json', lang, f"{title}.json")
        return json.loads(open(fp).read())['text']

    def get_datas_dict(self):
        datas = {}
        for lang in self.translations: # 'english', 'malayalam']:
            datas[lang] = {}
            for title in self.titles:
                datas[lang][title] = self.load_json(lang,title)
        return datas

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
            filedata = render_to_string('static.html', context)
            fp = open('../docs/index.html','w')
            fp.write(filedata)  

def generate():
    c=GenerateHtml()
    c.generate()