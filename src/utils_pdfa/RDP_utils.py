from src.utils_pdfa.test import RDPState
import numpy as np


def get_candidates(Q_prev, pdfa):
    Q_t = []
    for q in Q_prev:
        unq, cnt = np.unique(q.Data[q.ix, q.t], axis=0, return_counts=True)
        #sorted in descending order of frequency of aor
        candidates_sorted = unq[np.argsort(-cnt)]
        for i in range(len(candidates_sorted)):
            Q_t.append(
                RDPState(pdfa.get_name(), q, candidates_sorted[i][0], candidates_sorted[i][1], candidates_sorted[i][2]))

    return Q_t

def get_candidate(oq, pdfa):
    q = oq[1]
    o = oq[0]
    Q_t = []
    unq, cnt = np.unique(q.Data[q.ix, q.t+1], axis=0, return_counts=True)
    candidates_sorted = unq[np.argsort(-cnt)]
    for i in range(len(candidates_sorted)):
        # if candidates_sorted[i][1] == o:
            #Q_t.append(RDPState(pdfa.get_name(), q, candidates_sorted[i][0], candidates_sorted[i][1], candidates_sorted[i][2]))
        Q_t.append([candidates_sorted[i][0], candidates_sorted[i][1]])
    return Q_t


def remove_candidate(Q_t):
    Q_t.pop(0)
    return Q_t


def test_distinct(traj1, traj2, H, thres):
    # if q1.t == H + 1:
    #     return True
    #r, o = q1.operatorC11()

    #q1_prob = np.concatenate((np.concatenate((r,o),axis=0), q1.operatorC13()), axis=0)
    q1_prob =operatorC13(traj1)
    # r, o = q2.operatorC11()
    # q2_prob = np.concatenate((np.concatenate((r,o),axis=0), q2.operatorC13()), axis=0)
    q2_prob = q2.operatorC13()
    seq = list(set(q1_prob[:, 0])) + list(set(q2_prob[:, 0]) - set(q1_prob[:, 0]))
    for s in seq:
        p1 = get_probability(s,q1_prob)
        p2 = get_probability(s,q2_prob)
        if np.abs(p1 - p2) > thres:
            return False
    return True

def operatorC13(trajs):
    print("here",trajs)
    brek
        # compute the empirical probabilities of each *triplet*
    # ct = Counter([x for elem in self.Trp[self.ix, self.t-1] for x in elem])
    # trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
    return 0



def get_probability(aor, q_tr):
    p = np.where(q_tr[:, 0] == aor)[0]
    if len(p) == 0:
        return 0
    return float(q_tr[p[0], 1])



def get_ix(q,o):
    L=[]
    for i in range(q.Data.shape[0]):
        if q.Data[i,q.t][1]== o:
            L.append(q.Data[i,q.t+1:])
    L = np.array(L)
    return np.reshape(L, (L.shape[0], L.shape[1]))

def get_suffixes(pdfa,o,u,ao):
    t = u.t
    L=[]

    for i in range(len(u.ix)):
        print(u.Data[u.ix[i], t][1] , u.Data[u.ix[i], t+1][0], u.Data[u.ix[i], t+1][1], o, ao[0], ao[1])
        if u.Data[u.ix[i], t][1] ==o and u.Data[u.ix[i], t+1][0]== ao[0] and u.Data[u.ix[i], t+1][1]== ao[1]:
            L.append(u.Data[u.ix[i], t+1:])
    # q = RDPState(pdfa.get_name(), u, ao[0], ao[1], 0)
    # q.ix = L
    L = np.array(L)
    return np.reshape(L, (L.shape[0], L.shape[1]))