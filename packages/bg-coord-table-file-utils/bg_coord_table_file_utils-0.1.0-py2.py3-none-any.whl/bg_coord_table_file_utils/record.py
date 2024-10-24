import pydantic


class Record(pydantic.BaseModel):
    """This class represents a record in the gene-exons coordinates table file."""

    # Chromosome of the exon boundary.
    chr: str

    # The exon number containing the stop codon.
    end_codon_exon: int

    # End position of the exon boundary.
    exon_end_coord: int

    # The exon number.
    exon_number: int

    # The number of nucleotides in the exon.
    exon_nucleotides: int

    # Start position of the exon boundary.
    exon_start_coord: int

    # The gene name corresponding with the current exon.
    gene_name: str

    # The number of nucleotides in the gene.
    gene_nucleotides: int

    # True if on positive strand, False if on negative strand.
    is_positive_strand: bool

    # Refseq accession number.
    refseq: str

    # Start codon genomic coordinate.
    start_codon_coord: int

    # The exon number containing the start codon.
    start_codon_exon: int

    # Stop codon genomic coordinate.
    stop_codon_coord: int
