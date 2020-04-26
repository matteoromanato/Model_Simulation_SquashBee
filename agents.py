from mesa import Agent
from random import *

class Bee(Agent):
   
    def __init__(self,pos,model, density_gender, gain_polline):

        super().__init__(pos,model)
        self.pos = pos
        self.type_agent = "Bee"                                                     # tipo di agente per identificarlo
        self.time_life = randint(130,170)                                                        # un'ape vive per circa 150 giorni, ad ogni step toglieremo un punto vita
        self.qnt_polline_perc = 0                                                   # è la quantità di polline che può portare in percentuale e determinerà la probabilità che faccia fecondare un fiore
        self.gain_polline = gain_polline                                            # è l'energia che ottiene andando su un fiore e aumenterà il parametro energy
        self.energy = 100                                                           # energy è l'attributo che definisce l'energia rimanente dell'ape se energy = 0 l'ape non ha trovato abbastanza rifornimento e muore 
        
        num = random()*100
        if num < density_gender:                                                      # in base alla densità di generescelta dall'utente si creeranno api maschio o femmina
            self.gender = "Female"
            self.newSon = False
            #self.time_son = 5                                                       # tempo di "gravidanza" è ancora da capire come gestirlo bene
        else:
            self.gender = "Male"
        

    def step(self):
        # deve muoversi a caso alla ricerca di un fiore
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,radius = 2,include_center=False)
        new_position = self.random.choice(possible_steps)
        #if(self.model.grid.is_cell_empty(new_position)):
        self.model.grid.move_agent(self, new_position)

        # deve trovare e depositare la larva vicino ad una zucca
        if self.gender == "Female":
            if self.newSon == True:
               # self.time_son -= 1
               # if self.time_son < 0: # and self.time_son > -10:
                for neighbor in self.model.grid.neighbor_iter(self.pos):
                    if neighbor.type_agent == "Zucca":
                        possible_steps = self.model.grid.get_neighborhood(neighbor.pos,moore=True,include_center=False)
                        new_position = self.random.choice(possible_steps)
                        if(self.model.grid.is_cell_empty(new_position)):
                            new_larva = Bee_son(new_position, self.model)
                            self.model.grid.place_agent(new_larva, new_position)
                            self.model.schedule.add(new_larva)
                            #self.time_son = 5
                            self.newSon= False
                
        # se finisce il tempo allora muore e la rimuovo
        self.time_life -= 1
        self.energy -= 1
        if(self.energy == 0 or self.time_life == 0):
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        
               

class Bee_son(Agent):

    def __init__(self,pos,model):

        super().__init__(pos,model)
        self.pos = pos
        self.type_agent = "Bee_son"
        self.time_grow = randint(230,260)
        

    def step(self):
        self.time_grow -= 1
        if(self.time_grow == 0):
            posizione = self.pos
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            new_bee = Bee(posizione, self.model, self.model.density_gender_bee, self.model.gain_polline_raccolto)
            self.model.grid.place_agent(new_bee, posizione)
            self.model.schedule.add(new_bee)


      
       
class Zucca_seed(Agent):
   
    def __init__(self,pos,model):
        super().__init__(pos,model)
        self.pos = pos
        self.type_agent = "Seed"
        self.time_life = randint(10,20)

    def step(self):
        self.time_life -= 1
        if(self.time_life == 0):
            posizione = self.pos
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            # fingiamo che quando muore a zucca si pianta un seme
            new_flower = Zucca_flower(posizione, self.model, self.model.prob_accoppiamento,45)
            self.model.grid.place_agent(new_flower, posizione)
            self.model.schedule.add(new_flower)
        

class Zucca_flower(Agent):
   
    def __init__(self,pos,model, prob_accoppiamento, time):

        super().__init__(pos,model)
        self.pos = pos
        self.impollinato = False
        self.type_agent = "Flower"
        self.time_life = randint(time-20,time+20)          #inizialmente range(10,30) successivamente range(35,55)
        self.prob_accoppiamento = prob_accoppiamento
        
    
    def step(self):
        n_bee_m = 0
        n_bee_f = 0
        # se ha sopra un'ape potrebbe impollinarsi
        # se ha vicino due api potrebbero accoppiarsi
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type_agent == "Bee":
                if neighbor.gender == "Female":
                    n_bee_f +=1
                    femmina = neighbor
                if neighbor.gender == "Male":
                    n_bee_m +=1
                if n_bee_m > 0 and n_bee_f > 0:
                    num = random()*100 
                    if num < self.prob_accoppiamento:
                        femmina.newSon = True
                        #print("abbiamo un figlio")
                neighbor.qnt_polline_perc = neighbor.gain_polline
                neighbor.energy = neighbor.gain_polline
                num = random()*100 
                if num < neighbor.qnt_polline_perc:
                    self.impollinato = True
                    #print("sono impollinato")
        

        # se il tempo di vita finisce appassisce e muore
        # se è stato impollinato però si trasforma in zucca
        self.time_life -= 1
        if(self.time_life == 0):
            posizione = self.pos
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            if self.impollinato == True:
                new_zucca = Zucca(posizione, self.model)
                self.model.grid.place_agent(new_zucca, posizione)
                self.model.schedule.add(new_zucca)


class Zucca(Agent):


    def __init__(self,pos,model):

        super().__init__(pos,model)
        self.pos = pos
        self.type_agent = "Zucca"
        self.time_life = randint(40,60)

    def step(self):
        self.time_life -= 1
        if(self.time_life == 0):
            """
            #i=0
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                possible_steps = self.model.grid.get_neighborhood(neighbor.pos,moore=True,include_center=False)
                new_position = self.random.choice(possible_steps)
                
                if self.model.grid.is_cell_empty(new_position) and randint(1,100)<self.model.prob_semina:
                    new_seme = Zucca_seed(new_position, self.model)
                    self.model.grid._place_agent(new_position, new_seme)
                    self.model.schedule.add(new_seme)
                    #i+=1
                    #print("nuovi semi :" + str(i))
                """
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)    


class flower(Agent):
   
    def __init__(self,pos,model, ):

        super().__init__(pos,model)
        self.pos = pos
        self.type_agent = "Flower_Random"
        self.time_life = randint(90-10,90+10)          #inizialmente range(10,30) successivamente range(35,55)
        
        
    
    def step(self):

        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type_agent == "Bee":
                neighbor.energy = neighbor.gain_polline*0.6
                
               

        # se il tempo di vita finisce appassisce e muore
        # se è stato impollinato però si trasforma in zucca
        self.time_life -= 1
        if(self.time_life == 0):
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            