import treelib
from treelib import Tree

# data 人员特性
SUPER_MODEL_NAME = "super_model"
SYSTEM_MODEL_NAME = "system_model"
SUB_MODEL_NAME = "sub_model"
PERSON_NAME = "person"
METHOD_NAME = "method"
PROCEDURE_NAME = "procedure"

from imkernel.utils import idgen
from imkernel.utils.tree_utils import tree_to_df


def find_node_by_tag(tree, tag):
    """通过节点的tag在树中查找"""
    for node in tree.all_nodes():
        if node.tag == tag:
            return node
    else:
        return None


def tree_sys(rootsys, supsys, sys, tree: Tree = None) -> Tree:
    if tree is None:
        treelib_tree = Tree()
        sup_node = treelib_tree.create_node(rootsys, idgen.next_id(), None, data=SUPER_MODEL_NAME)
    else:
        treelib_tree = tree
        sup_node = find_node_by_tag(tree, rootsys)
    if isinstance(supsys, str):
        if not (isinstance(sys, str) or isinstance(sys, list)):
            raise ValueError("name为字符串时，subname必须是字符串或列表.")
        sys_node = treelib_tree.create_node(supsys, idgen.next_id(), sup_node.identifier, data=SYSTEM_MODEL_NAME)
        if isinstance(sys, str):
            treelib_tree.create_node(sys, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
        elif isinstance(sys, list):
            for sub in sys:
                if sub is not None:
                    treelib_tree.create_node(sub, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
    elif isinstance(supsys, list):
        if not isinstance(sys, list):
            raise ValueError("name为列表时，subname必须是对应长度的列表.")
        if len(supsys) != len(sys):
            raise ValueError(f"name与subname长度不匹配: name长度：{len(supsys)}, subname长度：{len(sys)}.")
        for i, sys_name in enumerate(supsys):
            sys_node = treelib_tree.create_node(sys_name, idgen.next_id(), sup_node.identifier, data=SYSTEM_MODEL_NAME)
            sub_list = sys[i]
            if sub_list is None:
                continue
            if isinstance(sub_list, str):
                treelib_tree.create_node(sub_list, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
            elif isinstance(sub_list, list):
                for sub in sub_list:
                    treelib_tree.create_node(sub, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
            else:
                raise ValueError(f"subname的元素必须是None或列表，第{i + 1}个数组类型为{type(sub_list).__name__}")
    else:
        raise ValueError(f"name类型错误，仅允许字符串或列表，实际为{type(supsys).__name__}")

    return treelib_tree


def element(tree: treelib.Tree, sub_nid: str, dimension_type: str, name):
    if dimension_type not in [PERSON_NAME, METHOD_NAME, PROCEDURE_NAME]:
        raise Exception(f"dimension_type仅能为{[PERSON_NAME, METHOD_NAME, PROCEDURE_NAME]}中的一个")

    sub_node_list = list(tree.filter_nodes(lambda node: node.tag == sub_nid and node.data == SUB_MODEL_NAME))
    if len(sub_node_list) == 0:
        raise Exception(f"{sub_nid}不存在，请检查")
    elif len(sub_node_list) > 1:
        raise Exception(f"找到{len(sub_node_list)}个{sub_nid}，请检查")

    sub_node = sub_node_list[0]
    # tree.create_node(sub, idgen.next_id(), sys_node.identifier, data=PERSON_NAME)
    print(sub_node)


if __name__ == '__main__':
    system_tree = tree_sys(rootsys='insofsys', supsys=['insoftest'], sys=[['DTIS_511', 'NDT_SNPTC']])
    system_tree = tree_sys(tree=system_tree, rootsys='insofsys', supsys=['insofrobot'], sys=[['insoftube', 'insofbend', 'insoflaser']])
    system_tree = tree_sys(tree=system_tree, rootsys='insofsys', supsys='insofaiam', sys='insofmining')
    system_tree = tree_sys(tree=system_tree, rootsys='insofsys', supsys=['1', '2'], sys=[['insofminin7g', 'insofminin7213'], 'insofminin474g'])
    print(system_tree)
    print(1)
