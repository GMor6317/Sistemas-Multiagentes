
from model import AspiradoraModel

from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle
from matplotlib.colors import ListedColormap

def propertylayer_portrayal(layer):
    """Función que define como se pintará la cuadrícula y sus celdas sucias."""
    if layer.name == "suciedad":
        return PropertyLayerStyle(
            colormap=ListedColormap(["white", "tab:brown"]),
            alpha=1,
            colorbar=False,
            vmin=0,
            vmax=1
        )

def agent_portrayal():
    """Función que define como se visualizará el agente dentro de la simulación."""
    return AgentPortrayalStyle(
        size=40,
        color="tab:blue"
    )

# Aquí se definen los parámetros del modelo. Ayuda a configurar la simulación desde la interfaz de solara.
model_params = {
    "n": {
        "type": "SliderInt",
        "value": 5,
        "label": "Número de aspiradoras:",
        "min": 1,
        "max": 100,
        "step": 1,
    },
    "width": {
        "type": "SliderInt",
        "value": 50,
        "label": "Width",
        "min": 5,
        "max": 60,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 50,
        "label": "Height",
        "min": 5,
        "max": 60,
        "step": 1,
    },
    "porcentaje_sucias": {
        "type": "SliderFloat",
        "value": 0.3,
        "label": "Porcentaje de suciedad inicial:",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
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

# Creando la instancia inicial del modelo.
aspiradoras_model = AspiradoraModel(
    n=5,
    width=50,
    height=50,
    porcentaje_sucias=0.5,
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

# Creando la gráfica que muestra la cantidad de celdas sucias
CeldasSuciasPlot = make_plot_component("CeldasSucias")

# Configuración de la página
page = SolaraViz(
    aspiradoras_model,
    renderer,
    components=[CeldasSuciasPlot],
    model_params=model_params,
    name="Simulación de Aspiradoras"
)

page