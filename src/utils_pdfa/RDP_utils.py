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


def get_candidate(o, q, H):
    #problem here
    Q_t = []
    new =[]
    if q.t+1==H:
        return []
    for i in range(q.Data.shape[0]):
        # print(q.Data[i, q.t][1],o)
        if q.Data[i, q.t][1]==o and i in q.ix:
            new.append(i)
    # if q.parent!=None:
    #     print("Rer",o, q.name,q.parent.name,"time: ", q.t, new, q.ix)
   #brek

    unq, cnt = np.unique(q.Data[new, q.t + 1], axis=0, return_counts=True)
    candidates_sorted = unq[np.argsort(-cnt)]
    for i in range(len(candidates_sorted)):
        # if candidates_sorted[i][1] == o:
        #Q_t.append(RDPState(pdfa.get_name(), q, candidates_sorted[i][0], candidates_sorted[i][1], candidates_sorted[i][2]))
        Q_t.append([candidates_sorted[i][0], candidates_sorted[i][1]])
    return Q_t


def remove_candidate(Q_t):
    Q_t.pop(0)
    return Q_t


def test_distinct(q1, q2, o, H, thres):
    if q2.t == H + 1:
        return True
    #r, o = q1.operatorC11()

    # q1_prob = np.concatenate((np.concatenate((r, o), axis=0), q1.operatorC13o(o)), axis=0)
    q1_prob= q1.operatorC13o(o)
    # r, o = q2.operatorC11()
    # q2_prob = np.concatenate((np.concatenate((r, o), axis=0), q2.operatorC13()), axis=0)
    q2_prob = q2.operatorC13()
    # print("here", q1_prob, q2_prob)
    seq = list(set(q1_prob[:, 0])) + list(set(q2_prob[:, 0]) - set(q1_prob[:, 0]))
    print("comparing", q1.name, q2.name)
    for s in seq:
        p1 = get_probability(s, q1_prob)
        p2 = get_probability(s, q2_prob)
        print(s, p1, p2)
        if np.abs(p1 - p2) > thres:
            return False
    return True


def get_probability(aor, q_tr):
    p = np.where(q_tr[:, 0] == aor)[0]
    if len(p) == 0:
        return 0
    return float(q_tr[p[0], 1])


def get_ix(q, o):
    L = []
    for i in range(q.Data.shape[0]):
        if q.Data[i, q.t][1] == o:
            L.append(i)
    #print("added ix", L)
    if not L:
        print("here2", L)
        brej
    return L


def get_suffixes(pdfa, o, u, ao):
    t = u.t
    L = []
    # print("styat")
    for i in u.ix:
        # print(u.Data[u.ix[i], t][1], u.Data[u.ix[i], t + 1][0], u.Data[u.ix[i], t + 1][1], o, ao[0], ao[1])
      #  print(u.Data[i, t][1], o,  u.Data[i, t+1 ][0], ao[0] , u.Data[i, t+1][1],ao[1] )
        if u.Data[i, t][1] == o and u.Data[i, t+1 ][0] == ao[0] and u.Data[i, t+1][1] == ao[1]:
            # L.append(u.Data[u.ix[i], t+1:])
            L.append(i)
    # q = RDPState(pdfa.get_name(), u, ao[0], ao[1], 0)
    # q.ix = L
    #print("L ", L)
    # if not L:
    #     print("here1", L)
    #     brej
    return L
