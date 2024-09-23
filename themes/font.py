import dearpygui.dearpygui as dpg

with dpg.font_registry():
    font_path = 'fonts/LibreFranklin-Thin.ttf'
    global_font = dpg.add_font(font_path, 14)