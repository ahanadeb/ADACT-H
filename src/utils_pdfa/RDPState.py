import numpy as np
import sys

from simul import Simulator
from PyPOMDP.pypomdp.parsers import PomdpParser
from collections import Counter

class RDPState:
    # dataset stored as a *static* (shared) attribute
    Data = None

    # store sets of symbols in traces
    Act = None
    Obs = None
    Rew = None
    Trp = None
    Trptrp= None

    def __init__(self, name, cand=None, a='A', o='a', r='r'):
        self.trajs_set = {'a': [], 'b': [], 'c': [], 'd': []}
        self.name = name
        self.a = a
        self.o = o
        self.r = r
        self.O=[]
        self.parent = cand
        if cand == None:
            # if the state has no parent, create the state q0 with the entire dataset
            self.t = 0
            self.ix = range(self.Data.shape[0])
        else:
            # else extract the indices of traces that are consistent with (a,o) 
            ao = f'{a}{o}'
            self.t = cand.t + 1
            self.ix = [i for i in cand.ix if ao in self.Data[i, cand.t]]

    # make a operator which takes self and obs o, and returns the number of times an "aor" has occured, given a particular o.
    def add_o(self, o):
        self.O.append(o)

    def add_trajset(self, o, traj):
        self.trajs_set[o].append(traj)
    def operatorC13oo(self, ix):
        # if o is None:
        #     # o = self.o
        #     ct = Counter([x for elem in self.Trp[self.ix, self.t - 1] for x in elem])
        #     # print(ct)
        #     trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        #     return np.array(trpprob)
        # out = [i for i, v in enumerate(self.Data[:, self.t]) if o in v]
        # # print("out, ", out)
        #
        # out= remove_nc(out, self.ix)
        # print("out, ", out)
        ct = Counter([x for elem in self.Data[ix, self.t-1:] for x in elem])
        # print(ct)
       # print(ct)

        #print("here2",self.Trp[self.ix,:])
        # ct = Counter([x for elem in self.Trp[self.ix, self.t - 1] for x in elem])
        # print(ct)
        # trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        # print(trpprob)
        trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        # print(trpprob)
        return np.array(trpprob)
    def operatorC13o(self, o=None):
        # if o is None:
        #     ct = Counter([x for elem in self.Trp[self.ix, self.t - 1] for x in elem])
        #     trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        #     return np.array(trpprob)
        out = [i for i, v in enumerate(self.Data[:, self.t]) if o in v]
        out= remove_nc(out, self.ix)
        ct = Counter([x for elem in self.Data[out, self.t:] for x in elem])
        trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        # print(trpprob)

        return np.array(trpprob)
    def operatorC11o(self, o=None):


        out = [i for i, v in enumerate(self.Data[:, self.t]) if o in v]
        out = remove_nc(out, self.ix)


        ct = Counter([x for elem in self.Rew[out, self.t] for x in elem])
        rewprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        return np.array(rewprob)
    def operatorC11(self):
        # compute the empirical probabilities of each *action*
        ct = Counter([x for elem in self.Act[self.ix, self.t] for x in elem])
        actprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]

        # compute the empirical probabilities of each *observation*
        ct = Counter([x for elem in self.Obs[self.ix, self.t] for x in elem])
        obsprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]

        # compute the empirical probabilities of each *reward*
        ct = Counter([x for elem in self.Rew[self.ix, self.t] for x in elem])
        rewprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        return np.array(rewprob), np.array(obsprob)

    def operatornew(self):
        ct = Counter([x for elem in self.Trptrp[self.ix, self.t] for x in elem])
        trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        return np.array(trpprob)

    def operatorC13(self):
        # compute the empirical probabilities of each *triplet*
        ct = Counter([x for elem in self.Trp[self.ix, self.t-1] for x in elem])
        trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        return np.array(trpprob)



# incomplete function, intention is to learn an RDP with horizon H
def learnRDP(H):
    #print(RDPState.Data)
    # merging two states is achieved by taking the union of the indices (ix)
    # create the RDP state q0
    q0 = RDPState()

    # create the RDP states at time t=1 associated with (a,o)=(0,0) and (a,o)=(0,1)
    q1 = RDPState(q0, 'A', 'a')
    q2 = RDPState(q0, 'A', 'b')

    # create the RDP states at time t=2 associated with (a,o)=(1,2) and (a,o)=(1,3)
    q3 = RDPState(q1, 'B', 'c')
    q4 = RDPState(q1, 'B', 'd')

    # test the operators
    q1.operatorC11()
    q1.operatorC13()

    q3.operatorC11()
    q3.operatorC13()


# simulate K episodes of Tmaze with horizon H
def simTMaze(filename, K, H):


    D = np.empty((K, H + 1), dtype=np.dtype('U3'))

    with PomdpParser(filename) as parser:
        sim = Simulator(parser.copy_env())

    # map discrete rewards to integers
    rews = set(sim.R.flat)
    rewmap = {k: v for v, k in enumerate(list(rews))}
    for k in range(K):
        sim.reset()
        # get the observation in the first state
        a = np.random.randint(3)
        # a=0
        s, sp, o, r = sim.take_action(a)
        # o = 0
        # r = 0
        # sp = 0
        D[k, 0] = '{}{}{}'.format( chr(65 + a), chr(97 + o), chr(48 + rewmap[r]))
        # go east H - 1 times
        for i in range(H):
            print("here ", str(a), " ", str(o), " ", str(sp), " ", str(r))
            #a = np.random.randint(len(sim.actions))
            a = np.random.choice([0,1,2,3], 1, p=[1/4, 1/4,1/4, 1/4])[0]
            s, sp, o, r = sim.take_action(a)
            D[k, i + 1] = '{}{}{}'.format(chr(65 + a), chr(97 + o), chr(48 + rewmap[r]))

    return D
def remove_nc(a, b):
    xy = np.intersect1d(a, b, return_indices=False)
    return list(xy)


def main():
    H = int(sys.argv[2])
    K = int(sys.argv[3])

    RDPState.Data = simTMaze(sys.argv[1] + sys.argv[2] + '.POMDP', K, H)

    print(RDPState.Data)

    RDPState.Act = np.array([[set(RDPState.Data[i][j][0]) for j in range(H + 1)] for i in range(K)])
    RDPState.Obs = np.array([[set(RDPState.Data[i][j][1]) for j in range(H + 1)] for i in range(K)])
    RDPState.Rew = np.array([[set(RDPState.Data[i][j][2]) for j in range(H + 1)] for i in range(K)])
    RDPState.Trp = np.array([[set([RDPState.Data[i][j]]) for j in range(H + 1)] for i in range(K)])

    for j in range(H):
        RDPState.Act[:, H - 1 - j] = [RDPState.Act[i, H - 1 - j].union(RDPState.Act[i, H - j]) for i in range(K)]
        RDPState.Obs[:, H - 1 - j] = [RDPState.Obs[i, H - 1 - j].union(RDPState.Obs[i, H - j]) for i in range(K)]
        RDPState.Rew[:, H - 1 - j] = [RDPState.Rew[i, H - 1 - j].union(RDPState.Rew[i, H - j]) for i in range(K)]
        RDPState.Trp[:, H - 1 - j] = [RDPState.Trp[i, H - 1 - j].union(RDPState.Trp[i, H - j]) for i in range(K)]

    print(RDPState.Act)

    learnRDP(H)


# def testmaze(filename, K, H, RDP):
#     R = 0
#     with PomdpParser(filename) as parser:
#         sim = Simulator(parser.copy_env())
#
#     # map discrete rewards to integers
#     rews = set(sim.R.flat)
#     rewmap = {k: v for v, k in enumerate(list(rews))}
#     for k in range(K):
#         sim.reset()
#         # get the observation in the first state
#         a = np.random.randint(3)
#         # a=0
#
#         s, sp, o, r = sim.take_action(a)
#         # o = 0
#         # r = 0
#         # sp = 0
#         q0 = 'q0'
#
#         D[k, 0] = '{}{}{}'.format( chr(65 + a), chr(97 + o), chr(48 + rewmap[r]))
#         for i in range(H):
#
#             print("here ", str(a), " ", str(o), " ", str(sp), " ", str(r))
#             #a = np.random.randint(len(sim.actions))
#             a = np.random.choice([0,1,2,3], 1, p=[1/4, 1/4,1/4, 1/4])[0]
#             s, sp, o, r = sim.take_action(a)
#             D[k, i + 1] = '{}{}{}'.format(chr(65 + a), chr(97 + o), chr(48 + rewmap[r]))
#
#
#     return R
#
# def get_next_state(RDP, q, a, o):
#     for tr in RDP.transitions:
#         if tr[0] == q and tr[1]==a and tr[2]==o:
#             return tr[4]
#     return q


