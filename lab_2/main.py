import argparse
from ccf import *


def main():

    parser = argparse.ArgumentParser('KotlinCCF')
    parser.add_argument('-v', '--verify', action='store_true', help='Verify naming conventions')
    parser.add_argument('-fx', '--fix', action='store_true', help='Fix naming')
    parser.add_argument('-f', '--file', nargs=1, required=False, help='*.kt file')
    parser.add_argument('-p', '--project', nargs=1, required=False, help='Project with *.kt files')
    parser.add_argument('-d', '--directory', nargs=1, required=False, help='Directory with *.kt files')

    my_namespace = parser.parse_args()

    if not (my_namespace.verify or my_namespace.fix) or \
            not (my_namespace.directory is not None or
                 my_namespace.file is not None or
                 my_namespace.project is not None):
        print("error")
        parser.print_help()
        return

    ccf = CodeConventionsFixer()
    if my_namespace.fix:
        ccf.set_type(CCFType.FIX)
    else:
        ccf.set_type(CCFType.VERIFY)
    if my_namespace.directory is not None:
        ccf.set_file_walk_type(FileWalkType.DIRECTORY)
        ccf.run(my_namespace.directory[0])
    elif my_namespace.project is not None:
        ccf.set_file_walk_type(FileWalkType.PROJECT)
        ccf.run(my_namespace.project[0])
    else:
        ccf.run(my_namespace.file[0])


main()
