from src.utils_pdfa.RDP_utils import *
from src.pdfa import PDFA


def learnRDP2(H, obs, thres):
    queue = []  #queue of all ao
    states = [[] for _ in range(obs)]
    i = [0] * obs
    q0 = RDPState("q0")
    pdfa = PDFA(q0)
    D = q0.Data
    for k in range(D.shape[0]):
        o = D[k, 0][1]
        o_int = ord(D[k, 0][1]) - 97
        if i[o_int] == 0:
            queue.append([o, q0])
            # get the trajectories here, and put them in a queue directly
            q0.add_traj(get_ix(q0, o), o)
            states[o_int].append(q0)
            pdfa.add_transition(o, q0, q0, D[k, 0][0], o, D[k, 0][2])
            i[o_int] = 1

    while len(queue)!=0:
        ou = queue.pop(0)
        u1 = ou[1]
        o1 = ou[0]
        # traj1 = trajs.pop(0)

        AO = get_candidate(o1,u1, H)  #get ao sets (can we get this set at thw start?
        # print("from ", o1, u1.name, " getting candidates : ")
        # print("AO",AO)
        for ao in AO:
            a2 = ao[0]
            o2 = ao[1]
            o2_int = get_int(o2)
            # print(o1, u1.name, ao)
            # print("time", u1.t)
            traj2 = get_suffixes(pdfa, o1, u1, ao)

            #crete new candidate state here
            q2 = RDPState(pdfa.get_name(), u1, ao[0], o2, 0)
            q2.ix = traj2
            # print("name + trajs", q2.name, q2.ix)

            # q2.add_traj(traj2,o1)
            q2.add_traj(traj2,o2)
            j = i[o2_int]
            merge=False
            for k in range(i[o2_int]):
                #get all the u that are prefaced by o
                q3 = states[o2_int][k]
                # print("comparing ", q2.name, " ", q3.name)
                similar = test_distinct(q3, q2, o2, H, thres)
                if similar and merge==False:
                    j = k
                    state_to_merge_to=q3
                    merge=True
            if merge==True:
                #add the new state
                q3 = state_to_merge_to
                # print("merging ", q2.name, " to ", q3.name)
                # print("adding transition", o1, q2.parent.name, q3.name, a2, o2, 0)
                pdfa.add_transition(o1, q2.parent, q3, a2, o2, 0,  True)  #merge
                # queue.append([o1, q2])
            else:
                # print("promoting", q2.name)
                # print("adding transition", [o1, q2.parent.name, q2.name, a2, o2, 0])
                pdfa.add_transition(o1, q2.parent, q2, a2, o2, 0)
                # pdfa.add_transition(o1, parent, q2)  #promote
                queue.append([o2, q2])

                states[o2_int].append(q2)
                q2.add_traj(traj2, o2)
                i[o2_int] = i[o2_int] + 1
    # print(pdfa.transitions)
    return pdfa


def get_int(o):
    return ord(o) - 97
