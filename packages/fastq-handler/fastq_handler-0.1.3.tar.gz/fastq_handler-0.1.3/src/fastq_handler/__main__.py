import argparse

from fastq_handler.fastq_handler import PreMain

from fastq_handler.actions import ProcessActionMergeWithLast
from fastq_handler.configs import RunConfig


def get_arguments():
    parser = argparse.ArgumentParser(description="Process fastq files.")
    parser.add_argument(
        "-i", "--in_dir", help="Input directory", required=True)
    parser.add_argument("-o", "--out_dir",
                        help="Output directory", required=True)

    parser.add_argument("-s", "--sleep", help="Sleep time",
                        type=int, default=60)

    parser.add_argument("-n", "--tag", help="name tag, if given, will be added to the output file names",
                        required=False, type=str, default="")

    parser.add_argument(
        "--keep_names", help="keep original file names", action="store_true")

    parser.add_argument(
        "--monitor", help="run indefinitely", action="store_true")

    parser.add_argument(
        "--max-size", help="max size of the output file, in kilobytes", type=int, default=400000)

    return parser.parse_args()


def main():

    args = get_arguments()

    run_metadata = RunConfig(
        fastq_dir=args.in_dir,
        output_dir=args.out_dir,
        name_tag=args.tag,
        actions=[ProcessActionMergeWithLast],
        keep_name=args.keep_names,
        sleep_time=args.sleep,
        max_size=(args.max_size * 1000),
    )

    compressor = PreMain(
        run_metadata,
    )

    if args.monitor:

        compressor.run_until_killed()

    else:

        compressor.run()


if __name__ == "__main__":
    main()
