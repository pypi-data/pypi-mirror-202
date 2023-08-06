import os
from treelib import Tree, Node 
import numpy as np


def get_file_list(directory, file_extension=".pkl"):
    """
    Get the list of files with a specific extension in a directory and its subdirectories.
    :param directory: The directory to search for files.
    :param file_extension: The file extension to search for.
    :return: A list of file names with their absolute paths.
    """

    # Create an empty list to store the file names and their absolute paths
    file_list = []
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the absolute path of the file
            abs_path = os.path.abspath(os.path.join(root, file))
            
            # Add the file name and its absolute path to the list
            if file.endswith(file_extension):
                file_list.append( abs_path)

    return file_list

def dict_to_tree(data, parent_id=None, tree=None):
    """
    Convert a dictionary to a tree.
    :param data: The dictionary to convert.
    :param parent_id: The parent node id.
    :param tree: The tree object.
    :return: The tree object.

    # Convert the nested dictionary to a tree structure diagram
    tree = dict_to_tree(nested_dict)

    # Display the tree structure diagram
    tree.show()
    """

    if tree is None:
        tree = Tree()
        root_id = "root"
        tree.create_node(tag="Root", identifier=root_id)
        return dict_to_tree(data, parent_id=root_id, tree=tree)

    for key, value in data.items():
        node_id = f"{parent_id}.{key}" if parent_id else key
        tag = f"{key} ({type(value).__name__}"
        
        if isinstance(value, (list, tuple, np.ndarray)):
            tag += f", length: {len(value)}"
        elif isinstance(value, dict):
            tag += f", length: {len(value)}"
        elif isinstance(value, str):
            tag += f", length: {len(value)}"
            tag += f", value: {value}"
        elif isinstance(value, (int, float)):
            tag += f", value: {value}"
        
        tag += ")"
        
        tree.create_node(tag=tag, identifier=node_id, parent=parent_id)
        
        if isinstance(value, dict):
            dict_to_tree(value, parent_id=node_id, tree=tree)

    return tree


def func3():
    pass
