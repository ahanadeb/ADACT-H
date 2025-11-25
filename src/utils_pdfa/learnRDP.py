import numpy as np
from numpy.matlib import empty

from src.utils_pdfa.RDP_utils import *
from src.pdfa import PDFA

def learnRDP_prior(H,obs, thres):
    u0= RDPState("q0")
    q0 = RDPState("q0")
    pdfa = PDFA(q0)
    D = q0.Data
    queue=[]
    queue.append([u0,q0])
    i={u0:1}
    while len(queue)!=0:
        [u_p,u_r] = queue.pop(0)
        U_new = get_candidates_ao(u_r, pdfa)
        #create the new state
        for u in U_new:
            j = i[u_p]
            for k in range(0, i[u_p]-1):
                for [a,b] in queue:
                    if b.t==k:
                        if not test_distinct2(u, b, H, thres):
                            j = k
            pdfa.add_transition()
            brek


    return pdfa

def learnRDP3(H,obs, thres,K):
    prior_pdfa = ['q0', 'q1', 'q2', 'q3' ,'q4', 'q5']
    i={'q0':0, 'q1':0, 'q2':0, 'q3':0 ,'q4':0}
    a1=['A', 'B', 'C', 'D']
    o1 =['a', 'b', 'c', 'd', 'e', 'f']
    AO = [(x,y) for x in a1 for y in o1]
    u0= RDPState("u0")
    pdfa = PDFA(u0)
    D = u0.Data
    i['q0']=1
    Q =[]
    Q.append(['q0',u0])
    traj_dict={'q0u0':np.arange(K)}
    suffix_dict = {'q0u0':D}
    Q_copy = []
    Q_copy.append(['q0',u0])
    time = 0
    while Q :
        time= time +1
        print("STARTING", Q)

        qu=Q.pop()
        q = qu[0]
        o_prior = chr(int(q[1])+97)
        u=qu[1]
        print("popped out", u.name, u.ix)
        if u.t == H:
            break
        for ao in AO:

            a = ao[0]
            o = ao[1]
            q_next = prior_pdfa[ord(o)-97]
            suffixes = get_suffixes23(q, o_prior, u, ao)
            if not suffixes and u.t==1:
                suffixes = get_suffixes23(q, 'c', u, ao)
                print(suffixes)



            if suffixes:
                print("Ech")
                merge = False

                u2 = RDPState(pdfa.get_name(), u, ao[0], o, 0)
                u2.ix=suffixes
                u2.trajs_set[o] = suffixes
                for qu_prev in Q_copy:
                    u_prev = qu_prev[1]
                    # the prior state HAS TO BE q_next
                    print("prev list",qu_prev[0], q_next, u_prev.name)
                    similar, p = test_distinct(u_prev,u2, o,H, thres )
                    print("similar", similar)
                    if p == False:
                        print("skip1")
                        continue
                    if similar:
                        merge = True
                        to_merge_to=qu_prev
                        print("merging ", u_prev.name, " with ", u2.name)
                        pdfa.add_transition(qu_prev[0], u2.parent, a, o, u_prev, merge=True)
                        print("check2", pdfa.transitions)
                        # Q.append([q_next, u2])
                        Q.append(['q4', u2])
                        Q_copy.append(['q4', u2])

                        break
                    #add transition funciton
                    # print("promoting directly", u2.name)
                    # print("check1", pdfa.transitions)
                    pdfa.add_transition(q, u, a, o, u2)
                    print("check11", pdfa.transitions)
                    #add to queue
                    Q.append([q_next, u2])

                    Q_copy.append([q_next, u2])
                    print("added ", Q)



            #get suffixes
    print("final", pdfa.transitions)
    # for s in pdfa.states:
    #     print("reve", s.name, s.ix)

    return pdfa

            # so here at u with observation o and a, get suffixesdsa                `


def learnRDP2(H, obs, thres):
    prior_pdfa = ['qi', 'q0', 'q1', 'q2', 'q3', 'q4']
    i = {'q0': 0, 'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0}
    queue = []  #queue of all ao
    states = [[] for _ in range(obs)]
    q0 = RDPState("q0")
    pdfa = PDFA(q0)
    D = q0.Data

    # for k in range(D.shape[0]):
    #     o = D[k, 0][1]
    #     o_int = ord(D[k, 0][1]) - 97
    #     if i[o_int] == 0:
    #         queue.append([o, q0])
    #         # get the trajectories here, and put them in a queue directly
    #         q0.add_traj(get_ix(q0, o), o)
    #         states[o_int].append(q0)
    #         pdfa.add_transition(o, q0, q0, D[k, 0][0], o, D[k, 0][2])
    #         i[o_int] = 1

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
