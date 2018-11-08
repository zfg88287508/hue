import re


def pre_order_graph(node, nodes, edges, parent):
    match = re.search("(.*?)\s\(id=(\d+)\)", node.val.name)
    if match:
        if parent:
            edges.append("node_%s -> %s;" % (match.group(2), parent))
        nodes.append("node_%s [label=\"%s\"];" % (match.group(2),
                                                  match.group(1)))
        for c in node.children:
            pre_order_graph(c, nodes, edges, "node_%s" % (match.group(2), ))


def graph_to_dot(fragments):
    """Parse the list of fragements to build the graph"""
    # get all nodes of the fragement
    nodes = []
    edges = []
    for f in fragments:
        parent = None
        for c in f.children:
            dst = re.search("dst_id=(\d+)", c.val.name)
            if dst:
                parent = "node_%s" % (dst.group(1))
            pre_order_graph(c, nodes, edges, parent)

    return """ digraph q { %s %s } """ % (
        " ".join(nodes),
        " ".join(edges)
    )
