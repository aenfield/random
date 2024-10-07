from craps import craps

def test_split_at_pointcycle_initial_seven_and_eleven():
    pc, rest = craps.split_at_pointcycle([7, 2, 3])
    assert pc == [7]
    assert rest == [2, 3]

    pc, rest = craps.split_at_pointcycle([11, 2, 3])
    assert pc == [11]
    assert rest == [2, 3]

def test_split_at_pointcycle_craps():
    pc, rest = craps.split_at_pointcycle([2, 2, 3])
    assert pc == [2]
    assert rest == [2, 3]

    pc, rest = craps.split_at_pointcycle([3, 2, 3])
    assert pc == [3]
    assert rest == [2, 3]

    pc, rest = craps.split_at_pointcycle([12, 2, 3])
    assert pc == [12]
    assert rest == [2, 3]

def test_split_at_pointcycle_point_immediately():
    pc, rest = craps.split_at_pointcycle([4, 4, 12])
    assert pc == [4, 4]
    assert rest == [12]

def test_split_at_pointcycle_point_afterafew():
    pc, rest = craps.split_at_pointcycle([4, 8, 6, 4, 12, 11])
    assert pc == [4, 8, 6, 4]
    assert rest == [12, 11]

def test_split_at_pointcycle_sevenout():
    pc, rest = craps.split_at_pointcycle([4, 8, 7, 9, 10, 11])
    assert pc == [4, 8, 7]
    assert rest == [9, 10, 11]

def test_split_at_pointcycle_nothingattheend():
    pc, rest = craps.split_at_pointcycle([4, 5, 4])
    assert pc == [4, 5, 4]
    assert rest == []

def test_split_at_pointcycle_nothingattheendsevenout():
    pc, rest = craps.split_at_pointcycle([4, 5, 7])
    assert pc == [4, 5, 7]
    assert rest == []
