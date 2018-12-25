"""
Draw a bus without transformations
"""
if __name__ == "__main__":
    from easygraphics import *
    import draw_bus

    init_graph(500, 300)

    draw_bus.draw_bus()

    set_color("gray")
    set_line_style(LineStyle.DASH_LINE)
    line(0, 0, 500, 300)
    set_line_style(LineStyle.SOLID_LINE)

    reflect(500, 300)
    draw_bus.draw_bus()
    pause()
    close_graph()
