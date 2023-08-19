import networkx as nx
import csv
import pandas as pd

def simple_network_graph(df:pd.DataFrame):
    # ,origin,url,title,updated,doc_links,vid_links,text
    df.pop('origin')
    print(df)

    nodes = []
    edges = []
    for index, row in df.iterrows():
        for edge in row['doc_links']:
            edges.append((row['url'],edge))
        nodes.append((row['url'], {**row, 'label':row['title']}))


    #network_doc_set = set()
    #network_word_set = set()
    #network_edge_list = []
    #network_word_set.add(word)
    #network_edge_list.append((doc_id,word,{"count":count}))
#
    ## Build the nodes
    #nodes = []
    #if row[id_key] in network_doc_set:
    #    nodes.append((row[id_key], {**row, 'label':row[id_key], 'type':'document'}))
#
    #    nodes.append((row[word_key], {**row, 'label':row[word_key], 'type':'term'}))
#
    ## Build edges
    #edges = network_edge_list
#
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print("Done building network graph")
    return G


if __name__ == '__main__':
    # Input file
    input_file = "xfetcher_planday_452.csv"

    doc_df = pd.read_csv(input_file, index_col=0, quotechar='"', encoding='utf8', doublequote=True, quoting=csv.QUOTE_NONNUMERIC, dtype=object, on_bad_lines='skip')
    
    graph = simple_network_graph(doc_df)

    output_file_network = "link_network.gexf"
    nx.write_gexf(graph, output_file_network)


