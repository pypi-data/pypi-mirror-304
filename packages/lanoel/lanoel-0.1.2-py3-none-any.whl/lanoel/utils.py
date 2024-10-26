def max_count(data):
    # Get the key with the maximum list length
    count = {}
    for entry in data:
        cat = entry.category
        if cat in count:
            count[cat] += 1
        else:
            count[cat] = 0

    return max(count, key=count.get)


def inner_category(data, category):
    return [entry for entry in data if entry.category == category]


def outter_category(data, category):
    return [entry for entry in data if entry.category != category]


def has_duplicate_names(data):
    name_set = set()
    for entry in data:
        name = entry.name
        if name in name_set:
            return True
        name_set.add(name)
    return False
