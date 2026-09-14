
import time
from cube_model import cubereal, MOVES, MOVE_NAMES, PHASE2_MOVE_NAMES, scramble_to_cube
import coordinates as C

N_TWIST, N_FLIP, N_SLICE = 2187, 2048, 495
N_CPERM, N_EPERM8, N_SPERM4 = 40320, 40320, 24




# make tables or smth
# idk if bfs is actually better so imma leave this here so im reminded to check dfs

def _bfs_prune(n_states, n_moves, combine_next, start=0):
    dist = [-1] * n_states
    dist[start] = 0
    frontier = [start]
    d = 0
    while frontier:
        d += 1
        nxt = []
        for s in frontier:
            for mi in range(n_moves):
                ns = combine_next(s, mi)
                if dist[ns] == -1:
                    dist[ns] = d
                    nxt.append(ns)
        frontier = nxt
    return dist


#takes forver part
class Tables:

    def __init__(self, verbose=False):
        t0 = time.time()
        self.twist_tab = C.build_twist_table()
        self.flip_tab = C.build_flip_table()
        self.slice_tab = C.build_slice_table()
        self.cperm_tab = C.build_corner_perm_table()
        self.eperm8_tab = C.build_edge_perm8_table()
        self.sperm4_tab = C.build_slice_perm4_table()
        if verbose:
            print(f"move tables built in {time.time()-t0:.2f}s")

        t0 = time.time()
        # Get domino
        n1 = N_TWIST * N_SLICE

        def next1a(s, mi):
            tw, sl = divmod(s, N_SLICE)
            return self.twist_tab[tw][mi] * N_SLICE + self.slice_tab[sl][mi]

        self.prune_twist_slice = _bfs_prune(n1, 18, next1a)

        n1b = N_FLIP * N_SLICE

        def next1b(s, mi):
            fl, sl = divmod(s, N_SLICE)
            return self.flip_tab[fl][mi] * N_SLICE + self.slice_tab[sl][mi]

        self.prune_flip_slice = _bfs_prune(n1b, 18, next1b)
        if verbose:
            print(f"phase1 pruning tables built in {time.time()-t0:.2f}s")

        t0 = time.time()
        # get htr
        n2 = N_CPERM * N_SPERM4

        def next2a(s, mi):
            cp, sp = divmod(s, N_SPERM4)
            return self.cperm_tab[cp][mi] * N_SPERM4 + self.sperm4_tab[sp][mi]

        self.prune_cperm_sperm = _bfs_prune(n2, 10, next2a)

        n2b = N_EPERM8 * N_SPERM4

        def next2b(s, mi):
            ep, sp = divmod(s, N_SPERM4)
            return self.eperm8_tab[ep][mi] * N_SPERM4 + self.sperm4_tab[sp][mi]

        self.prune_eperm_sperm = _bfs_prune(n2b, 10, next2b)
        if verbose:
            print(f"phase2 pruning tables built in {time.time()-t0:.2f}s")

    # kociemba jjust says this is better idk (lowk dont get it that well)
    def phase1_heuristic(self, twist, flip, slice_):
        a = self.prune_twist_slice[twist * N_SLICE + slice_]
        b = self.prune_flip_slice[flip * N_SLICE + slice_]
        return max(a, b)

    def phase2_heuristic(self, cperm, eperm8, sperm4):
        a = self.prune_cperm_sperm[cperm * N_SPERM4 + sperm4]
        b = self.prune_eperm_sperm[eperm8 * N_SPERM4 + sperm4]
        return max(a, b)


def _face_of(move_name):
    return move_name[0]


def solve_phase1(cube, tables, max_len=12):
    twist = C.get_twist(cube)
    flip = C.get_flip(cube)
    slice_ = C.get_slice(cube)
    path = []

    def dfs(twist, flip, slice_, g, last_face, threshold):
        h = tables.phase1_heuristic(twist, flip, slice_)
        if h == 0:
            return True
        if g + h > threshold:
            return False
        for mi, name in enumerate(MOVE_NAMES):
            face = _face_of(name)
            if face == last_face:
                continue 
            nt = tables.twist_tab[twist][mi]
            nf = tables.flip_tab[flip][mi]
            ns = tables.slice_tab[slice_][mi]
            path.append(name)
            if dfs(nt, nf, ns, g + 1, face, threshold):
                return True
            path.pop()
        return False

    threshold = tables.phase1_heuristic(twist, flip, slice_)
    while threshold <= max_len:
        if dfs(twist, flip, slice_, 0, None, threshold):
            return path[:]
        threshold += 1
    return None # so hopefully this doesnt happen (i dont think its possible)

def solve_phase2(cube, tables, max_len=18):
    cperm = C.get_corner_perm(cube)
    eperm8 = C.get_edge_perm8(cube)
    sperm4 = C.get_slice_perm4(cube)
    path = []

    def dfs(cperm, eperm8, sperm4, g, last_face, threshold):
        h = tables.phase2_heuristic(cperm, eperm8, sperm4)
        if h == 0:
            return True
        if g + h > threshold:
            return False
        for mi, name in enumerate(PHASE2_MOVE_NAMES):
            face = _face_of(name)
            if face == last_face:
                continue
            nc = tables.cperm_tab[cperm][mi]
            ne = tables.eperm8_tab[eperm8][mi]
            ns = tables.sperm4_tab[sperm4][mi]
            path.append(name)
            if dfs(nc, ne, ns, g + 1, face, threshold):
                return True
            path.pop()
        return False

    threshold = tables.phase2_heuristic(cperm, eperm8, sperm4)
    while threshold <= max_len:
        if dfs(cperm, eperm8, sperm4, 0, None, threshold):
            return path[:]
        threshold += 1
    return None


def solve(cube, tables, phase1_max=12, phase2_max=18):
    p1 = solve_phase1(cube, tables, max_len=phase1_max)
    if p1 is None:
        raise RuntimeError("DR search didn't work lol")
    mid_cube = cube
    for name in p1:
        mid_cube = mid_cube.apply_move(MOVES[name])
    p2 = solve_phase2(mid_cube, tables, max_len=phase2_max)
    if p2 is None:
        raise RuntimeError("HTR search failed try inputting a possible cubestate next time bruh")
    return p1 + p2


def solve_scramble(scramble_move_names, tables):
    cube = scramble_to_cube(scramble_move_names)
    return solve(cube, tables)

#that took a while hope it works

