# "kjv.py" & "esv.py" must have been ran respectively.
from bible_stats import BibleStats
import pandas as pd

VERSION = 'esv'
BOOKS_PATH = f'{VERSION}/{VERSION}_books.csv'
SECTIONS_PATH = f'{VERSION}/{VERSION}_sections.csv'

def main():
    generate_sections()
    print_html()

# Generate the Sections.CSV File(s)
def generate_sections():
    book = pd.read_csv(BOOKS_PATH).set_index('Book')

    reading_times = [f'Time ({word_count} WPM)' for word_count in BibleStats.reading_speeds]
    if BibleStats.include_reading_times: book.drop(reading_times, axis=1, inplace=True)
    if BibleStats.include_metrics: book.drop(['Vs/Ch', 'Wd/Ch', 'Wd/Vs'], axis=1, inplace=True)
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

    if BibleStats.include_metrics:
        sections_df['Ch/Book'] = round(sections_df['Chapters'] / sections_df['Books'], 1)
        sections_df['Vs/Book'] = round(sections_df['Verses'] / sections_df['Books'], 1)
        sections_df['Wd/Book'] = round(sections_df['Words'] / sections_df['Books']).astype('int')
        sections_df['Vs/Ch'] = round(sections_df['Verses'] / sections_df['Chapters'], 1)
        sections_df['Wd/Ch'] = round(sections_df['Words'] / sections_df['Chapters'], 1)
        sections_df['Wd/Vs'] = round(sections_df['Words'] / sections_df['Verses'], 1)
    if BibleStats.include_reading_times:
        for time in BibleStats.reading_speeds:
            sections_df[f'Time ({time} WPM)'] = sections_df['Words'].apply(lambda x: BibleStats.wpm(x, time))

    sections_df.to_csv(SECTIONS_PATH)
    print(f'Successfully Created "{SECTIONS_PATH}"')


# Print in HTML the Code for Bible Statistics
def print_html():
    books = pd.read_csv(BOOKS_PATH).set_index('Book').to_dict(orient='index')
    sections = pd.read_csv(SECTIONS_PATH).set_index('Section').to_dict(orient='index')
    print()

    for section, data in sections.items():
        print(f'{section}: ({data['Books']} Books | {data['Chapters']:,} Chapters | {data['Verses']:,} Verses | {data['Words']:,} Words)')
    print()
    for book, data in books.items():
        print(f'{book} ({data['Chapters']} Chapters | {data['Verses']:,} Verses | {data['Words']:,} Words)')

    for key, value in sections.items():
        sections[key] = list(value.values())

    # -------------------------------------------------------------------------------------

    def print_section(section: str):
        print(f'\n<h3>{section}:</h3>')
        print(f'<p class="sub-p">({sections[section][0]} Books | {sections[section][1]:,} Chapters | <nobr>{sections[section][2]:,} Verses</nobr> | <nobr>{sections[section][3]:,} Words)</nobr></p>\n')

    print('\n\n\n<h1>Bible Statistics</h1>\n<hr>')
    s = sections['Bible']
    print(f'<p class="mid-p">{s[0]} Books | {s[1]:,} Chapters | <nobr>{s[2]:,} Verses</nobr> | <nobr>{s[3]:,} Words</nobr></p>\n<br>\n')

    s = sections['Old Testament']
    print('<h2>Old Testament:</h2>')
    print(f'<p class="sub-p">({s[0]} Books | {s[1]:,} Chapters | <nobr>{s[2]:,} Verses</nobr> | <nobr>{s[3]:,} Words)</nobr></p>')

    print_section('Pentateuch')

    i = 0
    for book, data in books.items():
        if i == 5: print_section('History')
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
        elif i == 65: print('\n<h3>Apocrypha:</h3>')

        print(f'<p>{book}</p>')
        print(f'<p class="sub-p">({data['Chapters']} Chapters | <nobr>{data['Verses']:,} Verses</nobr> | <nobr>{data['Words']:,} Words)</nobr></p>')
        i += 1
    print('<br>\n<br>\n\n\n')

    '''
    for section, data in sections.items():
        print(f'<h3>{section}:</h3>')
        print(f'<p class="sub-p">({data['Books']} Books | {data['Chapters']:,} Chapters | {data['Verses']:,} Verses | <nobr>{data['Words']:,} Words)</nobr></p>')
        print()
    '''

if __name__ == '__main__':
    main()
