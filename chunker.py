def make_chunks(unchunked_text, limit):
    chunks = []

    while unchunked_text:
        if len(unchunked_text) <= limit:
            chunks.append(unchunked_text)
            break
        else:
            unchunked_text = solve_spacing_at_beggining(unchunked_text)

            index = unchunked_text.rfind("\n", 0, limit)

            if index == -1:
                return "can't do it"
 
            chunks.append(unchunked_text[:index+1])
            unchunked_text = unchunked_text[index+1:]
    return chunks

def solve_spacing_at_beggining(text):
    if(text.startswith("\t")):
        text = text.replace("\t", "_ _   ", 1)
    return text

