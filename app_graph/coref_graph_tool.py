import json
import os.path
import pickle
import random
import time
import streamlit as st
import pandas as pd
import csv
from collections import *
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import ConfigBuilder


@st.cache_data
def read_file(file, format):
    if format == "csv":
        return pd.read_csv(file)
    elif format == "pkl":
        return pickle.load(file)
    return


def query_dict(target):
    if target not in phrase2id_updated:
        return
    id_target = phrase2id_updated[target]
    # print(target, id_target)
    children_target = children_updated[id_target]
    # print(id_target, children_target)
    st.sidebar.write(str(len(children_target)) + " children were found !")
    for id_child in children_target:
        if len(nodes) > 200:
            break
        if id_child not in dict_com_updated:
            continue
        edges.append(Edge(source=id_target, target=id_child, type="CURVE_SMOOTH"))
        if id_target not in nodes_set:
            nodes.append(Node(id=id_target, label=str(dict_com_updated[id_target]), size=NODE_SIZE, ))
            nodes_set.add(id_target)
        if id_child not in nodes_set:
            nodes.append(Node(id=id_child, label=str(dict_com_updated[id_child]), size=NODE_SIZE, ))
            nodes_set.add(id_child)


def surprise_me(unique_values):
    selected_value = random.choice(unique_values)
    st.write(f"**Querying:** {selected_value}")
    return selected_value


def main():
    global dict_com_updated, phrase2id_updated, children_updated

    st.set_page_config(layout="wide")

    with open(dict_com_file, "rb") as f:
        dict_com_updated = read_file(f, "pkl")
    with open(phrase2id_file, "rb") as f:
        phrase2id_updated = read_file(f, "pkl")
    with open(children_file, "rb") as f:
        children_updated = read_file(f, "pkl")
    unique_ph = list([k for k, v in phrase2id_updated.items() if len(children_updated[v]) > 0])

    st.sidebar.title('Coreference Graph')
    query_phrase = st.sidebar.text_input("**Query:**")
    surprise_button = st.sidebar.button('Surprise Me!')

    if surprise_button:
        random_query = random.choice(unique_ph)
        st.sidebar.write(f"**Querying:** {random_query}...")
        query_dict(random_query)
    if query_phrase:
        query_dict(query_phrase.lower())
        if len(nodes) == 0:
            st.write("No results to display. Please try another query.")
    config_path = "/Users/shir/PycharmProjects/Coreference-Graph/app_graph/config.json"
    if os.path.exists(config_path):
        config = Config(from_json=config_path)
    else:
        config_builder = ConfigBuilder(nodes)
        config = config_builder.build()
        # config.save(config_path)
    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)


if __name__ == '__main__':
    dict_com_file = "app_graph/data/dict_com_updated1.pkl"
    phrase2id_file = "/Users/shir/PycharmProjects/Coreference-Graph/app_graph/data/phrase2id_updated1.pkl"
    children_file = "/Users/shir/PycharmProjects/Coreference-Graph/app_graph/data/children_updated.pkl"
    NODE_SIZE = 10

    nodes = []
    edges = []
    nodes_set = set()

    main()
