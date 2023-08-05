class FullIndex(object):
    """Represents a CANOpen address with node-id, index and subindex."""
    
    def __init__(self, node, index, subindex):
        self.NodeId = node
        self.Index = index
        self.SubIndex = subindex

    def __hash__(self):
        i = self.NodeId << 24 | self.Index << 8 | self.SubIndex
        return hash(i)

    def __eq__(self, other):
        # return (self.NodeId, self.Index, self.SubIndex) == (other.Node, other.Index, other.SubIndex)
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __getitem__(self, k):
        return k

    def __repr__(self):
        return 'N{0:00}-0x{1:4X}-0x{2:02X}'.format(self.NodeId, self.Index, self.SubIndex)

    def Node(self, newnode):
        # if isinstance(newnode, mfx4device):
        #    return FullIndex(newnode.TheNode(),self.Index,self.SubIndex)
        return FullIndex(newnode, self.Index, self.SubIndex)
