class Args():
    # parser: argparse instance
    def addArguments(parser):
        parser.add_argument("--name", "-n", type=str, default="zeek.db", help="Name of the sqlite database written to result")
        parser.add_argument("--path", "-p", type=str, required=True, help="Path to folder where the zeek logs are located")
        parser.add_argument("--result", "-r", type=str, default=".\zeek-sqlite", help="Directory to write the resulting sqlite db")
        parser.add_argument("--separator", "-s", type=str, default="\t", help="The separator used in the zeek files")