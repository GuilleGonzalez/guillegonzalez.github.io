"""
This script requires the following initial directory structure:

<project_root>/
├── kjv/
│   └── TEXT-PCE.txt                                # From {extracted} "King James Bible: Pure Cambridge Edition: Text Format: Compressed Zip (1.27 MB)." from https://www.bibleprotector.com/
├── esv/
│   ├── _esv_verses.csv                             # From https://versenotes.org/a-list-of-books-in-the-bible-by-number-of-chapters/ (renamed with '_' prefix)
│   ├── _esv_chapters.csv                           # From https://versenotes.org/a-list-of-books-in-the-bible-by-number-of-chapters/ (renamed with '_' prefix)
│   ├── _esv_books.csv                              # From https://versenotes.org/a-list-of-books-in-the-bible-by-number-of-chapters/ (renamed with '_' prefix)
│   └── _esv_running_chapters.csv (OPTIONALLY)      # From https://versenotes.org/a-list-of-books-in-the-bible-by-number-of-chapters/ (renamed with '_' prefix)
└── bible_stats.py

A Free Open-Source Resource (Not Used): https://openbible.com/downloads.htm
"""

import os
import pandas as pd

METRICS = True
READING_TIMES = True
READING_SPEEDS = range(150, 251, 50)
def wpm(word_count: int, speed):
    time = word_count / speed
    hrs, mins, secs = int(time // 60), int(time % 60), int(float(time * 60) % 60)
    return f'{hrs}hr {mins}m' if hrs > 0 else f'{mins}m {secs}s'

KJV_SRC = os.path.join('kjv', 'TEXT-PCE.txt')
KJV_VERSES = os.path.join('kjv', 'kjv_verses.csv')
KJV_CHAPTERS = os.path.join('kjv', 'kjv_chapters.csv')
KJV_BOOKS = os.path.join('kjv', 'kjv_books.csv')
KJV_SECTIONS = os.path.join('kjv', 'kjv_sections.csv')
KJV_VS_FREQS = os.path.join('kjv', 'KJV-Verse-Frequencies.txt')

ESV_VS_SRC = os.path.join('esv', '_esv_verses.csv')
ESV_CH_SRC = os.path.join('esv', '_esv_chapters.csv')
ESV_BK_SRC = os.path.join('esv', '_esv_books.csv')
ESV_VERSES = os.path.join('esv', 'esv_verses.csv')
ESV_CHAPTERS = os.path.join('esv', 'esv_chapters.csv')
ESV_BOOKS = os.path.join('esv', 'esv_books.csv')
ESV_SECTIONS = os.path.join('esv', 'esv_sections.csv')


def main() -> None:
    kjv()
    esv()
    kjv_verse_freqs(verbose=False, create_txt=True)
    # print_html(KJV_BOOKS, KJV_CHAPTERS)
    # print_html(ESV_BOOKS, ESV_CHAPTERS)


def kjv() -> None:
    def verses() -> None: # Generates KJV Verses File
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

        with open(KJV_SRC) as src:
            lines = src.readlines()

        data = []
        for line in lines:
            ref = abbrev_dict.get(line.split()[0], line.split()[0]) + ' ' + line.split()[1]
            data.append({'Reference': ref, 'Words': (len(line.split())-2) })
        
        pd.DataFrame(data).to_csv(KJV_VERSES, index=False)
        print(f'Successfully Created "{KJV_VERSES}"')


    def chapters() -> None: # Generates KJV Chapters File 
        with open(KJV_VERSES) as src:
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

        if METRICS: kjv_chapters['Wd/Vs'] = round(kjv_chapters['Words'] / kjv_chapters['Verses'], 1)
        if READING_TIMES:   
            for time in READING_SPEEDS: 
                kjv_chapters[f'Time ({time} WPM)'] = kjv_chapters['Words'].apply(lambda x: wpm(x, time))
        
        kjv_chapters.to_csv(KJV_CHAPTERS, index=False)
        print(f'Successfully Created "{KJV_CHAPTERS}"')


    def books() -> None: # Generates KJV Books File 
        with open(KJV_CHAPTERS) as src:
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

        if METRICS:
            kjv_books['Vs/Ch'] = round(kjv_books['Verses'] / kjv_books['Chapters'], 1)
            kjv_books['Wd/Ch'] = round(kjv_books['Words'] / kjv_books['Chapters'], 1)
            kjv_books['Wd/Vs'] = round(kjv_books['Words'] / kjv_books['Verses'], 1)
        if READING_TIMES:
            for time in READING_SPEEDS:
                kjv_books[f'Time ({time} WPM)'] = kjv_books['Words'].apply(lambda x: wpm(x, time))
        
        kjv_books.to_csv(KJV_BOOKS, index=False)
        print(f'Successfully Created "{KJV_BOOKS}"')


    verses()
    chapters() # Prerequisite Functions: verses()
    books() # Prerequisite Functions: verses(), chapters()
    generate_sections(KJV_BOOKS, KJV_SECTIONS)


def esv() -> None:
    verses = pd.read_csv(ESV_VS_SRC)
    chapters = pd.read_csv(ESV_CH_SRC)
    books = pd.read_csv(ESV_BK_SRC).drop('book_num', axis=1)

    # Verses --------------------------------------------------------------------------------------

    verses.rename(columns={'word_count': 'Words'}, inplace=True)
    verses['Reference'] = verses['book'].astype(str) + ' ' + verses['chapter'].astype(str) + ':' + verses['verse'].astype(str)
    verses.set_index('Reference', inplace=True)
    verses.drop(['book', 'chapter', 'verse'], axis=1, inplace=True)
    verses.to_csv(ESV_VERSES)
    print(f'Successfully Created "{ESV_VERSES}"')

    # Chapters ------------------------------------------------------------------------------------

    chapters.rename(columns={'book': 'Book', 'chapter': 'Chapter', 'num_verses': 'Verses', 'num_words': 'Words'}, inplace=True)
    chapters['Reference'] = chapters['Book'].astype(str) + ' ' + chapters['Chapter'].astype(str)
    chapters.set_index('Reference', inplace=True)
    chapters.drop(['Book', 'Chapter'], axis=1, inplace=True)

    if METRICS: chapters['Wd/Vs'] = round(chapters['Words'] / chapters['Verses'], 1)
    if READING_TIMES:
        for time in READING_SPEEDS:
            chapters[f'Time ({time} WPM)'] = chapters['Words'].apply(lambda x: wpm(x, time))

    chapters.to_csv(ESV_CHAPTERS)
    print(f'Successfully Created "{ESV_CHAPTERS}"')

    # Books --------------------------------------------------------------------------------------

    books.rename(columns={'book': 'Book', 'num_chapters': 'Chapters', 'num_verses': 'Verses', 'num_words': 'Words'}, inplace=True)
    books.set_index('Book', inplace=True)
    
    if METRICS:
        books['Vs/Ch'] = round(books['Verses'] / books['Chapters'], 1)
        books['Wd/Ch'] = round(books['Words'] / books['Chapters'], 1)
        books['Wd/Vs'] = round(books['Words'] / books['Verses'], 1)
    if READING_TIMES:
        for time in READING_SPEEDS:
            books[f'Time ({time} WPM)'] = books['Words'].apply(lambda x: wpm(x, time))
    
    books.to_csv(ESV_BOOKS)
    print(f'Successfully Created "{ESV_BOOKS}"')

    # Sections --------------------------------------------------------------------------------------
    generate_sections(ESV_BOOKS, ESV_SECTIONS)


# Generate Section.CSV File(s)
def generate_sections(books_path: str, sections_path: str):
    book = pd.read_csv(books_path).set_index('Book')

    reading_times = [f'Time ({word_count} WPM)' for word_count in READING_SPEEDS]
    if READING_TIMES: book.drop(reading_times, axis=1, inplace=True)
    if METRICS: book.drop(['Vs/Ch', 'Wd/Ch', 'Wd/Vs'], axis=1, inplace=True)
    bk = book.rename(columns={'Chapters': 'c', 'Verses': 'v', 'Words': 'w'})

    sections = [
        {'S': 'Bible', 'B': 66, 'C': bk.sum()['c'], 'V': bk.sum()['v'], 'W': bk.sum()['w']},
        {'S': 'Old Testament', 'B': 39, 'C': bk.iloc[:39].sum()['c'], 'V': bk.iloc[:39].sum()['v'], 'W': bk.iloc[:39].sum()['w']},
        {'S': 'New Testament', 'B': 27, 'C': bk.iloc[39:].sum()['c'], 'V': bk.iloc[39:].sum()['v'], 'W': bk.iloc[39:].sum()['w']},
        {'S': 'Pentateuch', 'B': 5, 'C': bk.iloc[0:5].sum()['c'], 'V': bk.iloc[0:5].sum()['v'], 'W': bk.iloc[0:5].sum()['w']},
        {'S': 'History', 'B': 12, 'C': bk.iloc[5:17].sum()['c'], 'V': bk.iloc[5:17].sum()['v'], 'W': bk.iloc[5:17].sum()['w']},
        {'S': 'Poetry', 'B': 5, 'C': bk.iloc[17:22].sum()['c'], 'V': bk.iloc[17:22].sum()['v'], 'W': bk.iloc[17:22].sum()['w']},
        {'S': 'Major Prophets', 'B': 5, 'C': bk.iloc[22:27].sum()['c'], 'V': bk.iloc[22:27].sum()['v'], 'W': bk.iloc[22:27].sum()['w']},
        {'S': 'Minor Prophets', 'B': 12, 'C': bk.iloc[27:39].sum()['c'], 'V': bk.iloc[27:39].sum()['v'], 'W': bk.iloc[27:39].sum()['w']},
        {'S': 'Gospels', 'B': 4, 'C': bk.iloc[39:43].sum()['c'], 'V': bk.iloc[39:43].sum()['v'], 'W': bk.iloc[39:43].sum()['w']},
        {'S': 'History (Acts)', 'B': 1, 'C': bk.iloc[43:44].sum()['c'], 'V': bk.iloc[43:44].sum()['v'], 'W': bk.iloc[43:44].sum()['w']},
        {'S': 'Pauline Epistles', 'B': 13, 'C': bk.iloc[44:57].sum()['c'], 'V': bk.iloc[44:57].sum()['v'], 'W': bk.iloc[44:57].sum()['w']},
        {'S': 'General Epistles', 'B': 8, 'C': bk.iloc[57:65].sum()['c'], 'V': bk.iloc[57:65].sum()['v'], 'W': bk.iloc[57:65].sum()['w']},
        {'S': 'Apocalypse (Revelation)', 'B': 1, 'C': bk.iloc[65:].sum()['c'], 'V': bk.iloc[65:].sum()['v'], 'W': bk.iloc[65:].sum()['w']},
    ]

    sections_df = pd.DataFrame(sections)
    sections_df.rename(columns={'S': 'Section', 'B': 'Books', 'C': 'Chapters', 'V': 'Verses', 'W': 'Words'}, inplace=True)
    sections_df.set_index('Section', inplace=True)

    if METRICS:
        sections_df['Ch/Book'] = round(sections_df['Chapters'] / sections_df['Books'], 1)
        sections_df['Vs/Book'] = round(sections_df['Verses'] / sections_df['Books'], 1)
        sections_df['Wd/Book'] = round(sections_df['Words'] / sections_df['Books']).astype('int')
        sections_df['Vs/Ch'] = round(sections_df['Verses'] / sections_df['Chapters'], 1)
        sections_df['Wd/Ch'] = round(sections_df['Words'] / sections_df['Chapters'], 1)
        sections_df['Wd/Vs'] = round(sections_df['Words'] / sections_df['Verses'], 1)
    if READING_TIMES:
        for time in READING_SPEEDS:
            sections_df[f'Time ({time} WPM)'] = sections_df['Words'].apply(lambda x: wpm(x, time))

    sections_df.to_csv(sections_path)
    print(f'Successfully Created "{sections_path}"')


# Print in HTML the Code for Bible Statistics
def print_html(books_path: str, sections_path: str):
    books = pd.read_csv(books_path).set_index('Book').to_dict(orient='index')
    sections = pd.read_csv(sections_path).set_index('Section').to_dict(orient='index')

    print()
    for section, data in sections.items():
        print(f'{section}: ({data['Books']} Books | {data['Chapters']:,} Chapters | {data['Verses']:,} Verses | {data['Words']:,} Words)')
    print()
    for book, data in books.items():
        print(f'{book} ({data['Chapters']} Chapters | {data['Verses']:,} Verses | {data['Words']:,} Words)')
    for key, value in sections.items():
        sections[key] = list(value.values())

    def print_section(section: str):
        print(f'\n<h3>{section}:</h3>')
        print(f'<p class="sub-p">({sections[section][0]} Books | {sections[section][1]:,} Chapters | <nobr>{sections[section][2]:,} Verses</nobr> | <nobr>{sections[section][3]:,} Words)</nobr></p>\n')

    print('\n\n\n<h1>Bible Statistics</h1>\n<hr>')
    s = sections['Bible']
    print(f'<p class="mid-p">{s[0]} Books | {s[1]:,} Chapters | <nobr>{s[2]:,} Verses</nobr> | <nobr>{s[3]:,} Words</nobr></p>\n<br>\n')

    for i, (book, data) in books.items():
        if i == 0:
            s = sections['Old Testament']
            print('<h2>Old Testament:</h2>')
            print(f'<p class="sub-p">({s[0]} Books | {s[1]:,} Chapters | <nobr>{s[2]:,} Verses</nobr> | <nobr>{s[3]:,} Words)</nobr></p>')
            print_section('Pentateuch')
        elif i == 5: print_section('History')
        elif i == 17: print_section('Poetry')
        elif i == 22: print_section('Major Prophets')
        elif i == 27: print_section('Minor Prophets')
        elif i == 39:
            s = sections['New Testament']
            print('<br>\n<h2>New Testament:</h2>')
            print(f'<p class="sub-p">({s[0]} Books | {s[1]:,} Chapters | <nobr>{s[2]:,} Verses</nobr> | <nobr>{s[3]:,} Words)</nobr></p>')
            print_section('Gospels')
        elif i == 43: print('\n<h3>History:</h3>')
        elif i == 44: print_section('Pauline Epistles')
        elif i == 57: print_section('General Epistles')
        elif i == 65: print('\n<h3>Apocalypse:</h3>')

        print(f'<p>{book}</p>')
        print(f'<p class="sub-p">({data['Chapters']} Chapters | <nobr>{data['Verses']:,} Verses</nobr> | <nobr>{data['Words']:,} Words)</nobr></p>')
    print('<br>\n<br>\n\n\n')

    '''
    for section, data in sections.items():
        print(f'<h3>{section}:</h3>')
        print(f'<p class="sub-p">({data['Books']} Books | {data['Chapters']:,} Chapters | {data['Verses']:,} Verses | <nobr>{data['Words']:,} Words)</nobr></p>\n')
    '''


def kjv_verse_freqs(verbose: bool = True, create_txt: bool = True):
    from collections import defaultdict
    # table = {'Ge': 'Genesis', 'Ex': 'Exodus', 'Le': 'Leviticus', 'Nu': 'Numbers', 'De': 'Deuteronomy', 'Jos': 'Joshua', 'Jg': 'Judges', 'Ru': 'Ruth', '1Sa': '1 Samuel', '2Sa': '2 Samuel', '1Ki': '1 Kings', '2Ki': '2 Kings', '1Ch': '1 Chronicles', '2Ch': '2 Chronicles', 'Ezr': 'Ezra', 'Ne': 'Nehemiah', 'Es': 'Esther', 'Job': 'Job', 'Ps': 'Psalms', 'Pr': 'Proverbs', 'Ec': 'Ecclesiastes', 'Song': 'Song of Solomon', 'Isa': 'Isaiah', 'Jer': 'Jeremiah', 'La': 'Lamentations', 'Eze': 'Ezekiel', 'Da': 'Daniel', 'Ho': 'Hosea', 'Joe': 'Joel', 'Am': 'Amos', 'Ob': 'Obadiah', 'Jon': 'Jonah', 'Mic': 'Micah', 'Na': 'Nahum', 'Hab': 'Habakkuk', 'Zep': 'Zephaniah', 'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi', 'Mt': 'Matthew', 'Mr': 'Mark', 'Lu': 'Luke', 'Joh': 'John', 'Ac': 'Acts', 'Ro': 'Romans', '1Co': '1 Corinthians', '2Co': '2 Corinthians', 'Ga': 'Galatians', 'Eph': 'Ephesians', 'Php': 'Philippians', 'Col': 'Colossians', '1Th': '1 Thessalonians', '2Th': '2 Thessalonians', '1Ti': '1 Timothy', '2Ti': '2 Timothy', 'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James', '1Pe': '1 Peter', '2Pe': '2 Peter', '1Jo': '1 John', '2Jo': '2 John', '3Jo': '3 John', 'Jude': 'Jude', 'Re': 'Revelation'}
    with open(KJV_SRC) as src: lines = src.readlines()
    verses = defaultdict(list)
    for line in lines:
        ref = ' '.join(line.split()[:2])
         # ref = table.get(line.split()[0], line.split()[0]) + ' ' + line.split()[1]
        verse = ' '.join(line.split()[2:])
        verses[verse].append(ref)
        
    filtered_verses = {k: v for k, v in verses.items() if len(v) > 1}
    sorted_verses = dict(sorted(filtered_verses.items(), key=lambda item: len(item[1]), reverse=True))

    if verbose:
        print('Verses are in the King James Version (KJV) - which is in the Public Domain in the U.S.\nBracketed words are equivalent to italicized words (English words added for fluidity from the translated original language) in traditionally printed KJV Bibles.\nThe format is... {Number of Occurances} -> {The Verse in Parentheses} -> {All the Abbreviated Verse References Separated by Commas}\n')
        for verse, refs in sorted_verses.items():
            print(f'{len(refs)} -> \"{verse}\" -> {", ".join(refs)}')
    if create_txt:
        with open(KJV_VS_FREQS, 'w') as txt:
            txt.write('Verses are in the King James Version (KJV) - which is in the Public Domain in the U.S.\nBracketed words are equivalent to italicized words (English words added for fluidity from the translated original language) in traditionally printed KJV Bibles.\nThe format is... {Number of Occurances} -> {The Verse in Parentheses} -> {All the Abbreviated Verse References Separated by Commas}\n\n')
            for verse, refs in sorted_verses.items():
                txt.write(f'{len(refs)} -> \"{verse}\" -> {", ".join(refs)}\n')
        print(f'Successfully Created "{KJV_VS_FREQS}"')

        '''
        with open('kjv_verse_frequencies (abbrev).txt', 'w') as txt:
            for verse, refs in sorted_verses.items():
                txt.write(f'{", ".join(refs)} -> {verse}\n')

        with open('kjv_verse_frequencies (counts).txt', 'w') as txt:
            for verse, refs in sorted_verses.items():
                txt.write(f'{len(refs)} -> {verse}\n')
        '''


if __name__ == "__main__":
    main()
