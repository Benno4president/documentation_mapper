import networkx as nx
import csv
import pandas as pd
import argparse
import pathlib
import ast

def simple_network_graph(df:pd.DataFrame):
    # ,origin,url,title,updated,doc_links,vid_links,text
    df.pop('origin')
    print(df)

    nodes = []
    edges = []
    for index, row in df.iterrows():
        links = row.pop('doc_links')
        node_url = row.pop('url')
        for edge in links:
            edges.append((node_url,edge))
        nodes.append((node_url, {**row, 'label':row['title'], 'type':'article'}))

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print("Done building network graph")
    return G



def parse_args():
    parser = argparse.ArgumentParser(prog='Link Graph Builder',description='Create map of page links.')
    parser.add_argument('file', type=pathlib.Path, help="CSV ingest.")
    return parser.parse_args()

if __name__ == '__main__':
    # Input file
    args = parse_args()

    doc_df = pd.read_csv(args.file, index_col=0, quotechar='"', encoding='utf8', doublequote=True, quoting=csv.QUOTE_NONNUMERIC, dtype=object, on_bad_lines='skip')
    doc_df['doc_links'] = doc_df['doc_links'].apply(lambda x: ast.literal_eval(x))


    graph = simple_network_graph(doc_df)

    output_file_network = "link_network.gexf"
    nx.write_gexf(graph, output_file_network)


