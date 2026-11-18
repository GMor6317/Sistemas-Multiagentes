#----------------------------------------------------------
# Implementación de la estructura del modelo utilizado para 
# la simulación de aspiradoras.
#
# Fecha: 18-Nov-2026
# Autores:
#           A01753547 Cassandra Padilla
#           A01803172 Giancarlo Moreno
#----------------------------------------------------------
from mesa.discrete_space import CellAgent

class AspiradoraAgent(CellAgent):
    """Un agente con una celda asignada, número de movimientos y la cantidad de celdas que ha limpiado."""
    
    def __init__(self, model, cell):
        """Inicializar una instancia AspiradoraAgent
        
        Args:
            model: Una instancia modelo
            cell: Una celda de la cuadrícula    
        """
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
        """Definición de lo que se ejecutará en cada paso de la simulación."""
        self.mover()
        self.limpiar()
