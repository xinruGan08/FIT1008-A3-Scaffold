from landsites import Land
from data_structures.heap import MaxHeap
from data_structures.referential_array import ArrayR
from data_structures.hash_table import LinearProbeTable


class Mode2Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, n_teams: int) -> None:
        """
        Initialises the Mode2Navigator with the number of teams.
        :param n_teams: int: The number of teams.
        """
        self.n_teams = n_teams
        self.land_sites = []
        self.mapped_sites = LinearProbeTable()
        self.score_land_heap = MaxHeap(0)

    def add_sites(self, sites: list[Land]) -> None:
        """
        A method stores and adds land sites to the Mode2Navigator.
        :param sites: list[Land]: A list of land sites to add.

        :complexity: 
        Defining N = number of sites
        Defining S = length of input sites
        Worst Case = O(N + S):
        """
        self.land_sites.extend(sites)

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        A method to simulate a day of the game.
        :param adventurer_size: int: The number of adventurers for every team.
        :return: list[tuple[Land | None, int]]: A list of tuples containing the land site and the number of adventurers sent to the land site.

        :complexity:
        Defining N = number of sites
        Defining K = number of adventure teams participating in the game 
        Worst Case = O(N + KlogN):
        """
        # for loop for N -> data structure for mapping
        # for site in self.land_sites:
        #     if site.get_guardians() > 0:
        #         score,_,_ = self.compute_score(adventurer_size,site)
        #         self.mapped_sites[str(score)] = site
            # score,_,_ = self.compute_score(adventurer_size,site)
            # self.mapped_sites[str(score)] = site
        # for loop for K and invoke getMAX()
        self.construct_score_data_structure(adventurer_size)
        return_list = []

        for _ in range(self.n_teams):
            try:
               max_score = self.score_land_heap.get_max() #may occur nothing to plunder
               not_sending_score = 2.5 * adventurer_size
               best_case = max(max_score,not_sending_score)

               land_site = self.mapped_sites[str(best_case)] #do nothing is better
               score, remaining_adventures, reward = self.compute_score(adventurer_size, land_site)
               
               sent_adventurers = adventurer_size - remaining_adventures
               land_site.set_guardians(land_site.get_guardians() - sent_adventurers)
               land_site.set_gold(land_site.get_gold() - reward)
               if land_site.get_guardians() > 0:
                    new_score,_,_ = self.compute_score(adventurer_size,land_site)
                    self.score_land_heap.add(new_score)
                    del self.mapped_sites[str(score)]
                    self.mapped_sites[str(new_score)] = land_site
            #    not_sending_score = 2.5 * adventurer_size
            except (IndexError,KeyError):
                land_site = None
                sent_adventurers = 0
            return_list.append((land_site,sent_adventurers))
        return return_list

        #        if not_sending_score > score:
        #            self.score_land_heap.add(land_site)
        #            score = not_sending_score
        #            remaining_adventures = adventurer_size
        #            sent_adventurers = 0
        #        else:
        #         sent_adventurers = adventurer_size - remaining_adventures
        #         print(i,land_site.get_name(),adventurer_size - remaining_adventures, score)
        #    except IndexError:
        #        land_site = None
        #        sent_adventurers = 0
        #        score, remaining_adventures, reward = self.compute_score(adventurer_size, land_site)
        #        print(i,score)
           
        return return_list

        
    def compute_score(self,adventures: int, site: Land = None) -> tuple[int, float,int]:
        """
        A method to compute the maximum score of a land site, based on the number of adventures.
        :param site: Land: The land site to compute the score for.
        :param sent_adventurers: int: The number of adventurers sent to the land site.

        :return: tuple[int, float]: 
        int: The remaining adventurers 
        float: The amount of gold received.

        :complexity:
        Best Case = Worst Case = O(1), only performing simple arithmetic operations with some if conditions.
        """
        reward = 0
        if site == None:
            sent_adventures = 0
            remaining_adventures = adventures
            score = 2.5 * adventures + reward
            return (2.5 * adventures, adventures, reward)
    
        sent_adventures = site.get_guardians() if site.get_guardians() <= adventures else adventures
        remaining_adventures = adventures - sent_adventures
        reward = min(sent_adventures*site.get_gold()/site.get_guardians(),site.get_gold())
        score = 2.5 * remaining_adventures + reward
        return (score,remaining_adventures, reward)
    
    def construct_score_data_structure(self,adventures_sizes: int) -> None:
        """
        Student-TODO: Best/Worst Case
        A method to construct the appropriate data structure(s) to organize the scores of all the land sites, and their relationships to all the land sites (sites).
        :param adventures_sizes: int: The number of adventurers for every team.

        """
        score_land_heap = MaxHeap(len(self.land_sites))
        for site in self.land_sites:
            if site.get_guardians() > 0:
                score,_,_ = self.compute_score(adventures_sizes,site)
                score_land_heap.add(score)
                self.mapped_sites[str(score)] = site
        self.score_land_heap = score_land_heap

        # for site in self.land_sites:
        #     if site.get_guardians() > 0:
        #         score,_,_ = self.compute_score(adventurer_size,site)
        #         self.mapped_sites[str(score)] = site
        
