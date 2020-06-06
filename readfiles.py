"""Read the file info and load into db table"""
import sys
import os
import sqlite3


def prepare_db(db_file_name):
    """Function to create the db"""
    if os.path.exists(db_file_name):
        os.remove(db_file_name)

    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    cur.execute('''CREATE TABLE files( 
                fExt TEXT,
                fPath TEXT,
                fName TEXT)''')
    con.commit()
    return con, cur


def load_db(input_directory_name, cur, con):
    """Function to read file info and insert to db"""
    input_directory_path = os.path.abspath(input_directory_name)
    for dir_path, dir_names, file_names in os.walk(input_directory_path):
        for file_name in file_names:
            ext = file_name.split('.')
            if len(ext) == 2:
                ext = ext[1]
            elif len(ext) == 1:
                ext = None
            else:
                continue
            cur.execute('''INSERT INTO files(
                        fExt, fPath, fName) 
                        VALUES ( ?, ?, ?)''',
                        (ext, dir_path, file_name))
            con.commit()


def write_to_file(cur):
    """Function to read from db and write to txt"""
    rows = cur.execute('select * from files')
    if os.path.exists('files-part1.txt'):
        os.remove('files-part1.txt')

    with open('files-part1.txt', 'w+') as file:
        file.write('\n'.join("'%s', '%s', '%s'" % x for x in rows))


def main():
    """Main function for ReadFiles script"""
    assert (len(sys.argv) == 2), "Incorrect number of arguments"

    con, cur = prepare_db('filesdb.db')
    input_directory_name = sys.argv[1]
    load_db(input_directory_name, cur, con)
    write_to_file(cur)
    con.commit()
    con.close()


main()
