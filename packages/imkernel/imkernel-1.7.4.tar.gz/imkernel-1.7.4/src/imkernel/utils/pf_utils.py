import pandas as pd
import treelib


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
    node_id = 'system ' if node.identifier == 'rootsystem' else node.identifier + '.'
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


def tree_sys(supsys: list, sys: list = None, name_lev3: list = None, tree=None):
    """
    系统树，创建tree或向tree中添加分支
    :param supsys: 第一层节点列表（必填）
    :param sys: 第二层节点列表（可选）
    :param name_lev3: 第三层节点列表（可选）
    :param tree: 传入表示向tree中添加分支，不传入表示新建tree（可选）
    :return: 系统树tree
    """
    # tree为空先新创建树
    root_name = 'insofsys'
    if tree is None:
        tree = treelib.Tree()
        tree.create_node(root_name, 'rootsystem')  # 创建根节点
    elif isinstance(tree, str):
        root_name = tree
        tree = treelib.Tree()
        tree.create_node(root_name, 'rootsystem')  # 创建根节点
        # 增加分支节点
        sys_add_branch_nodes(tree, root_name, supsys, sys, name_lev3)
    else:
        # tree存在rootname则直接新增分支
        node = find_node_by_tag(tree, root_name)
        if node is not None:  # rootname节点存在，直接增加分支
            sys_add_branch_nodes(tree, root_name, supsys, sys, name_lev3)
        else:  # rootname节点不存在，新建后再增加分支
            print('树中没有', root_name, '，在树的根节点下创建')
            num = len(tree.children('rootsystem'))
            tree.create_node(root_name, 'system ' + str(num + 1), 'rootsystem')
            sys_add_branch_nodes(tree, root_name, supsys, sys, name_lev3)
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
    root_name = root_ele + '_' + dimension
    if tree is None:
        tree = treelib.Tree()
        tree.create_node(root_name, root_name)  # 创建根节点

    node_child_num = len(tree.children(tree.all_nodes()[0].identifier))

    ele_idf = dimension + ' ' + str(node_child_num + 1)
    tree.create_node(ele, ele_idf, root_name)  # 创建单元名（一级节点）
    tree.create_node(eleid, dimension + 'id ' + str(node_child_num + 1), ele_idf)  # 创建单元的名称（二级节点）
    tree.create_node(eleprop, dimension + 'prop ' + str(node_child_num + 1), ele_idf)  # 创建单元的特性（二级节点）
    for i, var in enumerate(elevar):
        tree.create_node(var, dimension + 'var ' + str(node_child_num + 1) + '.' + str(i + 1),
                         dimension + 'prop ' + str(node_child_num + 1))  # 创建单元的特性变量（三级节点）
    return tree


def combine_sys_ele(system_tree, root_ele, person_tree=None, machine_tree=None, product_tree=None):
    """
    将单元树合并到系统树下的root_ele对应节点
    :param system_tree: 需要合并的系统树
    :param root_ele: 系统树下的指定节点tag
    :param person_tree: 人员单元树
    :param machine_tree: 机器单元树
    :param product_tree: 产品单元树
    :return: None
    """
    node = find_node_by_tag(system_tree, root_ele)
    if person_tree:
        system_tree.paste(node.identifier, person_tree, deep=False)
    if machine_tree:
        system_tree.paste(node.identifier, machine_tree, deep=False)
    if product_tree:
        system_tree.paste(node.identifier, product_tree, deep=False)


def tree_to_df(tree, dimension: str, columns_num: int):
    """
    将树转换为dataframe，所有节点作为多级索引
    :param tree: 需要转换的树
    :param dimension: person(人员), machine(机器), product(产品),
    :param columns_num: 初始化列的数量
    :return: 返回转换的dataframe
    """
    if dimension not in ['person', 'machine', 'product']:
        print('维度输入错误')
        return None

    paths = []
    max_len = tree.depth()  # 树的深度

    for path in tree.paths_to_leaves():
        tag_path = []
        for p in path:
            tag_path.append(tree.get_node(p).tag)
        paths.append(tuple(tag_path + ['None'] * (max_len - len(path[:-1]))))

    # 创建多级行索引
    index = pd.MultiIndex.from_tuples(
        tuples=paths,
        names=['dimension', dimension, 'prop', 'variable']
    )
    df = pd.DataFrame(data=[[None] * columns_num] * len(paths), index=index,
                      columns=[dimension + ' ' + str(i) for i in range(columns_num)])

    return df


def element_data_value(df, dimension: str, root_ele: str, ele: str, eleid: str, elevar: list):
    """
    向传入的df中进行维度单元的输入操作
    :param df: 需要输入的df对象
    :param dimension: 维度 person(人员), machine(机器), product(产品),
    :param root_ele: 树的根节点名称，系统树中的项目名称
    :param ele: 单元树中的一级节点，df中的一级索引
    :param eleid: 二级节点'名称'的值
    :param elevar: 二级节点'特征'对应三级节点对应的值
    :return: None
    """
    # 列满需要添加新列之后进行插入，标记哪一列没有值
    tmp = len(df.columns) + 1  # 默认新一列
    # 查找是否有没有值的列
    for i, col in enumerate(df.columns):
        if df.loc[:, col].all():
            tmp = i  # i列没有值，可以进行插入
            break
    # 插值
    df.loc[(root_ele + '_' + dimension, ele, '名称'), [dimension + ' ' + str(tmp)]] = eleid
    for idx, var in zip(df.index.get_level_values(-1)[1:], elevar):
        df.loc[(root_ele + '_' + dimension, ele, '特性', idx), [dimension + ' ' + str(tmp)]] = var
