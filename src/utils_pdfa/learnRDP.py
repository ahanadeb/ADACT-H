from src.utils_pdfa.RDP_utils import *
from src.pdfa import PDFA
def learnRDP(H, thres):
    q0 = RDPState("q0")
    pdfa = PDFA(q0)
    Q_prev = [q0]
    for h in range(H+1):
        print("h: ", h)
        Q_promoted = []
        Q_t= get_candidates(Q_prev, pdfa)
        pdfa.add_transition(Q_t[0].parent, Q_t[0])
        Q_promoted.append(Q_t[0])
        Q_t= remove_candidate(Q_t)  #removing the promoted candidate
        while len(Q_t)>0:
            for q_promoted in Q_promoted:
                similar = test_distinct(Q_t[0],q_promoted,H,thres)
                if not similar:
                    if q_promoted == Q_promoted[-1]:
                        #promote candidate
                        pdfa.add_transition(Q_t[0].parent,  Q_t[0])
                        Q_promoted.append(Q_t[0])
                        break
                else:
                    pdfa.add_transition(Q_t[0].parent, q_promoted, True, Q_t[0])
                    break
            Q_t = remove_candidate(Q_t)
        Q_prev = Q_promoted



    return pdfa

def learnRDP2(H,obs, thres):
    queue = [] #queue of all ao
    trajs = [] #queue of all respective trajs (ix)
    states =  [[] for _ in range(obs)]
    i = [0]*obs
    q0 = RDPState("q0")
    pdfa = PDFA(q0)
    D = q0.Data
    for k in range(D.shape[0]):
        o = D[k,0][1]
        o_int=ord(D[k,0][1])-97
        if i[o_int]==0:
            queue.append([o,q0])
            # get the trajectories here, and put them in a queue directly
            trajs.append(get_ix(q0,o))
            q0.add_trajset(o,get_ix(q0,o))
            states[o_int].append(q0)
            pdfa.add_transition(o, q0, q0)
            i[o_int]=1


    while queue:
        ou= queue.pop(0)
        traj1 = trajs.pop(0)
        AO = get_candidate(ou, pdfa)  #get ao sets (can we get this set at thw start?
        for ao in AO:
            u1 = ou[1]
            o1 = ou[0]
            o2 = ao[1]
            o2_int=get_int(o2)
            traj2= get_suffixes(pdfa, o1,u1,ao)

            j = i[o2_int]

            for k in range(i[o2_int]):
                #get all the u that are prefaced by o
                q_state2 = states[o2_int][k]
                print("XXXX")
                similar = test_distinct(traj1, traj2, H, thres)
                if not similar:
                    j=k
            if j < i[o2_int]:
                #add the new state
                pdfa.add_transition(o1, q_state2.parent, q_state1, True, q_state2) #merge
            else:
                print("Fvev")
                # if i[o_int] ==0:
                #     parent = q_state1.parent
                # else:
                #     parent = q_state2.parent
                # pdfa.add_transition(o1, parent, q_state1) #promote
                # queue.append([o, q_state1])
                # trajs.append(get_ix(q_state1, o))
                # states[o_int].append(q_state1)
                i[o_int]=i[o_int]+1
    print(pdfa.transitions)
    return pdfa


def get_int(o):
    return ord(o)-97