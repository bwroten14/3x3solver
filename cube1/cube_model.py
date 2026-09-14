# edge orientation and corner orientation:
# should be 0/1 for edges 0/1/2 for corners

from copy import deepcopy

CORNER_NAMES = ["URF", "UFL", "ULB", "UBR", "DFR", "DLF", "DBL", "DRB"]
EDGE_NAMES = ["UR", "UF", "UL", "UB", "DR", "DF", "DL", "DB", "FR", "FL", "BL", "BR"]

FACES = ["U", "R", "F", "D", "L", "B"]


class cubereal:
    __slots__ = ("cp", "co", "ep", "eo")

    def __init__(self, cp=None, co=None, ep=None, eo=None):
        self.cp = list(cp) if cp is not None else list(range(8))
        self.co = list(co) if co is not None else [0] * 8
        self.ep = list(ep) if ep is not None else list(range(12))
        self.eo = list(eo) if eo is not None else [0] * 12

    def copy(self):
        return cubereal(self.cp, self.co, self.ep, self.eo)

    def is_solved(self):
        return (self.cp == list(range(8)) and self.co == [0] * 8 and
                self.ep == list(range(12)) and self.eo == [0] * 12)

    def __eq__(self, other):
        return (self.cp == other.cp and self.co == other.co and
                self.ep == other.ep and self.eo == other.eo)


    #adds move to cube (cube meaning most fully updataed cube)
    def corner_multiply(self, b):
        cp = [0] * 8
        co = [0] * 8
        for i in range(8):
            cp[i] = self.cp[b.cp[i]]
            co[i] = (self.co[b.cp[i]] + b.co[i]) % 3
        self.cp, self.co = cp, co

    def edge_multiply(self, b):
        ep = [0] * 12
        eo = [0] * 12
        for i in range(12):
            ep[i] = self.ep[b.ep[i]]
            eo[i] = (self.eo[b.ep[i]] + b.eo[i]) % 2
        self.ep, self.eo = ep, eo

    def multiply(self, b):
        self.corner_multiply(b)
        self.edge_multiply(b)

    def apply_move(self, move_cube):
        result = self.copy()
        result.multiply(move_cube)
        return result



#move defs
#might be more tedious than cuberep
#CHECK THIS LATER
_BASIC = {
    "U": cubereal(
        cp=[3, 0, 1, 2, 4, 5, 6, 7],
        co=[0, 0, 0, 0, 0, 0, 0, 0],
        ep=[3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
        eo=[0] * 12,
    ),
    "D": cubereal(
        cp=[0, 1, 2, 3, 5, 6, 7, 4],
        co=[0, 0, 0, 0, 0, 0, 0, 0],
        ep=[0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11],
        eo=[0] * 12,
    ),
    "R": cubereal(
        cp=[4, 1, 2, 0, 7, 5, 6, 3],
        co=[2, 0, 0, 1, 1, 0, 0, 2],
        ep=[8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0],
        eo=[0] * 12,
    ),
    "L": cubereal(
        cp=[0, 2, 6, 3, 4, 1, 5, 7],
        co=[0, 1, 2, 0, 0, 2, 1, 0],
        ep=[0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11],
        eo=[0] * 12,
    ),
    "F": cubereal(
        cp=[1, 5, 2, 3, 0, 4, 6, 7],
        co=[1, 2, 0, 0, 2, 1, 0, 0],
        ep=[0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11],
        eo=[0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
    ),
    "B": cubereal(
        cp=[0, 1, 3, 7, 4, 5, 2, 6],
        co=[0, 0, 1, 2, 0, 0, 2, 1],
        ep=[0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7],
        eo=[0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    ),
}

MOVE_NAMES = []     
MOVES = {}                

for face in FACES:
    m1 = _BASIC[face]
    m2 = m1.copy(); m2.multiply(m1)          
    m3 = m2.copy(); m3.multiply(m1)          
    MOVES[face] = m1
    MOVES[face + "2"] = m2
    MOVES[face + "'"] = m3
    MOVE_NAMES.extend([face, face + "2", face + "'"])

#DR moves might need later

PHASE2_MOVE_NAMES = ["U", "U2", "U'", "D", "D2", "D'", "R2", "L2", "F2", "B2"]

#HTR moves

PHASE2real_MOVE_NAMES = ["U2", "D2", "R2", "L2", "F2", "B2"]


#implement moves on cube for real
def apply_sequence(cube, move_names):
    for name in move_names:
        cube = cube.apply_move(MOVES[name])
    return cube


def inverse_move_name(name):
    if name.endswith("2"):
        return name
    if name.endswith("'"):
        return name[0]
    return name + "'"

def scramble_to_cube(move_names):
    cube = cubereal()
    return apply_sequence(cube, move_names)

