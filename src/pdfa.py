class PDFA:
    def __init__(self, q0):
        self.initial_state = q0
        self.transitions = []
        self.name_counter = 1
        self.states = []
        self.states.append(q0)

    def get_name(self):
        name = "u" + str(self.name_counter)
        self.name_counter += 1
        return name

    def add_transition(self,q1, u1,   a, o, u2,merge=False):
        if not merge:
            # a = q2.a
            # o = q2.o
            # r = q2.r
            self.transitions.append([q1, u1.name, a, o, u2.name])
        else:
            # a = q3.a
            # o = q3.o
            # r = q3.r
            self.transitions.append([q1, u1.name, a, o, u1.name])
            print("appending", [q1, u1.name, a, o, u1.name])
            u1.ix = list(set(u2.ix)) + list(set(u1.ix) - set(u2.ix))
            u1.add_traj(u1.ix, o)
        if u2 not in self.states:
            self.states.append(u2)
        if u1 not in self.states:
            self.states.append(q1)

