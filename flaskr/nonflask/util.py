def remove_bad_spaces(text):
    return str(text.encode())[2:-1].replace("\\xc2\\xa0", " ").replace("\\xa0", " ")
