import spotify


def _split(words: list[str], num_parts) -> list[list[list[str]]]:
    """Get all splits with specified number of parts."""

    if num_parts == 1:
        return [[words]]

    # Remove all possible first parts and split remaining part recursively.
    splits = []
    for i in range(1, len(words)):
        for s in _split(words[i:], num_parts - 1):
            splits.append([words[:i], *s])

    return splits


def _get_splits(
    phrase: str, min_words_per_q: int = 1, max_words_per_q: int = 5
) -> list[list[str]]:
    """Get all splits of phrase with min and max number of words per part."""

    words = phrase.split()

    # Generate all possible splits.
    splits = []
    for n in range(1, len(words) + 1):
        splits += _split(words, n)

    # Filter out unwanted splits and transform parts to lowercase.
    splits = [
        [' '.join(q) for q in split]
        for split in splits
        if all(min_words_per_q <= len(q) <= max_words_per_q for q in split)
    ]

    return splits


def _search_split(
    split: list[str], auth_token: str, cache: dict
) -> list[spotify.Track]:
    """Search tracks for each part of split and return them if all are found."""

    tracks = []
    for q in split:
        if q not in cache:
            track = spotify.search_track(q, auth_token)
            cache[q] = track

        if cache[q] is None:
            return

        tracks.append(cache[q])

    return tracks


def search(phrase: str) -> list[spotify.Track]:
    """Search for list of tracks the result in phrase when combining names."""

    auth_token = spotify.get_auth_token()

    # Try out all different splits
    splits = _get_splits(phrase.lower())
    cache = {}
    for split in splits:
        tracks = _search_split(split, auth_token, cache)
        if tracks:
            return tracks

    return []
