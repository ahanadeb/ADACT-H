import numpy as np


def solve_mdp(pdfa, gamma =0.9):
    keys = [s.name for s in pdfa.states]
    values = [0]*len(pdfa.states)
    dictionary = dict(zip(keys, values))

    for i in range(100):
        for s in pdfa.states:
            #get connected states
            for tr in pdfa.transitions:
                if tr[0]==s.name:




            if s.name in pdfa.transitions:
                for a in pdfa.transitions[s.name]:
                    for q in pdfa.transitions[s.name][a]:
                        q_state = get_state_from_name(q, pdfa)
                        if a in a_dict:
                            #print(a, a_dict[a])
                            s.VA[a_dict[a]] = s.A[a_dict[a]]+ gamma*max(q_state.VA)



    return pdfa

def get_optimal_policy(pdfa,a_dict1):
    for q in pdfa.states:
        if q!=pdfa.initial_state:
            pdfa.policy[q.name]= a_dict1[(q.VA).index(max(q.VA))]

    return pdfa



def get_state_from_name(s, pdfa):
    for q in pdfa.states:
        if q.name ==s:
            return q
    raise ValueError('Incorrect state query, '+ s+ " not present in pdfa.")


def get_V_max(pdfa):
    V_max = -1000
    for q in pdfa.states:
        if q.V >= V_max:
            V_max=q.V#.copy()
    return V_max