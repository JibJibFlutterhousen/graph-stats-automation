import re
import math
import csv

import networkx as nx
import matplotlib.pyplot as plt

def cell_wrapper(graph, graph_name = None, lower_left = None, lower_right = None, upper_left = None, upper_right = None):
    graph_layout = nx.kamada_kawai_layout(graph)
    
    node_styles=dict()
    default_node_style = "draw=black,fill=black!0,shape=circle,text=black,inner sep=0pt,minimum size=4pt"
    meta_node_style = "shape=circle,text=black,inner sep=0pt,minimum size=4pt,fill opacity=0,text opacity=1"
    for node in graph:
        node_styles[node] = default_node_style
    
    tikz_code = re.sub(r'\{\d+\}', '{}', nx.to_latex_raw(graph, pos=graph_layout, node_options=node_styles)).strip()

    tikz_picture_code = r"\resizebox{1in}{!}{tikz_code}".replace('tikz_code',tikz_code)
    
    if graph_name is not None:
        name_label = max(int(x) for x in re.findall(r'\((\d+)\)', tikz_picture_code))+1
        graph_name_line = f"      \draw\n        (0.0,1.35) node[{meta_node_style}]" + f"({name_label})" + r" {\textbf{" + f"{graph_name}" + "}};\n"
        lines = tikz_picture_code.split("\n")
        tikz_picture_code = ""
        for line in lines:
            if r"\begin{scope}[-]" in line:
                tikz_picture_code += graph_name_line
            tikz_picture_code += line
            if r"    \end{tikzpicture}}" in line:
                break
            else:
                tikz_picture_code += "\n"
    
    if lower_left is not None:
        name_label = max(int(x) for x in re.findall(r'\((\d+)\)', tikz_picture_code))+1
        graph_name_line = f"      \draw\n        (-1.0,-1.15) node[{meta_node_style}]" + f"({name_label})" + r" {" + f"{lower_left}" + "};\n"
        lines = tikz_picture_code.split("\n")
        tikz_picture_code = ""
        for line in lines:
            if r"\begin{scope}[-]" in line:
                tikz_picture_code += graph_name_line
            tikz_picture_code += line
            if r"    \end{tikzpicture}}" in line:
                break
            else:
                tikz_picture_code += "\n"
    
    if upper_left is not None:
        name_label = max(int(x) for x in re.findall(r'\((\d+)\)', tikz_picture_code))+1
        graph_name_line = f"      \draw\n        (-1.0,1.35) node[{meta_node_style}]" + f"({name_label})" + r" {" + f"{upper_left}" + "};\n"
        lines = tikz_picture_code.split("\n")
        tikz_picture_code = ""
        for line in lines:
            if r"\begin{scope}[-]" in line:
                tikz_picture_code += graph_name_line
            tikz_picture_code += line
            if r"    \end{tikzpicture}}" in line:
                break
            else:
                tikz_picture_code += "\n"
    
    if lower_right is not None:
        name_label = max(int(x) for x in re.findall(r'\((\d+)\)', tikz_picture_code))+1
        graph_name_line = f"      \draw\n        (1.0,-1.15) node[{meta_node_style}]" + f"({name_label})" + r" {" + f"{lower_right}" + "};\n"
        lines = tikz_picture_code.split("\n")
        tikz_picture_code = ""
        for line in lines:
            if r"\begin{scope}[-]" in line:
                tikz_picture_code += graph_name_line
            tikz_picture_code += line
            if r"    \end{tikzpicture}}" in line:
                break
            else:
                tikz_picture_code += "\n"
    
    if upper_right is not None:
        name_label = max(int(x) for x in re.findall(r'\((\d+)\)', tikz_picture_code))+1
        graph_name_line = f"      \draw\n        (1.0,1.35) node[{meta_node_style}]" + f"({name_label})" + r" {" + f"{upper_right}" + "};\n"
        lines = tikz_picture_code.split("\n")
        tikz_picture_code = ""
        for line in lines:
            if r"\begin{scope}[-]" in line:
                tikz_picture_code += graph_name_line
            tikz_picture_code += line
            if r"    \end{tikzpicture}}" in line:
                break
            else:
                tikz_picture_code += "\n"
            

    return tikz_picture_code

def table_wrapper(stats_file):
    longtable_code = r"""\begin{longtable}{|c|c|c|c|c|c|}
\hline
"""
    with open(stats_file, "r") as in_file:
        csv_reader = csv.reader(in_file)
        first = True
        counter = 0
        number_of_lines = sum(1 for dummy in in_file)-1
        in_file.seek(0)
        for line in csv_reader:
            if first:
                first = False
                continue
            else:
                graph_name = line[0]
                graph = nx.from_graph6_bytes(line[1].encode())
                top_left = None
                top_right = None
                bottom_right = None
                bottom_left = None
                if len(line) > 2:
                    top_left = line[2]
                if len(line) > 3:
                    top_right = line[3]
                if len(line) > 4:
                    bottom_right = line[4]
                if len(line) > 5:
                    bottom_left = line[5]
                longtable_code += cell_wrapper(graph, graph_name=graph_name, upper_left=top_left, upper_right=top_right, lower_right=bottom_right, lower_left=bottom_left)
                counter += 1
                if counter == number_of_lines:
                    longtable_code += "\n"
                    break
                if counter % 6 == 0:
                    longtable_code += r"""\\ \hline
"""
                else:
                    longtable_code += "&"
    longtable_code += r"""\\ \hline
\end{longtable}
"""
    return longtable_code