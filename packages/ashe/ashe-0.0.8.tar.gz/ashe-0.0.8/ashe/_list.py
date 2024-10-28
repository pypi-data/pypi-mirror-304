from typing import List, Any


def reverse(input_list: List) -> List:
    input_list.reverse()
    return input_list

def max_count(input_list: List) -> Any:
    return max(set(input_list), key=input_list.count)
