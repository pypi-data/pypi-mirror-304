import argparse
import roi

parser = argparse.ArgumentParser(
    prog='textutils',
    description='Very useful text utilities'
)

parser.add_argument('--revenue')
parser.add_argument('--costs')

args = parser.parse_args()


roi.roi(int(args.revenue), int(args.costs))
