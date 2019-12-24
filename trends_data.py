import argparse
import logging
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from pytrends.request import TrendReq

def get_year_data(trends, term):
    df = trends.interest_over_time()
    df = df.reset_index()
    df.date = pd.to_datetime(df.date)
    df.set_index(['date'], inplace=True)
    year_data = []
    for year in [2009, 2014, 2019]:
        year_data.append(
            df.loc[datetime(year, 12, 1):datetime(year, 12, 31)][term].sum()
        )
    return [str(d) for d in year_data]

def get_most_active_region(trends, term, resolution='COUNTRY'):
    df = trends.interest_by_region(resolution=resolution)
    df = df.reset_index()
    df.sort_values(by=term, ascending=False, inplace=True)
    return df.iloc[0].geoName

def main(input_file, output_file, debug=False):
    logger = logging.Logger(__name__)
    if debug:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    cols = 'Search term,Global search interest (12/09),Global search interest (12/14),Global search interest (12/19),Most active country,US search interest (12/09),US search interest (12/14),US search interest (12/19),Most active state,\n'
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write(cols)
        search_terms = infile.readline() if debug else tqdm(infile.readlines())
        for term in search_terms:
            term = term.strip()
            logger.debug(f'Processing {term}...')
            try:
                kw_list = [term]
                trends = TrendReq(hl='en-US', tz=360)
                trends.build_payload(kw_list, timeframe='all', geo='')

                year_data = ','.join(get_year_data(trends, term))
                active_region = get_most_active_region(trends, term, resolution='COUNTRY')
                row = f'{term},{year_data},{active_region}'

                trends = TrendReq(hl='en-US', tz=360)
                trends.build_payload(kw_list, timeframe='all', geo='US')
                year_data = ','.join(get_year_data(trends, term))
                active_region = get_most_active_region(trends, term, resolution='REGION')
                row += f',{year_data},{active_region},\n'
            except Exception as e:
                logger.warning(f'WARNING - could not find data for \"{term}\".\nError: {str(e)}')
                row = f'{term},0,0,0,NA,0,0,0,NA,\n'
            logger.debug(row)
            outfile.write(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input-file',
        action='store',
        dest='input_file',
        type=str,
        help='The path to the input file'
    )
    parser.add_argument(
        '-o',
        '--output-file',
        action='store',
        dest='output_file',
        type=str,
        help='The path to the output file'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        dest='verbose',
        help='Run in verbose mode',
    )
    args = parser.parse_args()
    if not args.input_file:
        parser.error('input file argument is required')
    if not args.output_file:
        parser.error('output file argument is required')
    main(args.input_file, args.output_file, debug=args.verbose)
