def make_chunks(unchunked_text, limit):
    chunks = []

    while unchunked_text:
        if len(unchunked_text) <= limit:
            chunks.append(unchunked_text)
            break
        else:
            index = unchunked_text.rfind("\n", 0, limit)
            if index == -1:
                return "can't do it"
            chunks.append(unchunked_text[:index+1])
            unchunked_text = unchunked_text[index+1:]
    return chunks
