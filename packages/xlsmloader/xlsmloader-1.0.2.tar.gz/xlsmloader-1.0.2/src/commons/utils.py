import datetime
import math
import time
import re

def to_excel_date(number_of_days):
    if type(number_of_days) == str:
        return number_of_days
    else:
        return datetime.datetime(1900, 1, 1) + datetime.timedelta(days=number_of_days - 2)

def to_excel_datetime(number_of_days):
    if type(number_of_days) == str:
        return number_of_days
    elif type(number_of_days) == float and math.isnan(number_of_days):
        return None
    else:
        return datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + int(number_of_days - 2)) + datetime.timedelta(days=number_of_days % 1)

def sqlescape(str):
    return str.translate(
        str.maketrans({
            "\0": "' || CHR(0) || '",
            "\r": "' || CHR(10) || '",
            "\x08": "' || CHR(8) || '",
            "\x09": "' || CHR(9) || '",
            "\n": "' || CHR(13) || '",
            "\r": "' || CHR(10) || '",
            "\"": "' || CHR(34) || '",
             "'": "' || CHR(39) || '",
            "\\": "' || CHR(92) || '",
            "%": "' || CHR(37) || '"
        }))

def split_oracle_string(str, max_size):
    chunks = []
    for i in range(0, len(str), max_size):
        chunks.append(f"'{sqlescape(str[i:i + max_size])}'")
    return chunks

def sanitize(value):
    if type(value) == str:
        return " ||\n".join(split_oracle_string(value, 1000))
    elif isinstance(value, datetime.datetime):
        return f"'{value.strftime('%m/%d/%Y')}'"
    else:
        return value if value != None and not math.isnan(value) else 'null'

def generate_log_filename(workbook_index: int):
    now = datetime.datetime.now()
    return f"assets-data-{now.strftime('%Y-%m-%d %H:%M:%S.%f')}-{'{:0>4}'.format(workbook_index)}.sql"

def current_milli_time():
    return int(round(time.time() * 1000))

def remove_chars(data):
    if type(data) == str:
        return ''.join(filter(str.isdigit, data))
    else:
        return data

def to_canonical_date_format(str_date):
    if type(str_date) == str:
        pattern = r'^([0-2]*\d|3[01])[-/]([0-2]*\d|3[01])[-/](\d{2}|\d{4})$'
        match = re.match(pattern, str_date)
        if not match:
            raise ValueError(f"{str_date} is not a valid date")
        date_parts = [int(str_part) for str_part in match.groups()]
        if date_parts[2] < 100:
            date_parts[2] = date_parts[2] + 2000
        if date_parts[0] > 12:
            return datetime.datetime(date_parts[2], date_parts[1], date_parts[0]).strftime('%m-%d-%Y')
        else:
            return datetime.datetime(date_parts[2], date_parts[0], date_parts[1]).strftime('%m-%d-%Y')
    elif isinstance(str_date, datetime.datetime):
        return str_date.strftime('%m/%d/%Y')
    else:
        return str_date if str_date != None and not math.isnan(str_date) else 'null'

def validate_integer(field_label, str_value):
    if type(str_value) == str:
        pattern = r'^\d+$'
        if not re.match(pattern, str_value.strip()):
            raise ValueError(f"The value '{str_value}' for the field '{field_label}' isn't a valid integer.")

def is_valid_asset_id(asset_id):
    pattern = r'AST-\d+'
    return type(asset_id) == str and re.match(pattern, asset_id)

def is_site(workbook_filename:str):
    file_name = workbook_filename.upper()
    return file_name.endswith("-SITE.XLSM") or file_name.endswith("-SITE1.XLSM")

def extract_asset_name(asset_code_and_name: str):
    pattern = r'^(\d+\s*-*\s*)*([\w\W]*)$'
    matches = re.search(pattern, asset_code_and_name)
    return matches.group(len(matches.groups()))

def parse_asset_floors(value: any):
    if type(value) == str:
        pattern = r'(\d+)'
        matches = re.search(pattern, value)
        if matches == None:
            return 0
        else:
            return int(matches.group(1))
    else:
        return value
