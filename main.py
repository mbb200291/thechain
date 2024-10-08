import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ing")
args = parser.parse_args()
print(args.echo)
