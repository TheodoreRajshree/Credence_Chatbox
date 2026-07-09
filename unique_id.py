def normalize_unique_id(value):

    values = []

    if value is None:
        return values


    # original value
    values.append(value)


    # string version
    values.append(str(value))


    # integer version only if safe
    try:
        num = int(value)

        # MongoDB Int64 safe range
        if num <= 9223372036854775807:
            values.append(num)

    except:
        pass


    return list(set(values))