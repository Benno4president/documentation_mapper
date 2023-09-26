import networkx as nx
import csv
import pandas as pd
import argparse
import pathlib
import ast
from pathlib import Path

def simple_network_graph(df:pd.DataFrame):
    # ,origin,url,title,updated,doc_links,vid_links,text
    df.pop('origin')
    print(df)

    nodes = []
    edges = []
    for index, row in df.iterrows():
        links = row.pop('doc_links')
        vids = row.pop('vid_links')
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


def get_graph(file:str):
    # Input file
    doc_df = pd.read_csv(args.file, index_col=0, quotechar='"', encoding='utf8', doublequote=True, quoting=csv.QUOTE_NONNUMERIC, dtype=object, on_bad_lines='skip')
    doc_df['doc_links'] = doc_df['doc_links'].apply(lambda x: ast.literal_eval(x))
    doc_df['vid_links'] = doc_df['vid_links'].apply(lambda x: ast.literal_eval(x))
    g = simple_network_graph(doc_df)
    return g

    graph = simple_network_graph(doc_df)
if __name__ == '__main__':
    args = parse_args()
    graph = get_graph(args.file)
    in_file_root = Path(args.file).stem #or 'unknown'
    output_file_network = f"{in_file_root}_network.gexf"
    nx.write_gexf(graph, output_file_network)
    print('Saved as:', output_file_network)


