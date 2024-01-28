def increment_dictionary_values(d, i):
    result = {}
    for k, v in d.items():
        result[k] = v + i
    return result
