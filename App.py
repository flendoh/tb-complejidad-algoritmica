import dearpygui.dearpygui as dpg
import random
dpg.create_context()
from themes.theme import *
from themes.font import *

VACIO = 0
JUGADOR_1 = 1
JUGADOR_2 = 2

class App:
    def __init__(self):
        dpg.create_viewport(title="TB Complejidad Algoritmica", width=800, height=600, x_pos=0, y_pos=0)
        dpg.bind_theme(global_theme)
        dpg.bind_font(global_font)
        dpg.setup_dearpygui()
        self.log_window = None
        self.main_window = None
        self.table_window = None
        self.CELL_SIZE = 50
        self.table = []
        self.main_window_setup()
        dpg.show_viewport()
        dpg.set_viewport_max_height(600)
        dpg.set_viewport_max_width(800)
        dpg.set_viewport_resizable(False)
        dpg.start_dearpygui()

    def add_text_log(self, text):
        dpg.add_text(text, wrap=200, parent=self.log_window)
    
    def draw_piece(self, x, y, player):
        P2_COLOR = [84, 82, 79]
        P1_COLOR = [226, 226, 226] 
        dpg.draw_circle(
            center=[x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2],
            radius=self.CELL_SIZE // 3,
            color=P1_COLOR if player == JUGADOR_1 else P2_COLOR,
            fill=P1_COLOR if player == JUGADOR_1 else P2_COLOR,
            parent=self.table_window
        )

    def restart_game(self):
        self.table = [
            [VACIO, JUGADOR_1, VACIO, JUGADOR_1, VACIO, JUGADOR_1, VACIO, JUGADOR_1],
            [JUGADOR_1, VACIO, JUGADOR_1, VACIO, JUGADOR_1, VACIO, JUGADOR_1, VACIO],
            [VACIO, JUGADOR_1, VACIO, JUGADOR_1, VACIO, JUGADOR_1, VACIO, JUGADOR_1],
            [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO],
            [JUGADOR_2, VACIO, JUGADOR_2, VACIO, JUGADOR_2, VACIO, JUGADOR_2, VACIO],
            [VACIO, JUGADOR_2, VACIO, JUGADOR_2, VACIO, JUGADOR_2, VACIO, JUGADOR_2],
            [JUGADOR_2, VACIO, JUGADOR_2, VACIO, JUGADOR_2, VACIO, JUGADOR_2, VACIO]
        ]
        dpg.delete_item(self.log_window, children_only=True)
        self.update_board()
        self.jugar_damas()
    
    def draw_table(self):
        TABLE_SIZE = 8
        for i in range(TABLE_SIZE):
            for j in range(TABLE_SIZE):
                color = [255, 255, 255] if (i + j) % 2 == 0 else [50,50,50]
                dpg.draw_rectangle(
                    pmin=[j * self.CELL_SIZE, i * self.CELL_SIZE],
                    pmax=[(j + 1) * self.CELL_SIZE, (i + 1) * self.CELL_SIZE],
                    thickness=0,
                    color=[50,50,50],
                    fill=color,
                    parent=self.table_window
                )
    
    def update_board(self):
        #dpg.delete_item(self.table_window, children_only=True)
        self.draw_table()
        for i in range(8):
            for j in range(8):
                if self.table[i][j] == JUGADOR_1:
                    self.draw_piece(j, i, JUGADOR_1)
                elif self.table[i][j] == JUGADOR_2:
                    self.draw_piece(j, i, JUGADOR_2)
    
    def movimientos_posibles(self, jugador):
        movimientos = []
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if self.table[i][j] == jugador:
                    if jugador == JUGADOR_1:
                        direcciones = [(1, -1), (1, 1)]
                    else:
                        direcciones = [(-1, -1), (-1, 1)]

                    for dir in direcciones:
                        nueva_fila, nueva_col = i + dir[0], j + dir[1]
                        if 0 <= nueva_fila < 8 and 0 <= nueva_col < 8 and self.table[nueva_fila][nueva_col] == VACIO:
                            movimientos.append(((i, j), (nueva_fila, nueva_col)))
        return movimientos
    
    def hacer_movimiento(self, movimiento):
        (fila_actual, col_actual), (fila_nueva, col_nueva) = movimiento
        self.table[fila_nueva][col_nueva] = self.table[fila_actual][col_actual]
        self.table[fila_actual][col_actual] = VACIO
        self.update_board()

    def jugada_bot(self):
        movimientos = self.movimientos_posibles(JUGADOR_2)
        if movimientos:
            return random.choice(movimientos)
        return None

    def main_window_setup(self):
        TABLE_SIZE = 8
        with dpg.window() as self.main_window:
            with dpg.menu_bar():
                with dpg.menu(label="Archivo"):
                    dpg.add_menu_item(label="Nuevo Juego", callback=self.restart_game)
                    dpg.add_menu_item(label="Salir", callback=dpg.stop_dearpygui)
                with dpg.menu(label="Ayuda"):
                    dpg.add_menu_item(label="Acerca de")

            with dpg.group(horizontal=True):
                with dpg.group(horizontal=False):
                    with dpg.child_window(width=235, height=400) as self.log_window:
                        pass
                    dpg.add_text("Pos 1 (Seleccionar ficha)")
                    self.pos1_x = dpg.add_input_int(label="X", default_value=0, width=100, callback=lambda: self.draw_highlight((dpg.get_value(self.pos1_y), dpg.get_value(self.pos1_x)), (dpg.get_value(self.pos2_y), dpg.get_value(self.pos2_x))))
                    dpg.add_same_line()
                    self.pos1_y = dpg.add_input_int(label="Y", default_value=0, width=100, callback=lambda: self.draw_highlight((dpg.get_value(self.pos1_y), dpg.get_value(self.pos1_x)), (dpg.get_value(self.pos2_y), dpg.get_value(self.pos2_x))))
                    dpg.add_text("Pos 2 (Mover ficha)")
                    self.pos2_x = dpg.add_input_int(label="X", default_value=0, width=100, callback=lambda: self.draw_highlight((dpg.get_value(self.pos1_y), dpg.get_value(self.pos1_x)), (dpg.get_value(self.pos2_y), dpg.get_value(self.pos2_x))))
                    dpg.add_same_line()
                    self.pos2_y = dpg.add_input_int(label="Y", default_value=0, width=100, callback=lambda: self.draw_highlight((dpg.get_value(self.pos1_y), dpg.get_value(self.pos1_x)), (dpg.get_value(self.pos2_y), dpg.get_value(self.pos2_x))))
                    dpg.add_button(label="Mover", width=235, callback=self.realizar_movimiento_jugador)

                with dpg.plot(no_menus=False, no_title=True, no_box_select=True, no_mouse_pos=True, width=525,height=525, equal_aspects=True) as self.table_window:
                    default_x = dpg.add_plot_axis(axis=0, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                                label="", lock_min=True)
                    dpg.set_axis_limits(axis=default_x, ymin=0, ymax=self.CELL_SIZE*TABLE_SIZE)
                    default_y = dpg.add_plot_axis(axis=1, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                                label="", lock_min=True)
                    dpg.set_axis_limits(axis=default_y, ymin=0, ymax=self.CELL_SIZE*TABLE_SIZE)
                    self.restart_game()
                
        dpg.set_primary_window(self.main_window, True)
    
    def draw_highlight(self, pos1, pos2):
        self.update_board()
        color = [255, 0, 0, 255]
        thickness = 3
        dpg.draw_rectangle(
            pmin=[pos1[1] * self.CELL_SIZE, pos1[0] * self.CELL_SIZE],
            pmax=[(pos1[1] + 1) * self.CELL_SIZE, (pos1[0] + 1) * self.CELL_SIZE],
            color=color,
            thickness=thickness,
            parent=self.table_window
        )
        dpg.draw_rectangle(
            pmin=[pos2[1] * self.CELL_SIZE, pos2[0] * self.CELL_SIZE],
            pmax=[(pos2[1] + 1) * self.CELL_SIZE, (pos2[0] + 1) * self.CELL_SIZE],
            color=color,
            thickness=thickness,
            parent=self.table_window
        )
    
    def realizar_movimiento_jugador(self):
        pos1_x = dpg.get_value(self.pos1_x)
        pos1_y = dpg.get_value(self.pos1_y)
        pos2_x = dpg.get_value(self.pos2_x)
        pos2_y = dpg.get_value(self.pos2_y)
        if self.turno == JUGADOR_1 and self.table[pos1_y][pos1_x] == JUGADOR_1 and self.table[pos2_y][pos2_x] == VACIO:
            movimiento = ((pos1_y, pos1_x), (pos2_y, pos2_x))
            self.hacer_movimiento(movimiento)
            self.add_text_log(f"Jugador 1 movió de ({pos1_x}, {pos1_y}) a ({pos2_x}, {pos2_y})")
            self.turno = JUGADOR_2
            self.add_text_log("Turno del Bot")
            self.realizar_movimiento_bot()

    def realizar_movimiento_bot(self):
        movimiento_bot = self.jugada_bot()
        if movimiento_bot:
            self.hacer_movimiento(movimiento_bot)
            self.draw_highlight(movimiento_bot[0], movimiento_bot[1])
            self.add_text_log(f"Bot movió de {movimiento_bot[0]} a {movimiento_bot[1]}")
            self.turno = JUGADOR_1
            self.add_text_log("Turno del Jugador 1")
        else:
            self.add_text_log("El bot no puede hacer más movimientos.")

    def jugar_damas(self):
        self.add_text_log("Empezó el juego.")
        self.turno = JUGADOR_1
        self.update_board()
        self.add_text_log("Turno del Jugador 1")

    def __del__(self):
        dpg.destroy_context()

if __name__ == "__main__":
    app = App()