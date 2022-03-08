import argparse


def load(filepath):
    """Loads data from filepath to the database"""
    try:
        with open(filepath) as file_:
            for line in file_:
                print(line)
    except FileNotFoundError as e:
        print(f"File not found {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Dunder Mifflin Rewards CLI",
        epilog="Enjoy and use with cautious.",
    )   
    parser.add_argument(
        "subcommand",
        type=str,
        help="The subcommand to run",
        choices=("load", "show", "send"),
        default="help",
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="File path to load",
        default=None,
    )
    args = parser.parse_args()

    
    globals()[args.subcommand](args.filepath)    
    

if __name__ == "__main__":
    main()
