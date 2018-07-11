caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class CaseException(Exception):
    pass


def headline_to_snake(headline_input):
    if (not headline_input) or headline_input[0] not in caps:
        raise CaseException('Input must be in headline case')
    return '_'.join(_tokenise_headline(headline_input)).lower()


def _tokenise_headline(headline_input):
    remaining_input = headline_input
    tokens = []
    while remaining_input:
        parts = _split_headline(remaining_input)
        tokens.append(parts[0])
        remaining_input = parts[1]
    return tokens


def _split_headline(headline_input):
    if len(headline_input) == 1:
        return headline_input, None
    for i in range(1, len(headline_input)):
        if headline_input[i] in caps:
            return headline_input[:i], headline_input[i:]
    return headline_input, None
