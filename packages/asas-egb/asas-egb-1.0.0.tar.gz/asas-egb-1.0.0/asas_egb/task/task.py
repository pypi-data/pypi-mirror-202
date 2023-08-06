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

from ..component import SplEvent, Segment, SNP, get_all_exons_of_multiple_isoforms


class Task:
    """Task.

    Attributes:
        id: Task ID.
        event: The target event.
        snps: The SNPs located on the segment.
        ploidy: The ploidy of the SNP.
        phased: If the task is phased.
    """

    def __init__(self, task_id: str, event: SplEvent, phased: bool, ploidy: int, snps: List[SNP]):
        self.id = task_id
        self.event = event
        self.phased = phased
        self.ploidy = ploidy
        self.snps = snps

        if not self.phased:
            assert len(self.snps) == 1

        for snp in self.snps:
            assert self.phased == snp.phased
            assert self.ploidy == snp.ploidy

    @property
    def segment(self) -> Segment:
        return self.event.gene

    @property
    def isoforms_count(self):
        """Isoforms count."""
        return len(self.segment.isoforms)

    def isoform_snps(self, isoform_num: int) -> List[SNP]:
        """SNPs located on isoform."""
        isoform = self.segment.isoforms[isoform_num]
        snps = []
        for snp in self.snps:
            for exon in isoform.exons:
                if exon.start <= snp.pos <= exon.end:
                    snps.append(snp)
                    break
        return snps

    def _support_gene_isoform_snps_and_exons_nums(self, exons):
        snps = []
        exon_nums = set()
        for snp in self.snps:
            for i, exon in enumerate(exons):
                if exon.start <= snp.pos <= exon.end:
                    snps.append(snp)
                    exon_nums.add(i)
                    break
        return snps, exon_nums

    def support_gene_isoform_snps_and_exons(self, isoform_nums: List[int]):
        exons = get_all_exons_of_multiple_isoforms(self.segment.isoforms, isoform_nums)
        snps, exon_nums = self._support_gene_isoform_snps_and_exons_nums(exons)
        exons = [exons[num] for num in exon_nums]
        exons = sorted(exons, key=lambda _iv: _iv.start)
        return snps, exons

    def get_all_support_gene_exons_containing_snps_and_overlap_with_event_isoforms(self):
        isoform_nums = self.event.gene_isoform_idxes_support_isoform1 + self.event.gene_isoform_idxes_support_isoform2
        return self.get_support_gene_exons_containing_snps_and_overlap_with_event_isoforms(isoform_nums)

    def get_support_gene_exons_containing_snps_and_overlap_with_event_isoforms(self, isoform_nums):
        exons = get_all_exons_of_multiple_isoforms(self.segment.isoforms, isoform_nums)

        snps, exon_nums_containing_snps = self._support_gene_isoform_snps_and_exons_nums(exons)
        exon_nums_overlap_with_event_isoforms = self.support_exon_nums_overlap_with_event_isoforms(exons)
        exon_nums = exon_nums_containing_snps.union(exon_nums_overlap_with_event_isoforms)

        exons = [exons[num] for num in exon_nums]
        exons = sorted(exons, key=lambda _iv: _iv.start)

        return exons

    def _exon_nums_overlap_with_event_isoforms(self, exons, event_exons):
        nums = []

        for i, exon in enumerate(exons):
            for e in event_exons:
                if len(set(range(exon.start, exon.end)).intersection(set(range(e.start, e.end)))) > 0:
                    nums.append(i)
                    continue

        return nums

    def support_exon_nums_overlap_with_event_isoforms(self, exons) -> List[int]:
        event_exons = self.event.get_all_exons()

        return self._exon_nums_overlap_with_event_isoforms(exons, event_exons)

