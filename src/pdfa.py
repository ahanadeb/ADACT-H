class PDFA:
    def __init__(self, q0):
        self.initial_state = q0
        self.transitions = []
        self.name_counter = 1
        self.states = []
        self.states.append(q0)

    def get_name(self):
        name = "q" + str(self.name_counter)
        self.name_counter += 1
        return name

    def add_transition(self,o1, q1, q2,  a, o, r,merge=False):
        if not merge:
            # a = q2.a
            # o = q2.o
            # r = q2.r
            self.transitions.append([o1, q1.name, a, o, r, q2.name])
        else:
            # a = q3.a
            # o = q3.o
            # r = q3.r
            self.transitions.append([o1, q1.name, a, o, r, q2.name])
            q1.ix = list(set(q2.ix)) + list(set(q1.ix) - set(q2.ix))
            q1.add_traj(q1.ix, o1)
        if q2 not in self.states:
            self.states.append(q2)
        if q1 not in self.states:
            self.states.append(q1)

