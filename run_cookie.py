from src.utils_pdfa.test import RDPState, simTMaze
from src.utils_pdfa.learnRDP import  learnRDP2
import numpy as np
from src.utils_pdfa.renderRDP import render
import sys
from src.utils_pdfa.save_to_json import save_json
import time
def main():
    H = int(sys.argv[2])
    K = int(sys.argv[3])
    thres = float(sys.argv[4])

    #print("env/"+sys.argv[1]+"/"+ sys.argv[1]  + '.POMDP')

    RDPState.Data = simTMaze("env/"+sys.argv[1]+"/" + sys.argv[1] + '.POMDP', K, H)

    #RDPState.Data = get_env(K, H)

    print(RDPState.Data)
    print(type(RDPState.Data))

    RDPState.Act = np.array([[set(RDPState.Data[i][j][0]) for j in range(H + 1)] for i in range(K)])
    RDPState.Obs = np.array([[set(RDPState.Data[i][j][1]) for j in range(H + 1)] for i in range(K)])
    RDPState.Rew = np.array([[set(RDPState.Data[i][j][2]) for j in range(H + 1)] for i in range(K)])
    RDPState.Trp = np.array([[set([RDPState.Data[i][j]]) for j in range(H + 1)] for i in range(K)])



    for j in range(H+1):
        RDPState.Act[:, H - 1 - j] = [RDPState.Act[i, H - 1 - j].union(RDPState.Act[i, H - j]) for i in range(K)]
        RDPState.Obs[:, H - 1 - j] = [RDPState.Obs[i, H - 1 - j].union(RDPState.Obs[i, H - j]) for i in range(K)]
        RDPState.Rew[:, H - 1 - j] = [RDPState.Rew[i, H - 1 - j].union(RDPState.Rew[i, H - j]) for i in range(K)]
        RDPState.Trp[:, H - 1 - j] = [RDPState.Trp[i, H - 1 - j].union(RDPState.Trp[i, H - j]) for i in range(K)]
    t = time.time()
    RDP = learnRDP2(H,9, thres)
    print("time taken: ", time.time()-t)
    print("State space: ", len(RDP.states))
    graph = render(RDP)
    savefile = "/graphs/" + sys.argv[1] + sys.argv[2] +"_K_"+ str(K)
    graph.render("." + savefile)
    print("Graph saved at: ", savefile+".svg")
    save_json(RDP,sys.argv)
    print(RDP.transitions)



if __name__ == "__main__":
    main()