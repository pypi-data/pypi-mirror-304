from __future__ import annotations
from tqdm import tqdm
import random
import copy
from catpynet.algorithm.MaxRAFAlgorithm import MaxRAFAlgorithm
from catpynet.algorithm.AlgorithmBase import AlgorithmBase
from catpynet.model.ReactionSystem import ReactionSystem

import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class MinIRAFHeuristic(AlgorithmBase):

    NAME: str = "iRAF"
    NUMBER_OF_RANDOM_INSERTION_ORDERS: int

    @property
    def number_of_random_insertion_orders(self):
        return self.NUMBER_OF_RANDOM_INSERTION_ORDERS

    @number_of_random_insertion_orders.setter
    def number_of_random_insertion_orders(self, value: int):
        self.NUMBER_OF_RANDOM_INSERTION_ORDERS = value

    @property
    def name(self):
        return self.NAME

    @name.setter
    def name(self, value: str):
        self.NAME = value

    @property
    def description(self):
        return "searches for irreducible RAFs in a heuristic fashion"

    def apply(self, input: ReactionSystem) -> ReactionSystem | None:
        """returns one of the smallest reaction systems possible produced by RAF

        Args:
            input (ReactionSystem): reaction system to be computed

        Returns:
            list[ReactionSystem]: reaction systems which are minimal
        """
        list = self.apply_all_smallest(input)
        if list:
            return list[0]
        else:
            return ReactionSystem()

    def apply_all_smallest(self, input: ReactionSystem) -> list[ReactionSystem]:
        """returns a list of the smallest reaction systems 

        Args:
            input (ReactionSystem): reaction system to be computed

        Returns:
            list[ReactionSystem]: reaction systems which are minimal
        """
        
        max_raf = MaxRAFAlgorithm().apply(input)
        
        try:
            isinstance(self.number_of_random_insertion_orders, int)
        except:
            self.number_of_random_insertion_orders = 10
        seeds = [
            i*123 for i in range(0, self.number_of_random_insertion_orders)]

        best: list[ReactionSystem] = []
        best_size = max_raf.size

        for seed in tqdm(seeds, desc="MinIRafHeuristic seeds: "):
            
            work_system = ReactionSystem(self.name)
            work_system.reactions = max_raf.reactions.copy()
            work_system.foods.update(max_raf.foods)
            ordering = max_raf.reactions.copy()
            random.Random(seed).shuffle(ordering)
            
            for reaction in ordering:
                try: work_system.reactions.remove(reaction)
                except: pass
                next = MaxRAFAlgorithm().apply(work_system)
                next.name = self.name
                if next.size > 0 and next.size <= work_system.size:
                    work_system = next
                    if next.size < best_size:
                        best.clear()
                        best_size = next.size
                    if (next.size == best_size 
                        and not any([set(next.reactions) == set(a.reactions) 
                                     for a in best])):
                        best.append(next)
                    if best_size == 1:
                        break
                else:
                    work_system.reactions.append(reaction)
                
        if not best:
            result = copy.copy(max_raf)
            result.name = self.name
            best.append(result)

        return best
