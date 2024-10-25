import json

import pandas
import treelib
from treelib import Tree
import numpy as np
import pandas as pd
def find_node_by_tag(tree, tag):
    """通过节点的tag在树中查找"""
    for node in tree.all_nodes():
        if node.tag == tag:
            return node
    else:
        return None

def sys_add_branch_nodes(tree, node_name, names1, names2, names3):
    """为tree_sys添加分支节点"""
    node = find_node_by_tag(tree, node_name)
    node_child_num = len(tree.children(node.identifier))
    node_id = 'system ' if node.identifier == 'rootsystem' else node.identifier+'.'
    for i, name1 in enumerate(names1):
        id_1 = node_id + str(i + 1 + node_child_num)
        tree.create_node(name1, id_1, node.identifier)
        if names2:
            for j, name2 in enumerate(names2[i]):
                id_2 = node_id + str(i + 1 + node_child_num) + '.' + str(j + 1)
                tree.create_node(name2, id_2, id_1)
                if names3:
                    for k, name3 in enumerate(names3[i][j]):
                        id_3 = node_id + str(i + 1 + node_child_num) + '.' + str(j + 1) + '.' + str(k + 1)
                        tree.create_node(name3, id_3, id_2)


def tree_sys(rootname: str, name_lev1: list, name_lev2: list = None, name_lev3: list = None, tree=None):
    """
    系统树，创建tree或向tree中添加分支
    :param rootname: 节点名称（必填）
    :param name_lev1: 第一层节点列表（必填）
    :param name_lev2: 第二层节点列表（可选）
    :param name_lev3: 第三层节点列表（可选）
    :param tree: 传入表示向tree中添加分支，不传入表示新建tree（可选）
    :return: 系统树tree
    """
    # tree为空先新创建树
    if tree is None:
        tree = treelib.Tree()
        tree.create_node(rootname, 'rootsystem')  # 创建根节点
        # 增加分支节点
        sys_add_branch_nodes(tree, rootname, name_lev1, name_lev2, name_lev3)
    else:
        # tree存在rootname则直接新增分支
        node = find_node_by_tag(tree, rootname)
        if node is not None:  # rootname节点存在，直接增加分支
            sys_add_branch_nodes(tree, rootname, name_lev1, name_lev2, name_lev3)
        else:  # rootname节点不存在，新建后再增加分支
            print('树中没有', rootname, '，在树的根节点下创建')
            num = len(tree.children('rootsystem'))
            tree.create_node(rootname, 'system ' + str(num + 1), 'rootsystem')
            sys_add_branch_nodes(tree, rootname, name_lev1, name_lev2, name_lev3)
    return tree

def tree_ele(dimension: str, root_ele: str, ele: str, eleid: str, eleprop: str, elevar: list, tree=None):
    """
    单元树，创建tree或向tree中添加分支
    :param dimension: person(人员), machine(机器), product(产品),
    :param root_ele: 根节点名称
    :param ele: 单元名（一级节点）
    :param eleid: 单元的名称（二级节点）
    :param eleprop: 单元的特性（二级节点）
    :param elevar: 单元的特性变量（三级节点）
    :param tree: 传入表示向tree中添加分支，不传入表示新建tree（可选）
    :return: 单元树tree
    """
    if dimension not in ['person', 'machine', 'product']:
        print('维度输入错误')
        return None
    root_name = root_ele+'_'+dimension
    if tree is None:
        tree = treelib.Tree()
        tree.create_node(root_name, root_name)  # 创建根节点

    node_child_num = len(tree.children(tree.all_nodes()[0].identifier))

    ele_idf = dimension + ' ' + str(node_child_num + 1)
    tree.create_node(ele, ele_idf, root_name)  # 创建单元名（一级节点）
    tree.create_node(eleid, dimension + 'id ' + str(node_child_num + 1), ele_idf)  # 创建单元的名称（二级节点）
    tree.create_node(eleprop, dimension + 'prop ' + str(node_child_num + 1), ele_idf)  # 创建单元的特性（二级节点）
    for i, var in enumerate(elevar):
        tree.create_node(var, dimension + 'var ' + str(node_child_num + 1) + '.' + str(i+1),
                         dimension + 'prop ' + str(node_child_num + 1))  # 创建单元的特性变量（三级节点）
    return tree
def tree_to_df(tree, index_num=None, columns_num=None, index_levels=None, columns=None) -> pd.DataFrame:
    """
    获取从根节点到叶子节点的路径，并将ID替换为TAG，返回一个df。
    根据路径字典生成df，多级索引的层数可以根据用户输入的index_num选择。
    未选择的层级将作为值保留，columns_num决定列的数量。
    如果index_num超过路径层次或其他参数不匹配则报错。
    Args:
        tree (Tree): treelib中的树结构。
        index_num: 选择的多级索引层数，默认为路径的最大层数
        columns_num: DataFrame列的数量，默认为None
        index_levels: 多级索引的列名，默认使用 ['level_1', 'level_2', ..., 'level_n']
        columns: 除未选择层级外的其他列名，默认为 ['column_1', 'column_2', ..., 'column_n']

    Returns:
        包含从根节点到叶子节点路径的DataFrame，路径以节点TAG表示。


    """
    # 获取所有从根节点到叶子节点的路径
    paths = tree.paths_to_leaves()

    # 检查路径的最大层数
    max_depth = max(len(path) for path in paths)

    # 如果没有指定index_num，默认使用最大深度
    if index_num is None:
        index_num = max_depth

    # 如果指定的index_num超过了路径的最大深度，报错
    if index_num > max_depth:
        raise ValueError(f"输入的index_num超过了路径的层次，路径最大层次为 {max_depth}")

    # 检查 index_levels 的长度是否匹配 index_num
    if index_levels is not None and len(index_levels) != index_num:
        raise ValueError(f"提供的index_levels长度 ({len(index_levels)}) 不等于index_num ({index_num})")

    # 如果没有指定index_levels，默认使用 ['level_1', 'level_2', ..., 'level_n']
    if index_levels is None:
        index_levels = [f'level_{i + 1}' for i in range(index_num)]

    # 如果columns为None且columns_num为NaN，默认columns_num为2
    if columns_num is None and columns is None:
        columns_num = 2

    # 如果传入了columns且columns_num为NaN，则columns_num等于columns的长度
    if columns is not None and columns_num is None:
        columns_num = len(columns)

    # 如果用户提供的columns长度大于columns_num，报错
    if columns is not None and len(columns) > columns_num:
        raise ValueError(f"提供的columns长度 ({len(columns)}) 超过了columns_num ({columns_num})")

    # 如果columns不够columns_num长度，补齐
    if columns is None:
        columns = [f'column_{i + 1}' for i in range(columns_num)]
    elif len(columns) < columns_num:
        columns += [f'column_{i + 1}' for i in range(len(columns), columns_num)]

    # 将路径从ID转换为TAG，并构建字典
    paths_dict = {}
    for i, path in enumerate(paths):
        # 使用tag替代id
        tag_path = [tree.get_node(node_id).tag for node_id in path]
        paths_dict[f"path_{i + 1}"] = tag_path

    # 切割路径为多级索引部分和剩余层级部分
    truncated_paths = [tuple(path[:index_num]) for path in paths_dict.values()]
    remaining_levels = [path[index_num:] for path in paths_dict.values()]

    # 转换为多级索引
    multi_index = pd.MultiIndex.from_tuples(truncated_paths, names=index_levels)

    # 将剩余层级转为DataFrame列，值为剩下的路径层级
    remaining_columns = pd.DataFrame(remaining_levels, index=multi_index,
                                     columns=[f"level_{i + 1}" for i in range(index_num, max_depth)])

    # 创建DataFrame，值为NaN，并结合剩余层级的列
    df = pd.DataFrame(np.nan, index=multi_index, columns=columns)

    # 将剩余的层级与空的DataFrame合并
    df = pd.concat([df, remaining_columns], axis=1)
    # 替换 NaN 为 None
    df = df.map(lambda x: None if pd.isna(x) else x)

    return df


def df_to_tree(df) -> treelib.Tree:
    """
    将 DataFrame 的 MultiIndex 转换为树结构，并将行的值作为叶子节点添加到树中。
    Args:
        df(pd.DataFrame):包含 MultiIndex 的 DataFrame，其索引层次及对应的行值将被转换为树结构。

    Returns:
        返回由 DataFrame 的 MultiIndex 构建的树结构，并将行的值作为叶节点附加。

    """
    # 初始化树
    tree = Tree()

    # 遍历 DataFrame 的 MultiIndex，并附加行值作为叶节点
    for idx_tuple, row_values in df.iterrows():
        current_parent = None  # 没有根节点，直接从第一个索引级别开始
        for i, level in enumerate(idx_tuple):
            if pd.notna(level):  # 确保不处理 None 或 NaN 值
                # 如果 current_parent 为空，说明这是树的顶层节点
                if current_parent is None:
                    if not tree.contains(level):
                        tree.create_node(level, level)  # 顶层节点
                else:
                    if not tree.contains(level):
                        tree.create_node(level, level, parent=current_parent)  # 子节点
                current_parent = level

        # 将行的所有值作为叶节点添加到树中
        for i, value in enumerate(row_values):
            if value is not None:
                tree.create_node(tag=value, identifier=value, parent=current_parent)

    return tree


from treelib import Tree


def create_tree(supname, name, subname=None, origin=None):
    """
    构建或合并树结构。
    该方法用于创建或合并一棵树，提供一个根节点（supname）、二级节点（name 列表），
    以及每个二级节点的子节点（subname 列表）。如果提供了 origin 树，则在该树的基础上进行合并；
    如果 supname 已经在 origin 树中，则合并新的节点；否则，创建一棵新的树。

    参数:
    supname (str): 根节点的名称。作为树的一级节点。
    name (list of list of str): 每个子列表代表 supname 的直接子节点的名称列表。
    subname (list of list of str, optional): 每个子列表表示对应 name 节点的子节点，默认为 None。
    origin (Tree, optional): 现有树对象。如果提供，将在此基础上进行节点合并。默认为 None。

    返回:
    Tree: 构建或合并后的树结构。如果 `supname` 不存在于 `origin` 中，则返回一棵新的树。
    如果 `origin` 不为空且包含 `supname`，则对原树进行修改并返回。

    逻辑:
    - 如果 origin 为空，或者 origin 中不包含 supname，创建一个新树，supname 作为根节点。
    - 遍历 name 列表：
        - 为每个子列表中的 name 创建子节点，如果节点不存在则添加到树中。
        - 如果提供了 subname 且对应的子列表存在，则为 name 的每个子节点添加子节点。
    """
    # 如果 origin 为空，或者 origin 中不包含 supname，创建新树
    if origin is None or not origin.contains(supname):
        tree = Tree()
        tree.create_node(supname, supname)  # 创建根节点
    else:
        # 如果 origin 存在并且包含 supname，则直接使用 origin 进行扩展
        tree = origin

    # 添加 name 节点和对应的 subname 节点
    for idx, node_list in enumerate(name):
        for node_name in node_list:
            # 检查 name 节点是否已存在于树中
            if not tree.contains(node_name):
                tree.create_node(node_name, node_name, parent=supname)  # 如果不存在则创建 name 节点

            # 如果 subname 不为 None，则添加子节点
            if subname is not None and idx < len(subname):
                for sub_node_name in subname[idx]:
                    # 检查子节点是否已存在于树中
                    if not tree.contains(sub_node_name):
                        tree.create_node(sub_node_name, sub_node_name, parent=node_name)  # 如果不存在则创建子节点

    return tree


def tree_to_json(tree: treelib.Tree) -> str:
    """将treelib的Tree对象转换为通用json对象
    Args:
        tree (treelib.Tree): 要转换的树对象
    Returns:
        str: 树结构的JSON字符串表示
    """

    def node_to_dict(node):
        """将树节点转换为字典格式。
        Args:
            node: 要转换的树节点
        Returns:
            dict: 包含节点信息的字典
        """
        children = tree.children(node.identifier)
        return {
            'id': node.identifier,
            'name': node.tag,
            'data': node.data,
            'children': [node_to_dict(child) for child in children]
        }

    root = tree.get_node(tree.root)
    return json.dumps(node_to_dict(root), ensure_ascii=False)
