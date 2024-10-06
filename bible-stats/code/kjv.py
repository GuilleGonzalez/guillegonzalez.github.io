# The Entire King James Bible (KJV) is in the Public Domain in the United States
# Another Resource for Free Open Source Downloads: https://openbible.com/downloads.htm (Free Open-Source Download)
# Derived & Dependant on FILE (https://www.bibleprotector.com/)...
# kjv_raw.txt -> "King James Bible: Pure Cambridge Edition: Text Format: Compressed Zip (1.27 MB)." from https://www.bibleprotector.com/

from bible_stats import BibleStats
import pandas as pd

SRC_FILE = 'kjv/raw_kjv.txt' 
VERSES_PATH = 'kjv/kjv_verses.csv'
CHAPTERS_PATH = 'kjv/kjv_chapters.csv'
BOOKS_PATH = 'kjv/kjv_books.csv'

def main():
    verses()
    chapters() # Requires verses() to have already been executed.
    books() # Requires verses() & chapters() to have already been executed.

# Generates the KJV Verses File
def verses():
    abbrev_dict = {
        'Ge': 'Genesis', 'Ex': 'Exodus', 'Le': 'Leviticus', 'Nu': 'Numbers', 'De': 'Deuteronomy',
        'Jos': 'Joshua', 'Jg': 'Judges', 'Ru': 'Ruth', '1Sa': '1 Samuel', '2Sa': '2 Samuel',
        '1Ki': '1 Kings', '2Ki': '2 Kings', '1Ch': '1 Chronicles', '2Ch': '2 Chronicles',
        'Ezr': 'Ezra', 'Ne': 'Nehemiah', 'Es': 'Esther', 'Job': 'Job', 'Ps': 'Psalms',
        'Pr': 'Proverbs', 'Ec': 'Ecclesiastes', 'Song': 'Song of Solomon', 'Isa': 'Isaiah',
        'Jer': 'Jeremiah', 'La': 'Lamentations', 'Eze': 'Ezekiel', 'Da': 'Daniel', 'Ho': 'Hosea',
        'Joe': 'Joel', 'Am': 'Amos', 'Ob': 'Obadiah', 'Jon': 'Jonah', 'Mic': 'Micah', 'Na': 'Nahum',
        'Hab': 'Habakkuk', 'Zep': 'Zephaniah', 'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi',
        'Mt': 'Matthew', 'Mr': 'Mark', 'Lu': 'Luke', 'Joh': 'John', 'Ac': 'Acts', 'Ro': 'Romans',
        '1Co': '1 Corinthians', '2Co': '2 Corinthians', 'Ga': 'Galatians', 'Eph': 'Ephesians',
        'Php': 'Philippians', 'Col': 'Colossians', '1Th': '1 Thessalonians', '2Th': '2 Thessalonians',
        '1Ti': '1 Timothy', '2Ti': '2 Timothy', 'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews',
        'Jas': 'James', '1Pe': '1 Peter', '2Pe': '2 Peter', '1Jo': '1 John', '2Jo': '2 John',
        '3Jo': '3 John', 'Jude': 'Jude', 'Re': 'Revelation'
    }

    with open(SRC_FILE) as src:
        lines = src.readlines()

    data = []
    for line in lines:
        ref = abbrev_dict.get(line.split()[0], line.split()[0]) + ' ' + line.split()[1]
        data.append({'Reference': ref, 'Words': (len(line.split())-2) })
    
    pd.DataFrame(data).to_csv(VERSES_PATH, index=False)
    print(f'Successfully Created "{VERSES_PATH}"')


# Generates the KJV Chapters File 
def chapters():
    with open(VERSES_PATH) as src:
        lines = src.readlines()

    data, i, prev_ch = [], 1, None
    temp_verse, temp_words = 0, 0
    while i < len(lines):
        curr_ch = lines[i].split(':')[0]
        if i == 1: prev_ch = curr_ch
        if curr_ch != prev_ch:
            data.append({'Reference': prev_ch, 'Verses': temp_verse, 'Words': temp_words})
            temp_verse = temp_words = 0
        temp_verse += 1
        temp_words += int(lines[i].split(':')[1].split(',')[1])
        prev_ch = curr_ch
        i += 1

    data.append({'Reference': prev_ch, 'Verses': temp_verse, 'Words': temp_words})
    kjv_chapters = pd.DataFrame(data)

    if BibleStats.include_metrics: kjv_chapters['Wd/Vs'] = round(kjv_chapters['Words'] / kjv_chapters['Verses'], 1)
    if BibleStats.include_reading_times:   
        for time in BibleStats.reading_speeds: 
            kjv_chapters[f'Time ({time} WPM)'] = kjv_chapters['Words'].apply(lambda x: BibleStats.wpm(x, time))
    
    kjv_chapters.to_csv(CHAPTERS_PATH, index=False)
    print(f'Successfully Created "{CHAPTERS_PATH}"')


# Generates the KJV Books File 
def books():
    with open(CHAPTERS_PATH) as src:
        lines = src.readlines()

    data, i, prev_bk = [], 1, None
    temp_chapter, temp_verse, temp_words = 0, 0, 0
    while i < len(lines):

        curr_bk = lines[i].split()[0]
        if curr_bk in ('1', '2', '3'): curr_bk = ' '.join(lines[i].split()[:2])
        elif curr_bk == 'Song': curr_bk = ' '.join(lines[i].split()[:3])
        if i == 1: prev_bk = curr_bk

        if curr_bk != prev_bk:
            data.append({'Book': prev_bk, 'Chapters': temp_chapter, 'Verses': temp_verse, 'Words': temp_words})
            temp_chapter = temp_verse = temp_words = 0

        temp_chapter += 1
        temp_verse += int(lines[i].split(',')[1])
        temp_words += int(lines[i].split(',')[2])
        prev_bk = curr_bk
        i += 1
    
    data.append({'Book': prev_bk, 'Chapters': temp_chapter, 'Verses': temp_verse, 'Words': temp_words})
    kjv_books = pd.DataFrame(data)

    if BibleStats.include_metrics:
        kjv_books['Vs/Ch'] = round(kjv_books['Verses'] / kjv_books['Chapters'], 1)
        kjv_books['Wd/Ch'] = round(kjv_books['Words'] / kjv_books['Chapters'], 1)
        kjv_books['Wd/Vs'] = round(kjv_books['Words'] / kjv_books['Verses'], 1)
    if BibleStats.include_reading_times:
        for time in BibleStats.reading_speeds:
            kjv_books[f'Time ({time} WPM)'] = kjv_books['Words'].apply(lambda x: BibleStats.wpm(x, time))
    
    kjv_books.to_csv(BOOKS_PATH, index=False)
    print(f'Successfully Created "{BOOKS_PATH}"')


# Runs the main() function.
if __name__ == '__main__':
    main()
