"""Class for parsing the gene-exons coordinates table file."""
import csv
import logging
import os
import pathlib
import yaml


from singleton_decorator import singleton
from typing import Dict, List, Optional

from .record import Record as CoordTableRecord

# We only want to accumulate a maximum of 5 neighbor genes for each gene.

MAX_NUM_NEIGHBOR_GENES = 5

DEFAULT_FILE_TYPE_NAME = "gene-exons coordinates table"


@singleton
class Parser:
    """Class for parsing the gene-exons coordinates table file."""
    MAX_NUM_NEIGHBOR_GENES = 5

    def __init__(self, **kwargs):
        """Class constructor"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.infile = kwargs.get("infile", None)

        if self.config is None:
            logging.info(f"Will load contents of config file '{self.config_file}'")
            self.config = yaml.safe_load(pathlib.Path(self.config_file).read_text())

        if self.infile is None or self.infile == "":
            self.infile = self.config.get("coordinates_table_file", None)
            if self.infile is None or self.infile == "":
                raise Exception(f"Could not derive the {DEFAULT_FILE_TYPE_NAME} file from the config file '{self.config_file}'")

        self._gene_lookup = {}
        self._gene_to_exon_count_lookup = {}
        self._gene_to_neighbors_gene_lookup = {}
        self._gene_to_gene_lookup = {}
        self.chromosome_to_records_lookup = {}
        self.chromsome_to_gene_to_records_lookup = {}

        self.is_parsed = False
        self._parse_file()

        logging.info(f"Instantiated Parser in '{os.path.abspath(__file__)}'")

    def _parse_file(self) -> None:
        infile = self.infile

        if not os.path.exists(infile):
            raise Exception(f"{DEFAULT_FILE_TYPE_NAME} file '{infile}' does not exist")

        header_to_position_lookup = {}

        record_ctr = 0

        with open(infile) as f:
            reader = csv.reader(f, delimiter=',')
            row_ctr = 0
            previous_gene = None
            previous_neighbor_gene = None

            for row in reader:
                row_ctr += 1
                if row_ctr == 1:
                    field_ctr = 0
                    for field in row:
                        header_to_position_lookup[field] = field_ctr
                        field_ctr += 1
                    logging.info(f"Processed the header of {DEFAULT_FILE_TYPE_NAME} file '{infile}'")
                else:
                    current_gene = row[header_to_position_lookup['Gene']]
                    self._gene_lookup[current_gene] = True
                    if current_gene not in self._gene_to_exon_count_lookup:
                        self._gene_to_exon_count_lookup[current_gene] = 1
                    else:
                        if previous_gene is not None and previous_gene == current_gene:
                            self._gene_to_exon_count_lookup[current_gene] += 1
                    previous_gene = current_gene
                    try:
                        # Instantiate a Record object
                        record = CoordTableRecord(
                            chr=row[header_to_position_lookup['Chr']],
                            end_codon_exon=int(row[header_to_position_lookup["Terminal Exon"]]),
                            exon_end_coord=int(row[header_to_position_lookup['End']]),
                            exon_nucleotides=int(row[header_to_position_lookup["Exon Nucleotides"]]),
                            exon_number=int(row[header_to_position_lookup['Exon']]),
                            exon_residues_excluding_stop=int(row[header_to_position_lookup["Exon Residues Excluding STOP"]]),
                            exon_start_coord=int(row[header_to_position_lookup['Start']]),
                            gene_name=row[header_to_position_lookup['Gene']],
                            gene_exons=row[header_to_position_lookup['Gene Exons']],
                            gene_nucleotides=int(row[header_to_position_lookup["Gene Nucleotides"]]),
                            gene_residues_excluding_stop=int(row[header_to_position_lookup["Gene Residues Excluding STOP"]]),
                            is_positive_strand=row[header_to_position_lookup['Strand']] == '+',
                            refseq=row[header_to_position_lookup['Refseq']],
                            start_codon_coord=int(row[header_to_position_lookup["5' Coord"]]),
                            start_codon_exon=int(row[header_to_position_lookup["Met-1 Exon"]]),
                            stop_codon_coord=int(row[header_to_position_lookup["3' Coord"]]),
                        )
                    except Exception as e:
                        if row[header_to_position_lookup['Exon']] == "-":
                            if row[header_to_position_lookup['Gene']] == "TERC" or row[header_to_position_lookup['Gene']] == "RMRP":
                                logging.info(f"Will ignore non-coding RNA gene '{row[header_to_position_lookup['Gene']]}' with exon number '-' in file '{infile}' at row number '{row_ctr}' while processing row: '{row}'")
                                continue
                        logging.error(f"Error in {DEFAULT_FILE_TYPE_NAME} file '{infile}' at row number '{row_ctr}' while processing row: '{row}': {e}")
                        raise Exception(f"Error in {DEFAULT_FILE_TYPE_NAME} file '{infile}' at row number '{row_ctr}' while processing row: '{row}': {e}")

                    chromosome = row[header_to_position_lookup['Chr']]

                    if chromosome not in self.chromosome_to_records_lookup:
                        self.chromosome_to_records_lookup[chromosome] = []
                    self.chromosome_to_records_lookup[chromosome].append(record)

                    if chromosome not in self.chromsome_to_gene_to_records_lookup:
                        self.chromsome_to_gene_to_records_lookup[chromosome] = {}

                    if record.gene_name not in self.chromsome_to_gene_to_records_lookup[chromosome]:
                        self.chromsome_to_gene_to_records_lookup[chromosome][record.gene_name] = []
                    self.chromsome_to_gene_to_records_lookup[chromosome][record.gene_name].append(record)
                    record_ctr += 1

        logging.info(f"Processed '{record_ctr}' records in the {DEFAULT_FILE_TYPE_NAME} file '{infile}'")

        self.is_parsed = True

    def get_gene_lookup(self) -> Dict[str, bool]:
        if not self.is_parsed:
            self._parse_file()
        return self._gene_lookup

    def get_exon_count_by_gene(self, gene_name: str) -> Optional[int]:
        if gene_name in self._gene_to_exon_count_lookup:
            return self._gene_to_exon_count_lookup[gene_name]
        logging.warning(f"Did not find gene '{gene_name}' in the {DEFAULT_FILE_TYPE_NAME} file '{self.infile}'")
        return None

    def get_chromosome_to_records_lookup(self) -> Dict[str, List[CoordTableRecord]]:
        if not self.is_parsed:
            self._parse_file()
        return self.chromosome_to_records_lookup

    def get_records_by_chromosome(self, chromosome: str) -> List[CoordTableRecord]:
        if not self.is_parsed:
            self._parse_file()
        if chromosome in self.chromosome_to_records_lookup:
            return self.chromosome_to_records_lookup[chromosome]
        logging.warning(f"Did not find chromosome '{chromosome}' in the {DEFAULT_FILE_TYPE_NAME} file '{self.infile}'")
        return []

    def get_records_by_chromosome_gene(self, chromosome: str, gene: str) -> List[CoordTableRecord]:
        if chromosome is None:
            raise Exception("chromosome cannot be None")
        if gene is None:
            raise Exception("gene cannot be None")
        if chromosome not in self.chromsome_to_gene_to_records_lookup:
            raise Exception(f"Did not find chromosome '{chromosome}' in the {DEFAULT_FILE_TYPE_NAME} file '{self.infile}'")
        if gene not in self.chromsome_to_gene_to_records_lookup[chromosome]:
            raise Exception(f"Did not find gene '{gene}' for chromosome '{chromosome}' in the {DEFAULT_FILE_TYPE_NAME} file '{self.infile}'")
        return self.chromsome_to_gene_to_records_lookup[chromosome][gene]

    def get_neighbor_genes(self, gene: str) -> Optional[List[str]]:
        if gene in self._gene_to_neighbors_gene_lookup:
            return self._gene_to_neighbors_gene_lookup[gene]
        logging.info(f"Did not find gene '{gene}' in the {DEFAULT_FILE_TYPE_NAME} file '{self.infile}'")
        return None

    def _store_neighbor_gene(self, previous_neighbor_gene: str, current_gene: str) -> str:
        if previous_neighbor_gene != current_gene:
            if previous_neighbor_gene not in self._gene_to_gene_lookup:
                self._gene_to_gene_lookup[previous_neighbor_gene] = {}
            if current_gene not in self._gene_to_gene_lookup[previous_neighbor_gene]:
                self._gene_to_gene_lookup[previous_neighbor_gene][current_gene] = True
                if previous_neighbor_gene not in self._gene_to_neighbors_gene_lookup:
                    self._gene_to_neighbors_gene_lookup[previous_neighbor_gene] = []
                if len(self._gene_to_neighbors_gene_lookup[previous_neighbor_gene]) < MAX_NUM_NEIGHBOR_GENES:
                    logging.info(f"Adding previous neighbor gene '{previous_neighbor_gene}' to current gene '{previous_neighbor_gene}'")
                    self._gene_to_neighbors_gene_lookup[previous_neighbor_gene].append(current_gene)
                else:
                    logging.info(f"Reached maximum number of neighbor genes '{MAX_NUM_NEIGHBOR_GENES}' for gene '{previous_neighbor_gene}'")
            previous_neighbor_gene = current_gene
        return previous_neighbor_gene
