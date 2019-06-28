from rtreelib import RTree, Rect, rtree
from rtreelib.util.diagram import create_rtree_diagram
import index_dataset
import rtreenode_minheap

def k_NN_search(minheap, query_point, k):
    """
    :param minheap: the instance of heap
    :param query_point: query_point(x,y)
    :param k: desire number of group size
    :return: a set of RTreeEntry
    """
    s=set()

    while len(s)<k and not minheap.is_empty():
        out=minheap.delete()
        if isinstance(out,rtree.RTreeEntry):
            s.add(out)

    return s


i = index_dataset.IndexDatabase("munged_BrightkiteEurope_SpatioTemporal.csv")

t = RTree()
# t.get_levels()


# Create an RTree instance with some sample data
t = RTree(max_entries=2)
t.insert('a', Rect(0, 0, 0, 0))
t.insert('b', Rect(2, 2, 2, 2))
t.insert('c', Rect(1, 1, 1, 1))
t.insert('d', Rect(8, 8, 8, 8))
t.insert('f', Rect(7, 7, 7, 7))
t.insert('g', Rect(4, 4, 4, 4))
t.insert('h', Rect(5, 5, 5, 5))
t.insert('i', Rect(6, 6, 6, 6))

# t.get_leaf_entries()
# print(level)
# print(level[1][0].entries)
# print(level[1][1].entries)
# print(level[1][2].entries)
# _g=t.get_leaf_entries()
# print(t.get_leaves())

# for v in i.mat:
#    t.insert(str(v[0]), Rect(v[3], v[4], v[3], v[4]))


level=t.get_levels()
print(level)
print("level00: "+ str(level[0][0]))
print(level[0][0].entries[0].child)
print(level[0][0].entries[0])
print(level[0][0].get_bounding_rect().max_x)
# level[0][0].get_bounding_rect().min_x, min_y, max_x, max_y >> Rect()
print("===minheap===")
p=(2.5, 2.5)
H = rtreenode_minheap.RtreenodeMinheap(p)
H.insert(level[0][0])

print("===delete===")

result=k_NN_search(H, p, 4)
print(result)

# Create a diagram of the R-tree structure
# create_rtree_diagram(t)