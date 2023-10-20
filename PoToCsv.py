import os
import fnmatch
import csv
import polib

def find_po_files(directory):
    """
    Find all .po files in the given directory and its subdirectories.
    """
    po_files = []

    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.po'):
            po_files.append(os.path.join(root, filename))

    return po_files

def merge_to_csv(po_files, csv_output_path):
    """
    Merge multiple .po files into a single CSV file.
    """
    translations = {}
    languages = set()

    for po_file_path in po_files:
        po_data = polib.pofile(po_file_path)
        lang = os.path.basename(os.path.dirname(po_file_path))  # Get the folder name as the language identifier
        languages.add(lang)

        for entry in po_data:
            key = (entry.msgctxt, entry.msgid)
            if key not in translations:
                translations[key] = {}
            translations[key][lang] = entry.msgstr

    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['msgctxt', 'msgid'] + list(languages)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)  # Quote all fields
        writer.writeheader()

        for (msgctxt, msgid), langs in translations.items():
            row = {'msgctxt': msgctxt, 'msgid': msgid}
            for lang in languages:
                row[lang] = langs.get(lang, "")
            writer.writerow(row)

if __name__ == '__main__':
    directory = 'po2csv'
    po_files = find_po_files(directory)
    csv_output_path = 'merged_translations.csv'
    
    merge_to_csv(po_files, csv_output_path)
    print(f"Merged translations saved to {csv_output_path}")
