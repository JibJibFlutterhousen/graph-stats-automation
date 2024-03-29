import re
import os

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
    min_x = min((data['x_coordinate'] for node, data in graph.nodes(data=True)), default=1)
    max_x = max((data['x_coordinate'] for node, data in graph.nodes(data=True)), default=1)
    min_y = min((data['y_coordinate'] for node, data in graph.nodes(data=True)), default=1)
    max_y = max((data['y_coordinate'] for node, data in graph.nodes(data=True)), default=1)

    if min_x != max_x:
        x_range = max_x - min_x
        [data.update({'x_coordinate':(data['x_coordinate']-min_x)/x_range}) for node, data in graph.nodes(data=True)]
    if min_y != max_y:
        y_range = max_y - min_y
        [data.update({'y_coordinate':(data['y_coordinate']-min_y)/y_range}) for node, data in graph.nodes(data=True)]

    layout = {node:(data['x_coordinate'],data['y_coordinate']) for node, data in graph.nodes(data=True)}
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
        graph_file_label.configure(text='Graph File: ' + filename)
        graph, layout = load_graph(filename)
        refresh_image(Graph=graph, Layout=layout)
        return

    def load_table_dir():
        print('load_table_dir not implemented just yet')
        dirname = tkinter.filedialog.askdirectory()
        table_dir_label.configure(text='Table Directory: ' + dirname)
        os.chdir(dirname)
        return

    def make_new_table():
        print('make_new_table not implemented just yet')
        return

    def insert_meta_node(X_coordinate, Y_coordinate, Node_label, Tikz_code):
        meta_node_style = "shape=circle,text=black,inner sep=0pt,minimum size=1em,fill opacity=0,text opacity=1"
        node_id = max(int(x) for x in re.findall(r'\((\d+)\)', Tikz_code))+1
        insert_line = f"      \draw\n        ({X_coordinate},{Y_coordinate}) node[{meta_node_style}]" + f"({node_id})" + r" {" + f"{Node_label}" + "};\n"
        lines = Tikz_code.split('\n')
        tikzpicture = ""
        for line in lines:
            if r"\begin{scope}[-]" in line:
                tikzpicture += insert_line
            tikzpicture += line
            if r"    \end{tikzpicture}}" in line:
                break
            else:
                tikzpicture += "\n"
        return tikzpicture

    def export_graph():
        print('export_graph not fully implemented just yet')
        filename = graph_file_label.cget('text')[12:]
        print(filename)
        if filename != 'None':
            graph, layout = load_graph(filename)
            default_node_styles = {node:"draw=black,fill=black!0,shape=circle,text=black,inner sep=0pt,minimum size=4pt" for node in graph}
            tikzpicture = r"\resizebox{1in}{1in}{tikz_code}".replace('tikz_code',re.sub(r'\{\d+\}', '{}', nx.to_latex_raw(graph, pos=layout, node_options=default_node_styles)).strip())

            upper_left = top_left_textbox.get()
            upper_center = top_center_textbox.get()
            upper_right = top_right_textbox.get()
            lower_left = bottom_left_textbox.get()
            lower_center = bottom_center_textbox.get()
            lower_right = bottom_right_textbox.get()
    
            if len(upper_left) > 0:
                tikzpicture = insert_meta_node(-0.35,1.35,upper_left,tikzpicture)
            if len(upper_center) > 0:
                tikzpicture = insert_meta_node(0.5,1.35,upper_center,tikzpicture)
            if len(upper_right) > 0:
                tikzpicture = insert_meta_node(1.35,1.35,upper_right,tikzpicture)
            if len(lower_left) > 0:
                tikzpicture = insert_meta_node(-0.35,-0.35,lower_left,tikzpicture)
            if len(lower_center) > 0:
                tikzpicture = insert_meta_node(0.5,1.35,lower_center,tikzpicture)
            if len(lower_right) > 0:
                tikzpicture = insert_meta_node(1.35,-0.35,lower_right,tikzpicture)

            table_number = table_number_spinbox.get()
            graph_number = graph_number_spinbox.get()

            table_name = f'table {table_number.zfill(4)}'
            graph_file_name = f'graph {graph_number.zfill(4)}.tex'

            if not os.path.exists(table_name):
                os.mkdir(table_name)
            with open(f'{table_name}/{graph_file_name}', 'w') as out_file:
                out_file.write(tikzpicture)

            print(tikzpicture)
        return

    # Main window
    tkinter.Tk().withdraw()
    main_window = tkinter.Tk()
    main_window.title('Tikz Parser')
    main_window.state('zoomed')

    # constants
    WIDTH = 100
    HEIGHT = 5
    FONT = tkinter.font.Font(family='Helvetica', size=36, weight='bold')

    # Static Labels
    top_left_delimiter = tkinter.Label(main_window, text='Top left:', bg='lightgrey', height=1, font=FONT, width=WIDTH)
    top_center_delimiter = tkinter.Label(main_window, text='Top center:', bg='lightgrey', height=1, font=FONT, width=WIDTH)
    top_right_delimiter = tkinter.Label(main_window, text='Top right:', bg='lightgrey', height=1, font=FONT, width=WIDTH)
    bottom_left_delimiter = tkinter.Label(main_window, text='Bottom left:', bg='lightgrey', height=1, font=FONT, width=WIDTH)
    bottom_center_delimiter = tkinter.Label(main_window, text='Bottom center:', bg='lightgrey', height=1, font=FONT, width=WIDTH)
    bottom_right_delimiter = tkinter.Label(main_window, text='Bottom right:', bg='lightgrey', height=1, font=FONT, width=WIDTH)

    # Dynamic Labels
    table_dir_label = tkinter.Label(main_window, text='Table Directory: None', bg='lightgrey', height=HEIGHT, font=FONT, width=WIDTH)
    graph_file_label = tkinter.Label(main_window, text='Graph File: None', bg='lightgrey', height=HEIGHT, font=FONT, width=WIDTH)

    # Buttons
    load_graph_button = tkinter.Button(main_window, text='Load Graph', command=load_graph_file, bg='silver', height=HEIGHT, font=FONT, width=WIDTH)
    load_table_dir_button = tkinter.Button(main_window, text='Set Tables Directory', command=load_table_dir, bg='silver', height=HEIGHT, font=FONT, width=WIDTH)
    new_table_button = tkinter.Button(main_window, text='New Table', command=make_new_table, bg='silver', height=HEIGHT, font=FONT, width=WIDTH)
    export_graph_button = tkinter.Button(main_window, text='Export Graph', command=export_graph, bg='silver', height=HEIGHT, font=FONT, width=WIDTH)
    exit_button = tkinter.Button(main_window, text='Exit', command=exit, bg='silver', height=HEIGHT, font=FONT, width=WIDTH)

    # Textboxes
    top_left_entry = tkinter.StringVar()
    top_left_textbox = tkinter.Entry(main_window, width=WIDTH, font=FONT, textvariable=top_left_entry)
    top_center_entry = tkinter.StringVar()
    top_center_textbox = tkinter.Entry(main_window, width=WIDTH, font=FONT, textvariable=top_center_entry)
    top_right_entry = tkinter.StringVar()
    top_right_textbox = tkinter.Entry(main_window, width=WIDTH, font=FONT, textvariable=top_right_entry)
    bottom_left_entry = tkinter.StringVar()
    bottom_left_textbox = tkinter.Entry(main_window, width=WIDTH, font=FONT, textvariable=bottom_left_entry)
    bottom_center_entry = tkinter.StringVar()
    bottom_center_textbox = tkinter.Entry(main_window, width=WIDTH, font=FONT, textvariable=bottom_center_entry)
    bottom_right_entry = tkinter.StringVar()
    bottom_right_textbox = tkinter.Entry(main_window, width=WIDTH, font=FONT, textvariable=bottom_right_entry)

    # Scroll buttons to select table and graph number
    table_number_spinbox = tkinter.Spinbox(main_window, width=WIDTH, font=FONT, from_=1, to=9223372036854775807, increment=1)
    graph_number_spinbox = tkinter.Spinbox(main_window, width=WIDTH, font=FONT, from_=1, to=9223372036854775807, increment=1)

    # Canvases
    figure,axes = plt.subplots(figsize=(5,5), dpi=250)
    canvas = FigureCanvasTkAgg(figure, master=main_window)
    refresh_image()

    # Packing
    # Row 1
    load_graph_button.grid(row=1, column=1) #1, 1
    graph_file_label.grid(row=1, column=2) #1, 2
    graph_number_spinbox.grid(row=1, column=3) #1, 3
    # Row 2
    load_table_dir_button.grid(row=2, column=1) #2, 1
    table_dir_label.grid(row=2, column=2) #2, 2
    table_number_spinbox.grid(row=2, column=3) #2, 3
    # Row 3
    new_table_button.grid(row=3, column=1) #
    export_graph_button.grid(row=3, column=3) #
    # Row 4
    top_left_delimiter.grid(row=4, column=1) #
    top_center_delimiter.grid(row=4, column=2) #
    top_right_delimiter.grid(row=4, column=3) #
    # Row 5
    top_left_textbox.grid(row=5, column=1) #
    top_center_textbox.grid(row=5, column=2) #
    top_right_textbox.grid(row=5, column=3) #
    # Row 6
    canvas.get_tk_widget().grid(row=6, column=1, columnspan=3) #
    # Row 7
    bottom_left_delimiter.grid(row=7, column=1) #
    bottom_center_delimiter.grid(row=7, column=2) #
    bottom_right_delimiter.grid(row=7, column=3) #
    # Row 8
    bottom_left_textbox.grid(row=8, column=1) #
    bottom_center_textbox.grid(row=8, column=2) #
    bottom_right_textbox.grid(row=8, column=3) #
    # Row 9
    exit_button.grid(row=9, column=1, columnspan=3) #

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

    main_window.mainloop()

if __name__ == '__main__':
    main()