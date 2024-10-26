import os
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict

import pandas as pd

from bdm2.logger import build_logger

logger = build_logger(Path(__file__), save_log=False)


def update_df(df1: pd.DataFrame, df2: pd.DataFrame):
    output_df = df1.copy()
    rows_intersections = list(set(df2.index).intersection(set(df1.index)))
    rows_difference = list(set(df2.index).difference(set(df1.index)))
    cols_intersections = list(set(df2.columns).intersection(set(df1.columns)))
    cols_difference = list(set(df2.columns).difference(set(df1.columns)))

    # update intersections
    output_df.loc[rows_intersections, cols_intersections] = df2.loc[
        rows_intersections, cols_intersections
    ]
    # add new indexes
    output_df = pd.concat(
        [output_df, df2.loc[rows_difference, cols_intersections]], axis=0
    )

    # add new column
    output_df = pd.concat([output_df, df2[cols_difference]], axis=1)
    return output_df


class CSVUpdater:

    def __init__(
            self, csv_fname: str, sep: str = ";", index_col=None, header_rows=None
    ):
        self.fname = csv_fname
        self.sep = sep
        self.index_col = index_col
        self.df = pd.DataFrame()
        if os.path.exists(csv_fname):
            self.df = pd.read_csv(
                self.fname, sep=self.sep, index_col=index_col, header=list(header_rows)
            )

    def update(self, df: pd.DataFrame):
        self.df = update_df(self.df, df)

    def save(self, fname: str):
        self.df.to_csv(fname, sep=self.sep)


class Updater(ABC):
    def __init__(
            self,
            base_df_filename: str,
            index_id: str or List[str],
            header=0,
            index_col=None,
            skip_rows=[],
    ):
        """
        Use existed table as base and update in with new values
        :param base_df_filename: filename
        :param index_id: index column names, by which matching will be made
        :param header: the same as pandas columns
        :param index_col: the same as pandas index_col
        :param skip_rows: the same as pandas skip_rows
        """

        self.base_df_filename: str = base_df_filename

        if not os.path.exists(os.path.dirname(base_df_filename)):
            os.makedirs(os.path.dirname(base_df_filename))

        self.index_id: List[str] = []
        if isinstance(index_id, str):
            self.index_id = [index_id]
        else:
            self.index_id = index_id

        self.sheets: Dict[str, pd.DataFrame] = {}

        self.load(header, index_col, skip_rows)

    @abstractmethod
    def load(self, header, index_col, skip_rows):
        """"""


class XLSXUpdater(Updater):
    def __init__(
            self,
            base_df_filename: str,
            index_id: str,
            header=0,
            index_col=None,
            skip_rows=[],
    ):
        Updater.__init__(self, base_df_filename, index_id, header, index_col, skip_rows)
        self.writer = pd.ExcelWriter(self.base_df_filename, engine="openpyxl")

    def load(self, header, index_col, skip_rows):
        if os.path.exists(self.base_df_filename):
            try:
                reader = pd.ExcelFile(self.base_df_filename, engine="openpyxl")
            except Exception as e:
                warnings.warn(
                    f"Could not load {self.base_df_filename}. It will be rewritten: {e}"
                )
                return
                # os.rename(self.base_df_filename, self.base_df_filename.replace('.xlsx', '_broken.xlsx'))
                # reader = pd.ExcelFile(self.base_df_filename, engine='openpyxl')
            for sheet in reader.sheet_names:
                try:
                    tmp_df = reader.parse(
                        sheet, index_col=index_col, header=header, skiprows=skip_rows
                    )
                    if len(self.index_id) > 0:
                        if any(
                                [
                                    index_id not in tmp_df.columns
                                    for index_id in self.index_id
                                ]
                        ):
                            logger.info(
                                f"No {self.index_id} in sheet {sheet}. {sheet} will not be added"
                            )
                            continue
                        else:
                            tmp_df = tmp_df.set_index(self.index_id)
                    self.sheets[sheet] = tmp_df

                except:
                    pass
            reader.close()

    def sort_sheet_by(self, sheet: str, by: List[str]):
        if sheet not in self.sheets:
            logger.info(f"No {sheet} in sheets")
            return
        tmp_sheet_df = self.sheets[sheet]
        if any([by_col not in tmp_sheet_df.columns for by_col in by]):
            logger.info(f"Not all by columns are in {sheet}")
            return

        tmp_sheet_df = tmp_sheet_df.sort_values(by=by)
        self.sheets[sheet] = tmp_sheet_df

    def update_sheet(self, sheet: str, new_df: pd.DataFrame) -> bool:
        df = new_df.astype("object")
        if sheet in self.sheets:
            sheet_df = self.sheets[sheet].astype("object")
            # update
            df = update_df(sheet_df, df)

        self.sheets[sheet] = df
        return True

    def save(self):
        for sheet in self.sheets:
            df = self.sheets[sheet].copy()
            if len(self.index_id) > 0:
                df = df.reset_index()
            df.to_excel(self.writer, sheet, index=False)
        if len(self.writer.sheets) > 0:
            self.writer.save()
        logger.info(f"{self.base_df_filename} was updated")
