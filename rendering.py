from graphviz import Digraph, escape
import json

def buildGraph(node, graph = None, explored = []):
    """
        Creates a graph for the current node
    
        Arguments:
            node {Node} -- Father node
            graph {Digraph}
            mainBranch {bool} -- If display only the main branch or all of the tree
        Returns:
            Digraph
    """
    if graph is None:
        graph = Digraph('png')
    graph.node(str(node.id), label="<<table cellborder='0'><tr><td title='{}' href=''>{}</td></tr></table>>".format(escape(str(json.dumps(node.hyperparams, indent=1, sort_keys=True))), node.name))
    for arg_type, child in node.children:
        graph.edge(str(node.id), str(child.id), label=arg_type)
        if child.id not in explored:
            explored.append(child.id)
            graph = buildGraph(child, graph, explored)

    return apply_styles(graph)

def apply_styles(graph):
    styles = {
        'nodes': {
            'fontname': 'Helvetica',
            'shape': 'hexagon',
            'fontcolor': 'white',
            'color': 'black',
            'pencolor': '#006699',
            'style': 'filled',
            'fillcolor': '#006699',
        },
        'edges': {
            'style': 'dashed',
            'color': 'black',
            'arrowhead': 'open',
            'fontname': 'Helvetica',
            'fontsize': '12',
            'fontcolor': 'black',
            'fontstyle': 'italic',
        }
    }

    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph