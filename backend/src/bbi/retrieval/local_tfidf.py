from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bbi.domain.memory import MemoryCard


def rank_memories(query: str, cards: list[MemoryCard]) -> list[tuple[MemoryCard, float]]:
    if not cards:
        return []
    documents = [
        " ".join(
            [card.content, *[qualifier.text for qualifier in card.scope_qualifiers], *card.tags]
        )
        for card in cards
    ]
    try:
        matrix = TfidfVectorizer(lowercase=True, ngram_range=(1, 2)).fit_transform(
            [query, *documents]
        )
    except ValueError:
        return sorted(((card, 0.0) for card in cards), key=lambda pair: pair[0].memory_id)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
    return sorted(zip(cards, scores, strict=True), key=lambda pair: (-pair[1], pair[0].memory_id))
