# Derived & Dependent on FILES...
# raw_esv_verses.csv -> https://versenotes.org/a-list-of-books-in-the-bible-by-number-of-chapters/
# raw_esv_chapters.csv -> https://versenotes.org/a-list-of-books-in-the-bible-by-number-of-chapters/
# raw_esv_books.csv -> https://versenotes.org/a-list-of-books-in-the-bible-by-number-of-chapters/

from bible_stats import BibleStats
import pandas as pd

def main():
    VERSES_PATH = 'esv/esv_verses.csv'
    CHAPTERS_PATH = 'esv/esv_chapters.csv'
    BOOKS_PATH = 'esv/esv_books.csv'
    verses = pd.read_csv('esv/raw_esv_verses.csv')
    chapters = pd.read_csv('esv/raw_esv_chapters.csv')
    books = pd.read_csv('esv/raw_esv_books.csv').drop('book_num', axis=1)

    # Verses --------------------------------------------------------------------------------------

    verses.rename(columns={'word_count': 'Words'}, inplace=True)
    verses['Reference'] = verses['book'].astype(str) + ' ' + verses['chapter'].astype(str) + ':' + verses['verse'].astype(str)
    verses.set_index('Reference', inplace=True)
    verses.drop(['book', 'chapter', 'verse'], axis=1, inplace=True)
    verses.to_csv(VERSES_PATH)
    print(f'Successfully Created "{VERSES_PATH}"')

    # Chapters ------------------------------------------------------------------------------------

    chapters.rename(columns={'book': 'Book', 'chapter': 'Chapter', 'num_verses': 'Verses', 'num_words': 'Words'}, inplace=True)
    chapters['Reference'] = chapters['Book'].astype(str) + ' ' + chapters['Chapter'].astype(str)
    chapters.set_index('Reference', inplace=True)
    chapters.drop(['Book', 'Chapter'], axis=1, inplace=True)

    if BibleStats.include_metrics: chapters['Wd/Vs'] = round(chapters['Words'] / chapters['Verses'], 1)
    if BibleStats.include_reading_times:
        for time in BibleStats.reading_speeds:
            chapters[f'Time ({time} WPM)'] = chapters['Words'].apply(lambda x: BibleStats.wpm(x, time))

    chapters.to_csv(CHAPTERS_PATH)
    print(f'Successfully Created "{CHAPTERS_PATH}"')

    # Books --------------------------------------------------------------------------------------

    books.rename(columns={'book': 'Book', 'num_chapters': 'Chapters', 'num_verses': 'Verses', 'num_words': 'Words'}, inplace=True)
    books.set_index('Book', inplace=True)
    
    if BibleStats.include_metrics:
        books['Vs/Ch'] = round(books['Verses'] / books['Chapters'], 1)
        books['Wd/Ch'] = round(books['Words'] / books['Chapters'], 1)
        books['Wd/Vs'] = round(books['Words'] / books['Verses'], 1)
    if BibleStats.include_reading_times:
        for time in BibleStats.reading_speeds:
            books[f'Time ({time} WPM)'] = books['Words'].apply(lambda x: BibleStats.wpm(x, time))
    
    books.to_csv(BOOKS_PATH)
    print(f'Successfully Created "{BOOKS_PATH}"')


if __name__ == '__main__':
    main()
