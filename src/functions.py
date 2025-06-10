def binary_search(val: str, arr: list[str]) -> int | None:
    '''Возвращает номер строки записи по индексу'''
    split_arr = [el.rstrip().split(';') for el in arr]
    left_point = 0
    right_point = len(arr) - 1
    while left_point <= right_point:
        middle = (left_point + right_point) // 2
        if split_arr[middle][0] == val:
            return int(split_arr[middle][1])
        elif split_arr[middle][0] < val:
            left_point = middle + 1
        else:
            right_point = middle - 1
    return None
