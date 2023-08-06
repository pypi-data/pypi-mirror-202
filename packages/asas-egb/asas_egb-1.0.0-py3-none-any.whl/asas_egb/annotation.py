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

import os
from typing import List, Optional

import HTSeq

from .message import MessageCenter
from .component import SplEvent, Segment, Isoform, SNP
from .task import Task
from .db import DB, Field


class AnnotationError(Exception):
    """Annotation error."""
    def __init__(self, msg):
        super().__init__(msg)


class AnnotationPathError(AnnotationError):
    """Path error."""
    def __init__(self, path, msg):
        super().__init__('[PATH: {}] {}'.format(path, msg))


class AnnotationParseError(AnnotationError):
    """Parsing error."""
    def __init__(self, path, msg):
        super().__init__('[PARSE: {}] {}'.format(path, msg))


class AnnotationDBError(AnnotationError):
    """Database error."""
    def __init__(self, path, msg):
        super().__init__('[DATABASE: {}] {}'.format(path, msg))


def _read_gff(gff_path: str, segment_feature_name: str, isoform_feature_name: str,
              gene_name_attr: str, isoform_name_attr: str, mc: MessageCenter) -> List[Segment]:
    """Read all segments from GFF file.

    Args:
        gff_path: The path of GFF file.
        segment_feature_name: Segment feature name in GFF hierarchy.
        isoform_feature_name: Isoform feature name in GFF hierarchy.
        gene_name_attr: Name of attribute which describes gene name.
        isoform_name_attr: Name of attribute which describes isoform name.
        mc: Message center.
    """

    mc.log_debug('gff_path: {}'.format(gff_path))
    mc.log_debug('segment_feature_name: {}'.format(segment_feature_name))
    mc.log_debug('isoform_feature_name: {}'.format(isoform_feature_name))
    mc.log_debug('gene_name_attr: {}'.format(gene_name_attr))
    mc.log_debug('isoform_name_attr: {}'.format(isoform_name_attr))

    mc.handle_progress('Reading GFF file...')

    if not os.path.exists(gff_path):
        raise AnnotationPathError(gff_path, 'File not exists.')

    segments = []
    segments_dict = {}
    isoforms_dict = {}

    gff = HTSeq.GFF_Reader(gff_path)
    n = -1
    for ft in gff:
        n += 1
        if n != 0 and n % 100000 == 0:
            mc.handle_progress('{} lines read from GFF file...'.format(n))

        if ft.type == segment_feature_name:
            if gene_name_attr not in ft.attr:
                raise AnnotationParseError(gff_path, '"{}" not in attributes.'.format(gene_name_attr))
            segment = Segment(ft.attr['ID'], ft.attr[gene_name_attr], ft.iv)
            if segment.id in segments_dict:
                raise AnnotationParseError(gff_path, 'Segment ID is not unique: {}'.format(segment.id))
            segments_dict[segment.id] = segment
            segments.append(segment)
        elif ft.type == isoform_feature_name:
            if isoform_name_attr not in ft.attr:
                raise AnnotationParseError(gff_path, '"{}" not in attributes.'.format(isoform_name_attr))
            isoform = Isoform(ft.attr['ID'], ft.attr[isoform_name_attr], ft.iv)
            if isoform.id in isoforms_dict:
                raise AnnotationParseError(gff_path, 'Isoform ID is not unique: {}'.format(isoform.id))
            isoforms_dict[isoform.id] = isoform
            parent_id = ft.attr['Parent']
            if parent_id not in segments_dict:
                raise AnnotationParseError(gff_path, 'Cannot find the parent of isoform "{}", the segment feature '
                                                     'type name may be incorrect.'.format(isoform.id))
            parent = segments_dict[parent_id]
            assert parent.iv.chrom == isoform.iv.chrom
            assert parent.iv.strand == isoform.iv.strand
            parent.isoforms.append(isoform)
        elif ft.type == 'exon':
            parent_id = ft.attr['Parent']
            if parent_id not in isoforms_dict:
                raise AnnotationParseError(gff_path, 'Cannot find the parent of exon "{}", the isoform feature '
                                                     'type name may be incorrect.'.format(ft.attr['ID']))
            parent = isoforms_dict[parent_id]
            assert parent.iv.chrom == ft.iv.chrom
            assert parent.iv.strand == ft.iv.strand
            parent.exons.append(ft.iv)

    return segments


class HeteroSNPReader:
    """Heterozygous SNP reader.

    Attributes:
        vcf_path: The path of VCF file.
        sample: The name of sample to be extracted.
        ploidy: The ploidy of the sample
        add_chrom_prefix: If add "chr" prefix to chromosome.
        mc: Message center.
    """

    def __init__(self, vcf_path: str, sample: str, ploidy: int, add_chrom_prefix: bool, mc: MessageCenter):
        self.vcf_path = vcf_path
        self.sample = sample
        self.ploidy = ploidy
        self.add_chrom_prefix = add_chrom_prefix
        self.mc = mc

        if not os.path.exists(self.vcf_path):
            raise AnnotationPathError(self.vcf_path, 'File not exists.')

    def __iter__(self):
        self.mc.log_debug('vcf_path: {}'.format(self.vcf_path))
        self.mc.log_debug('sample: {}'.format(self.sample))
        self.mc.log_debug('ploidy: {}'.format(self.ploidy))
        self.mc.log_debug('add_chrom_prefix: {}'.format(self.add_chrom_prefix))

        vcf = HTSeq.VCF_Reader(self.vcf_path)
        vcf.parse_meta()

        self.mc.handle_progress('Reading VCF file...')

        n = -1
        for vc in vcf:
            n += 1
            if n != 0 and n % 500000 == 0:
                self.mc.handle_progress('{} lines read from VCF file...'.format(n))

            if self.sample not in vc.samples:
                raise AnnotationParseError(self.vcf_path, 'Sample "{}" not in VCF file.'.format(self.sample))

            gt = vc.samples[self.sample]['GT']
            if '.' in gt:
                continue
            if '/' in gt:
                phased = False
                if '|' in gt:
                    gt = gt.replace('|', '/')
                sep = '/'
            else:
                assert '|' in gt
                phased = True
                sep = '|'

            gt = gt.split(sep)
            if len(gt) != self.ploidy:
                raise AnnotationParseError(self.vcf_path,
                                           'The ploidy({}) may be inconsistent with the '
                                           'sample "{}"({}).'.format(self.ploidy, self.sample, len(gt)))

            ref_alt = [vc.ref] + vc.alt
            alleles = [ref_alt[int(g)] for g in gt]

            for allele in alleles:
                if len(allele) != 1:
                    continue
            if len(set(alleles)) < 2:
                continue

            chrom = vc.pos.chrom
            if self.add_chrom_prefix:
                chrom = 'chr{}'.format(chrom)
            pos = vc.pos.pos - 1

            snp = SNP(chrom, pos, alleles, phased)
            assert self.ploidy == snp.ploidy
            yield snp


_EVENT_DB_FILENAME = 'event.db'
_SEGMENT_DB_FILENAME = 'gene.db'
_ISOFORM_DB_FILENAME = 'isoform.db'
_SNP_DB_FILENAME = 'snp.db'
_TASK_DB_FILENAME = 'task.db'


class AnnotationDB:
    """Annotation Database."""

    _event_scheme = [Field('id', 'S'), Field('location', 'S'), Field('isoform0', 'S'), Field('isoform1', 'S'),
                     Field('gene_id', 'S'), Field('gene_isoform_idxes1', 'S'), Field('gene_isoform_idxes2', 'S')]
    _segment_scheme = [Field('id', 'S'), Field('gene_name', 'S'), Field('chrom', 'S'),
                       Field('start', 'I'), Field('end', 'I'), Field('strand', 'S'),
                       Field('isoforms_count', 'I'), Field('isoforms', 'S'), Field('isoforms_db_offsets', 'S')]
    _isoform_schema = [Field('id', 'S'), Field('name', 'S'), Field('start', 'I'), Field('end', 'I'),
                       Field('exons_count', 'I'), Field('exons_starts', 'S'), Field('exons_ends', 'S')]
    _snp_schema = [Field('id', 'S'), Field('chrom', 'S'), Field('pos', 'I'), Field('phased', 'I'),
                   Field('ploidy', 'I'), Field('alleles', 'S')]
    _task_schema = [Field('id', 'S'), Field('event', 'S'), Field('phased', 'I'), Field('ploidy', 'I'),
                    Field('snps_count', 'I'), Field('snps', 'S')]

    def __init__(self, dir_path: str, initialize: bool = False, mc: Optional[MessageCenter] = None):
        self._mc = mc

        if not os.path.isdir(dir_path):
            raise AnnotationPathError(dir_path, 'Invalid directory.')

        read_only = not initialize

        self._event_db = DB(os.path.join(dir_path, _EVENT_DB_FILENAME),
                            AnnotationDB._event_scheme if initialize else None, read_only=read_only)
        self._segment_db = DB(os.path.join(dir_path, _SEGMENT_DB_FILENAME),
                              AnnotationDB._segment_scheme if initialize else None, read_only=read_only)
        self._isoform_db = DB(os.path.join(dir_path, _ISOFORM_DB_FILENAME),
                              AnnotationDB._isoform_schema if initialize else None, read_only=read_only)
        self._snp_db = DB(os.path.join(dir_path, _SNP_DB_FILENAME),
                          AnnotationDB._snp_schema if initialize else None, read_only=read_only)
        self._task_db = DB(os.path.join(dir_path, _TASK_DB_FILENAME),
                           AnnotationDB._task_schema if initialize else None, read_only=read_only)

        if not initialize:
            assert self._event_db.read_only
            assert self._segment_db.read_only
            assert self._isoform_db.read_only
            assert self._snp_db.read_only
            assert self._task_db.read_only

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._event_db.close()
        self._segment_db.close()
        self._isoform_db.close()
        self._snp_db.close()
        self._task_db.close()

    def get_all_event_ids(self):
        return self._event_db.get_all_item_ids()

    def get_event(self, event_id: str) -> SplEvent:
        item = self._event_db.get_item(event_id)
        event_id, location, isoform1_str, isoform2_str, gene_id, idxes1, idxes2 = item

        def _create_interval_from_str(s: str):
            chrom, start, end, strand = s.split(':')
            return HTSeq.GenomicInterval(chrom, int(start), int(end), strand)

        def _create_isoform_from_str(s: str, event_id: str, isoform_name: str):
            exons = []
            location_and_exon_strs = s.split(';')
            location_str = location_and_exon_strs[0]
            exon_strs = location_and_exon_strs[1:]
            for exon_str in exon_strs:
                exon = _create_interval_from_str(exon_str)
                exons.append(exon)
            isoform = Isoform(isoform_id='{}.{}'.format(event_id, isoform_name), isoform_name=isoform_name,
                              iv=_create_interval_from_str(location_str))
            isoform.exons = exons
            return isoform

        def _create_idx_list_from_str(s: str):
            return [int(i) for i in s.split(';')]

        iv = _create_interval_from_str(location)

        isoform1 = _create_isoform_from_str(isoform1_str, event_id, 'A')
        isoform2 = _create_isoform_from_str(isoform2_str, event_id, 'B')

        gene = self.get_segment(gene_id)
        idxes1 = _create_idx_list_from_str(idxes1)
        idxes2 = _create_idx_list_from_str(idxes2)

        event = SplEvent(event_id=event_id, iv=iv, isoform1=isoform1, isoform2=isoform2,
                         gene=gene, idxes1=idxes1, idxes2=idxes2)
        return event

    def get_all_segment_ids(self):
        """Get all segment IDs."""
        return self._segment_db.get_all_item_ids()

    def get_segment_basic_info(self, segment_id):
        """Get segment basic information."""
        item = self._segment_db.get_item(segment_id)
        _, gene_name, chrom, start, end, _, isoforms_count, _, _ = item
        return {'gene_name': gene_name, 'location': '{}:{}-{}'.format(chrom, start, end),
                'isoforms_count': isoforms_count}

    def get_segment(self, segment_id):
        """Get segment by ID."""
        item = self._segment_db.get_item(segment_id)
        segment_id, gene_name, chrom, start, end, strand, isoforms_count, isoform_ids, isoform_offsets = item
        iv = HTSeq.GenomicInterval(chrom, start, end, strand)
        segment = Segment(segment_id, gene_name, iv)

        isoform_ids = isoform_ids.split(';')
        isoform_offsets = [int(offset) for offset in isoform_offsets.split(';')]
        assert isoforms_count == len(isoform_ids)
        assert isoforms_count == len(isoform_offsets)
        for n, isoform_offset in enumerate(isoform_offsets):
            item = self._isoform_db.get_item_by_offset(isoform_offset)
            isoform_id, isoform_name, start, end, exons_count, exons_starts, exons_ends = item
            assert isoform_id == isoform_ids[n]
            iv = HTSeq.GenomicInterval(chrom, start, end, strand)
            isoform = Isoform(isoform_id, isoform_name, iv)
            segment.isoforms.append(isoform)

            exons_starts = [int(s) for s in exons_starts.split(';')]
            exons_ends = [int(e) for e in exons_ends.split(';')]
            assert exons_count == len(exons_starts) == len(exons_ends)
            for i in range(exons_count):
                exon_iv = HTSeq.GenomicInterval(chrom, exons_starts[i], exons_ends[i], strand)
                isoform.exons.append(exon_iv)
            assert len(isoform.exons) == exons_count
        assert len(segment.isoforms) == isoforms_count
        return segment

    def get_snp(self, snp_id):
        """Get SNP by ID."""
        snp_id, chrom, pos, phased_code, ploidy, alleles = self._snp_db.get_item(snp_id)
        alleles = alleles.split(';')
        assert len(alleles) == ploidy
        if phased_code == 1:
            phased = True
        else:
            assert phased_code == 0
            phased = False
        snp = SNP(chrom, pos, alleles, phased)
        return snp

    def get_all_task_ids(self):
        """Get all task IDs."""
        return self._task_db.get_all_item_ids()

    def _construct_task(self, item):
        """Construct task from database item."""
        task_id, event_id, phased_code, ploidy, snps_count, snp_ids = item
        if phased_code == 1:
            phased = True
        else:
            assert phased_code == 0
            phased = False
        snp_ids = snp_ids.split(';')
        assert len(snp_ids) == snps_count
        event = self.get_event(event_id)
        snps = [self.get_snp(snp_id) for snp_id in snp_ids]
        task = Task(task_id, event, phased, ploidy, snps)
        return task

    def tasks_iterator(self):
        """Tasks iterator."""
        for item in self._task_db.item_iterator():
            yield self._construct_task(item)

    def tasks_db_fields_iterator(self):
        """Tasks database fields iterator."""
        for item in self._task_db.item_iterator():
            yield {self._task_schema[n].name: item[n] for n in range(len(self._task_schema))}

    def get_task(self, task_id):
        """Get task by ID."""
        item = self._task_db.get_item(task_id)
        return self._construct_task(item)

    def store_segments(self, segments: List[Segment]):
        """Store segments into the database."""
        for segment in segments:
            for isoform in segment.isoforms:
                self._isoform_db.store_item(
                    (isoform.id, isoform.name, isoform.iv.start, isoform.iv.end, len(isoform.exons),
                     ';'.join([str(e.start) for e in isoform.exons]),
                     ';'.join([str(e.end) for e in isoform.exons])))
        for segment in segments:
            isoform_offsets = []
            for isoform in segment.isoforms:
                offset = self._isoform_db.find_item_offset(isoform.id)
                assert offset is not None
                isoform_offsets.append(str(offset))
            self._segment_db.store_item(
                (segment.id, segment.gene_name, segment.iv.chrom, segment.iv.start, segment.iv.end, segment.iv.strand,
                 len(segment.isoforms), ';'.join([i.id for i in segment.isoforms]), ';'.join(isoform_offsets)))

    def link_and_store_events(self, seg_events: List[Segment]):
        """Link events with gene information and store events to database."""

        not_compatible_count = 0
        not_linked_count = 0

        # n = -1
        for seg_event in seg_events:
            # n += 1
            # if n != 0 and n % 10000 == 0:
            #     self._mc.handle_progress('{} events stored...'.format(n))

            if seg_event.isoforms_count != 2:
                print('Isoforms count not equal to 2: {}'.format(seg_event.isoforms_count))
                continue

            # print(seg_event)

            gene_id = seg_event.gene_name

            gene = self.get_segment(gene_id)

            # print(gene)

            isoform1 = seg_event.isoforms[0]
            isoform2 = seg_event.isoforms[1]

            g = HTSeq.GenomicArrayOfSets('auto', stranded=False)

            for exon in isoform1.exons:
                g[exon] += -1
            for exon in isoform2.exons:
                g[exon] += -2

            for idx, isoform in enumerate(gene.isoforms):
                for exon in isoform.exons:
                    g[exon] += idx

            def _calc_gene_isoform_idxes_support_isoforms(strict=False):
                idxes1 = set([c for c in range(gene.isoforms_count)])
                idxes2 = set([c for c in range(gene.isoforms_count)])

                for iv, evs in g.steps():
                    if not strict:
                        if iv.length < 10:
                            continue
                    if -1 in evs and -2 in evs:
                        vs = evs - {-1, -2}
                        idxes1.intersection_update(vs)
                        idxes2.intersection_update(vs)
                    elif -1 in evs and -2 not in evs:
                        vs = evs - {-1}
                        idxes1.intersection_update(vs)
                        idxes2 -= vs
                    elif -1 not in evs and -2 in evs:
                        vs = evs - {-2}
                        idxes1 -= vs
                        idxes2.intersection_update(vs)
                return idxes1, idxes2

            gene_isoform_idxes_support_isoform1, gene_isoform_idxes_support_isoform2 = _calc_gene_isoform_idxes_support_isoforms()

            if len(gene_isoform_idxes_support_isoform1.intersection(gene_isoform_idxes_support_isoform2)) != 0:
                gene_isoform_idxes_support_isoform1, gene_isoform_idxes_support_isoform2 = _calc_gene_isoform_idxes_support_isoforms(strict=True)

            if len(gene_isoform_idxes_support_isoform1.intersection(gene_isoform_idxes_support_isoform2)) != 0:
                print('Unexpected error: gene isoform idxes have intersection', gene_id, gene_isoform_idxes_support_isoform1, gene_isoform_idxes_support_isoform2)

            gene_isoform_idxes_support_isoform1 = sorted(gene_isoform_idxes_support_isoform1)
            gene_isoform_idxes_support_isoform2 = sorted(gene_isoform_idxes_support_isoform2)

            if len(gene_isoform_idxes_support_isoform1) == 0 or len(gene_isoform_idxes_support_isoform2) == 0:
                not_compatible_count += 1
                # print('not compatible', gene_id, gene.isoforms_count, gene_isoform_idxes_support_isoform1, gene_isoform_idxes_support_isoform2)
                continue

            event = SplEvent(event_id=seg_event.id, iv=seg_event.iv, isoform1=isoform1, isoform2=isoform2, gene=gene,
                             idxes1=gene_isoform_idxes_support_isoform1, idxes2=gene_isoform_idxes_support_isoform2)

            # print(event)

            def _convert_genomic_interval_to_str(iv) -> str:
                return '{}:{}:{}:{}'.format(iv.chrom, iv.start, iv.end, iv.strand)

            def _convert_isoform_to_db_field_str(isoform: Isoform) -> str:
                isoform_location_str = _convert_genomic_interval_to_str(isoform.iv)
                exon_strs = [_convert_genomic_interval_to_str(exon) for exon in isoform.exons]
                return ';'.join([isoform_location_str] + exon_strs)

            self._event_db.store_item((event.id,
                                       _convert_genomic_interval_to_str(event.iv),
                                       _convert_isoform_to_db_field_str(event.isoform1),
                                       _convert_isoform_to_db_field_str(isoform2),
                                       event.gene.id,
                                       ';'.join([str(i) for i in event.gene_isoform_idxes_support_isoform1]),
                                       ';'.join([str(i) for i in event.gene_isoform_idxes_support_isoform2])))

        # print('total: {}, not compatible: {}, not linked: {}'.format(len(seg_events), not_compatible_count, not_linked_count))

    def store_snps(self, snps):
        """Store SNPs into the database."""
        for snp in snps:
            snp = snp  # type: SNP
            self._snp_db.store_item(
                (snp.id, snp.iv.chrom, snp.iv.start, 1 if snp.phased else 0, len(snp.alleles), ';'.join(snp.alleles)))

    def create_tasks(self, ploidy: int, snps):
        """Create tasks."""
        vc_sites = HTSeq.GenomicArray('auto', stranded=False, typecode='O')

        for snp in snps:
            snp = snp  # type: SNP
            vc_sites[snp.iv] = snp

        self._mc.handle_progress('Creating tasks...')
        selected_snp_ids = set()
        selected_snps = []
        n = -1
        event_ids = self.get_all_event_ids()
        for event_id in event_ids:
            event = self.get_event(event_id)
            # print(event)
            segment = event.gene
            phased_snp_ids, unphased_snp_ids = [], []
            for isoform in segment.isoforms:
                for exon in isoform.exons:
                    for vc_iv, snp in vc_sites[exon].steps():
                        if snp is not None:
                            if snp.id not in selected_snp_ids:
                                selected_snp_ids.add(snp.id)
                                selected_snps.append(snp)
                            if snp.phased and snp.id not in phased_snp_ids:
                                phased_snp_ids.append(snp.id)
                            if not snp.phased and snp.id not in unphased_snp_ids:
                                unphased_snp_ids.append(snp.id)
            if len(phased_snp_ids) > 0:
                n = self._create_task(n, event.id, True, ploidy, phased_snp_ids)
            for unphased_snp_id in unphased_snp_ids:
                n = self._create_task(n, event.id, False, ploidy, [unphased_snp_id])

        self.store_snps(selected_snps)

    def _create_task(self, n: int, event_id: str, phased: bool, ploidy: int, snp_ids: List[str]) -> int:
        """Create task."""
        assert self._mc is not None

        n += 1
        if n != 0 and n % 10000 == 0:
            self._mc.handle_progress('{} tasks created...'.format(n))
        if phased:
            task_id = '{}-PHASED'.format(event_id)
        else:
            assert len(snp_ids) == 1
            task_id = '{}-{}'.format(event_id, snp_ids[0])

        # print('Task {}, {}'.format(task_id, [snp_id for snp_id in snp_ids]))

        self._task_db.store_item((task_id, event_id, 1 if phased else 0, ploidy, len(snp_ids), ';'.join(snp_ids)))
        return n


def generate_annotation(args):
    """Generate annotation."""
    event_gff_path = args['event_gff']
    event_gene_feature_name = args['event_gene_feature']
    event_isoform_feature_name = args['event_isoform_feature']
    gene_id_attr = args['event_gene_id_attr']

    gene_gff_path = args['gene_gff']
    segment_feature_name = args['gene_feature']
    isoform_feature_name = args['isoform_feature']
    gene_name_attr = args['gene_name_attr']

    vcf_path = args['vcf']
    vcf_sample = args['sample']
    ploidy = 2
    add_chrom_prefix = args['add_chrom_prefix']

    out_dir = args['out_dir']
    mc = args['mc']  # type: MessageCenter

    if not os.path.isdir(out_dir):
        raise AnnotationPathError(out_dir, 'Invalid directory.')

    with AnnotationDB(out_dir, initialize=True, mc=mc) as anno_db:
        segments = _read_gff(gene_gff_path, segment_feature_name, isoform_feature_name,
                             gene_name_attr, 'ID', mc)
        anno_db.store_segments(segments)
        del segments

        segments_for_events = _read_gff(event_gff_path, event_gene_feature_name, event_isoform_feature_name,
                                        gene_id_attr, 'ID', mc)
        anno_db.link_and_store_events(segments_for_events)

        anno_db.create_tasks(ploidy, HeteroSNPReader(vcf_path, vcf_sample, ploidy, add_chrom_prefix, mc))
