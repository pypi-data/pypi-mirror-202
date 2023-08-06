from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Tuple

from span_marker.configuration import SpanMarkerConfig

Entity = Tuple[int, int, int]


class LabelNormalizer(ABC):
    """Class to convert NER training data into a common format used in the SpanMarkerModel.

    The common format involves tokenized texts and labels as Entity instances.
    """

    def __init__(self, config: SpanMarkerConfig) -> None:
        super().__init__()
        self.config = config

    @abstractmethod
    def __call__(self, ner_tags: List[int]) -> Dict[str, List[Any]]:
        raise NotImplementedError


class LabelNormalizerScheme(LabelNormalizer):
    def __init__(self, config: SpanMarkerConfig) -> None:
        super().__init__(config)
        self.label_ids_by_tag = self.config.group_label_ids_by_tag()
        self.start_ids = set()
        self.end_ids = set()

    def ner_tags_to_entities(self, ner_tags: List[int]) -> Iterator[Entity]:
        """Assumes a correct IOB or IOB2 annotation scheme"""
        start_idx = None
        reduced_label_id = None
        for idx, label_id in enumerate(ner_tags):
            # End of an entity
            if start_idx is not None and label_id in self.end_ids:
                yield (reduced_label_id, start_idx, idx)
                start_idx = None

            # Start of an entity
            if start_idx is None and label_id in self.start_ids:
                # compute the schemeless label ID
                reduced_label_id = self.config.id2reduced_id[label_id]
                start_idx = idx

        if start_idx is not None:
            yield (reduced_label_id, start_idx, idx)

    def __call__(self, ner_tags: List[int]) -> Dict[str, List[Any]]:
        batch_entities = []
        for tags in ner_tags:
            entities = list(self.ner_tags_to_entities(tags))
            batch_entities.append(entities)
        return {"ner_tags": batch_entities}


class LabelNormalizerIOB(LabelNormalizerScheme):
    def __init__(self, config: SpanMarkerConfig) -> None:
        super().__init__(config)
        # Support for IOB2 and IOB, respectively:
        self.start_ids = self.label_ids_by_tag["B"] | self.label_ids_by_tag["I"]
        self.end_ids = self.label_ids_by_tag["B"] | self.label_ids_by_tag["O"]


class LabelNormalizerBIOES(LabelNormalizerScheme):
    def __init__(self, config: SpanMarkerConfig) -> None:
        super().__init__(config)
        self.start_ids = self.label_ids_by_tag["B"] | self.label_ids_by_tag["S"]
        self.end_ids = self.label_ids_by_tag["B"] | self.label_ids_by_tag["O"] | self.label_ids_by_tag["S"]


class LabelNormalizerBILOU(LabelNormalizerScheme):
    def __init__(self, config: SpanMarkerConfig) -> None:
        super().__init__(config)
        self.start_ids = self.label_ids_by_tag["B"] & self.label_ids_by_tag["U"]
        self.end_ids = self.label_ids_by_tag["B"] & self.label_ids_by_tag["O"] & self.label_ids_by_tag["U"]


class LabelNormalizerNoScheme(LabelNormalizer):
    def ner_tags_to_entities(self, ner_tags: List[int]) -> Iterator[Entity]:
        start_idx = None
        entity_label_id = None
        for idx, label_id in enumerate(ner_tags):
            # End of an entity
            if start_idx is not None and label_id != entity_label_id:
                yield (entity_label_id, start_idx, idx)
                start_idx = None

            # Start of an entity
            if start_idx is None and label_id != self.config.outside_id:
                entity_label_id = label_id
                start_idx = idx

        if start_idx is not None:
            yield (entity_label_id, start_idx, idx)

    def __call__(self, ner_tags: List[int]) -> Dict[str, List[Any]]:
        batch_entities = []
        for tags in ner_tags:
            entities = list(self.ner_tags_to_entities(tags))
            batch_entities.append(entities)
        return {"ner_tags": batch_entities}


class AutoLabelNormalizer:
    """Factory class to return the correct LabelNormalizer subclass."""

    @staticmethod
    def from_config(config: SpanMarkerConfig) -> LabelNormalizer:
        if not config.are_labels_schemed():
            return LabelNormalizerNoScheme(config)

        tags = config.get_scheme_tags()
        if tags == set("BIO"):
            return LabelNormalizerIOB(config)
        if tags == set("BIOES"):
            return LabelNormalizerBIOES(config)
        if tags == set("BILOU"):
            return LabelNormalizerBILOU(config)
        raise ValueError(
            "Data labeling scheme not recognized. Expected either IOB, IOB2, BIOES, BILOU "
            "or no scheme (i.e. one label per class, no B-, I- scheme prefixes, etc.)"
        )
