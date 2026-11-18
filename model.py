#----------------------------------------------------------
# Implementación de la estructura del modelo utilizado para 
# la simulación de aspiradoras.
#
# Fecha: 18-Nov-2026
# Autores:
#           A01753547 Cassandra Padilla
#           A01803172 Giancarlo Moreno
#----------------------------------------------------------
import mesa
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.discrete_space.property_layer import PropertyLayer
from agents import AspiradoraAgent

def calcular_celdas_sucias(model):
    """Función que calcula la cantidad de celdas sucias.
    
    Args:
        model: El modelo de las aspiradoras.
    """
    return int(model.capa_suciedad.data.sum())


def calcular_porcentaje_celdas_sucias(model):
    """Función que calcula el porcentaje de celdas sucias.
    
    Args:
        model: El modelo de las aspiradoras.
    """
    return float(model.capa_suciedad.data.sum() / (model.grid.width * model.grid.height) * 100)

class AspiradoraModel(mesa.Model):
    """Un modelo con un determinado número de agentes."""

    def __init__(self, *, n=5, width=10, height=10, porcentaje_sucias=0.5, tiempo_max=100, rng=None):
        """Inicializar una instancia de AspiradoraModel
        
            Args:
                N: El número de agentes.
                width: El ancho de la cuadrícula.
                height: La altura de la cuadrícula.
                porcentaje_sucias: La probabilidad de que una celda esté sucia.
                tiempo_max: El tiempo máximo (pasos) que dura la simulación.
        """

        super().__init__(rng=rng)
        self.num_agentes = n
        self.tiempo_max = tiempo_max
        self.tiempo_actual = 0

        self.grid = OrthogonalMooreGrid(
            (width, height),
            random=self.random
        )

        self.capa_suciedad = PropertyLayer(
            "suciedad",
            (width, height),
            default_value=0,
            dtype=int
        )

        for cell in self.grid.all_cells:
            if self.random.random() < porcentaje_sucias:
                self.capa_suciedad.data[cell.coordinate] = 1

        self.grid.add_property_layer(self.capa_suciedad)

        celda_inicial = self.grid[1, 1]

        # Crear los agentes
        AspiradoraAgent.create_agents(
            self,
            self.num_agentes,
            [celda_inicial] * self.num_agentes
        )

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "CeldasSucias": calcular_celdas_sucias,
                "PorcentajeCeldasSucias": calcular_porcentaje_celdas_sucias,
                "Tiempo": lambda m: m.tiempo_actual
            },
            agent_reporters={
                "CeldasLimpias": "celdasLimpias",
                "Movimientos": "movimientosRealizados"
            }
        )

        self.datacollector.collect(self)
        self.running = True

    def step(self):
        """Función que define las acciones que se ejecutarán en cada paso."""
        if not self.running:
            return

        self.agents.shuffle_do("step")
        self.tiempo_actual += 1

        self.datacollector.collect(self)

        if self.tiempo_actual >= self.tiempo_max or calcular_celdas_sucias(self) == 0:
            self.running = False