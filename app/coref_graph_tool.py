import random
import streamlit as st
import pandas as pd
from streamlit_tree_select import tree_select
import csv
from collections import *

def equiv_set(s):
    cur = {s}
    prev_len = len(cur)
    while True:
        for x in list(cur):
            cur.update(equiv_pairs.get(x,[]))
        if len(cur) == prev_len: break
        prev_len = len(cur)
    return list(cur)


def traverse(x, seen=None, dir="c"):
    D = children if dir == "c" else parents
    max_depth_of_child = defaultdict(int)
    senses = split_nodes.get(x, [x])
    k = [(s, "R", 0) for s in senses]
    while k:
        s, et, depth = k.pop()
        max_depth_of_child[s] = depth
        k.extend([(c, edge_types[(s,c)], depth+1) for c in D.get(s,[])])
    k = [(s, "R", 0) for s in senses]
    result = []
    while k:
        s, et, depth = k.pop()
        if depth < max_depth_of_child[s]: continue # we will get to this one later.
        equivs = equiv_set(s)
        equiv_string = "; ".join([e for e in equivs if e != x])
        # print(f"{'  ' * depth}{et}: {s} [{equiv_string}]")
        result.append((depth, et, s, equiv_string))
        k.extend([(c, edge_types[(s,c)], depth+1) for c in D.get(s,[])])
    # print(result)
    return result


def list_to_hierarchy(tree_list):
    hierarchy = []
    stack = [hierarchy]  # Using a stack to keep track of parent dictionaries
    prev_indent = -1
    used_values = set()

    for indent, label in tree_list:
        value = label
        suffix = 1

        while value in used_values:
            value = f"{label.lower().replace(' ', '_')}_{suffix}"
            suffix += 1

        node = {"label": label, "value": value}
        used_values.add(value)

        if indent > prev_indent:
            # If the current indentation is greater than the previous, append to the last dictionary in the stack
            stack[-1].append(node)
            stack.append(node.setdefault('children', []))
        elif indent < prev_indent:
            # If the current indentation is less than the previous, pop from the stack
            diff = prev_indent - indent
            for _ in range(diff + 1):
                stack.pop()

            stack[-1].append(node)
            stack.append(node.setdefault('children', []))
        else:
            stack[-2].append(node)
            stack.pop()
            stack.append(node.setdefault('children', []))

        prev_indent = indent

    return hierarchy


def render_df(phrase="", children_option=True, fathers_option=True):
    st.write("**Query Results:**")

    if phrase:
        query_phrase = phrase

    if query_phrase:
        try:
            l_hierarchy_children = []
            l_hierarchy_parents = []

            if children_option:
                hquery_result_children = traverse(query_phrase, dir="c")
                for depth, et, s, equiv_string in hquery_result_children:
                    et = "Children" if et == "R" else et
                    l_hierarchy_children.append((depth, f"{et}: {s} [{equiv_string}]"))

            if fathers_option:
                hquery_result_parents = traverse(query_phrase, dir="p")
                for depth, et, s, equiv_string in hquery_result_parents:
                    et = "Fathers" if et == "R" else et
                    l_hierarchy_parents.append((depth, f"{et}: {s} [{equiv_string}]"))

        except:
            st.write("Something went wrong")

    nodes = list_to_hierarchy(l_hierarchy_children + l_hierarchy_parents)
    tree_select(nodes, show_expand_all=True)


def surprise_me(unique_values):
    selected_value = random.choice(unique_values)
    st.write(f"**Querying:** {selected_value}")
    return selected_value


def main(data_path):
    st.set_page_config(layout="wide")
    df = pd.read_csv(data_path)
    # unique_values = pd.unique(df[['node1', 'node2']].values.ravel())
    unique_values = df['node1'].unique()

    st.title('Coreference Graph -Query Tool :)')
    st.write(
        'Please enter a query phrase into the following text box or click the Surprise Me button to get a random '
        'value in the graph. \n')
    st.write('Use the checkboxes to select which type of query you prefer.')
    query_phrase = st.text_input("**Query:**")
    surprise_button = st.button('Surprise Me!')
    children_option = st.checkbox('Children', value=True)
    fathers_option = st.checkbox('Fathers', value=True)

    if surprise_button:
        random_query = surprise_me(unique_values)
        render_df(random_query, children_option, fathers_option)
    elif query_phrase:
        render_df(query_phrase, children_option, fathers_option)


if __name__ == '__main__':
    path = "/app/data/full_graph_tagged5_2024-05-02_20:39.csv"

    children = defaultdict(list)
    parents = defaultdict(list)
    equiv_pairs = defaultdict(set)
    edge_types = {}
    split_nodes = defaultdict(set)

    fh = open(path, "r")
    next(fh)
    for _, n1, n2, w, kind in csv.reader(fh):
        if float(w) < 4: continue
        if kind[0] == "h":
            if kind[-1] in "56": continue
            children[n1].append(n2)
            parents[n2].append(n1)
            edge_types[(n1, n2)] = f"{kind[0]}{kind[-1]}"
            edge_types[(n2, n1)] = f"{kind[0]}{kind[-1]}"
        if kind[0] == "i":
            equiv_pairs[n1].add(n2)
            equiv_pairs[n2].add(n1)
        n1_base = n1.split(" [[[")[0]
        n2_base = n2.split(" [[[")[0]
        split_nodes[n1_base].add(n1)
        split_nodes[n2_base].add(n2)

    main(path)
