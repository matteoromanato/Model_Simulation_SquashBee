
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from collections import defaultdict
from agents import *


class SquashBee(Model):
    def __init__ (self, height=50, width=50, time = 0, density_bee = 50, density_gender_bee = 50,  gain_polline_raccolto = 40, density_zucca = 50, prob_accoppiamento = 50, offsetX = 5, offsetY = 5):
        
        self.height = height
        self.width = width
        self.time = 200
        self.density_bee = density_bee
        self.density_gender_bee = density_gender_bee
        self.gain_polline_raccolto = gain_polline_raccolto
        self.density_zucca = density_zucca
        self.prob_accoppiamento = prob_accoppiamento
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.anno = 1


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
            x = self.random.randrange(2,33)       
            y = self.random.randrange(2,33)
            new_bee = Bee((x, y), self, self.density_gender_bee, self.gain_polline_raccolto)
            self.grid.place_agent(new_bee, (x, y))
            self.schedule.add(new_bee)

        # metto i fiori delle zucche nella griglia
        for i in range(self.density_zucca):   
            x = self.random.randrange(5,30)       
            y = self.random.randrange(5,30)
            new_zucca = Zucca_flower((x,y), self, self.prob_accoppiamento, 45)
            self.grid._place_agent((x,y), new_zucca)
            self.schedule.add(new_zucca)
        
        # metto i fiori nella griglia
        for i in range(150):   
            x = self.random.randrange(self.height)       
            y = self.random.randrange(self.width)
            new_f = flower((x,y), self)
            self.grid._place_agent((x,y), new_f)
            self.schedule.add(new_f)

        self.running = True
        self.datacollector.collect(self)

    

    def step(self):
        self.time += 1

        #fioritura primaverile
        if self.time == 90:
            # metto i fiori nella griglia
            for i in range(150):   
                x = self.random.randrange(self.height)       
                y = self.random.randrange(self.width)
                new_f = flower((x,y), self)
                self.grid._place_agent((x,y), new_f)
                self.schedule.add(new_f)

        # semina ogni anno
        if self.time == 160:
            # metto i fiori delle zucche nella griglia
            if self.anno%2 == 0:
                for i in range(self.density_zucca):   
                    x = self.random.randrange(5 + self.offsetX,30 + self.offsetX)       
                    y = self.random.randrange(5 + self.offsetY,30 + self.offsetY)
                    new_seme = Zucca_seed((x,y), self)
                    self.grid._place_agent((x,y), new_seme)
                    self.schedule.add(new_seme)
            if self.anno%2 == 1:
                for i in range(self.density_zucca):   
                    x = self.random.randrange(5,30)       
                    y = self.random.randrange(5,30)
                    new_seme = Zucca_seed((x,y), self)
                    self.grid._place_agent((x,y), new_seme)
                    self.schedule.add(new_seme)


        # reset anno
        if self.time == 360:
            self.time = 0
            self.anno += 1




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

    