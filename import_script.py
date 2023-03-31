import psycopg2
import pandas as pd
from math import isnan
from db_credentials import *


def clean_data(element):
    if isnan(element):
        return 0
    return element


def transform_row_to_data(row):
    result = [row[0], row[1]]

    # first two elements are strings that define which store is in the row
    # 6th, 8th and last element of the row are subtotals and are therefore ignored
    for element in row[3:]:
        result.append(clean_data(element))
    return result


def get_conn():
    return psycopg2.connect(host=host,
                            database=db_db,
                            user=db_user,
                            password=db_password)


file_name = 'SpaceNK_2.0.xlsx'

xlsx_file = pd.read_excel(file_name)
tup = []

# first 6 rows are the same in every file so we skip them
for line in xlsx_file.values[5:, 2:]:
    try:
        # if line does not have a name that means there are no more stores to be loaded
        if not isinstance(line[1], str):
            break

        tup.append(transform_row_to_data(line))

    except (ValueError, IndexError) as e:
        print(e)
        print(line)
        continue

conn = get_conn()
cur = conn.cursor()
cur.executemany("INSERT INTO weekly_report (store_no, store_name, ty_units, ly_units, tw_sales, lw_sales,"
                " lw_var_pct, ly_sales, ly_var_pct, ytd_sales, lytd_sales, lytd_var_pct)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                "ON CONFLICT (store_name) DO UPDATE SET "
                "(ty_units, ly_units, tw_sales, lw_sales,"
                " lw_var_pct, ly_sales, ly_var_pct, ytd_sales, lytd_sales, lytd_var_pct) = "
                "(EXCLUDED.ty_units, EXCLUDED.ly_units, EXCLUDED.tw_sales, EXCLUDED.lw_sales,"
                " EXCLUDED.lw_var_pct, EXCLUDED.ly_sales, EXCLUDED.ly_var_pct, EXCLUDED.ytd_sales, EXCLUDED.lytd_sales,"
                " EXCLUDED.lytd_var_pct)", tup)
conn.commit()
cur.close()
conn.close()
