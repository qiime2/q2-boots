# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd

import qiime2
from qiime2.plugin.testing import TestPluginBase


def _table_collection_equality(tables1, tables2):
    # Determine if two Collections of tables contain the same tables or not
    tables1 = [table.view(pd.DataFrame) for table in tables1.values()]
    tables2 = [table.view(pd.DataFrame) for table in tables2.values()]

    for table1, table2 in zip(tables1, tables2):
        if not table1.equals(table2):
            return False

    return True


def _table_collection_equality_print(tables1, tables2):
    # Determine if two Collections of tables contain the same tables or not
    tables1 = [table.view(pd.DataFrame) for table in tables1.values()]
    tables2 = [table.view(pd.DataFrame) for table in tables2.values()]
    for table in tables1:
        print(table)
    print('\n\n')
    for table in tables2:
        print(table)
    for table1, table2 in zip(tables1, tables2):
        if not table1.equals(table2):
            return False

    return True


def _table_list_contains_different_tables(tables):
    # Determine if all tables in a collection of tables are identical or not
    tables = [table.view(pd.DataFrame) for table in tables.values()]

    for i in range(len(tables)):
        for j in range(i + 1, len(tables)):
            if not tables[i].equals(tables[j]):
                return True

    return False


class ResampleTests(TestPluginBase):
    package = 'q2_boots.tests'

    def setUp(self):
        super().setUp()
        self.resample_pipeline = self.plugin.pipelines['resample']

        table1 = pd.DataFrame(data=[[0, 1], [1, 1], [3, 2]],
                              columns=['F1', 'F2'],
                              index=['S1', 'S2', 'S3'])
        self.table_artifact1 = qiime2.Artifact.import_data(
            "FeatureTable[Frequency]", table1, view_type=pd.DataFrame
        )

        table2 = pd.DataFrame(data=[[0, 1, 1],
                                    [10, 10, 9],
                                    [30, 20, 9],
                                    [42, 42, 9]],
                              columns=['F1', 'F2', 'F3'],
                              index=['S1', 'S2', 'S3', 'S4'])
        self.table_artifact2 = qiime2.Artifact.import_data(
            "FeatureTable[Frequency]", table2, view_type=pd.DataFrame
        )

        table3 = pd.DataFrame(data=[[1, 1]],
                              columns=['F1', 'F2'],
                              index=['S1'])
        self.table_artifact3 = qiime2.Artifact.import_data(
            "FeatureTable[Frequency]", table3, view_type=pd.DataFrame
        )

    def test_rarefy_seed_cross_iteration(self):
        tables1, = self.resample_pipeline(table=self.table_artifact2,
                                          sampling_depth=1,
                                          n=10,
                                          replacement=True,
                                          random_seed=123)
        tables2, = self.resample_pipeline(table=self.table_artifact2,
                                          sampling_depth=1,
                                          n=10,
                                          replacement=True,
                                          random_seed=123)
        tables3, = self.resample_pipeline(table=self.table_artifact2,
                                          sampling_depth=1,
                                          n=10,
                                          replacement=True,
                                          random_seed=321)

        self.assertTrue(_table_collection_equality_print(tables1, tables2))
        self.assertFalse(_table_collection_equality(tables1, tables3))

        self.assertTrue(_table_list_contains_different_tables(tables1))
        self.assertTrue(_table_list_contains_different_tables(tables3))

    # test helper functions
    def _expected_sampling_depth(self, replacement):
        obs_tables, = self.resample_pipeline(table=self.table_artifact2,
                                             sampling_depth=1,
                                             n=4,
                                             replacement=replacement)
        for obs_table in obs_tables.values():
            obs_table = obs_table.view(pd.DataFrame)
            self.assertEqual(list(obs_table.sum(axis=1)),
                             [1., 1., 1., 1.])

        obs_tables, = self.resample_pipeline(table=self.table_artifact2,
                                             sampling_depth=2,
                                             n=3,
                                             replacement=replacement)
        for obs_table in obs_tables.values():
            obs_table = obs_table.view(pd.DataFrame)
            self.assertEqual(list(obs_table.sum(axis=1)),
                             [2., 2., 2., 2.])

        obs_tables, = self.resample_pipeline(table=self.table_artifact2,
                                             sampling_depth=50,
                                             n=2,
                                             replacement=replacement)
        for obs_table in obs_tables.values():
            obs_table = obs_table.view(pd.DataFrame)
            self.assertEqual(list(obs_table.sum(axis=1)),
                             [50., 50.])

    def _resample_filters_sample(self, replacement):
        with self.assertRaisesRegex(ValueError, "no samples or features"):
            _ = self.resample_pipeline(table=self.table_artifact1,
                                       sampling_depth=6,
                                       n=1,
                                       replacement=replacement)

        obs_tables, = self.resample_pipeline(table=self.table_artifact1,
                                             sampling_depth=5,
                                             n=2,
                                             replacement=replacement)
        for obs_table in obs_tables.values():
            obs_table = obs_table.view(pd.DataFrame)
            sids = list(obs_table.index)
            self.assertEqual(sids, ['S3'])

        obs_tables, = self.resample_pipeline(table=self.table_artifact1,
                                             sampling_depth=2,
                                             n=2,
                                             replacement=replacement)
        for obs_table in obs_tables.values():
            obs_table = obs_table.view(pd.DataFrame)
            sids = list(obs_table.index)
            self.assertEqual(sids, ['S2', 'S3'])

        obs_tables, = self.resample_pipeline(table=self.table_artifact1,
                                             sampling_depth=1,
                                             n=2,
                                             replacement=replacement)
        for obs_table in obs_tables.values():
            obs_table = obs_table.view(pd.DataFrame)
            sids = list(obs_table.index)
            self.assertEqual(sids, ['S1', 'S2', 'S3'])
