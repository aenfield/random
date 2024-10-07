from more_itertools import split_after

def split_at_pointcycle(rolls):
    """
    Returns the first point cycle in the list - [2], [3], [7], [11], [12], or a multi-element list where the first 
    item is the point and the rest are until the point again or seven - and then the remainder of the list.
    """
    come_out = rolls[0] 

    if come_out in [2, 3, 7, 11, 12]:
        return [come_out], rolls[1:]
    
    point = come_out
    split = list(split_after(rolls[1:], 
                             lambda r: r == 7 or r == point,
                             maxsplit=1))
    pc = [point] + split[0]
    rest = [] if len(split) == 1 else split[1]
    return pc, rest
    


