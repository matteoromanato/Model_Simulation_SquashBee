from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from agents import *
from model import SquashBee


def Squash_Bee_portrayal(agent):
    
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.8, "Filled": "true"}

    if type(agent) is Bee:
        #portrayal["Shape"] = "ape.jfif"
        #portrayal["scale"] = 0.9
        portrayal["Color"] = ["#FFFF00", "#FFFF00"]
        portrayal["stroke_color"] = "#000000"
        portrayal["text_color"] = "yellow"
        portrayal["Layer"] = 3
    if type(agent) is Bee_son:
        portrayal["Color"] = ["#ADA96E", "#ADA96E"]
        portrayal["stroke_color"] = "#000000"
        #portrayal["text"] = round(agent.time_grow, 1)
        portrayal["text_color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2
    if type(agent) is Zucca:
        portrayal["Color"] = ["#FBB917", "#FBB917"]
        portrayal["stroke_color"] = "#000000"
        portrayal["text_color"] = "#FBB917"
        portrayal["Layer"] = 1
    if type(agent) is Zucca_flower:
        portrayal["Color"] = ["#8AFB17", "#8AFB17"]
        portrayal["stroke_color"] = "#000000"
        portrayal["text"] = round(agent.time_life, 1)
        portrayal["text_color"] = "#8AFB17"
        portrayal["Layer"] = 1
    if type(agent) is Zucca_seed:
        portrayal["Color"] = ["#C8B560", "#C8B560"]
        portrayal["stroke_color"] = "#000000"
        portrayal["text_color"] = "#C8B560"
        portrayal["Layer"] = 0
    if type(agent) is flower:
        portrayal["Color"] = ["#FF0000", "#FF0000"]
        portrayal["stroke_color"] = "#000000"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.35
    return portrayal


canvas_element = CanvasGrid(Squash_Bee_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "Zucche_fiori", "Color": "#8AF017"},
                                {"Label": "Zucche", "Color": "#FBB917"},
                                {"Label": "Seed", "Color": "#C8B560"},
                                {"Label": "Api", "Color": "#FFFF00"},
                                {"Label": "Larve", "Color": "#ADA96E"}])

model_params = {"density_bee": UserSettableParameter('slider', 'numero di api nel prato', 180, 0, 500),
                "density_gender_bee": UserSettableParameter('slider', 'Densità di api femmine', 60, 0, 100),
                "gain_polline_raccolto": UserSettableParameter('slider', 'guadagno energia dal polline', 60, 0, 100),
                "density_zucca": UserSettableParameter('slider', 'numero di fiori di zucca nel prato', 200, 1, 500),
                "prob_accoppiamento": UserSettableParameter('slider', 'probabilità di accoppiamento tra due api', 80, 0, 100),
                "offsetX": UserSettableParameter('slider', 'spostamento campo X', 5, 0, 20),
                "offsetY": UserSettableParameter('slider', 'spostamento campo Y', 5, 0, 20)}

server = ModularServer(SquashBee, [canvas_element, chart_element], "Simulazione comportamento dell'ape della zucca", model_params)
server.port = 8521
