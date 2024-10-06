translation_table = str.maketrans({
    "“": "\"",
    "”": "\"",
    "’": "\'",
    "‘": "\'",
    "—": " &#8212; ",
    "…": "..."
})

def main(): 
    while True:
        try:
            url = input('\nUrl: ').strip() # From Bible Gateway
            version = url.split('&version=')[1]
            
            ref = url.split('?search=')[1].split('&version=')[0]
            ref = ref.replace('+', ' ').replace('%3A', ':').title()

            first_verse = ref.split(':')[1].split('-')[0] if '-' in ref else ref.split(':')[1]
            verse = input("Verse: ").strip().translate(translation_table)

            print(f'\n<!--{ref}--><p><sup>{first_verse} </sup>{verse} <nobr><a href="{url}" target="_blank">{ref}</a> ({version})</nobr></p>\n')
            print(f'<nobr><a href="{url}" target="_blank">{ref}</a></nobr>\n')           
        except IndexError:
            print('\nAn Error Occured.\n')


if __name__ == '__main__':
    main()





"""
reorder.py

##########################################################################

old_testament= [
    'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 
    'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', 
    '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 
    'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm', # OR "Psalms" Plural 
    'Proverbs', 'Ecclesiastes', 'Song of Solomon', 
    'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 
    'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 
    'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 
    'Haggai', 'Zechariah', 'Malachi'
]
new_testament = [
    'Matthew', 'Mark', 'Luke', 'John', 'Acts', 
    'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 
    'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', 
    '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 
    'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', 
    '1 John', '2 John', '3 John', 'Jude', 'Revelation'
]

bible_books = old_testament + new_testament
src = 'contents.txt'

def replace_nums(s: str) -> str:
    return ''.join([c for c in s if not c.isdigit()])

refs, refs_and_verses = [], []
with open(src) as data:
    for line in data.readlines():
        line = line.strip()
        for book in bible_books:
            if f' {book} ' not in line: continue # Move on to the next iteration.
            if (book == 'John' and any(_ in line for _ in ['1 John', '2 John', '3 John'])):
                continue # Move on to the next iteration.
 
            # Get the verse and reference as separate variables.
            verse, ref = line.split(f' {book} ')
            ref = f'{book} {ref.strip()}'
            verse = replace_nums(verse).strip().replace('  ', ' ')
                
            # 2 Timothy 3:1 (NIV) -> Mark this... -----> It is a special case.
            if ref.startswith('Mark this:'): continue # Move on to the next iteration.

            refs.append(f'{ref}\n')
            refs_and_verses.append(f'{ref} -> {verse}\n')

with open('output.txt', 'w') as export:
    export.writelines(refs_and_verses)

# with open('refs.txt', 'w') as export:
   # export.writelines(refs)

##########################################################################

"""
