import glob

import pandas as pd
from pandas.errors import EmptyDataError
from tqdm import tqdm

from exporters import DropBlankFieldsXmlItemExporter
from items import JobDetails


def convert_to_item(row):
    d = row.to_dict()
    # filter all non-NaN keys before creating a JobDetails item
    d = dict(filter(lambda item: not pd.isnull(item[1]), d.items()))
    return JobDetails(d)


def xmlencode(desc: str):
    return desc.encode('ascii', 'xmlcharrefreplace').decode('utf-8')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('glob_path', help='glob path for files to be merged')
    parser.add_argument('output_path',
                        help='output file name',
                        default='merged.xml',
                        nargs='?')
    args = parser.parse_args()

    file_paths = glob.glob(args.glob_path)
    all_items = []

    for path in tqdm(file_paths):
        try:
            # TODO: for now, assume files are always CSV
            df = pd.read_csv(path)
        except EmptyDataError as e: 
            print(f'Encountered empty CSV ({path}), skipping...')
            continue

        print(f'Merging CSV: {path}')
        
        # encode any fields that may contain invalid chars
        try:
            df['description'] = df['description'].fillna("").astype(str).apply(xmlencode)
        except Exception as e:
            print(f'Encountered error while encoding columns to XML ({path}), skipping...')
            print(f'Error detail: {e}')
            continue

        # convert CSV to scrapy items
        try:
            items = df.apply(convert_to_item,
                             axis=1).tolist()
        except Exception as e:
            print(f'Encountered error while converting CSV data ({path}) to scrapy item, skipping...')
            print(f'Error detail: {e}')
            continue

        all_items.extend(items)

    print(f'Merged {len(file_paths)} CSVs: {len(all_items)} jobs in total.')
    
    # use DropBlankFieldsXmlItemExporter to export a final merged XML
    with open(args.output_path, 'w') as output_file:
        # use iso-8859-1 so latin characters can be used in XML
        exporter = DropBlankFieldsXmlItemExporter(output_file, encoding="iso-8859-1")
        exporter.start_exporting()
        for item in all_items:
            exporter.export_item(item)
        exporter.finish_exporting()
