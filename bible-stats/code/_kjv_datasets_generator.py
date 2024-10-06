"""
Filename: kjv_datasets_generator.py
Author: Guillermo Gonzalez (guillermofwgonzalez@gmail.com)
Creation Date: 2023
Last Modified: 2024-08-25
Description: Generate CSV files of Data On the Verses, Chapters, Books, and Sections of the KJV Bible by Simply Running This Script.
Dependencies/Usage: 
    1) Python & The Pandas Python Library
    2) "King James Bible: Pure Cambridge Edition: Text Format: Compressed Zip (1.27 MB)." from https://www.bibleprotector.com/
        - The Entire King James Bible is in the Public Domain in the United States (https://en.wikipedia.org/wiki/King_James_Version#Copyright_status).
        - Unzip the Compressed Zip File & Rename the .txt to Whatever You Have it Named as in the "KJV_SOURCE_FILE" Variable Below
        - Ensure All the Folder Paths in the CONSTANT Python Variables Below Exist & Are in the Correct Relative Paths
    3) Run This Script - Good Luck if it Doesn't Work...
Notes from the Author: Sorry that this script is not more thoroughly commented. I originally wrote the script a long while back and do not currently have the time to reupdate and comment it through.
""" 

import pandas as pd # Import the Pandas Python Library

# METRICS Include the Following: Ch/Book, Vs/Book, Wd/Book, Vs/Ch, Wd/Ch, Wd/Vs
# READING TIMES Include the Approximate Times It Takes to Read Through the Section at Given Word Per Minutes (WPM): See the " WPM - For Calculating Reading Speeds" Below.
INCLUDE_METRICS, INCLUDE_READING_TIMES = True, True
    
# ALL INPUT/OUTPUT FILE PATHS LISTED BELOW MUST HAVE THE CORRESPONDING FOLDERS EXISTING.
KJV_SOURCE_FILE = 'raw_kjv.txt' # See #2 of "Dependencies/Usage" Above... "King James Bible: Pure Cambridge Edition: Text Format: Compressed Zip (1.27 MB)." from https://www.bibleprotector.com/
KJV_VERSES_PATH = 'kjv_verses.csv'
KJV_CHAPTERS_PATH = 'kjv_chapters.csv'
KJV_BOOKS_PATH = 'kjv_books.csv'
KJV_SECTIONS_PATH = 'kjv_sections.csv'


# WPM - For Calculating Reading Speeds
START_WPM, END_WPM, WPM_INCREMENT = 150, 250, 50
reading_speeds = range(START_WPM, END_WPM+1, WPM_INCREMENT)
def wpm(word_count: int, wpm_speed): # This wpm() function takes a word count and WPM speed to calculate in Hours/Minutes/Seconds how long it will take to read the given selection.
    time = word_count / wpm_speed
    hrs, mins, secs = int(time // 60), int(time % 60), int(float(time * 60) % 60)
    return f'{hrs}hr {mins}m' if hrs > 0 else f'{mins}m {secs}s'


def main():
    generate_kjv_verses()
    generate_kjv_chapters() # Requires kjv_verses() to have already been executed.
    generate_kjv_books() # Requires kjv_verses() & kjv_chapters() to have already been executed.
    generate_kjv_sections() # Requires kjv_verses(), kjv_chapters(), & kjv_books() to have already been executed.


# Generates the KJV Verses File (The Function isn't Commented)
def generate_kjv_verses():
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

    with open(KJV_SOURCE_FILE) as src:
        lines = src.readlines()

    data = []
    for line in lines:
        ref = abbrev_dict.get(line.split()[0], line.split()[0]) + ' ' + line.split()[1]
        data.append({'Reference': ref, 'Words': (len(line.split())-2) })
    pd.DataFrame(data).to_csv(KJV_VERSES_PATH, index=False)
    print(f'Successfully Created "{KJV_VERSES_PATH}"')


# Generates the KJV Chapters File (The Function isn't Commented)
def generate_kjv_chapters():
    with open(KJV_VERSES_PATH) as src:
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
    if INCLUDE_METRICS: kjv_chapters['Wd/Vs'] = round(kjv_chapters['Words'] / kjv_chapters['Verses'], 1)
    if INCLUDE_READING_TIMES: 
        for time in reading_speeds: 
            kjv_chapters[f'Time ({time} WPM)'] = kjv_chapters['Words'].apply(lambda x: wpm(x, time))

    kjv_chapters.to_csv(KJV_CHAPTERS_PATH, index=False)
    print(f'Successfully Created "{KJV_CHAPTERS_PATH}"')


# Generates the KJV Books File (The Function isn't Commented)
def generate_kjv_books():
    with open(KJV_CHAPTERS_PATH) as src:
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

    if INCLUDE_METRICS: 
        kjv_books['Vs/Ch'] = round(kjv_books['Verses'] / kjv_books['Chapters'], 1)
        kjv_books['Wd/Ch'] = round(kjv_books['Words'] / kjv_books['Chapters'], 1)
        kjv_books['Wd/Vs'] = round(kjv_books['Words'] / kjv_books['Verses'], 1)
    if INCLUDE_READING_TIMES:
        for time in reading_speeds:
            kjv_books[f'Time ({time} WPM)'] = kjv_books['Words'].apply(lambda x: wpm(x, time))

    kjv_books.to_csv(KJV_BOOKS_PATH, index=False)
    print(f'Successfully Created "{KJV_BOOKS_PATH}"')


# Generates the KJV Sections File (The Function isn't Commented)
def generate_kjv_sections():
    book = pd.read_csv(KJV_BOOKS_PATH).set_index('Book')
    reading_times = [f'Time ({word_count} WPM)' for word_count in reading_speeds]
    
    if INCLUDE_READING_TIMES: book.drop(reading_times, axis=1, inplace=True)
    if INCLUDE_METRICS: book.drop(['Vs/Ch', 'Wd/Ch', 'Wd/Vs'], axis=1, inplace=True)
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

    if INCLUDE_METRICS:
        sections_df['Ch/Book'] = round(sections_df['Chapters'] / sections_df['Books'], 1)
        sections_df['Vs/Book'] = round(sections_df['Verses'] / sections_df['Books'], 1)
        sections_df['Wd/Book'] = round(sections_df['Words'] / sections_df['Books']).astype('int')

        sections_df['Vs/Ch'] = round(sections_df['Verses'] / sections_df['Chapters'], 1)
        sections_df['Wd/Ch'] = round(sections_df['Words'] / sections_df['Chapters'], 1)
        sections_df['Wd/Vs'] = round(sections_df['Words'] / sections_df['Verses'], 1)

    if INCLUDE_READING_TIMES:
        for time in reading_speeds:
            sections_df[f'Time ({time} WPM)'] = sections_df['Words'].apply(lambda x: wpm(x, time))

    sections_df.to_csv(KJV_SECTIONS_PATH)
    print(f'Successfully Created "{KJV_SECTIONS_PATH}"')
    

# Runs the main() function.
if __name__ == '__main__':
    main()
