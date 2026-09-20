def same(regex_char, text_char):
    return regex_char == "." or regex_char == text_char


def match(regex, text):
    if len(regex) == 0:
        return True

    if regex == "$":
        return len(text) == 0

    # NEW: escape character
    if regex[0] == "\\":
        if len(regex) < 2 or len(text) == 0:
            return False

        if regex[1] != text[0]:
            return False

        return match(regex[2:], text[1:])

    # ?, *, +
    if len(regex) > 1 and regex[1] in "?*+":
        char = regex[0]
        operator = regex[1]
        rest = regex[2:]

        first_match = len(text) > 0 and same(char, text[0])

        if operator == "?":
            return (
                match(rest, text)
                or
                (first_match and match(rest, text[1:]))
            )

        if operator == "*":
            return (
                match(rest, text)
                or
                (first_match and match(regex, text[1:]))
            )

        if operator == "+":
            return (
                first_match
                and (
                    match(rest, text[1:])
                    or
                    match(regex, text[1:])
                )
            )

    if len(text) == 0:
        return False

    if not same(regex[0], text[0]):
        return False

    return match(regex[1:], text[1:])


def search(regex, text):
    if regex.startswith("^"):
        return match(regex[1:], text)

    for i in range(len(text) + 1):
        if match(regex, text[i:]):
            return True

    return False


regex, text = input().split("|")
print(search(regex, text))