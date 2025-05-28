from src.utils_pdfa.RDPState import RDPState
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


def remove_candidate(Q_t):
    Q_t.pop(0)
    return Q_t

# we have to compare conditional on Observation seen in q2
def test_distinct_loops(q1, q2, H, thres):
    if q2.t == H + 1:
        if q1.t == H+1:
            return True
        return False

    q2_obs = get_obs_q(q2)
    # filtered_ix = get_ix(q1, q2_obs)
    # print((np.concatenate((r,o),axis=0)))
    for o in q2_obs:
        q1_prob = np.concatenate((q1.operatorC11o(o), q1.operatorC13o(o)), axis=0)
        q2_prob = np.concatenate((q2.operatorC11o(o), q2.operatorC13o(o)), axis=0)
        # print(q1_prob, q2_prob)
        if len(q1_prob)==0:
            return False
        seq = list(set(q1_prob[:, 0])) + list(set(q2_prob[:, 0]) - set(q1_prob[:, 0]))
        for s in seq:
            # print(s)
            p1 = get_probability(s, q1_prob)
            p2 = get_probability(s, q2_prob)
            # print("s ", s, " ", p1, " ", p2)

            if np.abs(p1 - p2) > thres:
                return False
    #
    # if len(n)==0:
    #     q1_prob=np.concatenate((r,o),axis=0)
    # else:
    #     Q1 = q1.operatorC13oo(filtered_ix)
    #     if len(Q1)==0:
    #         q1_prob = np.concatenate((r, o), axis=0)
    #     else:
    #         q1_prob = np.concatenate((np.concatenate((r,o),axis=0), q1.operatorC13o(o)), axis=0)
    # q2_prob = np.concatenate((np.concatenate((r, o),axis=0), q2.operatorC13o()), axis=0)
    return True



def get_obs_q(q):
    unq, cnt = np.unique(q.Data[q.ix, q.t], axis=0, return_counts=True)
    candidates_sorted = unq[np.argsort(-cnt)]
    c = [val[1:-1] for val in candidates_sorted]
    return c
def get_ix(q, obs):
    ix = []
    for o in obs:
        i=0
        for aor in q.Data[q.ix, q.t]:
            if aor[1]==o:
                ix.append(i)
            i+=1
    return ix


def get_probability(aor, q_tr):
    p = np.where(q_tr[:, 0] == aor)[0]
    if len(p) == 0:
        return 0
    return float(q_tr[p[0], 1])



