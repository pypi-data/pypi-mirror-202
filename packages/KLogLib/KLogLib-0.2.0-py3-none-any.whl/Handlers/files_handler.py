import os 
import Handlers.byte
from zipfile import ZipFile
from datetime import datetime
import tempfile
import glob

"""
    Check if file exists

    Arguments:
    file:   string  |   Log file path
"""
def file_exists(file):
    try:
        if os.path.exists(file) == False:
            create_file(file)
        return True
    except:
        raise Exception(f"There as an error.")

"""
    Creates the log file and directories

    Arguments:
    file:   string  |   Log file path
"""
def create_file(file):
    try:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as f:
            f.close
    except:
        raise Exception("There was an error creating Log file and directories...")

"""
    Write a log line in the file.

    Arguments:
    log_model:  LogModel()  |   Object with message, debug level...
"""
def write(log_model):
    try:
        log_file = os.path.join(log_model.folder, log_model.log_name)
        
        if(log_model.is_zip == True):
            zip_log(log_file=log_file, max_size=log_model.max_size, log_folder=log_model.folder)
            delete_oldest_zip(log_folder=log_model.folder, max_zips=log_model.max_zip)

        file_exists(log_file)

        with open(log_file, "a+") as f:
            f.write(f"{log_model.time}\t\t{log_model.where}\t\t{log_model.severity}\t\t{log_model.msg}")
            f.write("\n")
            f.close()
    except:
        raise Exception("There was an error writing in log file...")
    
"""
    This method get the current log stats and check if can be zipped

    Arguments:
    log_file:   string  |   Path to the current log file
    max_size:   double  |   Max size the log file can reach
    log_folder: string  |   Foler where the log file is located
"""
def zip_log(log_file, max_size, log_folder):
    try:
        file_stats = os.stat(log_file)

        mb = Handlers.byte.b_2_mb(size=file_stats.st_size)

        if mb > max_size:
            create_temp_log(log_file, log_folder)

    except:
        raise Exception("There was an error zipping log file")
    
"""
    This method create the temp log file and zip it

    Arguments:
    log_file:   string  |   Log name
    log_folder: string  |   Folder to log file
"""
def create_temp_log(log_file, log_folder):
    try:
        temp_log_file = tempfile.NamedTemporaryFile(delete=True)

        with open(log_file, "r") as f:
            log_file_content = f.read()
            temp_log_file.write(bytes(log_file_content, 'utf-8'))
            f.close()
        
        zip_name = datetime.now().isoformat(sep=" ", timespec="seconds").replace('/', ':')

        with ZipFile(f"{log_folder}/{zip_name}.zip", "w") as log_zip:
            log_zip.write(temp_log_file.name, os.path.basename(temp_log_file.name))
            temp_log_file.close()

        delete_file(log_file=log_file)

    except:
        raise Exception("Error creating temp file")
    
"""
    This method delete the log file

    Arguments:
    temp_log_file:  string  |   Path to the temp log
"""
def delete_file(log_file):
    try:
        if log_file != None:
            if os.path.exists(log_file):
                os.remove(log_file)
    except:
        raise Exception("Error deleting temp log")
    
"""
    This method delete the oldest zip file

    Arguments:

"""
def delete_oldest_zip(log_folder, max_zips):
    try:
        if os.path.exists(log_folder):
            os.chdir(log_folder)
            zip_files = glob.glob("*.zip")
            if len(zip_files) > max_zips:
                delete_file(sorted( zip_files, key = lambda file: os.path.getctime(file))[0])
    except:
        raise Exception("Error deleting the oldest zip file")