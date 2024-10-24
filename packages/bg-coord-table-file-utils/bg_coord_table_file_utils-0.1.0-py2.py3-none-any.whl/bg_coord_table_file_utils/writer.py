import csv
import logging
import os
from datetime import datetime

from singleton_decorator import singleton
from typing import List, Optional

from . import constants
from .record import Record

DEFAULT_FILE_TYPE_NAME = "gene-exons coordinates table"


@singleton
class Writer:
    """Class for writing comma-separated gene-exons coordinates table file."""

    def __init__(self, **kwargs):
        """Constructor for class Writer."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.outfile = kwargs.get("outfile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", constants.DEFAULT_OUTDIR)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        logging.info(f"Instantiated Writer in {os.path.abspath(__file__)}")

    def write_file(self, records: List[Record], outfile: Optional[str]) -> None:
        """Write the records to the output the comma-separated gene-exons coordinates table file.

        Args:
            records: List of records.
            outfile (Optional[str]): The path to the output file.
        """
        with open(outfile, 'w') as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## logfile: {self.logfile}\n")

            header_line = ",".join(self.config.get("column_headers"))

            of.write(f"{header_line}\n")

            for record in records:
                if record.is_positive_strand:
                    strand = "+"
                else:
                    strand = "-"

                line = record.lab_number + "," + \
                    record.gene + "," + \
                    record.exon + "," + \
                    strand + "," + \
                    record.chr + "," + \
                    record.exon_start_coord + "," + \
                    record.exon_end_coord + "," + \
                    record.refseq + "," + \
                    record.exon_nucleotides + "," + \
                    record.exon_residues_excluding_stop + "," + \
                    record.gene_nucleotides + "," + \
                    record.gene_residues_excluding_stop + "," + \
                    record.gene_exons + "," + \
                    record.met_1_exon + "," + \
                    record.end_codon_coord + "," + \
                    record.start_codon_exon + "," + \
                    record.start_codon_coord + "," + \
                    record.stop_codon_coord

                of.write(f"{line}\n")

        logging.info(f"Wrote comma-separated {DEFAULT_FILE_TYPE_NAME} file '{outfile}'")

        if self.verbose:
            print(f"Wrote comma-separated {DEFAULT_FILE_TYPE_NAME} file '{outfile}'")

