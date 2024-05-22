from landsites import Land
from data_structures.bst import BinarySearchTree, BSTPostOrderIterator,BSTInOrderIterator,BSTPreOrderIterator
from data_structures.heap import MaxHeap

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        site_storage = BinarySearchTree()
        for site in sites:
            site_storage[-1 * site.get_gold()/site.get_guardians()] = site
        self.sites = site_storage
        self.adventurers = adventurers

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        return_list = []
        remaining_adventures = self.adventurers
        for land in BSTInOrderIterator(self.sites.root):
            land = land.item
            if land.get_guardians() > 0 and remaining_adventures > 0:
                sent_guardians = land.get_guardians() if land.get_guardians() < remaining_adventures else remaining_adventures
                remaining_adventures -= sent_guardians
                return_list.append((land,sent_guardians))
        return return_list

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Student-TODO: Best/Worst Case
        """
        original_adventures = self.adventurers
        return_list = []
        for number in adventure_numbers:
            self.adventurers = number
            reward = 0
            for site, adventurers_sent in self.select_sites():
                reward += min(adventurers_sent*site.get_gold()/site.get_guardians(),site.get_gold())
            return_list.append(reward)
        self.adventurers = original_adventures
        return return_list


    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        land.set_gold(new_reward)
        land.set_guardians(new_guardians)
