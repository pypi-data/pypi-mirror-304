import os
import sys
import sqlite3
import argparse

from .args.Args import Args
from .output.Output import Output

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    Args.addArguments(parser)
    args = parser.parse_args()

    # Creates Output instance for printing header and footer of console output
    out = Output()
    out.printHeader()

    # Check if path exists, otherwise create folders
    if(not os.path.isdir(args.result)):
         os.makedirs(args.result)

    dbPath = os.path.join(args.result, args.name)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    print("            Separator: " + args.separator)
    print("Location of zeek logs: " + args.path)
    print("Location of sqlite db: " + dbPath)
    print("\n---\n")

    # First we need to loop over all files in the zeek dir:
    for dirPath, dirNames, fileNames in os.walk(args.path, topdown=True):
        for fileName in fileNames:
            if(fileName.endswith(".log")):
                filePath = os.path.join(dirPath, fileName)
                print("File to convert: " + filePath)
                
                with open(filePath, 'r') as file:
                    for line in file:
                        line = line.replace("\n", "")
                        if("#path" in line):
                            path = line.split(args.separator)[1]
                            print("Table Name: " + path)
                        if("#fields" in line):
                            fields = line.split(args.separator)
                            fields = fields[1:len(fields)]
                            print("Columns: " + str(fields))
                            break
                
                # Create the table statement, and drop data
                cols = ', '.join([f'"{col}" TEXT' for col in fields])
                createTable = f'CREATE TABLE IF NOT EXISTS "{path}" ({cols});'
                cursor.execute(createTable)
                cursor.execute(f"DELETE FROM {path}")
                # Create the placeholders for the insert statement 
                placeholder = ", ".join([f'?' for col in fields])
                
                # Insert data
                with open(filePath, 'r') as file:
                    count = 0
                    for line in file:
                        if(not line.startswith("#")):
                            line = line.replace("\n", "")
                            values = line.split(args.separator)
                            cursor.execute(f"INSERT INTO {path} VALUES ({placeholder})", values)
                            count = count + 1
                print("Inserted rows: " + str(count))
                conn.commit()
                print("\n---\n")

    conn.close()

    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
