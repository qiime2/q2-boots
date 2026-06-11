# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2
from qiime2.plugin.testing import TestPluginBase
from qiime2.plugin import Visualization
import pandas as pd

class KmerDiversityTests(TestPluginBase):

    package = 'q2_boots'

    def setUp(self):
        super().setUp()
        self.kmer_diversity = self.plugin.pipelines['kmer_diversity']
        table1 = pd.DataFrame(data=[[1, 1], [0, 4]],
                              columns=['F1', 'F2'],
                              index=['S1', 'S2'])
        self.table1 = qiime2.Artifact.import_data(
            "FeatureTable[Frequency]", table1, view_type=pd.DataFrame)

        sequences = pd.Series(['ACGTACGTACGTACGT', 'TGCATGCATGCATGCA'],
                                index=['F1', 'F2'])
        self.sequences1 = qiime2.Artifact.import_data(
            "FeatureData[Sequence]", sequences, view_type=pd.Series)

        metadata = pd.DataFrame(['not', 'of', 'interest'],
                                index=['S1', 'S2', 'S3'],
                                columns=['blank'])
        metadata.index.name = 'sample-id'
        self.metadata = qiime2.Metadata(metadata)

    def test_kmer_diversity_wo_replacement(self):
        output = self.kmer_diversity(table=self.table1,
                                     sequences=self.sequences1,
                                     sampling_depth=2,
                                     metadata=self.metadata,
                                     replacement=False,
                                     n=10)
        self.assertEqual(len(output[0]), 10)
        self.assertEqual(len(output[1]), 10)

        skbio_lt_060_alpha_keys = set(
            ['observed_features', 'pielou_evenness', 'shannon_entropy'])
        skbio_gte_060_alpha_keys = set(
            ['observed_features', 'pielou_e', 'shannon'])
        self.assertTrue(set(output[2].keys()) == skbio_lt_060_alpha_keys or
                        set(output[2].keys()) == skbio_gte_060_alpha_keys)

        self.assertEqual(set(output[3].keys()), set(['jaccard', 'braycurtis']))
        self.assertEqual(set(output[4].keys()), set(['jaccard', 'braycurtis']))

        self.assertEqual(output[5].type, Visualization)

    def test_kmer_diversity_custom_metrics(self):
        output = self.kmer_diversity(table=self.table1,
                                     sequences=self.sequences1,
                                     sampling_depth=2,
                                     metadata=self.metadata,
                                     replacement=False,
                                     n=2,
                                     alpha_metrics=['observed_features'],
                                     beta_metrics=['jaccard'])
        self.assertEqual(len(output[0]), 2)
        self.assertEqual(len(output[1]), 2)

        self.assertEqual(set(output[2].keys()), set(['observed_features']))
        self.assertEqual(set(output[3].keys()), set(['jaccard']))
        self.assertEqual(set(output[4].keys()), set(['jaccard']))

        self.assertEqual(output[5].type, Visualization)
