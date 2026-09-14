#coord representations
#goal is to get all 3 to 0
#means cube is in DR, HTR, then solved

from cube_model import cubereal, MOVES, MOVE_NAMES, PHASE2_MOVE_NAMES


def _binomial(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r = r * (n - i) // (i + 1)
    return r


def perm_to_index(perm):
    #lehmer
    perm = list(perm)
    n = len(perm)
    idx = 0
    for i in range(n):
        smaller = 0
        for j in range(i + 1, n):
            if perm[j] < perm[i]:
                smaller += 1
        idx = idx * (n - i) + smaller
    return idx


def index_to_perm(idx, n):
    elems = list(range(n))
    perm = []
    for i in range(n, 0, -1):
        f = 1
        for k in range(1, i):
            f *= k
        pos, idx = divmod(idx, f)
        perm.append(elems.pop(pos))
    return perm


# twist

def get_twist(cube):
    v = 0
    for i in range(7):
        v = v * 3 + cube.co[i]
    return v


def set_twist(cube, twist):
    total = 0
    co = [0] * 8
    for i in range(6, -1, -1):
        co[i] = twist % 3
        total += co[i]
        twist //= 3
    co[7] = (3 - total % 3) % 3
    cube.co = co


# flip

def get_flip(cube):
    v = 0
    for i in range(11):
        v = v * 2 + cube.eo[i]
    return v


def set_flip(cube, flip):
    total = 0
    eo = [0] * 12
    for i in range(10, -1, -1):
        eo[i] = flip % 2
        total += eo[i]
        flip //= 2
    eo[11] = (2 - total % 2) % 2
    cube.eo = eo




def get_slice(cube):
    occupied = [1 if cube.ep[i] >= 8 else 0 for i in range(12)]
    idx = 0
    x = 0  # number of slice edges seen so far while scanning i = 11..0
    for i in range(11, -1, -1):
        if occupied[i]:
            idx += _binomial(11 - i, x + 1)
            x += 1
    return idx


import itertools as _itertools


def _build_slice_lookup():
    lookup = [None] * 495
    tmp = cubereal()
    for combo in _itertools.combinations(range(12), 4):
        ep = [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0]
        #placeholder
        others = iter(range(8))
        full = [None] * 12
        oi = 0
        for i in range(12):
            if i in combo:
                full[i] = 8 
            else:
                full[i] = 0  
        tmp.ep = full
        idx = get_slice(tmp)
        lookup[idx] = combo
    return lookup


_SLICE_LOOKUP = _build_slice_lookup()


def set_slice(cube, slice_idx, ep_slice_ids=(8, 9, 10, 11), ep_other_ids=(0, 1, 2, 3, 4, 5, 6, 7)):
    #Place slice-edge ids into 4 of the 12 slots according to slice_idx, other ids fill remaining slots in order
    combo = set(_SLICE_LOOKUP[slice_idx])
    ep = [None] * 12
    si = 0
    oi = 0
    for i in range(12):
        if i in combo:
            ep[i] = ep_slice_ids[si]; si += 1
        else:
            ep[i] = ep_other_ids[oi]; oi += 1
    cube.ep = ep


#HTR coords

def get_corner_perm(cube):
    return perm_to_index(cube.cp)


def set_corner_perm(cube, idx):
    cube.cp = index_to_perm(idx, 8)


def get_edge_perm8(cube):
    #perm of non E slice edges
    return perm_to_index(cube.ep[0:8])


def set_edge_perm8(cube, idx):
    p = index_to_perm(idx, 8)
    cube.ep = p + cube.ep[8:12]


def get_slice_perm4(cube):
    #perm of E slice edges
    rel = [cube.ep[i] - 8 for i in range(8, 12)]
    return perm_to_index(rel)


def set_slice_perm4(cube, idx):
    rel = index_to_perm(idx, 4)
    cube.ep = cube.ep[0:8] + [x + 8 for x in rel]



def _build_move_table(n_states, set_fn, get_fn, move_names, apply_fn):
    table = [[0] * len(move_names) for _ in range(n_states)]
    for s in range(n_states):
        base = cubereal()
        set_fn(base, s)
        for mi, name in enumerate(move_names):
            nxt = apply_fn(base, MOVES[name])
            table[s][mi] = get_fn(nxt)
    return table


def build_twist_table(move_names=MOVE_NAMES):
    return _build_move_table(2187, set_twist, get_twist, move_names,
                              lambda c, m: c.apply_move(m))


def build_flip_table(move_names=MOVE_NAMES):
    return _build_move_table(2048, set_flip, get_flip, move_names,
                              lambda c, m: c.apply_move(m))


def build_slice_table(move_names=MOVE_NAMES):
    return _build_move_table(495, set_slice, get_slice, move_names,
                              lambda c, m: c.apply_move(m))


def build_corner_perm_table(move_names=PHASE2_MOVE_NAMES):
    return _build_move_table(40320, set_corner_perm, get_corner_perm, move_names,
                              lambda c, m: c.apply_move(m))


def build_edge_perm8_table(move_names=PHASE2_MOVE_NAMES):
    return _build_move_table(40320, set_edge_perm8, get_edge_perm8, move_names,
                              lambda c, m: c.apply_move(m))


def build_slice_perm4_table(move_names=PHASE2_MOVE_NAMES):
    return _build_move_table(24, set_slice_perm4, get_slice_perm4, move_names,
                              lambda c, m: c.apply_move(m))
