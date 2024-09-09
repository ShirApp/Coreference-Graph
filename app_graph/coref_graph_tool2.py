import json
import math
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


def query_children(target, family_type):
    if target in phrase2id_updated:
        id_target = phrase2id_updated[target]

        family_of_target = list(children_updated[id_target]) if family_type == "children" else list(
            parents_updated[id_target])
        num_of_chunks = math.ceil(len(family_of_target) / CHUNK_SIZE)

        return family_of_target, num_of_chunks

    return


def display_children(target, family_of_target, family_type, chunk_num=0):
    id_target = phrase2id_updated[target]
    if st.session_state.nodes:
        st.session_state.nodes = []
        st.session_state.edges = []

    st.session_state.nodes.append(Node(id=id_target, label=str(dict_com_updated[id_target]), size=NODE_SIZE, ))
    for id_neigh in family_of_target[chunk_num * CHUNK_SIZE: (chunk_num + 1) * CHUNK_SIZE]:
        if family_type == "parents":
            st.session_state.edges.append(Edge(source=id_neigh, target=id_target, type="CURVE_SMOOTH"))
        else:
            st.session_state.edges.append(Edge(source=id_target, target=id_neigh, type="CURVE_SMOOTH"))

        st.session_state.nodes.append(Node(id=id_neigh, label=str(dict_com_updated[id_neigh]), size=NODE_SIZE, ))


def main():
    global dict_com_updated, phrase2id_updated, children_updated, parents_updated

    st.set_page_config(layout="wide")

    with open(dict_com_file, "rb") as f:
        dict_com_updated = read_file(f, "pkl")
    with open(phrase2id_file, "rb") as f:
        phrase2id_updated = read_file(f, "pkl")
    with open(children_file, "rb") as f:
        children_updated = read_file(f, "pkl")
    with open(parents_file, "rb") as f:
        parents_updated = read_file(f, "pkl")

    st.sidebar.title('Coreference Graph')
    query_phrase = st.sidebar.text_input("**Query:** [for example: 'il-8', 'cancer']")
    family_type_radio = st.sidebar.radio(label="**Explore:**", options=["children", "parents"])

    next_button = None

    if query_phrase:
        if st.session_state.num_chunks > 1:
            st.write("The nodes are presented in chunks of size", CHUNK_SIZE)
            st.write("Chunk number", st.session_state.counter + 1, "out of", st.session_state.num_chunks)
            next_button = st.button('Next Chunk')

        if not next_button:
            family_of_target, num_of_chunks = query_children(query_phrase.lower(), family_type_radio)
            display_children(query_phrase.lower(), family_of_target, family_type_radio)
            st.session_state.counter = 1
            st.session_state.num_chunks = num_of_chunks
            st.session_state.family_target = family_of_target

            if len(st.session_state.nodes) == 0:
                st.write("No results to display. Please try another query.")
            if st.session_state.num_chunks > 1:
                st.write("the nodes are presented in chunks of size", CHUNK_SIZE)
                st.write("chunk number", st.session_state.counter, "out of", st.session_state.num_chunks)
                next_button = st.button('Next Chunk')
        else:
            display_children(query_phrase.lower(), st.session_state.family_target, family_type_radio,
                                 st.session_state.counter)
            st.session_state.counter += 1
        st.sidebar.write(str(len(st.session_state.family_target)), family_type_radio, "were found!")

    print("chunk_index", st.session_state.counter)

    config_path = "/Users/shir/PycharmProjects/Coreference-Graph/app_graph/config.json"
    if os.path.exists(config_path):
        config = Config(from_json=config_path)
    else:
        config_builder = ConfigBuilder(st.session_state.nodes)
        config = config_builder.build()
        # config.save(config_path)
    return_value = agraph(nodes=st.session_state.nodes,
                          edges=st.session_state.edges,
                          config=config)


dict_com_file = "data/dict_com_updated4.pkl"
phrase2id_file = "data/phrase2id_updated4.pkl"
children_file = "data/children_updated4.pkl"
parents_file = "data/parents_updated4.pkl"
NODE_SIZE = 10
CHUNK_SIZE = 50

if "counter" not in st.session_state:
    st.session_state.counter = 0
if "nodes" not in st.session_state:
    st.session_state.nodes = []
if "edges" not in st.session_state:
    st.session_state.edges = []
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0
if "family_target" not in st.session_state:
    st.session_state.family_target = []

main()
