"""Extract files from zip folder"""
import sys
import os
import zipfile
import re


def main():
    """Main function for ExtractFiles script"""
    assert len(sys.argv) == 3, "Incorrect number of arguments"
    zip_file_name = sys.argv[1]
    zip_file_path = os.path.abspath(zip_file_name)
    if os.path.exists(zip_file_path):
        z_file = zipfile.ZipFile(zip_file_path)
        pattern = re.compile(sys.argv[2])
        for z_info in z_file.infolist():
            file_path = os.path.dirname(z_info.filename)
            file_name = os.path.basename(z_info.filename)
            if file_path.startswith('_'):
                continue
            x = re.match(pattern, file_name)
            if x:
                z_file.extract(z_info.filename)


main()
