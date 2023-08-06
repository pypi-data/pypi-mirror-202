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

from typing import Optional

import numpy as np
import pandas as pd

from .task import Task


class TaskResultMeta:
    """Task result meta."""

    def _get_var_raw(self, iso_num: int, allele_num: int):
        """Get raw variable name."""
        # return self._get_var_name('raw', iso_num=iso_num, allele_num=allele_num)
        return 'RAW_I{}_A{}'.format(iso_num, allele_num)

    def get_var_expr(self, allele_num: int):
        return 'EXP_A{}'.format(allele_num)

    def get_var_expr_diff(self):
        return 'EXP_DIFF'


class TaskResult(Task, TaskResultMeta):
    """Task result.

    Attributes:
        trace: Inference results.
    """

    def __init__(self, task: Task, trace: pd.DataFrame):
        super().__init__(task.id, task.event, task.phased, task.ploidy, task.snps)
        self.trace = self.construct_full_trace(trace)

    def construct_full_trace(self, trace: pd.DataFrame) -> pd.DataFrame:
        """Construct full trace."""
        cols = trace.columns.tolist()
        trace = pd.DataFrame({col: trace[col].tolist() for col in cols}, index=trace.index)[cols]
        assert len(trace.columns) == self.isoforms_count * self.ploidy

        idx1 = self.event.gene_isoform_idxes_support_isoform1
        idx2 = self.event.gene_isoform_idxes_support_isoform2

        idxes = [idx1, idx2]

        for n in range(2):
            total_expr_support_event_isoforms = []
            for idx in idxes:
                cols = [self._get_var_raw(iso_num=i, allele_num=n) for i in idx]
                d = trace[cols].sum(axis=1)
                total_expr_support_event_isoforms.append(d)
            total = total_expr_support_event_isoforms[0] + total_expr_support_event_isoforms[1]
            expr = total_expr_support_event_isoforms[0] / total
            var = self.get_var_expr(allele_num=n)
            trace[var] = expr

        var = self.get_var_expr_diff()
        var1 = self.get_var_expr(allele_num=0)
        var2 = self.get_var_expr(allele_num=1)
        trace[var] = np.abs(trace[var1] - trace[var2])

        # print(trace)

        return trace

    def stats(self) -> pd.DataFrame:
        """Stats task result."""
        # import pymc3 as pm
        import arviz as az

        idxes = [col for col in self.trace.columns if not col.startswith('RAW')]

        means = []
        sds = []
        hpd_2_5s = []
        hpd_97_5s = []

        cols = ['mean', 'sd', 'hpd_2.5', 'hpd_97.5']
        data = [means, sds, hpd_2_5s, hpd_97_5s]

        for var_name in idxes:
            d_i = self.trace[var_name].to_numpy()
            means.append(np.mean(d_i))
            sds.append(np.std(d_i))
            hpd_2_5, hpd_97_5 = az.hdi(d_i, hdi_prob=0.95)
            hpd_2_5s.append(hpd_2_5)
            hpd_97_5s.append(hpd_97_5)

        df = pd.DataFrame({col: data[i] for i, col in enumerate(cols)}, index=idxes, columns=cols)

        # print(df)

        return df
