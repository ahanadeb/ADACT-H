import numpy as np

class State:
    # dataset stored as a *static* (shared) attribute
    Data = None

    # store sets of symbols in traces
    Act = None
    Obs = None
    Rew = None
    Trp = None
    def __init__(self, name, parent=None, a=None, o=None, r=0):
        self.trajs_set={'a':[],'b':[], 'c':[], 'd':[]}
        self.name = name
        self.a = a
        self.o = []
        self.r = r
        self.parent = parent
        self.o.append(o)
        if parent == None:
            # if the state has no parent, create the state q0 with the entire dataset
            self.t = 0
            self.ix = range(self.Data.shape[0])
        else:
            # else extract the indices of traces that are consistent with (a,o)
            ao = f'{a}{o}'
            self.t = parent.t + 1
            self.ix = [i for i in parent.ix if ao in self.Data[i, parent.t]]


    def add_o(self, o):
        self.o.append(o)

    def add_trajset(self, o, traj):
        self.trajs_set[o].append(traj)




