
# worlds most tedious part
# leaving this here but i dont really need it i have a cube
"""
           U0 U1 U2
           U3 U4 U5
           U6 U7 U8
 L0 L1 L2  F0 F1 F2  R0 R1 R2  B0 B1 B2
 L3 L4 L5  F3 F4 F5  R3 R4 R5  B3 B4 B5
 L6 L7 L8  F6 F7 F8  R6 R7 R8  B6 B7 B8
           D0 D1 D2
           D3 D4 D5
           D6 D7 D8
"""
#Face offsets: U=0, R=9, F=18, D=27, L=36, B=45


U, R, F, D, L, B = 0, 9, 18, 27, 36, 45
FACE_LETTERS = "URFDLB"


#UGHHHHHH typing maxxing

CORNER_FACELETS = [
    (U + 8, R + 0, F + 2),   # URF
    (U + 6, F + 0, L + 2),   # UFL
    (U + 0, L + 0, B + 2),   # ULB
    (U + 2, B + 0, R + 2),   # UBR
    (D + 2, F + 8, R + 6),   # DFR
    (D + 0, L + 8, F + 6),   # DLF
    (D + 6, B + 8, L + 6),   # DBL
    (D + 8, R + 8, B + 6),   # DRB
]

# check this again later

EDGE_FACELETS = [
    (U + 5, R + 1),   # UR
    (U + 7, F + 1),   # UF
    (U + 3, L + 1),   # UL
    (U + 1, B + 1),   # UB
    (D + 5, R + 7),   # DR
    (D + 1, F + 7),   # DF
    (D + 3, L + 7),   # DL
    (D + 7, B + 7),   # DB
    (F + 5, R + 3),   # FR
    (F + 3, L + 5),   # FL
    (B + 5, L + 3),   # BL
    (B + 3, R + 5),   # BR
]


CORNER_COLORS = [
    ("U", "R", "F"), ("U", "F", "L"), ("U", "L", "B"), ("U", "B", "R"),
    ("D", "F", "R"), ("D", "L", "F"), ("D", "B", "L"), ("D", "R", "B"),
]
EDGE_COLORS = [
    ("U", "R"), ("U", "F"), ("U", "L"), ("U", "B"),
    ("D", "R"), ("D", "F"), ("D", "L"), ("D", "B"),
    ("F", "R"), ("F", "L"), ("B", "L"), ("B", "R"),
]


def cubie_to_facelets(cube):
    facelets = [None] * 54
    for f in range(6):
        for i in range(9):
            facelets[f * 9 + i] = FACE_LETTERS[f]

    for slot in range(8):
        cubie = cube.cp[slot]
        o = cube.co[slot]
        positions = CORNER_FACELETS[slot]
        colors = CORNER_COLORS[cubie]
        for k in range(3):
            facelets[positions[k]] = colors[(k - o) % 3]

    for slot in range(12):
        cubie = cube.ep[slot]
        o = cube.eo[slot]
        positions = EDGE_FACELETS[slot]
        colors = EDGE_COLORS[cubie]
        for k in range(2):
            facelets[positions[k]] = colors[(k - o) % 2]

    return facelets


def print_cube(cube):
    f = cubie_to_facelets(cube)

    def row(face_offset, r):
        return " ".join(f[face_offset + r * 3 + c] for c in range(3))

    for r in range(3):
        print("      " + row(U, r))
    for r in range(3):
        print(f"{row(L, r)}  {row(F, r)}  {row(R, r)}  {row(B, r)}")
    for r in range(3):
        print("      " + row(D, r))
