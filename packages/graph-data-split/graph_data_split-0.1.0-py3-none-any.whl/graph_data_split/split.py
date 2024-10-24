import numpy as np
import random
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import copy
import sys
import pickle
import math

def split_list(d_list, n_folds, seed):
    '''
    :param d_list: list of tuples where each drug pairs or list of drugs or list of cell lines.
    :param n_folds: In how many folds to split the drug_combs list
    :return: a dict where key=fold number, value=list of drug_pairs in that fold.
    '''
    #split in n_folds
    random.Random(seed).shuffle(d_list)

    split_size= int(len(d_list) / n_folds)
    folds= {i: d_list[split_size * i: split_size * (i + 1)] for i in range(n_folds-1)}
    folds[n_folds-1] = d_list[split_size*(n_folds-1):]

    return folds

def verify_split(df, train_idx, test_idx, split_type):
    '''

    :return: Given a df with sample data (e.g., synergy triplets), verify that the train and test
    data have been created properly according to the split type.
    '''
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]

    if split_type=='random':
        test_triplets = set(zip(test_df['source'],test_df['target'],test_df['edge_type']))
        train_triplets = set(zip(train_df['source'],train_df['target'],train_df['edge_type']))
        n_common = len(test_triplets.intersection(train_triplets))
        assert n_common == 0, print(f'error in {split_type} split')


    if split_type=='leave_comb':
        test_edges = set(zip(test_df['source'],test_df['target']))
        train_edges = set(zip(train_df['source'],train_df['target']))
        n_common = len(test_edges.intersection(train_edges))
        assert n_common == 0, print(f'error in {split_type} split')


    if split_type=='leave_drug':
        test_nodes = set(test_df['source']).union(set(test_df['target']))
        train_nodes = set(train_df['source']).union(set(train_df['target']))
        n_common = len(test_nodes.intersection(train_nodes))
        assert n_common == 0, print(f'error in {split_type} split')


    if split_type=='leave_cell_line':
        test_edge_type = set(test_df['edge_type'])
        train_edge_type = set(train_df['edge_type'])
        n_common = len(test_edge_type.intersection(train_edge_type))
        assert n_common == 0, print(f'error in {split_type} split')


def get_random_train_test(df, test_frac=0.2, seed=None):
    indices = list(range(len(df)))
    train_idx, test_idx = train_test_split(indices, test_size=test_frac, random_state=seed)
    return train_idx, test_idx

def get_edge_split_train_test(df, test_frac, seed=None):
    '''
        Input: synergy_df = a dataframe with atleast two columns ['source','target'].

        Function: edge appearing in train (irrespective of the edge type) will not appear in test.
    '''

    df['ID'] = list(range(len(df)))

    edges = list(set(zip(df['source'], df['target'])))  #make sure that edges are unique.
    # as I used set() to get unique edges, we will lose the initial order of edges. Hence, we need to sort the edges. Otherwise the same edges can appear in different
    # order in different runs, thus using random_state=int(e.g., 42) will not ensure the reproducible split each time on the same dataset.
    edges.sort()
    #split edges into train and test set
    train_edges, test_edges = train_test_split(edges, test_size=test_frac, random_state=seed)

    test_idx = list(df[df[['source','target']].apply(tuple, axis=1).isin(test_edges)]['ID'])
    train_idx = list(df['ID'].drop(test_idx))

    df.drop(columns='ID', inplace=True)

    return train_idx, test_idx



def get_node_split_train_test(df, test_frac, seed=None):

    '''
    Function: Split the nodes appear in source or target into train test. Then split the samples (e.g., triplets)
    training samples only contain training nodes and the same for test samples.
    '''
    df['ID'] = list(range(len(df)))

    nodes = list(set(df['source']).union(set(df['target'])))
    # as I used set() to get unique nodes, we will lose the initial order of nodes. Hence, we need to sort the nodes. Otherwise the same nodes can appear in different
    # order in different runs, thus using random_state=int(e.g., 42) will not ensure the reproducible split each time on the same dataset.
    nodes.sort()

    count=0
    while True:
        count+=1

        # split nodes into train and test set
        train_nodes, test_nodes = train_test_split(nodes, test_size=test_frac, random_state=seed)

        #both source and target has to be in test_nodes for a triplet or edge to be considered in test dataset.
        test_idx = list(df[(df['source'].isin(test_nodes)) & (df['target'].isin(test_nodes))]['ID'])

        train_idx = list(df[(df['source'].isin(train_nodes)) & (df['target'].isin(train_nodes))]['ID'])

        if (len(test_idx)>0) and (len(train_idx)>0): #make sure that we don't get empty test or train dataset
            break

        if isinstance(seed, (int)):
            print('Failed to split nodes such that train and test dataset are not empty. Try using random_state=None or np.random.RandomState or a different integer value than the current one ')
            sys.exit(1)

        if count>1000:
            print('Failed to split nodes such that train and test dataset are not empty. Tried 1000 times ')
            sys.exit(1)

    df.drop(columns='ID', inplace=True)
    return train_idx, test_idx




def get_edge_type_split_train_test(df, test_frac, seed=None):
    '''
       Function: Split the nodes appear in source or target into train test. Then split the samples (e.g., triplets)
       training samples only contain training nodes and the same for test samples.
       '''
    df['ID'] = list(range(len(df)))

    edge_types = list(df['edge_type'].unique())
    edge_types.sort()


    # split nodes into train and test set
    train_edge_types, test_edge_types = train_test_split(edge_types, test_size=test_frac, random_state=seed)

    # both source and target has to be in test_nodes for a triplet or edge to be considered in test dataset.
    test_idx = list(df[(df['edge_type'].isin(test_edge_types))]['ID'])
    train_idx = list(df['ID'].drop(test_idx))


    df.drop(columns='ID', inplace=True)
    return train_idx, test_idx



def get_random_n_split(df, n_folds, seed=None):
    '''
    df: columns = ['source', 'target']
    function:  If edge with a certain edge_type appear in train, the same edge with the same edge_type will not
    appear in test. However, the same edge (i.e., same source and target) from another edge type may appear in test.
    '''

    indices = list(range(len(df)))
    fold_size = int(len(indices)/n_folds)

    remaining_idx = copy.deepcopy(indices)
    train_idx = {}
    val_idx = {}
    for i in range(n_folds):
        val_idx[i] = random.Random(seed).sample(remaining_idx, fold_size)
        train_idx[i] = list(set(indices).difference(set(val_idx[i])))
        remaining_idx = list(set(remaining_idx).difference(set(val_idx[i])))

    return train_idx, val_idx

def get_edge_n_split(df, n_folds, seed=None):
    '''
        Input: synergy_df = a dataframe with atleast two columns ['source','target'].

        Function: edge appearing in train (irrespective of the edge type) will not appear in test.
    '''
    df['ID'] = list(range(len(df)))

    edges = list(set(zip(df['source'], df['target'])))  # list of tuples
    edges.sort()

    #prepare train and val split
    edge_folds = split_list(edges, n_folds, seed=seed)

    df_split = {i: df[df[['source','target']].apply(tuple, axis=1).isin(edge_folds[i])] for i in range(n_folds)}

    train_idx = {}
    val_idx = {}
    for i in range(n_folds):
        val_idx[i] = list(df_split[i]['ID'])
        train_idx[i] = list(df['ID'].drop(val_idx[i]))

    df.drop(columns='ID', inplace=True)

    return train_idx, val_idx



def get_node_n_split(df, n_folds, seed=None):

    '''
    Function: Split the nodes appear in source or target into train test. Then split the samples (e.g., triplets)
    training samples only contain training nodes and the same for test samples.
    '''

    df['ID'] = list(range(len(df)))

    nodes = list(set(df['source']).union(set(df['target']))) # list of tuples
    nodes.sort()

    # now create 5 folds from the remaining drug and use each fold as val and the rest as train
    node_folds = split_list(nodes, n_folds, seed)

    df_split = {i: df[(df['source'].isin(node_folds[i])) & (df['target'].isin(node_folds[i]))]  for i in range(n_folds)}

    #catch: we will assign fold to triplets. It's expected that the triplets containing drugs from both
    # val and training set will not be used in training or validation. However, concatenate
    # triplets from the above 5 splits/folds will reduce the data unnecessarily. Let say, fold1 is validation fold.
    #In this case, any triplets containing drug from fold 2 and 3 should be part of training.
    train_idx = {}
    val_idx = {}
    for i in range(n_folds):
        val_idx[i] = list(df_split[i]['ID'])
        train_df = df[~(df['source'].isin(node_folds[i]) | df['target'].isin(node_folds[i]))]
        train_idx[i] = list(train_df['ID'])

    df.drop(columns='ID', inplace=True)

    return train_idx, val_idx




def get_edge_type_n_split(df, n_folds, seed=None):

    '''
    :param df:
    :param n_folds:


    :return:
    '''
    df['ID'] = list(range(len(df)))

    edge_types = list(df['edge_type'].unique())# list of strings
    edge_types.sort()

    # now create 5 folds from the remaining drug and use each fold as val and the rest as train
    edge_type_folds = split_list(edge_types, n_folds, seed)

    df_split = {i: df[df['edge_type'].isin(edge_type_folds[i])]  for i in range(n_folds)}

    train_idx = {}
    val_idx = {}
    for i in range(n_folds):
        val_idx[i] = list(df_split[i]['ID'])
        train_idx[i] = list(df['ID'].drop(val_idx[i]))

    df.drop(columns='ID', inplace=True)

    return train_idx, val_idx





# def wrapper_train_test(df, split_type, test_frac, spec_dir, force_run=True):
#     '''Rename column names to more generalized ones. Also, convert drug and cell line ids to numerical ids compatible with models.'''
#
#
#     split_type_2_function_map = {'random': get_random_train_test, 'leave_comb': get_edge_split_train_test,
#                       'leave_drug':get_node_split_train_test, 'leave_cell_line':get_edge_type_split_train_test}
#
#     test_file = f'{spec_dir}/test.tsv'
#     train_file = f'{spec_dir}/train.tsv'
#
#     all_triplets_file = f'{spec_dir}/all.tsv'
#     drug_idx_file = f'{spec_dir}/drug_2_idx.tsv'
#     cell_idx_file = f'{spec_dir}/cell_line_2_idx.tsv'
#
#     summary = f'{spec_dir}/train_test_summary.txt'
#
#     if (not os.path.exists(test_file)) or (force_run):
#         df, drug_2_idx, cell_line_2_idx = generalize_data(df)
#
#         # df['ID'] = list(range(len(df)))
#         print('Creating train test folds')
#         train_df, test_df = split_type_2_function_map[split_type](df, test_frac)
#         #save in file
#         # test_df.drop(columns='ID', inplace=True)
#         # train_df.drop(columns='ID', inplace=True)
#         # df.drop(columns='ID', inplace=True)
#         drug_2_idx_df = pd.DataFrame({'pid': list(drug_2_idx.keys()), 'idx': list(drug_2_idx.values())})
#         cell_2_idx_df = pd.DataFrame({'cell_line_name': list(cell_line_2_idx.keys()), 'idx': list(cell_line_2_idx.values())})
#
#
#         os.makedirs(spec_dir, exist_ok=True)
#         test_df.to_csv(test_file, sep='\t')
#         train_df.to_csv(train_file, sep='\t')
#         df.to_csv(all_triplets_file, sep='\t')
#         drug_2_idx_df.to_csv(drug_idx_file, sep='\t')
#         cell_2_idx_df.to_csv(cell_idx_file, sep='\t')
#
#
#     else:
#         print('Loading train test folds')
#         test_df = pd.read_csv(test_file, sep='\t', dtype={'drug_1_pid':str, 'drug_2_pid': str})
#         train_df = pd.read_csv(train_file, sep='\t', dtype={'drug_1_pid':str, 'drug_2_pid': str})
#         df = pd.read_csv(all_triplets_file, sep='\t', dtype={'drug_1_pid':str, 'drug_2_pid': str})
#
#         drug_2_idx_df = pd.read_csv(drug_idx_file, dtype={'pid':str}, sep='\t')
#         drug_2_idx = dict(zip(drug_2_idx_df['pid'], drug_2_idx_df['idx']))
#
#         cell_line_2_idx_df = pd.read_csv(cell_idx_file, sep='\t')
#         cell_line_2_idx = dict(zip(cell_line_2_idx_df['cell_line_name'],cell_line_2_idx_df['idx']))
#
#     verify_split(train_df, test_df, split_type)
#
#     test_drugs = set(test_df['source']).union(set(test_df['target']))
#     test_cell_lines = set(test_df['edge_type'])
#     print(f'TEST #triplets: {len(test_df)} \n #drugs: {len(test_drugs)}'
#           f' \n #cell lines: {len(test_cell_lines)}')
#
#     with open(summary, 'w') as file:
#         file.write(f'TEST #triplets: {len(test_df)} \n #drugs: {len(test_drugs)}'
#           f' \n #cell lines: {len(test_cell_lines)}')
#     file.close()
#     return train_df, test_df, drug_2_idx, cell_line_2_idx
#
# def wrapper_nfold_split(df, split_type, n_folds, spec_dir, force_run=True):
#
#     df['ID'] = list(range(len(df)))
#     split_type_2_function_map = {'random': get_random_n_split, 'leave_comb': get_edge_n_split,
#                       'leave_drug':get_node_n_split, 'leave_cell_line':get_edge_type_n_split}
#
#     val_file = f'{spec_dir}/val_nfolds.pkl'
#     train_file = f'{spec_dir}/train_nfolds.pkl'
#     summary = f'{spec_dir}/n_fold_summary.txt'
#
#     if (not os.path.exists(train_file)) or (force_run):
#         print('Creating train val folds')
#         train_idx, val_idx = split_type_2_function_map[split_type](df, n_folds)
#         os.makedirs(spec_dir, exist_ok=True)
#         with open(val_file, 'wb') as file:
#             pickle.dump(val_idx, file)
#         with open(train_file, 'wb') as file:
#             pickle.dump(train_idx, file)
#
#
#     else:
#         print('Loading train val folds')
#         with open(val_file, 'rb') as file:
#             val_idx = pickle.load(file)
#         with open(train_file, 'rb') as file:
#             train_idx = pickle.load(file)
#
#     #verify splits
#     for i in range(n_folds):
#         foldwise_train_df = df[df['ID'].isin(train_idx[i])]
#         foldwise_val_df = df[df['ID'].isin(val_idx[i])]
#         verify_split(foldwise_train_df,foldwise_val_df, split_type)
#
#     file = open(summary, 'w')
#     for i in range(n_folds):
#         print(f'fold {i} # TRAIN triplets:  {len(train_idx[i])}')
#         print(f'fold {i} # VAL triplets:  {len(val_idx[i])}')
#         file.write(f'fold {i} # TRAIN triplets:  {len(train_idx[i])}'
#                    f'\n fold {i} # VAL triplets:  {len(val_idx[i])} \n')
#     file.close()
#     return train_idx, val_idx



