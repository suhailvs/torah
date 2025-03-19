import csv
def get_csv(fn):
    with open(f"tanach/csv/{fn}.csv") as csv_file:
        return list(csv.reader(csv_file))

def calculate_line_number(book_no, chapter, line):
    index = 0
    t_count = get_csv('counts')
    # book = t_count[book_no+1]
    for i in range(len(t_count)):
        chapter_count = t_count[i]
        if i == book_no-1:
            if chapter < 1 or chapter > len(chapter_count):
                return "Invalid chapter number"

            if line < 1 or line > int(chapter_count[chapter - 1]):
                return "Invalid verse number"

            # Sum up all previous chapters' verses
            index += sum(int(c) for c in chapter_count[:chapter - 1])
            
            # Add the verse number (1-based index)
            index += line

            return index

        else:
            # Sum up all verses of previous books
            index += sum(int(c) for c in t_count[i])

    return "Book not found"