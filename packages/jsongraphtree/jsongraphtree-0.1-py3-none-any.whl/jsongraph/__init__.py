from __future__ import absolute_import
from .jsongraph import *
import argparse
import json
from graphviz import Digraph

name="jsongraph"

def output():
     print("测试")

def add_nodes(graph, data, parent_node=None, label=None):
    """
    添加节点和边的递归函数
    """

    if isinstance(data, dict):
        for key,value in data.items():
            print("遍历pipeline中的key："+key)
            node_id=str(id(key))
            node_label=label if label is not None else str(key)
            if parent_node is None:
                  graph.node(node_id,label=node_label)
                  add_nodes(graph,value,node_id)
            if parent_node is not None:
                    node_id = str(id(key))
                    print("key:"+key+" "+"parent_node:"+parent_node)
                    print("node_id: "+node_id)
                    print("当前的value: "+str(value))
                    # if len(list(value.items()))==0:
                    #     return
                    # second_key, second_value = list(value.items())[0]
                    # print("第二层的value： "+str(second_value))
                    if isinstance(value,int):
                            return
                    elif isinstance(value,list):
                        return

                    node_label = dict_alias[key] if key in dict_alias.keys() else str(key)

                    graph.node(node_id, label=node_label)
                    graph.edge(parent_node, node_id)
                
                
                    # 处理数据中的子节点
                    print("value:"+str(value))
                    print("**************")
                    if isinstance(value, dict):
                            # for k2, v2 in value.items():
                            #     print("k2:"+str(k2))
                            #     print("v2:"+str(v2))
                                # seconde_key, second_value = list(v2.items())[0]
                                # print(second_value)
                                # if(isinstance(second_value,int)):
                                #     continue
                                # elif isinstance(second_value,list):
                                #     continue
                        add_nodes(graph, value, node_id)
def ok(a):
     print("ok,测试成功"+str(a))


def draw():
    parser = argparse.ArgumentParser(description='A command-line JSON processor')
    parser.add_argument('json_file', metavar='JSON', type=str, help='the JSON file to process')
    args = parser.parse_args()

    with open(args.json_file) as f:
        data = json.load(f)

    print(json.dumps(data, indent=4))

    # 创建一个Digraph对象
    graph = Digraph()

    #添加一个字典存储alias内容
    dict_alias={}
    for key, value in data.items():
        if key=='alias':
            if isinstance(value, dict):
                dict_alias=value
                print("dict_alias: "+str(dict_alias))



    #在pipeline数组下面
    for key, value in data.items():
        print("开始的key："+key)  
        if key=='pipeline':
            add_nodes(graph,value)
    # 添加节点和边

    # add_nodes(graph, data)

    # 将图形保存为图像文件
    graph.render('pipeline_tree_test', format='png')
     