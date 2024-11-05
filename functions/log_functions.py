import glob
import logging
import os
#####################
def get_latest_log_file():
    log_path = "./logs/"
    log_files = glob.glob(f"{log_path}*.log")
    
    if not log_files:
        return None
    
    #sort file with date and time 
    log_files.sort(key=os.path.getmtime)
    
    #last file
    return log_files[-2]

#####################
def remove_old_logs():
    log_path = "./logs/"
    log_files = glob.glob(f"{log_path}*.log")
    log_files.sort(key=os.path.getmtime)

    if len(log_files) > 7:
        for file in log_files[:-7]:
            os.remove(file)
            logging.info(f"old log removed: {file}")
#####################
def get_last_errors(log_file,errorLines=3):
    """return error line , default 3 line"""
    with open(log_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    #filter line for finding errors
    error_lines = [line for line in lines if 'ERROR' in line]
    
    #get last errors
    return error_lines[-errorLines:] if len(error_lines) >= 3 else error_lines
#####################