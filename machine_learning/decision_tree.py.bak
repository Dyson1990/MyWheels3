# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: decision_tree.py
    @time: 2017/2/21 9:38
--------------------------------
"""
import sys
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"

log_obj = set_log.Logger('decision_tree.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('decision_tree.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件

print """


这里使用的是ID3算法来构造决策树


"""
class decision_tree(object):
    def __init__(self, target_type):
        print "===》需要分类的列为 %s 列" %target_type
        self.target_type = target_type

        self.decision_node = dict(boxstype='sawtooth', fc='0.8')
        self.leaf_node = dict(boxstyle='round4', fc='0.8')
        self.arrow_args = dict(arrowstyle='<-')

    def create_tree(self, df):
        # df = df0.copy()
        class_ser = df[self.target_type]
        if class_ser.drop_duplicates().shape[0] == 1:
            return class_ser.iloc[0] # 只有一种分类的情况
        if df.shape[1] == 1:
            # 遍历所有特征以后
            return self.majority_count(class_ser)

        if class_ser.drop_duplicates().shape[0] > df.drop([self.target_type], axis=1).drop_duplicates().shape[0]:
            print "Warning ！！！\n存在相同特征的数据对应不同的目标类型"
            print df
            return None

        best_feature = self.choose_best_feature(df)
        my_tree = {best_feature:{}}
        print "my_tree  =====>  ,", my_tree
        feature_values = df[best_feature]
        unique_values = feature_values.drop_duplicates()

        for value in unique_values:
            print "my_tree[%s][%s]" %(best_feature,value)
            print self.split_data(df, best_feature, value)
            my_tree[best_feature][value] = self.create_tree(self.split_data(df, best_feature, value))
        #df = df.drop([best_feature, ], axis=1)
        return my_tree


    def choose_best_feature(self, df):
        base_entropy = self.Shannon_ent_base(df)
        best_info_gain = 0.0
        best_feature = None
        for col in df.columns:
            # 此处针对的是除了目标列以外的特征计算熵
            if col == self.target_type:
                continue

            unique_values = df[col].drop_duplicates()
            new_ent = unique_values.apply(lambda value:self.Shannon_ent_new(df, col, value)).sum()
            info_gain = base_entropy - new_ent
            print "%s列的信息熵为%s" %(col, info_gain)

            # 选取信息熵的下降速度最大的特征
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_feature = col
        return best_feature

    def split_data(self, df, col, value):
        """
        1,1,T     1,T
        1,1,F =>  0,F
        0,1,F
        """
        print "split_data=>正在选出特征为%s, 对应的值为%s的数据表" %(col,value)
        #print "split_data=>输出的数据集为:源数据中%s列的数值为%s的集合，但是去掉%s列" %(col,value,col)
        df0 = df[df[col]==value]
        df0 = df0.drop([col,], axis=1)
        return df0

    def Shannon_ent_base(self, df):
        #print """Shannon_ent_base=>正在计算数据集的熵（entropy），用来度量集合的无序程度\n以%s列为数据分类依据""" %self.target_type
        if self.target_type not in df.columns:
            print "没有在数据集中找到%s列" %self.target_type
            return

        # 为所有可能分类创建字典
        label_counts = df[self.target_type].value_counts()

        Shannon_ent = 0.0
        for key in label_counts.index:
            prob = float(label_counts[key]) / df.shape[0]
            Shannon_ent = Shannon_ent - prob * math.log(prob, 2)

        #print "Shannon_ent_base=>数据集中%s列的熵为%s" %(self.target_type, Shannon_ent)
        return Shannon_ent

    def Shannon_ent_new(self, df, col, value):
        sub_df = self.split_data(df, col, value)
        prob = sub_df.shape[0] / float(df.shape[0])
        return prob * self.Shannon_ent_base(sub_df)

    def majority_count(self, ser):
        # 返回目标列中，个数最多的那一类
        class_count = ser.value_counts()
        max0 = class_count.index[0]
        print "majority_count ==>", max0
        return max0

    def plot_node(self, node_text, center_point, parent_point, node_type):
        self.create_plot.ax1.annotate(node_text, xy=parent_point, xycoords='axes fraction',xytext=center_point,
                                 textcoords='axes fraction', va='center', ha='center', bbox=node_type,arrow_props=self.arrow_args)
    def create_plot(self):
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        self.create_plot.ax1 = plt.subplot(111, frameon=False)
        self.plot_node(u'决策节点', (0.5,0.1), (0.1, 0.5), self.decision_node)
        self.plot_node(u'叶节点', (0.5, 0.1), (0.1, 0.5), self.leaf_node)
        plt.show()


if __name__ == '__main__':
    #import operator
    decision_tree = decision_tree('type')
    arr = np.array(
        [
            [1,1,1,'Lion'],
            [1,1,0,'Lion'],
            [1,0,2,'Wolf'],
            [0,1,1,'Shark'],
            [0,2,1,'DOOM'],
        ]
    )
    df = pd.DataFrame(arr, columns=['feature 1', 'feature 2', 'feature 3', 'type'])
    #print decision_tree.choose_best_feature(df)
    #class_count = df['type'].value_counts()
    print decision_tree.create_tree(df)
    #decision_tree.create_plot()
    #print sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)