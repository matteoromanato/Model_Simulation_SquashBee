
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from collections import defaultdict
from agents import Bee, Bee_son, Zucca_seed, Zucca_flower, Zucca


class SquashBee(Model):
    def __init__ (self, height=50, width=50, time = 0, density_bee = 50, density_gender_bee = 50,  gain_polline_raccolto = 40, density_zucca = 50, prob_accoppiamento = 50, prob_semina = 50):
        
        self.height = height
        self.width = width
        self.time = time
        self.density_bee = density_bee
        self.density_gender_bee = density_gender_bee
        self.gain_polline_raccolto = gain_polline_raccolto
        self.density_zucca = density_zucca
        self.prob_accoppiamento = prob_accoppiamento
        self.prob_semina = prob_semina


        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)

       
        self.datacollector = DataCollector(
            {"Zucche_fiori": lambda m: self.count_type(m, "Flower"),
             "Zucche": lambda m: self.count_type(m, "Zucca"),
             "Seed": lambda m: self.count_type(m, "Seed"),
             "Api": lambda m: self.count_type(m, "Bee"),
             "Larve": lambda m: self.count_type(m, "Bee_son")
            })

        # metto le api nella griglia 
        for i in range(self.density_bee):   
            x = self.random.randrange(self.width)       
            y = self.random.randrange(self.height)
            new_bee = Bee((x, y), self, self.density_gender_bee, self.gain_polline_raccolto)
            self.grid.place_agent(new_bee, (x, y))
            self.schedule.add(new_bee)

        # metto i fiori delle zucche nella griglia
        for i in range(self.density_zucca):   
            x = self.random.randrange(self.width)       
            y = self.random.randrange(self.height)
            new_zucca = Zucca_flower((x,y), self, self.prob_accoppiamento)
            self.grid._place_agent((x,y), new_zucca)
            self.schedule.add(new_zucca)

        self.running = True
        self.datacollector.collect(self)

    

    def step(self):
        self.time += 1
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        

    @staticmethod
    def count_type(model, agent_type):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for agent in model.schedule.agents:
            if agent.type_agent == agent_type:
                count += 1
        return count  

    