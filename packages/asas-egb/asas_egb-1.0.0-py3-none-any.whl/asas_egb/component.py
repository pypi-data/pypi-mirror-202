# This file is part of ASAS-EGB.
#
# ASAS-EGB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ASAS-EGB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASAS-EGB.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: Lili Dong
#

from typing import List

import HTSeq


class Isoform:
    """Isoform annotation.

    Attributes:
        id: Isoform ID in GFF file hierarchy.
        name: Isoform name.
        iv: the genomic location of the isoform.
        exons: A list of genomic locations, each represents an exon.
    """

    def __init__(self, isoform_id: str, isoform_name: str, iv: HTSeq.GenomicInterval):
        self.id = isoform_id
        self.name = isoform_name
        self.iv = iv
        self.exons = []  # type: List[HTSeq.GenomicInterval]

    def __str__(self):
        return '{} {} {}: {}'.format(self.id, self.name, self.iv,
                                     ','.join(['[{0},{1})'.format(e.start, e.end) for e in self.exons]))

    @property
    def length(self):
        """The total length of the isoform."""
        return sum([iv.end - iv.start for iv in self.exons])


class Segment:
    """Segment annotation.

    Attributes:
        id: Segment ID in GFF file hierarchy.
        gene_name: Gene name.
        iv: The genomic location of the segment.
        isoforms: The isoforms of the segment.
    """

    def __init__(self, segment_id: str, gene_name: str, iv: HTSeq.GenomicInterval):
        self.id = segment_id
        self.gene_name = gene_name
        self.iv = iv
        self.isoforms = []  # type: List[Isoform]

    @property
    def isoforms_count(self):
        """Isoforms count."""
        return len(self.isoforms)

    def __repr__(self):
        return '{} {} {}\n{}'.format(self.id, self.gene_name, self.iv,
                                     '\n'.join([str(i) for i in self.isoforms]))

    def get_all_exons(self) -> List[HTSeq.GenomicInterval]:
        """Get all exons."""
        exons = []
        tmp = HTSeq.GenomicArray('auto', stranded=False, typecode='i')
        for isoform in self.isoforms:
            for exon in isoform.exons:
                exon.strand = '.'
                tmp[exon] = 1
        for iv, v in tmp.steps():
            if v == 1:
                exons.append(iv)
        return exons


def get_all_exons_of_multiple_isoforms(isoforms: List[Isoform], idxes: List[int]) -> List[HTSeq.GenomicInterval]:
    """Get all exons."""
    tmp_isoforms = []
    for i in idxes:
        tmp_isoforms.append(isoforms[i])
    isoforms = tmp_isoforms

    exons = []
    tmp = HTSeq.GenomicArray('auto', stranded=False, typecode='i')
    for isoform in isoforms:
        for exon in isoform.exons:
            exon.strand = '.'
            tmp[exon] = 1
    for iv, v in tmp.steps():
        if v == 1:
            exons.append(iv)
    return exons


class SplEvent:

    def __init__(self, event_id: str, iv, isoform1: Isoform, isoform2: Isoform,
                 gene: Segment, idxes1: List[int], idxes2: List[int]):
        self.id = event_id
        self.iv = iv
        self.isoform1 = isoform1
        self.isoform2 = isoform2
        self.gene = gene
        self.gene_isoform_idxes_support_isoform1 = idxes1
        self.gene_isoform_idxes_support_isoform2 = idxes2

    def __repr__(self):
        return '{} {} {}\n{}, {}\n{}'.format(self.id, self.gene.id, self.iv,
                                        self.gene_isoform_idxes_support_isoform1,
                                        self.gene_isoform_idxes_support_isoform2,
                                        '\n'.join([str(i) for i in [self.isoform1, self. isoform2]]))

    def get_all_exons(self) -> List[HTSeq.GenomicInterval]:
        exons = []
        tmp = HTSeq.GenomicArray('auto', stranded=False, typecode='i')
        for isoform in [self.isoform1, self.isoform2]:
            for exon in isoform.exons:
                exon.strand = '.'
                tmp[exon] = 1
        for iv, v in tmp.steps():
            if v == 1:
                exons.append(iv)
        return exons

    def get_all_support_gene_exons(self) -> List[HTSeq.GenomicInterval]:
        return get_all_exons_of_multiple_isoforms(
            self.gene.isoforms,
            self.gene_isoform_idxes_support_isoform1 + self.gene_isoform_idxes_support_isoform2)


class SNP:
    """SNP.

    Attributes:
        id: The ID of the SNP.
        iv: The genomic location of the SNP.
        alleles: Alleles of the SNP.
        phased: If the SNP is phased.
    """

    def __init__(self, chrom: str, pos: int, alleles: List[str], phased: bool):
        self.iv = HTSeq.GenomicInterval(chrom, pos, pos+1, '.')
        self.alleles = alleles
        self.phased = phased
        self.id = '{}-{}-{}-{}'.format(self.iv.chrom, self.iv.start,
                                       '1' if self.phased else '0', ''.join(self.alleles))

    @property
    def ploidy(self):
        """The ploidy of the SNP."""
        return len(self.alleles)

    @property
    def chrom(self):
        """The chromosome of the SNP."""
        return self.iv.chrom

    @property
    def pos(self):
        """The position of the SNP."""
        return self.iv.start

    def __repr__(self):
        return '{}:{} {}'.format(self.chrom, self.pos, ('|' if self.phased else '/').join(self.alleles))
