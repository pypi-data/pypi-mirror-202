import glob
import sys
import warnings
import os
import traceback
from datetime import datetime, timedelta
from commons.utils import generate_log_filename, current_milli_time
import commons.openpyxl_wo_formatting as openpyxl_wo_formatting
from models.assets import Asset
from models.systems import System
from models.photos import Photo

RED = "\033[1;31m"
RESET = "\033[0;0m"
MAX_SPREADSHEETS_PER_SQL_FILE = 20;

warnings.simplefilter("ignore", category=UserWarning)

def load():
    if len(sys.argv) <= 1:
        directory_path = input("Inform the XLSM file directory: ")
    else:
        directory_path = sys.argv[1]

    start_time_ms = current_milli_time()
    print(f"Processing start time {datetime.now()}")
    print(f"processing XLSM files from {directory_path}")
    xlsm_files = glob.glob(directory_path + '/*.xlsm')
    print(f"{len(xlsm_files)} files found.")

    for subset_index in range(0, len(xlsm_files), MAX_SPREADSHEETS_PER_SQL_FILE):
        with open(generate_log_filename(subset_index // MAX_SPREADSHEETS_PER_SQL_FILE), "w") as sql_file:
            sql_file.write("DECLARE\n")
            sql_file.write("  description_clob CLOB;\n")
            sql_file.write("  asset_id number;\n")
            sql_file.write("  system_id number;\n")
            sql_file.write("  count_systems number;\n")
            sql_file.write("BEGIN\n")
            for workbook_filename in xlsm_files[subset_index:subset_index+MAX_SPREADSHEETS_PER_SQL_FILE]:
                try:
                    print(f"reading file {os.path.basename(workbook_filename)}...")
                    asset = Asset(workbook_filename)
                    system = System(workbook_filename, asset)
                    photo = Photo(workbook_filename, asset)
                    asset.setSystem(system)

                    asset_sql = asset.create_update_sql()
                    system_sql = system.create_update_sql()
                    photo_sql = photo.create_insert_sql()

                    sql_file.write(f"  -- {os.path.basename(workbook_filename)} data\r\n\n")
                    sql_file.write(asset_sql)
                    sql_file.write("\r\n\n")
                    sql_file.write(system_sql)
                    sql_file.write("\r\n\n")
                    sql_file.write(photo_sql)
                    sql_file.write("\r\n")
                    print(f"file {os.path.basename(workbook_filename)} processed successfully.")
                except (BaseException) as e:
                    error_message = f"File {os.path.basename(workbook_filename)} processed with error: {e}."
                    tb_info = traceback.format_exc()
                    print(f"{RED}{error_message}{RESET}", file=sys.stderr)
                    print(tb_info, file=sys.stderr)

            sql_file.write("  COMMIT;\n")
            sql_file.write("END;\n")
            sql_file.close()

    print(f"Processing finished time {datetime.now()}")
    end_time_ms = current_milli_time()
    elapsed_time_ms = end_time_ms - start_time_ms
    elapsed_time = timedelta(milliseconds=elapsed_time_ms)
    print(f"Elapsed time: {elapsed_time}")