import argparse
import re


def replace(file, pattern, replacement):
    lines = []
    with open(file) as f:
        for line in f:
            newline = re.sub(pattern, replacement, line)
            lines.append(newline)
    with open(file, "w") as f:
        f.truncate()
        for line in lines:
            f.writelines(line)


def main():
    parser = argparse.ArgumentParser(description="Apply a simple pattern substitution to a file")
    parser.add_argument("file", help="The target file for the substitution")
    parser.add_argument("-p", "--pattern", type=str, required=True, help="The pattern to substitute")
    parser.add_argument("-s", "--substitution", type=str, required=True, help="The pattern to substitute")
    args = parser.parse_args()
    replace(args.file, args.pattern, args.substitution)


if __name__ == "__main__":
    main()
