import os
import argparse

from datetime import datetime
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile
from zipfile import ZipInfo

ZIP_EPOCH = 315532800


def _get_argument_parser():
    parser = argparse.ArgumentParser(
        description='create a zip file', fromfile_prefix_chars='@'
    )

    parser.add_argument(
        '-o', '--output', type=str, help='The output zip file path.'
    )

    parser.add_argument(
        '-e', '--entrypoint', type=str, help='The entrypoint for the function',
    )

    parser.add_argument(
        '-t',
        '--timestamp',
        type=int,
        default=ZIP_EPOCH,
        help='The unix time to use for files added into the zip. values prior to'
        ' Jan 1, 1980 are ignored.',
    )

    parser.add_argument(
        '-s',
        '--stripprefix',
        type=str,
        help='The root of the executable',
    )

    parser.add_argument(
        'files',
        type=str,
        nargs='*',
        help='Files to be added to the zip',
    )

    return parser



def parse_date(ts):
    ts = datetime.utcfromtimestamp(ts)
    return (ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)


def main(args):
    unix_ts = max(ZIP_EPOCH, args.timestamp)
    ts = parse_date(unix_ts)
    with ZipFile(args.output, 'w') as _zip:
        main = args.entrypoint
        pre = args.stripprefix
        with open(main, 'rb') as entrypoint:
            path = os.path.relpath(main, pre)
            entry_info = ZipInfo(filename=path, date_time=ts)
            entry_info.external_attr = 0o777 << 16 #NB Python3 only
            entry_info.compress_type = ZIP_DEFLATED
            _zip.writestr(entry_info, entrypoint.read())
        for _file in [f for f in args.files if not f == main]:
            entry_info = ZipInfo(filename=_file, date_time=ts)
            entry_info.external_attr = 0o777 << 16 #NB Python3 only
            entry_info.compress_type = ZIP_DEFLATED
            with open(_file, 'rb') as src:
                data = src.read()
                _zip.writestr(entry_info, data)

if __name__ == '__main__':
    parser = _get_argument_parser()
    args = parser.parse_args()
    main(args)
