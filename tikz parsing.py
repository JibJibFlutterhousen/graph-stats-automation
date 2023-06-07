import re

import tkinter
import tkinter.filedialog

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt

import networkx as nx

def load_graph(Path):
    with open(Path, "r") as in_file:
        file_content = in_file.read()

    # Regular expression patterns
    #     \node [style=#1] (#2) at (#3,#4) {#5};
    vertex_pattern = r'\\node\s+\[style=([^\]]+)\]\s+\(([\d]+)\)\s+at\s+\(([-\d.]+),\s+([-\d.]+)\)\s+\{(\w*)\};'
    #     \draw [style=#1] (#2) to (#3);
    edge_pattern = r'\\draw\s+\[style=([^\]]+)\]\s+\((\w+)\)\s+to\s+\((\w+)\);'

    # Extract node information
    vertices = re.findall(vertex_pattern, file_content)
    edges = re.findall(edge_pattern, file_content)

    # Make graph from loaded data
    graph = nx.Graph()
    for node_style, node_id, x_coordinate, y_coordinate, node_label in vertices:
        node_attributes = {"node_style": node_style, "x_coordinate":float(x_coordinate), "y_coordinate":float(y_coordinate), "node_label":node_label}
        graph.add_node(node_id, **node_attributes)
    for edge_style, source_id, target_id in edges:
        edge_attributes = {"edge_style":edge_style}
        graph.add_edge(source_id, target_id, **edge_attributes)

    # Make adjusted layout from loaded data
    max_x = max((data['x_coordinate'] for node, data in graph.nodes(data=True)), default=1)
    max_y = max((data['y_coordinate'] for node, data in graph.nodes(data=True)), default=1)
    layout = {node:(data['x_coordinate']/max_x,data['y_coordinate']/max_y) for node, data in graph.nodes(data=True)}
    return graph, layout

def main():
    def refresh_image(Graph=None, Layout=None):
        if Graph == None:
            Graph = nx.null_graph()
        if Layout == None:
            Layout = nx.circular_layout(Graph)
        nx.draw(Graph, ax=axes, pos=Layout, node_color='black', edge_color='black')
        canvas.draw()
        return

    def load_graph_file():
        filename = tkinter.filedialog.askopenfilename(filetypes = (("Tikz files","*.tikz*"),("all files","*.*")))
        graph_file_label.configure(text=filename)
        graph, layout = load_graph(filename)
        refresh_image(Graph=graph, Layout=layout)
        return

    def load_table_file():
        print('load_table_file not implemented just yet')
        return

    def make_new_table():
        print('make_new_table not implemented just yet')
        return

    def export_table_file():
        print('export_table_file not implemented just yet')
        return

    # constants
    WIDTH = 100
    HEIGHT = 5

    # Main window
    tkinter.Tk().withdraw()
    main_window = tkinter.Tk()
    # main_window.configure(bg='silver')
    main_window.title('Tikz Parser')
    main_window.state('zoomed')

    # Static Labels
    graph_file_delimiter = tkinter.Label(main_window, text='Graph file:', bg='lightgrey', height=HEIGHT, width=WIDTH)
    table_file_delimiter = tkinter.Label(main_window, text='Table file:', bg='lightgrey', height=HEIGHT, width=WIDTH)
    top_left_delimiter = tkinter.Label(main_window, text='Top left:', bg='lightgrey', height=1, width=WIDTH)
    top_center_delimiter = tkinter.Label(main_window, text='Top center:', bg='lightgrey', height=1, width=WIDTH)
    top_right_delimiter = tkinter.Label(main_window, text='Top right:', bg='lightgrey', height=1, width=WIDTH)
    bottom_left_delimiter = tkinter.Label(main_window, text='Bottom left:', bg='lightgrey', height=1, width=WIDTH)
    bottom_right_delimiter = tkinter.Label(main_window, text='Bottom right:', bg='lightgrey', height=1, width=WIDTH)

    # Dynamic Labels
    graph_file_label = tkinter.Label(main_window, text='None', bg='lightgrey', height=HEIGHT, width=WIDTH)
    table_file_label = tkinter.Label(main_window, text='None', bg='lightgrey', height=HEIGHT, width=WIDTH)

    # Buttons
    load_graph_button = tkinter.Button(main_window, text='Load Graph', command=load_graph_file, bg='silver', height=HEIGHT, width=WIDTH)
    load_table_button = tkinter.Button(main_window, text='Load Table', command=load_table_file, bg='silver', height=HEIGHT, width=WIDTH)
    new_table_button = tkinter.Button(main_window, text='New Table', command=make_new_table, bg='silver', height=HEIGHT, width=WIDTH)
    export_table_button = tkinter.Button(main_window, text='Export Table', command=export_table_file, bg='silver', height=HEIGHT, width=WIDTH)
    exit_button = tkinter.Button(main_window, text='Exit', command=exit, bg='silver', height=HEIGHT, width=WIDTH)

    # Textboxes
    top_left_textbox = tkinter.Text(main_window, height=HEIGHT, width=WIDTH)
    top_center_textbox = tkinter.Text(main_window, height=HEIGHT, width=WIDTH)
    top_right_textbox = tkinter.Text(main_window, height=HEIGHT, width=WIDTH)
    bottom_left_textbox = tkinter.Text(main_window, height=HEIGHT, width=WIDTH)
    bottom_right_textbox = tkinter.Text(main_window, height=HEIGHT, width=WIDTH)

    # Canvases
    figure,axes = plt.subplots(figsize=(5,5), dpi=250)
    canvas = FigureCanvasTkAgg(figure, master=main_window)
    refresh_image()
    canvas.draw()
    # toolbar = NavigationToolbar2Tk(canvas, main_window)
    # toolbar.update()

    # Packing
    # Row 1
    graph_file_delimiter.grid(row=1, column=1)
    graph_file_label.grid(row=1, column=2)
    load_graph_button.grid(row=1, column=3)
    # Row 2
    table_file_delimiter.grid(row=2, column=1)
    table_file_label.grid(row=2, column=2)
    load_table_button.grid(row=2, column=3)
    # Row 3
    new_table_button.grid(row=3, column=1)
    export_table_button.grid(row=3, column=3)
    # Row 4
    top_left_delimiter.grid(row=4, column=1)
    top_center_delimiter.grid(row=4, column=2)
    top_right_delimiter.grid(row=4, column=3)
    # Row 5
    top_left_textbox.grid(row=5, column=1)
    top_center_textbox.grid(row=5, column=2)
    top_right_textbox.grid(row=5, column=3)
    # Row 6
    canvas.get_tk_widget().grid(row=6, column=1, columnspan=3)
    # Row 7
    bottom_left_delimiter.grid(row=7, column=1)
    bottom_right_delimiter.grid(row=7, column=3)
    # Row 8
    bottom_left_textbox.grid(row=8, column=1)
    bottom_right_textbox.grid(row=8, column=3)
    # Row 9
    exit_button.grid(row=9, column=1, columnspan=3)

    # Row spacing
    main_window.rowconfigure(1, weight=1)
    main_window.rowconfigure(2, weight=1)
    main_window.rowconfigure(3, weight=1)
    main_window.rowconfigure(4, weight=1)
    main_window.rowconfigure(5, weight=1)
    main_window.rowconfigure(6, weight=5)
    main_window.rowconfigure(7, weight=1)
    main_window.rowconfigure(8, weight=1)
    main_window.rowconfigure(9, weight=1)

    # Column spacing
    main_window.columnconfigure(1, weight=1)
    main_window.columnconfigure(2, weight=1)
    main_window.columnconfigure(3, weight=1)


    # main_window.grid_rowconfigure(6, minsize=200)
    # exit_button.pack(side=tkinter.BOTTOM)
    # load_graph_button.pack(side=tkinter.BOTTOM)
    # graph_file_label.pack(side=tkinter.BOTTOM)
    # canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    main_window.mainloop()

if __name__ == '__main__':
    main()