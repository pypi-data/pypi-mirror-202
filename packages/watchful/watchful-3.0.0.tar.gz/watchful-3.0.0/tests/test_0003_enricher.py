"""
This script tests data enrichment using `enricher`s directly.
"""
################################################################################

import os
import sys

from watchful import attributes

EXAMPLES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples"
)
sys.path.insert(1, EXAMPLES_DIR)
from ex_001.example import (
    StatisticsEnricher,
)  # pylint: disable=wrong-import-position,wrong-import-order,import-error
from ex_002.example import (
    SentimentEnricher,
)  # pylint: disable=wrong-import-position,wrong-import-order,import-error
from ex_003.example import (
    NEREnricher,
)  # pylint: disable=wrong-import-position,wrong-import-order,import-error


def test_statistics_enricher():
    """
    This test tests data enrichment using user variables for the statistics
    enrichment.
    """
    statistics_enricher = StatisticsEnricher()
    attributes.enrich(
        os.path.join(EXAMPLES_DIR, "ex_001", "dataset.csv"),
        os.path.join(EXAMPLES_DIR, "ex_001", "attributes.attrs"),
        statistics_enricher.enrich_row,
        statistics_enricher.enrichment_args,
    )
    assert True


def test_sentiment_enricher():
    """
    This test tests data enrichment using user variables for the sentiment
    enrichment.
    """
    sentiment_enricher = SentimentEnricher()
    attributes.enrich(
        os.path.join(EXAMPLES_DIR, "ex_002", "dataset.csv"),
        os.path.join(EXAMPLES_DIR, "ex_002", "attributes.attrs"),
        sentiment_enricher.enrich_row,
        sentiment_enricher.enrichment_args,
    )
    assert True


def test_ner_enricher():
    """
    This test tests data enrichment using user variables for the NER
    enrichment.
    """
    ner_enricher = NEREnricher()
    attributes.enrich(
        os.path.join(EXAMPLES_DIR, "ex_003", "dataset.csv"),
        os.path.join(EXAMPLES_DIR, "ex_003", "attributes.attrs"),
        ner_enricher.enrich_row,
        ner_enricher.enrichment_args,
    )
    assert True


if __name__ == "__main__":

    test_statistics_enricher()
    test_sentiment_enricher()
    test_ner_enricher()

    sys.exit(0)
