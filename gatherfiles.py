"""Gather files into zip folders"""
import sys
import os
import sqlite3
import zipfile


def load_db(db_file_name):
    """Function to load the db from db_file"""
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    return con, cur


def write_to_zip(ext, file_names):
    """Function to write files to zip"""
    zip_file_name = ext + '.zip'
    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as z_file:
        for f_name in file_names:
            z_file.write(f_name)
    print(str(len(file_names)) + " " + ext + " files gathered")


def get_filenames_from_db(cur, arg):
    rows = cur.execute('select fPath, fName, fExt '
                       'from files where fExt=?', (arg,))
    file_names = []
    for row in rows:
        file_name = row[0] + "\\" + row[1]
        file_names.append(file_name)
    return file_names


def main():
    """Main function for GatherFiles script"""
    assert len(sys.argv) >= 2, "Incorrect number of arguments"
    db_name = sys.argv[1]
    if len(db_name.split('.')) == 1:
        db_name += '.db'
    if os.path.exists(db_name):
        con, cur = load_db(db_name)
        num_args = len(sys.argv)
        for arg in sys.argv[2:num_args]:
            file_names = get_filenames_from_db(cur, arg)
            write_to_zip(arg, file_names)
        con.close()


main()
