import random
import numpy as np

Action = {}
class Cookie():
    def __init__(self):
        self.state = {'button': False, 'cookie': False}
        self.actions = {1:['right'], 2:['right', 'left','up'],3:['left'], 4: ['down']}
        self.colors = {1: 'blue', 2:'white', 3:'green', 4:'red'}
    def initialise(self):
        self.initial_states=random.choice([1,2,3,4])
        #self.current_state = self.initial_states
        self.current_state = 2
        self.state = {'button': False, 'cookie': False}

    def get_action(self):
        actions = self.actions[self.current_state]
        # if self.state['button']==True:
        #     if 'press' in actions:
        #         actions.remove('press')
        # if self.state['cookie']==False or self.state['cookie']!=self.current_state:
        #     if 'eat' in actions:
        #         actions.remove('eat')
        # if self.state['cookie'] == self.current_state:
        #     actions  = ['eat']
        if self.current_state == 4:
            actions = ['down']


        return actions

    def do_action(self,a):

        r = 0
        if a == 'right':
            if self.current_state ==1:
                o='white'
                self.current_state = 2
                return  o , r
            else:
                o = 'green'
                if self.state['cookie'] == 3:
                    o = o + " cookie"
                    r = 1
                    self.state['cookie'] = False
                    self.state['button'] = False
                self.current_state = 3
                return  o , r
        if a == 'left':
            if self.current_state ==3:
                o='white'
                self.current_state = 2
                return  o, r
            else:
                o = 'blue'
                if self.state['cookie'] == 1:
                    o = o + " cookie"
                    r =1
                    self.state['cookie'] = False
                    self.state['button'] = False
                self.current_state = 1
                return  o , r

        if a == 'up':
            o = 'red'
            self.current_state = 4
            self.state['button'] = True
            if random.uniform(0, 1) > 0.5:
                self.state['cookie'] = 1
                # print("cookie set at 1")
            else:
                self.state['cookie'] = 3
            return  o , r
        if a == 'down':
            o = 'white'
            self.current_state = 2
            return o , r
        # if a == 'eat':
        #     o = self.colors[self.current_state]
        #     self.state['cookie']=False
        #     self.state['button']=False
        #     r = 1
        #     return o , r
        # if a == 'press':
        #     self.state['button'] = True
        #     if random.uniform(0, 1) > 0.5:
        #         self.state['cookie']=1
        #         #print("cookie set at 1")
        #     else:
        #         self.state['cookie'] = 3
        #         #print("cookie set at 3")
        #     o = self.colors[self.current_state]
            return o, r

def test_cookie_domain(K,H,o_dict,a_dict, o_dict1):
    D = np.empty((K, H + 1), dtype=np.dtype('U3'))
    cookie_domain = Cookie()
    for k in range(0,K):
        cookie_domain.initialise()
       # print("first state: ", cookie_domain.current_state)
       #  first_obs[k] = cookie_domain.current_state
        l=[]
        l_n=[]
        D[k, 0] = '{}{}{}'.format(chr(65 + 0), chr(97 + cookie_domain.current_state), chr(48 + 0))
        l.append([0, cookie_domain.current_state, 0])
        l_n.append("0 "+ str(cookie_domain.current_state))
        for h in range(0,H):
            actions = cookie_domain.get_action()
            a = random.choice(actions)
            o, r = cookie_domain.do_action(a)
            a_n = a_dict[a]
            o_n = o_dict[o]
            l_n.append("action: "+ str(a)+ " observation: "+ str(o)+ " r: "+ str(r))
            #D[k,h+1] = np.array([a_n, o_n, r])
            l.append([a_n, o_n, r])
            D[k, h + 1] = '{}{}{}'.format(chr(65 + a_n), chr(97 + o_n), chr(48 + r))
        # write data to file (change location)
        # print(l_n)
        # print(l)

    return D

def get_env(K, H):
    o_dict = {'blue': 1, 'white': 2, 'green': 3, 'red': 4, 'green cookie':5, 'blue cookie': 6 }
    a_dict = {'right': 0, 'left': 1, 'up': 2, 'down': 3, 'press': 4, 'eat': 5}
    o_dict1 = {1: 'blue', 2: 'white', 3: 'green', 4: 'red', 5: 'green cookie', 6:'blue cookie'}
    a_dict1 = {0: 'right', 1: 'left', 2: 'up', 3: 'down', 4: 'press', 5: 'eat'}
    D= test_cookie_domain(K, H, o_dict, a_dict, o_dict1)
    return D