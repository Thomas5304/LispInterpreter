from collections import defaultdict

class UnionFind:
    def __init__(self, elements):
        # Each element is its own parent (its own set)
        self.parent = {el: el for el in elements}
        self.rank = {el: 0 for el in elements}
        self.num_sets = len(elements)

    def find(self, i):
        # Path compression: make nodes point directly to the root
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        #breakpoint()
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            # Union by rank: attach the smaller tree under the larger tree
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            self.num_sets -= 1
            return True
        return False

    def get_equivalence_classes(self):
        """Returns a dictionary of root: [elements] representing classes."""
        classes = {}
        for element in self.parent.keys():
            root = self.find(element)
            if root not in classes.keys():
                classes[root] = []
            classes[root].append(element)
        return classes


def printlpp(lpp):
    return f"lpp {lpp[0]}/{lpp[1]}"

def group_layer_table():
    layertable = [
        ("metal1", "drawing"),
        ("metal1", "dummy"),
        ("metal1", "dummyblock"),
        ("metal1", "keepout"),
        ("metal2", "drawing"),
        ("metal2", "dummy"),
        ("metal2", "dummyblock"),
        ("metal2", "keepout"),
        ("metal3", "drawing"),
        ("metal3", "dummy"),
        ("metal3", "dummyblock"),
        ("metal3", "keepout"),
        ("pn", "drawing"),
        ("poly1", "drawing"),
        ("well", "drawing"),
        ("dnwell", "drawing"),
        ("hvwell", "drawing"),
        ("re", "pn"),
        ("re", "poly1"),
        ("re", "metal1"),
        ("re", "metal2"),
        ("re", "metal3"),
    ]
    grouped_layer_table = {}

    ufgroups = UnionFind(layertable)

    keys = list(ufgroups.parent.values())
    for nr,key1 in enumerate(keys):
        for key2 in keys[nr+1:]:
            if key1[0] == key2[0]:
                ufgroups.union(key1, key2)

    #print(ufgroups.get_equivalence_classes())
    print("groups")
    ufgroupdict = ufgroups.get_equivalence_classes()
    for group in ufgroupdict.keys():
        print(f"{group[0]}:")
        print(f"    {'\n    '.join([printlpp(g) for g in ufgroupdict[group]])}")
        
    groups = defaultdict(list)
    for lpp in layertable:
        if lpp[0] in groups:
            groups[lpp[0]].append(lpp)
        elif lpp[1] in groups:
            groups[lpp[1]].append(lpp)
        else:
            groups[lpp[0]].append(lpp)

    print("groups")
    for group in groups.keys():
        print(f"{group}:")
        print(f"    {'\n    '.join([printlpp(g) for g in groups[group]])}")
        

def main():
    group_layer_table()

if __name__ == "__main__":
    main()