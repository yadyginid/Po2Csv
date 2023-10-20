import os
import csv
import polib

def csv_to_po(csv_file_path, output_directory, original_po_directory):
    """
    Convert a CSV file back to multiple .po files.
    """
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        languages = [field for field in reader.fieldnames if field not in ['msgid', 'msgctxt']]

        for lang in languages:
            original_po_path = os.path.join(original_po_directory, lang, 'Game.po')
            original_po = polib.pofile(original_po_path)
            new_po = polib.POFile()
            
            # Copy metadata from original .po file
            new_po.metadata = original_po.metadata

            csv_data = {row['msgid']: row[lang] for row in reader}
            csvfile.seek(0)  # Reset CSV reader position for next iteration

            for entry in original_po:
                if entry.msgid in csv_data:
                    entry.msgstr = csv_data[entry.msgid]
                new_po.append(entry)

            output_po_path = os.path.join(output_directory, lang, 'Game.po')
            os.makedirs(os.path.dirname(output_po_path), exist_ok=True)
            new_po.save(output_po_path)
            print(f"Updated .po file saved to {output_po_path}")

if __name__ == '__main__':
    csv_file_path = 'merged_translations.csv'
    output_directory = 'csv2po'
    original_po_directory = 'po2csv'
    
    csv_to_po(csv_file_path, output_directory, original_po_directory)
