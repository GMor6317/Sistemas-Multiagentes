import mesa
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.discrete_space.property_layer import PropertyLayer
from agents import AspiradoraAgent

def calcular_celdas_sucias(model):
    return int(model.capa_suciedad.data.sum())

class AspiradoraModel(mesa.Model):

    def __init__(self, *, n=5, width=10, height=10, tiempo_max=100, rng=None):
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
            if self.random.random() < 0.5:
                self.capa_suciedad.data[cell.coordinate] = 1

        self.grid.add_property_layer(self.capa_suciedad)

        celda_inicial = self.grid[1, 1]

        AspiradoraAgent.create_agents(
            self,
            self.num_agentes,
            [celda_inicial] * self.num_agentes
        )

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "CeldasSucias": calcular_celdas_sucias
            },
            agent_reporters={
                "CeldasLimpias": "celdasLimpias",
                "Movimientos": "movimientosRealizados"
            }
        )

        self.datacollector.collect(self)
        self.running = True

    def step(self):

        if not self.running:
            return

        self.agents.shuffle_do("step")
        self.tiempo_actual += 1
        self.datacollector.collect(self)

        if self.tiempo_actual >= self.tiempo_max or calcular_celdas_sucias(self) == 0:
            self.running = False