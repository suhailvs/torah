from django.core.management.base import BaseCommand
import csv
import importlib.resources
from tanach.models import Word
from tanach.misc import get_csv, calculate_line_number
"""
https://judaism.stackexchange.com/a/76293
Torah: 79,847 words (according to E.S.)
Neviim: 141,414 words (also, according to E. S.)
Kesuvim: 83,640 words (
"""
def get_books_count():
    with importlib.resources.open_text("tanach.csv","counts.csv") as csv_file:
        return list(csv.reader(csv_file))
    

class Command(BaseCommand):
    help = "Quran commands"

    def handle(self, *args, **options):
        # Words
        Word.objects.all().delete()

        self.stdout.write('Loading words...')
        if Word.objects.exists():
            self.stdout.write('Word table is not empty')
        else:            
            objs = []
            words_list = get_csv('words')
            books_count = get_csv('counts')
            for n_book,c_book in enumerate(books_count): #range(1, len(books_count)+1):
                self.stdout.write(f'Loading book {n_book} ...')
                self.stdout.write('='*20)
                for n_chapter,c_chapter in enumerate(c_book):
                    self.stdout.write(f'Loading chapter {n_chapter} ...')
                    for line in range(int(c_chapter)):
                        lineno = calculate_line_number(n_book+1, n_chapter+1,line+1)-1 # since index starts with zero
                        # line_words = words_list[lineno]
                        for position,word in enumerate(words_list[lineno]):                            
                            objs.append(
                                Word(book=n_book+1,chapter=n_chapter+1,line=line+1,
                                position=position+1, token=word)#,meaning=meaning)
                            )
            self.stdout.write('Running bulk create...')
            Word.objects.bulk_create(objs)
            self.stdout.write('Words completed')
        