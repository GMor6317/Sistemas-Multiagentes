from mesa.discrete_space import CellAgent

class AspiradoraAgent(CellAgent):

    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.celdasLimpias = 0
        self.movimientosRealizados = 0

    def mover(self):
        """Mover el agente a una celda vecina."""
        self.cell = self.cell.neighborhood.select_random_cell()
        self.movimientosRealizados += 1

    def limpiar(self):
        """Limpiar la celda actual si está sucia."""
        coord = self.cell.coordinate

        if self.model.capa_suciedad.data[coord] == 1:
            self.model.capa_suciedad.data[coord] = 0
            self.celdasLimpias += 1

    def step(self):
        self.mover()
        self.limpiar()
