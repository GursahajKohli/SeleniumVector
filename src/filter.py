import configparser
import glob
import re
from configparser import SectionProxy
from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError
from tqdm import tqdm


def read_config(config_path: Path, section: str = 'DEFAULT') -> SectionProxy:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config[section]


def apply_filter(dataframe: pd.DataFrame,
                 filter: SectionProxy) -> pd.DataFrame:
    df_ = dataframe.copy()

    for field in filter:
        field_regex = re.compile(filter[field], re.IGNORECASE)
        select = df_[field].str.contains(field_regex, regex=True, na=True)
        df_ = df_[select]

    return df_


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config', help='path of config folder for filtering all or per-site')
    parser.add_argument('input_path',
                        help='glob path for files to be filtered')
    parser.add_argument('output_path',
                        help='(optional) location to store filtered files; \
                        if not provided, will overwrite files specified in input_path',
                        nargs='?')
    args = parser.parse_args()

    # read filter config
    all_filter = read_config(Path(args.config, 'all.filter.config'))

    file_paths = [Path(path) for path in glob.glob(args.input_path)]

    for in_path in tqdm(file_paths):
        # generate output path for each file
        if args.output_path is None:
            out_path = in_path
        else:
            out_path = Path(args.output_path, in_path.name)

        try:
            df = pd.read_csv(in_path)
        except EmptyDataError as e: 
            print(f'Encountered empty CSV ({in_path}), skipping...')
            continue

        orig_len = len(df)

        try:
            df = apply_filter(df, all_filter)
        except Exception as e:
            print(f'Encountered error while filtering CSV ({in_path}), skipping...')
            print(f'Error detail: {e}')
            continue

        # additional filter per-site
        site_name = in_path.stem
        site_filter_path = next(
            Path(args.config).glob(f'{site_name}.filter.config'), None)

        if site_filter_path:
            site_filter = read_config(site_filter_path)

            try:
                df = apply_filter(df, site_filter)
            except Exception as e: 
                print(f'Encountered error while filtering CSV ({in_path}) (per-site filter), skipping...')
                print(f'Error detail: {e}')
                continue

        final_len = len(df)

        print(f'Filtered CSV ({in_path}): down to {final_len} rows from {orig_len}.')
        df.to_csv(out_path, index=False)
