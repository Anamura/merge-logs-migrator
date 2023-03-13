import argparse
import asyncio
import json
import time
import aiofiles

from utils import parse_args
from pathlib import Path
import heapq


def extract_timestamp(x):
    """Extract timestamp and use it for comparison.
    """
    return json.loads(x).get('timestamp')


def merge_logfiles(log_filepath1: Path, log_filepath2: Path, output_file: Path) -> None:
    print(f"Merging to {output_file.name}...")

    files = map(open, [log_filepath1, log_filepath2])
    file_contents = files
    with open(output_file, mode='w') as outfile:
        for content in heapq.merge(*file_contents, key=lambda x: extract_timestamp(x)):
            outfile.write(content)

    for file in files:
        file.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to Merge log files.')

    parser.add_argument('log1', metavar='<log1>', help='path to log1')
    parser.add_argument('log2', metavar='<log2>', help='path to log2')
    parser.add_argument('mergedLog', metavar='<merged log>', help='path to mergedLog')
    return parser.parse_args()


def main():
    args = parse_args()

    t = time.time()
    log_path1 = Path(args.log1)
    log_path2 = Path(args.log2)

    output_dir = Path(args.mergedLog)
    merge_logfiles(log_path1, log_path2, output_dir)
    print(f"Completed in {time.time() - t:0f} sec")


if __name__ == '__main__':
    main()
