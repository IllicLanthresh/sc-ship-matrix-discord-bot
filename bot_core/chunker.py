"""
Module containing the functionality to make chunks out of text and a limit size.
"""

def make_chunks(unchunked_text, limit):
    """
    Makes chunks of text within a limit size, spliting only at newlines.

    Returns a list of strings.
    """
    chunks = []

    while unchunked_text:
        unchunked_text = __solve_spacing_at_beggining(unchunked_text)
        if len(unchunked_text) <= limit:
            chunks.append(unchunked_text)
            break
        else:
            index = unchunked_text.rfind("\n", 0, limit)
            if index == -1:
                raise Exception("Can't chunk text")
            chunks.append(unchunked_text[:index+1])
            unchunked_text = unchunked_text[index+1:]
    return chunks


def __solve_spacing_at_beggining(text):
    """
    Discord removes empty spaces at the beggining of a message.

    This function replaces tabs with a magic string for discord to keep those spaces.
    """
    if text.startswith("\t"):
        text = text.replace("\t", "_ _   ", 1)
    return text
