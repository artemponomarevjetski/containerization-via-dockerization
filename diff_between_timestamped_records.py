# -*- coding: utf-8 -*-
"""
Spyder Editor

This is the master table script file
"""
#
import csv
import os
import tempfile
import time
from datetime import datetime
import argparse
#
#
def create_titles(s_s):
    """
    title string
    """
    title_str = []
    for t_t in s_s:
        title_str.append(t_t)
    return title_str


def main(working_dir_):
    """
    The parametrized main function for CLI in the cloud
    """
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
#
    print('\n\ncomparing corporate events data between timestamped historical data... ',
          datetime.now())
#
    working_dir = working_dir_
#
    print('\n\nprocessing ...', datetime.now())
#
    now = datetime.now()
    list_ = [[] for n in range(20750101)]
    dates = []
    idx = 0
    files_ = []
    for _, _, files in os.walk(working_dir):
        for f_2 in files:
            if '.csv' in f_2:
                files_.append(f_2)

    files_ = sorted(files_)

    for f_1 in files_:
        s_s = f_1[:-4]
        s_s = s_s.split('_')
        day = s_s[-1]
        s_s = s_s[:-1]
        month = s_s[-1]
        s_s = s_s[:-1]
        year = s_s[-1]
        date = year+month+day
        dates.append(date)
        ifp1 = os.path.join(working_dir, f_1)
        with open(ifp1, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            nrow = 0
            for row in csv_reader:
                if nrow != 0: # skip titles
                    idx1 = int(date)
                    list_[idx1].append(row)

                nrow += 1

        idx += 1

    list1_ = [[] for n in range(idx)]
    idx2 = 0
    for i in range(20750101):
        if list_[i]:
            for j in range(len(list_[i])):
                list1_[idx-idx2-1].append(list_[i][j][:-1])
            idx2 += 1

    table_diff = []
    for i in range(idx-1):
        s_s = dates[idx-i-1]
        date = ''
        idx3 = 0
        for c_c in s_s:
            if idx3 == 4:
                date += '/'
            else:
                if idx3 == 6:
                    date += '/'
            date += c_c
            idx3 += 1
        table_diff.append(['diff\'ng for timestamp of '+date, '', '', '', '', ''])
        for j in range(len(list1_[i])):
            item = list1_[i][j]
            s_s = item[0]
            s_s = s_s.split('/')
            day = s_s[1]
            month = s_s[0]
            year = s_s[2]
            date1 = year+month+day
            if date1 != dates[idx-i-1]:
                item_unique = False
                for i_1 in range(idx):
                    if i_1 > i:
                        if item not in list1_[i_1]:
                            item_unique = True
                            break
                if item_unique:
                    table_diff.append(item)
#
    print('\n\noutputting result ... ', datetime.now())
    table1 = []
    table1.append(create_titles([
        'EffectiveDate'
        , 'Ticker'
        , 'ComName'
        , 'ActionTypeCode'
        , 'NumNewShares'
        , 'NumOldShares'
        , 'AnnouncedDate'
        , 'RecordDate'
        , 'ExpiryDate'
        , 'OfferCmpyName'
        , 'CashAmt'
        , 'NumHypothShares'
        , 'NumSharesFinal'
        , 'LeftOverShares'
        , 'CashInLieu'
        , 'CashFinal'
        ]))
    table1 += table_diff
    now = datetime.now()
    ofp = os.path.join(working_dir, '../corporate_events_timestamped_diff_'
                       + now.strftime("%Y_%m_%d")+'.csv')
    with open(ofp, 'w') as result_file:
        w_r = csv.writer(result_file, dialect='excel')
        w_r.writerows(table1)
#
    print('\n\nexiting ... ', datetime.now())


def is_valid_date_string(maybe_date_string: str) -> str:
    """
    Errors out if maybe_date_string is not a valid date string (as expected by this
    script). Otherwise, simply returns the string.
    """
    time.strptime(maybe_date_string, '%Y-%m-%d')
    return maybe_date_string

if __name__ == '__main__':
#
    PARSER = argparse.ArgumentParser(description='Input parameters: ')
    PARSER.add_argument(
        '-d',
        '--working-directory',
        type=str, # make it start with ./ and end with /
        default=None,
        help='call Art at 409-443-4701, he\'ll refer you to Neeraj'
    )

    ARGS = PARSER.parse_args()

    WORKING_DIRECTORY = (
        ARGS.working_directory if ARGS.working_directory is not None else tempfile.mkdtemp()
    )

    print(f'Working directory: {WORKING_DIRECTORY}')

    main(
        WORKING_DIRECTORY
    )
