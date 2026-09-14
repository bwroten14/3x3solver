# for API purposes 


"""
    engine = SolverEngine()                 # builds move + pruning tables once
    cube   = engine.cube_from_scramble(["R", "U", "F'", ...])
    moves  = engine.solve(cube)             # -> list of move names
    engine.print_cube(cube)                 # ASCII net view
"""


import pickle
import os
import time

from cube_model import (
    cubereal, MOVES, MOVE_NAMES, PHASE2_MOVE_NAMES,
    apply_sequence, scramble_to_cube, inverse_move_name,
)
from solver import Tables, solve, solve_phase1, solve_phase2
from facelets import cubie_to_facelets, print_cube
import coordinates as C


class SolverEngine:
    #this gonna take a while
    #should store tables in file once ran 
    #(never done that before so might be slow all the time)

    CACHE_FILE = os.path.join(os.path.dirname(__file__), "tables.pkl")

    def __init__(self, use_cache=True, verbose=False):
        if use_cache and os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "rb") as fh:
                self.tables = pickle.load(fh)
            if verbose:
                print("loaded pruning tables from cache")
        else:
            self.tables = Tables(verbose=verbose)
            if use_cache:
                with open(self.CACHE_FILE, "wb") as fh:
                    pickle.dump(self.tables, fh)

    def solved_cube(self):
        return cubereal()

    def cube_from_scramble(self, move_names):
        return scramble_to_cube(move_names)


    def solve(self, cube, phase1_max=12, phase2_max=18):
    #actual sol
        return solve(cube, self.tables, phase1_max=phase1_max, phase2_max=phase2_max)

    def solve_scramble(self, move_names):
        cube = self.cube_from_scramble(move_names)
        return self.solve(cube)


    def is_solved(self, cube):
        return cube.is_solved()

    def facelets(self, cube):
        return cubie_to_facelets(cube)

    def print_cube(self, cube):
        print_cube(cube)

    def apply(self, cube, move_names):
        return apply_sequence(cube, move_names)


if __name__ == "__main__":
    engine = SolverEngine(use_cache=True, verbose=True)

    scramble = input("enter scramble: ").split()
    print("\nScramble:", " ".join(scramble))

    cube = engine.cube_from_scramble(scramble)
    print("\nScrambled cube:")
    engine.print_cube(cube)

    t0 = time.time()
    solution = engine.solve(cube)
    dt = time.time() - t0

    print(f"\nSolution ({len(solution)} moves, solved in {dt:.3f}s):")
    print(" ".join(solution))

    solved_cube = engine.apply(cube, solution)
    print("\nVerified solved:", engine.is_solved(solved_cube))
