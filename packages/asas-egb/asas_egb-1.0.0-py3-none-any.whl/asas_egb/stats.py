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
from typing import List

import pandas as pd

from .message import MessageCenter
from .inference import InferenceTool
from .annotation import AnnotationDB
from .result import ResultDB, ResultRecord
from .task.result import TaskResult, TaskResultMeta


_STATS_DIR_NAME = 'stats'
_TRACE_DIR_NAME = 'trace'
_HEAD_MEAN = 'Mean'
_HEAD_HPD_WIDTH = '95% HPD Width'


class StatsError(Exception):
    """Stats error."""
    def __init__(self, msg):
        super().__init__(msg)


class StatsTool(TaskResultMeta):
    """Stats tool.

    Attributes:
        anno_path: The path of annotation.
        result_path: The path of result.
        out_dir: The path of output directory.

        mc: Message center.
    """

    def __init__(self, anno_path: str, result_path: str, out_dir: str,  mc: MessageCenter):
        self.anno_path = anno_path
        self.result_path = result_path
        self.out_dir = out_dir
        self.mc = mc

    @property
    def _asas_stats_path(self):
        return os.path.join(self.out_dir, 'ASAS.csv')

    @staticmethod
    def _store(df: pd.DataFrame, file_path: str):
        """Store data frame."""
        df.to_csv(file_path, index=False)

    def _stats(self):
        """Generate stats."""
        asas_cols = ['Task ID', 'Gene ID', 'Gene Name', 'Location',
                     'Isoform numbers A', 'Isoform numbers B', 'SNP Count',
                     _HEAD_MEAN, _HEAD_HPD_WIDTH]

        asas_d = [[] for _ in asas_cols]

        def _add_mean(_data: list, _record: ResultRecord, _var_name: str):
            _var_stats = _record.trace_stats.loc[_var_name]
            _data.append(_var_stats['mean'])

        def _add_mean_and_hpd_width(_data: list, _record: ResultRecord, _var_name: str):
            _var_stats = _record.trace_stats.loc[_var_name]
            _data.append(_var_stats['mean'])
            _data.append(_var_stats['hpd_97.5'] - _var_stats['hpd_2.5'])

        def _add_row(_d: List[list], _cols: list, _row: list):
            assert len(_d) == len(_cols) == len(_row)
            for _i, _item in enumerate(_row):
                _d[_i].append(_item)

        n = -1
        with AnnotationDB(self.anno_path) as anno_db, ResultDB(self.result_path) as result_db:
            for task in anno_db.tasks_iterator():
                record = result_db.get_record(task.id)
                if not record.success:
                    continue

                n += 1
                if n != 0 and n % 100 == 0:
                    self.mc.handle_progress('Stats: {} tasks processed...'.format(n))

                event = task.event
                location = '{}:{}-{}'.format(event.iv.chrom, event.iv.start, event.iv.end)
                gene_row = [task.id, event.gene.id, event.gene.gene_name, location,
                            '['+','.join([str(i) for i in event.gene_isoform_idxes_support_isoform1])+']',
                            '['+','.join([str(i) for i in event.gene_isoform_idxes_support_isoform2])+']',
                            len(task.snps)]
                var = self.get_var_expr_diff()
                _add_mean_and_hpd_width(gene_row, record, var)
                _add_row(asas_d, asas_cols, gene_row)

        def _get_df(_d: List[list], _cols: list):
            assert len(_d) == len(_cols)
            return pd.DataFrame({_col: _d[_i] for _i, _col in enumerate(_cols)})[_cols]

        asas_df = _get_df(asas_d, asas_cols)

        self._store(asas_df, self._asas_stats_path)

    def stats(self):
        """Generate stats."""
        already_exists = True
        for file_path in [self._asas_stats_path]:
            if not os.path.exists(file_path):
                already_exists = False

        if not already_exists:
            self._stats()


def stats(args):
    """Generate stats."""
    result_dir = args['result_dir']

    mc = args['mc']  # type: MessageCenter

    mc.log_debug('result_dir: {}'.format(result_dir))

    inference_tool = InferenceTool(result_dir, n_process=1, param=None, mc=mc)

    stats_dir = os.path.join(result_dir, _STATS_DIR_NAME)
    if not os.path.exists(stats_dir):
        os.mkdir(stats_dir)

    stats_tool = StatsTool(anno_path=inference_tool.anno_path, result_path=inference_tool.result_path,
                           out_dir=stats_dir, mc=mc)
    stats_tool.stats()


def trace(args):
    """Get MCMC traces."""
    result_dir = args['result_dir']
    task_id = args['task_id']

    mc = args['mc']  # type: MessageCenter

    mc.log_debug('result_dir: {}'.format(result_dir))
    mc.log_debug('task_id: {}'.format(task_id))

    trace_dir = os.path.join(result_dir, _TRACE_DIR_NAME)
    if not os.path.exists(trace_dir):
        os.mkdir(trace_dir)

    out_path = os.path.join(trace_dir, '{}.csv'.format(task_id))

    inference_tool = InferenceTool(result_dir, n_process=1, param=None, mc=mc)
    anno_path = inference_tool.anno_path
    result_path = inference_tool.result_path

    with AnnotationDB(anno_path) as anno_db, ResultDB(result_path) as result_db:
        task = anno_db.get_task(task_id)
        record = result_db.get_record(task_id)
        result = TaskResult(task, record.trace)
        result.trace.to_csv(out_path, index=False)
