# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6


def add_node(tree_dic, comment):
    if comment.parent_comment is None:
        # 如果我是顶层，那我放在这
        tree_dic[comment] = {}
    else:  # 不是顶层，开始找父亲, 循环当前整个字典，直到找到位置
        for k, v in tree_dic.items():
            if k == comment.parent_comment:  # 找到了父亲
                print("find dad.", k)
                tree_dic[comment.parent_comment][comment] = {}
            else:  # 进入下一层继续找
                print('keep going deeper....')
                add_node(v, comment)


def render_tree_node(tree_dic,margin_val):
    html = ""
    for k, v in tree_dic.items():
        ele = "<div class='comment-node' style='margin-left:%spx'>" % margin_val + k.comment  + "<span style='margin-left:20px'>%s </span>"%k.date + \
                "<span style='margin-left:20px'>%s</span>" % k.user.name \
              + '<span comment-id="%s"' % k.id +' style="margin-left:20px" class="glyphicon glyphicon-comment add-comment" aria-hidden="true"></span>'\
              + "</div>"
        html += ele
        html += render_tree_node(v, margin_val+16)
    return html


def render_comment_tree(tree_dic):
    html = ""
    for k, v in tree_dic.items():
        ele = "<div class='root-comment'>" + k.comment + "<span style='margin-left:20px'>%s </span>" % k.date \
              + "<span style='margin-left:20px'>%s</span>" % k.user.name \
              + '<span comment-id="%s"' % k.id + ' style="margin-left:20px" class="glyphicon glyphicon-comment add-comment" aria-hidden="true"></span>' \
              + "</div>"
        html += ele
        html += render_tree_node(v, 10)
    return html


def build_tree(comment_set):
    #print(comment_set)
    tree_dic = {}
    for comment in comment_set:
        add_node(tree_dic, comment)

    print('----------')
    for k, v in tree_dic.items():
        print(k, v)

    return tree_dic











