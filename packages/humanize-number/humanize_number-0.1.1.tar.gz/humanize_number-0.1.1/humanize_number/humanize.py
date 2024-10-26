def humanize_number(num: int) -> str:
    """
    Takes an integer and humanizes it into a more readable form (1K, 1M, 1B, 1T)

    :param num: int
    :return: str
    """
    if num >= 1_000_000_000_000:
        return f'{num // 1_000_000_000_000}T'
    elif num >= 1_000_000_000:
        return f'{num // 1_000_000_000}B'
    elif num >= 1_000_000:
        return f'{num // 1_000_000}M'
    elif num >= 1_000:
        return f'{num // 1_000}K'
    else:
        return str(num)