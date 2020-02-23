from math import ceil


def split_list(lst: list, chunk_size: int):
    return [lst[i * chunk_size:chunk_size * (i + 1)]
            for i in range(ceil(len(lst) / chunk_size))]
