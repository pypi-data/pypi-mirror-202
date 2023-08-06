

import os
from dataclasses import dataclass
from typing import List, Optional, Type

import pandas as pd


class Processed:
    """
    class to keep track of processed files
    """
    output_file = "processed.tsv"

    processed_template = pd.DataFrame(
        columns=[
            "sample_id",
            "fastq",
            "dir",
            "barcode",
            "time",
            "merged",
        ]
    )

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.processed = self.read_processed()

        self._ignore = []

    @property
    def processed_entries(self) -> pd.DataFrame:
        """
        get processed entries
        """

        processed_entries = self.processed[self.processed["merged"]
                                           != self.processed["fastq"]].copy()

        return processed_entries

    def ignore_this(self, fastq_file: str):
        """
        ignore this file
        """

        self._ignore.append(fastq_file)

    def check_ignored(self, fastq_file: str):
        """
        check if ignored
        """

        if fastq_file in self._ignore:
            return True
        else:
            return False

    def processed_fastq_list(self) -> List[str]:
        """
        get list of fastq files
        """

        return self.processed_entries.fastq.tolist()

    def read_processed(self):
        """
        read processed tsv
        """

        processed_file = os.path.join(
            self.output_dir,
            self.output_file
        )

        try:
            processed = pd.read_csv(
                processed_file, sep='\t')
        except FileNotFoundError:
            processed = self.processed_template.copy()

        processed["barcode"] = processed.barcode.apply(
            lambda x: str(x).zfill(2) if not pd.isna(x) else x
        )

        return processed

    def file_exists(self, fastq_file, fastq_dir):
        """
        match to process dict
        """

        processed = self.processed.loc[
            (self.processed["dir"] == fastq_dir) & (
                self.processed["fastq"] == fastq_file)
        ]

        if len(processed) > 0:
            return True
        else:
            return False

    @staticmethod
    def get_run_num_from_filename(filename: str):
        """
        get underscore sep suffix, return empty string otherwise.
        """
        run_num = os.path.basename(filename).split("_")[-1]

        if run_num == os.path.basename(filename):
            run_num = ""

        if not run_num.isnumeric():
            run_num = ""

        return run_num

    def get_run_info(self, filename: str):
        """
        Gets the run_name and run_num by knowing the filename and file_format.

        Takes:              Returns:
            str*str             str*str
        """
        filename = os.path.basename(filename)
        run_name, ext = os.path.splitext(filename)
        if ext == ".gz":
            run_name = os.path.splitext(run_name)[0]

        run_num = self.get_run_num_from_filename(run_name)

        return run_name, run_num

    def generate_barcode(self, fastq_dir: str) -> str:
        """
        generate barcode
        """

        dir_processed = self.processed.loc[self.processed["dir"] == fastq_dir].sort_values(
            by="time", ascending=True)

        barcode = str(len(dir_processed))
        barcode = barcode.zfill(2)

        return barcode

    def get_dir_barcode_first(self, fastq_dir: str) -> str:
        """
        get first run
        """

        dir_processed = self.processed.loc[self.processed["dir"] == fastq_dir].sort_values(
            by="time", ascending=True)
        if len(dir_processed) > 0:
            return dir_processed["barcode"].iloc[0]
        else:
            return ""

    def get_dir_merged_last(self, fastq_dir: str) -> str:
        """
        get last run
        """

        dir_processed = self.processed.loc[self.processed["dir"] == fastq_dir].sort_values(
            by="time", ascending=False)
        if len(dir_processed) > 0:
            return dir_processed["merged"].iloc[0]
        else:
            return ""

    def get_id_merged_last(self, sample_id: str) -> str:
        """
        get last run
        """

        dir_processed = self.processed.loc[self.processed["sample_id"] == sample_id].sort_values(
            by="time", ascending=False)

        if len(dir_processed) > 0:
            return dir_processed["merged"].iloc[0]
        else:
            return ""

    def get_file_time(self, fastq_file, fastq_dir):
        """
        get time
        """

        time_elapsed = self.processed.loc[
            (self.processed["dir"] == fastq_dir) & (
                self.processed["fastq"] == os.path.basename(fastq_file))
        ]["time"]

        if len(time_elapsed) > 0:
            return time_elapsed.iloc[0]

        return 0

    def get_run_barcode(self, fastq_file, fastq_dir):
        """
        get run info
        """

        run_name, barcode = self.get_run_info(fastq_file)
        if barcode == "":
            barcode = self.generate_barcode(fastq_dir)

        return run_name, barcode

    @staticmethod
    def get_sample_id_from_merged(merged_file):
        """
        get project name
        """
        merged_filename = os.path.basename(merged_file)
        if merged_filename.endswith(".gz"):
            merged_filename = os.path.splitext(merged_filename)[0]

        sample_id = merged_filename.split("_")

        if len(sample_id) == 1:
            return sample_id[0]

        run_tag = sample_id[-1].split("-")
        if len(run_tag) == 1:
            return sample_id[0]

        return "_".join(sample_id[:-1])

    def update(self, fastq_file, fastq_dir, time_elapsed, merged_file):
        """
        update processed
        """

        _, barcode = self.get_run_barcode(fastq_file, fastq_dir)
        sample_id = self.get_sample_id_from_merged(merged_file)

        self.processed.loc[len(self.processed)] = [
            sample_id, os.path.basename(fastq_file), fastq_dir, barcode, time_elapsed, merged_file]

    def export(self, output_dir: str, output_file: str = "processed.tsv"):
        """
        export processed
        """
        self.processed.to_csv(os.path.join(
            output_dir, output_file), sep="\t", index=False)

        return self

    def delete_records(self):
        """
        delete records
        """
        print("Deleting records...")
        self.processed = pd.DataFrame(
            columns=[
                "sample_id",
                "fastq",
                "dir",
                "barcode",
                "time",
                "merged",
            ]
        )
