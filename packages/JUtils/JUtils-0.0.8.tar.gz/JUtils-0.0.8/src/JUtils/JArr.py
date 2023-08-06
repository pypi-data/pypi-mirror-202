#Functions for array analysing and modification

def segm(arr: list, n: int) -> list[list]:
    '''
    Divide a list into sublists of a specified size.
    
    Parameters:
        arr (list): The list to be divided into sublists.
        n (int): The size of each sublist.
        
    Returns:
        list: A list of sublists, where each sublist contains 'n' elements.
        
    Example:
        >>> segm([1, 1, 1, 1, 1, 1], 2)
        [[1, 1], [1, 1], [1, 1]]
    '''
    return [arr[x:x+n] for x in range(0, len(arr), n)]

def flt2d(arr: list[list]) -> list:
    '''
    Flatten a list of lists into a single list. Only for 2d lists, because the inner items should not be flattened.
    
    Parameters:
        arr (list): The list of lists to be flattened.
        
    Returns:
        list: The resulting flattened list.
        
    Example:
        >>> flt([[(), ()], [(), ()]])
        [(), (), (), (), (), ()]
    '''
    return [y for x in arr for y in x]

def overlp(l1: list, l2: list) -> bool:
    '''
    Checks if elements in l1 and l2 share any same elements

    Parameters:
        l1 (list): a list of elements
        l2 (list): a list of elements

    Returns:
        bool: if there are any overlaps between l1 and l2
    '''
    return bool(set(l1) & set(l2))