from typing import Callable


def bubble_sort[T](arr: list[T], compare_fn: Callable[[T, T], bool]):
    """
    Sorts the input list `arr` using the bubble sort algorithm. The order of elements
    is determined by the `compare_fn` function, which defines whether two elements are
    out of order and need to be swapped.

    Parameters:
    - arr (list[T]): The list of elements to be sorted.
    - compare_fn (Callable[[T, T], bool]): A comparison function that returns `True`
      if the first element should be placed after the second.

    Returns:
    - None: The list is sorted in place.
    """
    n = len(arr)
    while n > 0:
        new_n = 0
        for j in range(1, n):
            if compare_fn(arr[j - 1], arr[j]):
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                new_n = j
        n = new_n


def median_of_three[T](arr: list[T], low: int, mid: int, high: int) -> int:
    """
    Finds the median of three elements in the list `arr` at indices `low`, `mid`, and `high`.
    This is used for pivot selection in sorting algorithms like quicksort.

    Parameters:
    - arr (list[T]): The list of elements.
    - low (int): The index of the first element.
    - mid (int): The index of the middle element.
    - high (int): The index of the last element.

    Returns:
    - int: The index of the median element.
    """
    a, b, c = arr[low], arr[mid], arr[high]

    if (a <= b <= c) or (c <= b <= a):
        return mid

    if (b <= a <= c) or (c <= a <= b):
        return low

    return high


def insertion_sort[T](
        arr: list[T],
        low: int,
        high: int,
        compare_fn: Callable[[T, T], bool]) -> None:
    """
    Sorts a portion of the input list `arr` using the insertion sort algorithm. Sorting
    occurs between the indices `low` and `high` inclusive, using the provided `compare_fn`
    to determine the order of elements.

    Parameters:
    - arr (list[T]): The list of elements to be sorted.
    - low (int): The starting index of the portion to be sorted.
    - high (int): The ending index of the portion to be sorted.
    - compare_fn (Callable[[T, T], bool]): A comparison function that determines the order
      of two elements.

    Returns:
    - None: The specified portion of the list is sorted in place.
    """
    print('Insertion Sort')
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and compare_fn(key, arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def quicksort[T](
        arr: list[T],
        low: int = 0,
        high: int | None = None,
        compare_fn: Callable[[T, T], bool] | None = None) -> None:
    """
    Sorts the input list `arr` using the quicksort algorithm. The range between `low` and `high`
    is sorted, and the `compare_fn` determines the order of the elements. If `high` is None,
    the entire list is sorted. The function switches to insertion sort for small subarrays.

    Parameters:
    - arr (list[T]): The list of elements to be sorted.
    - low (int): The starting index for sorting (default is 0).
    - high (int | None): The ending index for sorting (default is None, which means the
      entire list is sorted).
    - compare_fn (Callable[[T, T], bool] | None): A comparison function that defines the
      sorting order. If None, the default order (`x < y`) is used.

    Returns:
    - None: The list is sorted in place.
    """
    if high is None:
        high = len(arr) - 1

    if compare_fn is None:
        compare_fn = lambda x, y: x < y

    while low < high:
        if high - low < 10:
            insertion_sort(arr, low, high, compare_fn)
            return

        pivot_index = median_of_three(arr, low, (low + high) // 2, high)
        pivot_new_index = partition(arr, low, high, pivot_index, compare_fn)

        if pivot_new_index - low < high - pivot_new_index:
            quicksort(arr, low, pivot_new_index - 1, compare_fn)
            low = pivot_new_index + 1
        else:
            quicksort(arr, pivot_new_index + 1, high, compare_fn)
            high = pivot_new_index - 1


def partition[T](
        arr: list[T],
        low: int, high: int,
        pivot_index: int,
        compare_fn: Callable[[T, T], bool]) -> int:
    """
    Partitions the list `arr` around the pivot element located at `pivot_index`. Elements smaller
    than the pivot are moved to the left, and elements greater are moved to the right. The
    comparison is done using the `compare_fn`.

    Parameters:
    - arr (list[T]): The list of elements to be partitioned.
    - low (int): The starting index of the range to partition.
    - high (int): The ending index of the range to partition.
    - pivot_index (int): The index of the pivot element.
    - compare_fn (Callable[[T, T], bool]): A comparison function to determine the order.

    Returns:
    - int: The new index of the pivot element after partitioning.
    """
    pivot_value = arr[pivot_index]
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

    store_index = low
    for i in range(low, high):
        if compare_fn(arr[i], pivot_value):
            arr[i], arr[store_index] = arr[store_index], arr[i]
            store_index += 1

    arr[store_index], arr[high] = arr[high], arr[store_index]
    return store_index


def merge_sort[T](
        arr: list[T],
        start: int = 0,
        end: int | None = None,
        compare_fn: Callable[[T, T], bool] | None = None) -> None:
    """
    Sorts the input list `arr` using the merge sort algorithm. The list is split and
    recursively sorted in halves, merging them at the end. The sorting is performed in
    the range `[start, end)`, and the `compare_fn` determines the sorting order.

    Parameters:
    - arr (list[T]): The list of elements to be sorted.
    - start (int): The starting index for sorting (default is 0).
    - end (int | None): The ending index for sorting (default is None, which means the
      entire list is sorted).
    - compare_fn (Callable[[T, T], bool] | None): A comparison function to determine the
      sorting order. If None, the default order (`x < y`) is used.

    Returns:
    - None: The list is sorted in place.
    """
    if end is None:
        end = len(arr)

    if compare_fn is None:
        compare_fn = lambda x, y: x < y

    if end - start > 1:
        mid = (start + end) // 2

        merge_sort(arr, start, mid, compare_fn)
        merge_sort(arr, mid, end, compare_fn)

        merge(arr, start, mid, end, compare_fn)


def merge[T](
        arr: list[T],
        start: int,
        mid: int,
        end: int,
        compare_fn: Callable[[T, T], bool]) -> None:
    """
    Merges two sorted sublists of `arr` into a single sorted list. The sublists are in the ranges
    `[start, mid)` and `[mid, end)`, and the merged list will occupy `[start, end)`.

    Parameters:
    - arr (list[T]): The list containing the sublists to be merged.
    - start (int): The starting index of the first sublist.
    - mid (int): The end index of the first sublist and the starting index of the second.
    - end (int): The ending index of the second sublist.
    - compare_fn (Callable[[T, T], bool]): A comparison function to determine the order of elements.

    Returns:
    - None: The merged sublists are stored in place in the original list.
    """
    left = arr[start:mid]
    right = arr[mid:end]

    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        if compare_fn(left[i], right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def selection_sort[T](
        arr: list[T],
        compare_fn: Callable[[T, T], bool],
        low: int = 0,
        high: int | None = None) -> None:
    """
    Sorts a portion of the list `arr` using the selection sort algorithm. The range of elements
    to be sorted is `[low, high)`. The `compare_fn` determines the sorting order.

    Parameters:
    - arr (list[T]): The list of elements to be sorted.
    - compare_fn (Callable[[T, T], bool]): A comparison function to determine the order.
    - low (int): The starting index for sorting (default is 0).
    - high (int | None): The ending index for sorting (default is None, which sorts the
      entire list).

    Returns:
    - None: The list is sorted in place.
    """
    if high is None:
        high = len(arr)
    print('Selection Sort')
    for i in range(low, high):
        min_idx = i
        for j in range(i + 1, high):
            if compare_fn(arr[j], arr[min_idx]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


def bucket_sort[T](arr: list[T], compare_fn: Callable[[T, T], bool], n: int | None = None) -> list[int]:
    """
    Sorts the list `arr` using the bucket sort algorithm. The list is divided into `n`
    buckets, each of which is sorted individually. The `compare_fn` determines the sorting
    order within each bucket.

    Parameters:
    - arr (list[T]): The list of elements to be sorted.
    - compare_fn (Callable[[T, T], bool]): A comparison function to determine the sorting order.
    - n (int | None): The number of buckets to divide the elements into (default is the length of the list).

    Returns:
    - list[int]: A new sorted list.
    """
    if not arr:
        return []

    if n is None:
        n = len(arr)

    min_v, max_v = min(arr), max(arr)
    range_v = max_v - min_v

    if range_v == 0:
        return arr if compare_fn(arr[0], arr[0]) else arr[::-1]

    buckets = [[] for _ in range(n)]

    for v in arr:
        index = int((v - min_v) / range_v * (n - 1))
        buckets[index].append(v)

    for i in range(n):
        quicksort(buckets[i], compare_fn=compare_fn)

    result = []
    if compare_fn(1, 0):
        for bucket in reversed(buckets):
            result.extend(bucket)
    else:
        for bucket in buckets:
            result.extend(bucket)

    return result

# def bucket_sort[T](arr: list[T], compare_fn: Callable[[T, T], bool], n: int | None = None) -> list[int]:
#     """
#     Sorts the list `arr` using the bucket sort algorithm. The list is divided into `n`
#     buckets, each of which is sorted individually. The `compare_fn` determines the sorting
#     order within each bucket.
#
#     Parameters:
#     - arr (list[T]): The list of elements to be sorted.
#     - compare_fn (Callable[[T, T], bool]): A comparison function to determine the sorting order.
#     - n (int | None): The number of buckets to divide the elements into (default is the length of the list).
#
#     Returns:
#     - list[int]: A new sorted list.
#     """
#     if not arr:
#         return []
#
#     if n is None:
#         n = len(arr)
#
#     min_v, max_v = min(arr), max(arr)
#     range_v = max_v - min_v
#
#     bucket_count = n
#     buckets = [[] for _ in range(bucket_count)]
#
#     for v in arr:
#         index = int((v - min_v) / range_v * (bucket_count - 1))
#         buckets[index].append(v)
#
#     for i in range(bucket_count):
#         buckets[i].sort(key=lambda x: (x, compare_fn))
#
#     result = []
#     for i in range(bucket_count):
#         result.extend(buckets[i])
#
#     return result
