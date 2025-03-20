import csv
from tanach.books import TANACH_BOOKS
def get_csv(fn):
    with open(f"tanach/csv/{fn}.csv") as csv_file:
        return list(csv.reader(csv_file))

def calculate_line_number(book_no, chapter, line):
    index = 0    
    for i in range(len(TANACH_BOOKS)):
        chapter_count = TANACH_BOOKS[i]['chapters']
        if i == book_no-1:
            if chapter < 1 or chapter > len(chapter_count):
                return "Invalid chapter number"

            if line < 1 or line > chapter_count[chapter - 1]:
                return "Invalid verse number"

            # Sum up all previous chapters' verses
            index += sum(chapter_count[:chapter - 1])
            
            # Add the verse number (1-based index)
            index += line

            return index

        else:
            # Sum up all verses of previous books
            index += sum(chapter_count)

    return "Book not found"