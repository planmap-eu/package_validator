import gpt
import check

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("\nUsage: {} <path/to/geopackage>".format(sys.argv[0]))
        sys.exit(1)

    filename = sys.argv[1]
    check.geopackage(filename)
