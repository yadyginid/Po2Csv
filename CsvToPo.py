import os
import csv
import polib

def csv_to_po(csv_file_path, output_directory, original_po_directory):
    """
    Convert a CSV file back to multiple .po files.
    """
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        languages = reader.fieldnames[1:]  # Exclude 'msgid'

        for lang in languages:
            original_po_path = os.path.join(original_po_directory, lang, 'Game.po')
            original_po = polib.pofile(original_po_path)

            # Update translations in the original .po file using the CSV data
            for row in reader:
                entry = original_po.find(row['msgid'])
                if entry:
                    entry.msgstr = row[lang]

            output_po_path = os.path.join(output_directory, lang, 'Game.po')
            os.makedirs(os.path.dirname(output_po_path), exist_ok=True)
            original_po.save(output_po_path)
            print(f"Updated .po file saved to {output_po_path}")

            csvfile.seek(0)  # Reset CSV reader position for next language

if __name__ == '__main__':
    csv_file_path = 'merged_translations.csv'
    output_directory = 'csv2po'
    original_po_directory = 'po2csv'
    
    csv_to_po(csv_file_path, output_directory, original_po_directory)
