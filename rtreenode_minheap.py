from rtreelib import RTree, Rect, rtree
class RtreenodeMinheap():
    def __init__(self, query_point):
        self.heap = [None]
        self.heap_size = 0
        # query_point(x,y)
        self.query_point=query_point

    def insert(self, vertex):
        self.heap.append(vertex)
        i = len(self.heap) - 1
        while i > 1:
            parent = i // 2
            if self.compare_dist(self.heap[parent], vertex):
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def delete(self):
        # removing phase
        i = len(self.heap) - 1
        self.heap[1], self.heap[i] = self.heap[i], self.heap[1]
        return_value = self.heap[i]
        self.heap.pop(i)

        if return_value.is_leaf:
            if isinstance(return_value, rtree.RTreeEntry):
                self.min_heapify(1)
                print(str(return_value.rect)+", "+str(self.dist(return_value)))
                # print(return_value)
                return return_value

            for e in return_value.entries:
                # print(e)
                self.insert(e)
        else:
            for e in return_value.entries:
                self.insert(e.child)

        # heapifying phase
        self.min_heapify(1)
        return return_value

    def min_heapify(self, i):
        left = i * 2
        right = i * 2 + 1
        smallest = i
        if left <= len(self.heap) - 1 and self.compare_dist(self.heap[smallest], self.heap[left]):
            smallest = left
        if right <= len(self.heap) - 1 and self.compare_dist(self.heap[smallest], self.heap[right]):
            smallest = right
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.min_heapify(smallest)

    def compare_dist(self, e1, e2):
        mc_vertex1 = self.moving_cost(e1)
        mc_vertex2 = self.moving_cost(e2)

        if mc_vertex1 > mc_vertex2:
            return True
        return False

    def moving_cost(self, e):
        mc = self.dist(e)
        return mc

    def dist(self, e):
        # self.min_x = min_x
        # self.min_y = min_y
        # self.max_x = max_x
        # self.max_y = max_y
        if not isinstance(e, rtree.RTreeEntry):
            rect=e.get_bounding_rect()
        else:
            rect=e.rect
        x=self.query_point[0]
        y=self.query_point[1]

        #check whether query_point is in bounding rectangle.
        if x>=rect.min_x and x<=rect.max_x\
            and y>=rect.min_y and y<=rect.max_y:
            distance=0
        else:
            if x>=rect.min_x and x<=rect.max_x:
                if y>rect.max_y:
                    distance=y-rect.max_y
                else: #y<rect.min_y
                    distance=rect.min_y-y
            elif x<rect.min_x:
                #case C
                if y>=rect.min_y and y<=rect.max_y:
                    distance=rect.min_x-x
                elif y>rect.max_y:
                    #case C1
                    square_diff_x = (x - rect.min_x) ** 2
                    square_diff_y = (y - rect.max_y) ** 2
                    distance = (square_diff_x + square_diff_y) ** (float(1) / 2)
                else: #y<rect.min_y
                    #case C3
                    square_diff_x = (x - rect.min_x) ** 2
                    square_diff_y = (y - rect.min_y) ** 2
                    distance = (square_diff_x + square_diff_y) ** (float(1) / 2)
            elif x>rect.max_x:
                #B case
                if y>=rect.min_y and y<=rect.max_y:
                    #case B2
                    distance=x-rect.max_x
                elif y>rect.max_y:
                    #case B1
                    square_diff_x = (x - rect.max_x) ** 2
                    square_diff_y = (y - rect.max_y) ** 2
                    distance = (square_diff_x + square_diff_y) ** (float(1) / 2)
                else: #y<rect.min_y
                    square_diff_x = (x - rect.max_x) ** 2
                    square_diff_y = (y - rect.min_y) ** 2
                    distance = (square_diff_x + square_diff_y) ** (float(1) / 2)
        return distance
        # square_diff_x = (p1[0] - p2[0]) ** 2
        # square_diff_y = (p1[1] - p2[1]) ** 2
        # distance = (square_diff_x + square_diff_y) ** (float(1) / 2)
        # return distance

    def is_empty(self):
        if len(self.heap) == 1:
            return True
        return False