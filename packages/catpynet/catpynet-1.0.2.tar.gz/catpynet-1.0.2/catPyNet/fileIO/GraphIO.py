from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from catpynet.model.ReactionSystem import ReactionSystem
from enum import StrEnum
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
import math



class edge_types(StrEnum):

    REACTANT = "reactant"
    PRODUCT = "product"
    INHIBITOR = "inhibitor"
    CATALYST = "catalyst"
    CATALYST_CONJUNCTION = "catalyst_conjuntion"


class node_types(StrEnum):

    REACTION = "reaction"
    MOLECULE = "molecule"
    CATALYST_CONJUNCTION = "catalyst_conjunction"


SUPPORTED_GRAPH_OUTPUT_FILE_FORMATS = {".gml", ".graphml"}

ARROW_SHAPE_DICT = {edge_types.INHIBITOR:'T',
                    edge_types.CATALYST:"Arrow",
                   edge_types.CATALYST_CONJUNCTION:"Arrow",
                   edge_types.REACTANT:"Arrow",
                   edge_types.PRODUCT:"Arrow"}
NODE_SHAPE_DICT = {node_types.MOLECULE:'ELLIPSE', 
                   node_types.REACTION:'TRIANGLE', 
                   node_types.CATALYST_CONJUNCTION:'OCTAGON'}

EDGE_COLOR_DICT = {edge_types.INHIBITOR:"#FF0000",
                   edge_types.CATALYST:"#00FF00",
                   edge_types.CATALYST_CONJUNCTION:"#00FF00",
                   edge_types.REACTANT:"#000000",
                   edge_types.PRODUCT:"#000000"}
NODE_COLOR_DICT = {node_types.MOLECULE:'#702963', 
                   node_types.REACTION:'#FFC300', 
                   node_types.CATALYST_CONJUNCTION:'#FFC300'}

def write(reaction_systems: list[ReactionSystem], 
          filename: str, output_format:str) -> None:
    """Generate '.gml' files from a list of reactions systems.

    Args:
        reaction_systems (list[ReactionSystem]): list of reaction systems to be written
        filename (str): path of output file. If reaction_systems contains more than 1 reaction system
                        this path will be a directory with 'filename' + index as the new filenames.
        algorithm (AlgorithmBase, optional): Only used for Message Generation if a reaction system is empty. Defaults to None.
    """
    if filename == "stdout":
        tqdm.write("stdout is not currently available for graph format")
        return None
    
    if isinstance(reaction_systems, list):
        if len(reaction_systems) > 1:
            output = os.path.split(os.path.abspath(filename))
            output_directory = os.path.join(output[0], output[1].split(".")[0])
            output_file = output[1]
            os.makedirs(os.path.dirname(output_directory), exist_ok=True)

    for i, rs in enumerate(reaction_systems):
        graph = parse_rs_to_graph(rs)
        if len(reaction_systems) > 1:
            output_file = ".".join(
                [output_file.split(".")[0] + str(i), output_file.split(".")[1]])
            filename = os.path.join(output_directory, output_file)
        if ".gml" == output_format:
            tqdm.write("Writing file: " + filename)
            tqdm.write(rs.get_header_line())
            nx.write_gml(graph, filename)
        elif ".graphml" in filename:
            res_node_dict = {} #node:{attr:..., attr:...}
            node_keys_set = set()
            for label in list(graph.nodes()):
                node = graph.nodes()[label]
                single_node_dict = {}
                for attr in ['graphics', 'att']:
                    flat_dict = flatten_dict_dpth_2(node[attr], attr)
                    node_keys_set.update(set(flat_dict.keys()))
                    single_node_dict.update(flat_dict)
                    node.pop(attr)
                res_node_dict.update({label:single_node_dict})
            res_edge_dict = {}
            edge_keys_set = set()
            for label in list(graph.edges()):
                edge = graph.edges()[label]
                single_edge_dict = {}
                for attr in ['graphics', 'att']:
                    flat_dict = flatten_dict_dpth_2(edge[attr], attr)
                    edge_keys_set.update(set(flat_dict.keys()))
                    single_edge_dict.update(flat_dict)
                    edge.pop(attr)
                res_edge_dict.update({label:single_edge_dict})
            for key in node_keys_set:
                nx.set_node_attributes(graph, "", name=key)
            for key in edge_keys_set:
                nx.set_edge_attributes(graph, "", name=key)
            for label in list(graph.nodes()):
                node = graph.nodes()[label]
                for key in node_keys_set:
                    try:
                        graph.nodes()[label][key] = res_node_dict[label][key]
                    except: pass
                if node['att#node_type'] == node_types.REACTION:
                    node.pop('att#Food')
            for label in list(graph.edges()):
                edge = graph.edges()[label]
                for key in edge_keys_set:
                    graph.edges()[label][key] = res_edge_dict[label][key]
            nodes = list(graph.nodes(data=True))
            edges = list(graph.edges(data=True))
            nx.write_graphml(graph, filename)
        else:
            tqdm.write("File format not recognized." +
                       " Assumed .gml.")
            tqdm.write(rs.get_header_line())
            nx.write_gml(graph, filename)

def flatten_dict_dpth_2(attr:dict, key:str, sep:str = "#") -> dict[str, str]:
    res = {}
    for deeper_key in list(attr.keys()):
        val = attr[deeper_key]
        res.update({key + sep + deeper_key:val})
    
    return res

def parse_rs_to_graph(reaction_system: ReactionSystem) -> nx.DiGraph:
    """parses a reaction system to a networkx DiGraph object.

    Args:
        reaction_system (ReactionSystem): the rs to be parsed

    Returns:
        nx.DiGraph: An equivalent graph
        
    The resulting graph has nodes for:
     - Molecules (ellipses, white fill)
     - Reactions (triangles, black fill)
     - Catalyst Conjunctions (octagons, white fill)
    The edges are the connecting interactions/relations. So:
     - Reactants: point from molecules to reactions (Arrow, black)
     - Products: point away from reactions to molecules (Arrow, black)
     - Catalysts: point from molecules or catalyst conjunctions to reactions (Arrow, green)
     - Catalyst Conjunctions: point from molecules to catalyst conjunctions (Arrow, green)
     - Inhibitions: point from molecules to reactions (T, red)
    
    The graphics attributes are saved under: 
    Nodes:
     - ['graphics'] ['NodeShape'] (str): Shape of the node
     - ['graphics'] ['fill'] (str): Hexcode of the node fill color
    Edges:
     - ['graphics'] ['ArrowShape'] (str): Shape of the Arrow
     - ['graphics'] ['color'] (str): Hexcode of the edge color
    
    Nodes have the additional attributes:
     - ['att'] ['node_type'] (node_types) Identifies their node type according to the list above
     - ['att'] ['Food'] (bool) Identifies if a node is part of the food set 
     
    Edges have the additional attributes:
     - ['att'] ['edge_type'] (edge_types) Identifies their edge type according to the list above
     - ['weight'] (float|str|None) if a coefficient for a reactant or product edge is present, it is added here.
    """
    graph = nx.DiGraph(name=reaction_system.name)
    molecule_nodes = reaction_system.get_mentioned_molecules()
    molecule_nodes = [(node.name,
                       {"graphics": {"NodeShape": NODE_SHAPE_DICT[node_types.MOLECULE],
                                     "fill": NODE_COLOR_DICT[node_types.MOLECULE]},
                        "att": {"node_type": node_types.MOLECULE.value,
                                "Food": False}})
                      for node in molecule_nodes]
    graph.add_nodes_from(molecule_nodes)
    for food in reaction_system.foods:
        graph.nodes[food.name]["att"]["Food"] = True
    reaction_nodes = [(reaction.name,
                       {"graphics": {"NodeShape": NODE_SHAPE_DICT[node_types.REACTION],
                                     "fill": NODE_COLOR_DICT[node_types.REACTION]},
                        "att": {"node_type": node_types.REACTION.value}})
                      for reaction in reaction_system.reactions]
    graph.add_nodes_from(reaction_nodes)

    for reaction in reaction_system.reactions:
        for i, reactant in enumerate(reaction.reactants):
            if reaction.reactant_coefficients:
                coefficient = reaction.reactant_coefficients[i]
            else:
                coefficient = None
            match reaction.direction:
                case "forward":
                    parse_edge(graph, reactant.name, reaction.name,
                               edge_types.REACTANT, coefficient)
                case "reverse":
                    parse_edge(graph, reaction.name, reactant.name,
                               edge_types.PRODUCT, coefficient)
                case "both":
                    parse_edge(graph, reactant.name, reaction.name,
                               edge_types.REACTANT, coefficient)
                    parse_edge(graph, reaction.name, reactant.name,
                               edge_types.PRODUCT, coefficient)
        for i, product in enumerate(reaction.products):
            if reaction.product_coefficients:
                coefficient = reaction.product_coefficients[i]
            else:
                coefficient = None
            match reaction.direction:
                case "reverse":
                    parse_edge(graph, product.name, reaction.name,
                               edge_types.REACTANT, coefficient)
                case "forward":
                    parse_edge(graph, reaction.name, product.name,
                               edge_types.PRODUCT, coefficient)
                case "both":
                    parse_edge(graph, product.name, reaction.name,
                               edge_types.REACTANT, coefficient)
                    parse_edge(graph, reaction.name, product.name,
                               edge_types.PRODUCT, coefficient)
        for inhibitor in reaction.inhibitions:
            parse_edge(graph, inhibitor.name, reaction.name,
                       edge_types.INHIBITOR)
        for catalyst in [cata.name for cata in reaction.get_catalyst_conjunctions()]:
            if "&" in catalyst:
                catalyst_node = [(catalyst, {"graphics": {"NodeShape": NODE_SHAPE_DICT[node_types.CATALYST_CONJUNCTION],
                                                          "fill": NODE_COLOR_DICT[node_types.CATALYST_CONJUNCTION]},
                                             "att": {"node_type":
                                                     node_types.CATALYST_CONJUNCTION.value}})]
                graph.add_nodes_from(catalyst_node)
                parse_edge(graph, catalyst, reaction.name, edge_types.CATALYST)
                catalyst_elements = catalyst.split("&")
                for catalyst_element in catalyst_elements:
                    parse_edge(graph, catalyst_element, catalyst,
                               edge_types.CATALYST_CONJUNCTION)
            else:
                parse_edge(graph, catalyst, reaction.name, edge_types.CATALYST)

    return graph

def print_graph(graph:nx.DiGraph) -> None:
    
    if not graph.nodes:
        tqdm.write("Graph cannot be printed as it is empty")
        return
    
    nodes = graph.nodes(data=True)
    edges = graph.edges(data=True)
    max_iter = int(math.trunc(200/math.sqrt(len(nodes))))
    if max_iter == 0: max_iter = 1
    pos = nx.spring_layout(graph, 2, iterations=max_iter)
    node_shape_dict = {'circle':[], 
                       'triangle':[], 
                       'hexagon':[]}
    for node in nodes:
        if node[1]['graphics']['NodeShape'] == 'ELLIPSE':
            node_shape_dict["circle"].append(node[0])
        elif node[1]['graphics']['NodeShape'] == 'TRIANGLE':
            node_shape_dict["triangle"].append(node[0])
        elif node[1]['graphics']['NodeShape'] == 'OCTAGON':
            node_shape_dict["hexagon"].append(node[0])
        else:
            tqdm.write("Node: " + node[0] + "could not be recognized as molecule, reaction or catalyst conjunction")

    for edge in edges:
        if edge[2]['graphics']['ArrowShape'] == 'Arrow':
            style = '->'
        else:
            style = '|-|'
        try:
            weight = edge[2]['weight']
        except KeyError:
            weight = 1
        nx.draw_networkx_edges(graph, 
                               pos, 
                               edgelist=[edge],
                               width = weight,
                               edge_color=edge[2]['graphics']['color'],
                               arrowstyle=style,
                               connectionstyle='arc3, rad = 0.1')
    
    nx.draw_networkx_nodes(graph, pos, nodelist=node_shape_dict["circle"], 
                           node_color=NODE_COLOR_DICT[node_types.MOLECULE], node_shape='o', edgecolors='black')
    nx.draw_networkx_nodes(graph, pos, nodelist=node_shape_dict["triangle"], 
                           node_color=NODE_COLOR_DICT[node_types.REACTION], node_shape='^', edgecolors='black')
    nx.draw_networkx_nodes(graph, pos, nodelist=node_shape_dict["hexagon"], 
                           node_color=NODE_COLOR_DICT[node_types.CATALYST_CONJUNCTION], node_shape='h', edgecolors='black')
    
    nx.draw_networkx_labels(graph, pos)
    
    plt.show()
    
def print_rs_as_graph(reaction_system:ReactionSystem) -> None:
    
    graph = parse_rs_to_graph(reaction_system)
    print_graph(graph)

def parse_edge(graph: nx.DiGraph,
               u: str,
               v: str,
               edge_type: edge_types,
               coefficient: str | None = None) -> None:
    """Adds one edge in the appropriate format given edge type.

    Args:
        graph (nx.DiGraph): Graph the edge should be added to
        u (str): name of the starting node of the edge
        v (str): name of the end node of the edge
        edge_type (edge_types): Format the edge should take
        coefficient (str | None, optional): reactant-/product coefficient. Is converted to weight. Defaults to None.
    """    
    if edge_type == edge_types.INHIBITOR:
        color = "#FF0000"
        arrow = "T"
    elif edge_type in [edge_types.CATALYST, edge_types.CATALYST_CONJUNCTION]:
        color = "#00FF00"
        arrow = "Arrow"
    elif edge_type in [edge_types.REACTANT, edge_types.PRODUCT]:
        color = "#000000"
        arrow = "Arrow"
    else:
        tqdm.write("Edge type: " + edge_type + " isn't recognized." +
                   "REACTANT properties are used.")
        color = "#000000"
        arrow = "Arrow"

    graph.add_edge(u, v, graphics={"color": color,
                                   "ArrowShape": arrow},
                   att={"edge_type": edge_type.value})
    if coefficient:
        try:
            graph[u][v]["weight"] = float(coefficient)
        except ValueError:
            graph[u][v]["weight"] = coefficient
