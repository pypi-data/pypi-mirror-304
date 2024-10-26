from __future__ import annotations
from dataclasses import dataclass
from py_concodese.bug_parsing.bug_report import BReport
from py_concodese.scoring.file_rank_data import FileRankData

from tabulate import tabulate


@dataclass
class BugResult:
    """holds the recommendations for a bug,
    and the evaluation of those recommendation's accuracy"""

    bug_report: BReport
    top_1: bool
    top_5: bool
    top_10: bool
    m_ap: float
    m_rr: float
    top10_frd: list[FileRankData]

    def pretty_print(self):
        """ prints the result """
        print()
        if self.bug_report is not None:
            print(
                f"id:{self.bug_report.bug_id}, summ: {self.bug_report.summary[:50]}...\n"
            )
        # print T10 files
        # for frd in self.top10_frd:
        #     frd.pretty_print()

        results_as_matrix = [file_rank_data.results_as_list() for file_rank_data in self.top10_frd]
        headers = ['Rank', 'File Name', 'Package', 'Textual Ranks', 'VSM Ranks', 'Sortable Ranks', 'Relative Path']
        print(tabulate(results_as_matrix, headers=headers))

        print(f"top 1: {self.top_1}")
        print(f"top 5: {self.top_5}")
        print(f"top 10: {self.top_10}")
        print(f"map: {self.m_ap}")
        print(f"mrr: {self.m_rr}")
        print()


@dataclass
class BugResultSummary:
    """A data class which holds cumulative/ average recommendation accuracy data
    for multiple bug reports"""

    heading: str
    top_1: bool
    top_5: bool
    top_10: bool
    m_ap: float
    m_rr: float

    def pretty_print(self):
        """ prints the result """
        print()
        if len(self.heading) > 0:
            print(f"{self.heading}")
        print(f"top 1: {self.top_1}")
        print(f"top 5: {self.top_5}")
        print(f"top 10: {self.top_10}")
        print(f"map: {self.m_ap}")
        print(f"mrr: {self.m_rr}")
        print()
