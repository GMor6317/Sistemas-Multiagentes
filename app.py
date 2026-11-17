
from model import AspiradoraModel

from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle
from matplotlib.colors import ListedColormap

def propertylayer_portrayal(layer):

    if layer.name == "suciedad":
        return PropertyLayerStyle(
            colormap=ListedColormap(["white", "tab:brown"]),
            alpha=1,
            colorbar=False,
            vmin=0,
            vmax=1
        )

def agent_portrayal(agent):
    return AgentPortrayalStyle(
        size=40,  # Reducido ligeramente para grids grandes como 50x50
        color="tab:blue"
    )

model_params = {
    "n": {
        "type": "SliderInt",
        "value": 5,
        "label": "Número de aspiradoras:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "width": {
        "type": "SliderInt",
        "value": 50,  # Valor por defecto inicial acorde a tus pruebas
        "label": "Width",
        "min": 5,
        "max": 60,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 50,  # Valor por defecto inicial
        "label": "Height",
        "min": 5,
        "max": 60,
        "step": 1,
    },
    "tiempo_max": {
        "type": "SliderInt",
        "value": 100,
        "label": "Tiempo Máximo (Pasos):",
        "min": 10,
        "max": 500,
        "step": 10,
    }
}

aspiradoras_model = AspiradoraModel(
    n=5,
    width=50,
    height=50,
    tiempo_max=100
)

renderer = (
    SpaceRenderer(
        model=aspiradoras_model,
        backend="matplotlib",
    )
    .setup_agents(agent_portrayal)
    .setup_propertylayer(propertylayer_portrayal)
    .render()
)

CeldasSuciasPlot = make_plot_component("CeldasSucias")

page = SolaraViz(
    aspiradoras_model,
    renderer,
    components=[CeldasSuciasPlot],
    model_params=model_params,
    name="Simulación de Aspiradoras"
)

page