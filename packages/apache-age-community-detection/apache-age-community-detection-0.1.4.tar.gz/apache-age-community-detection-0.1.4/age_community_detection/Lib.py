import ctypes
import os

absolute_path = os.path.dirname(__file__)
absolute_path_ubuntu = absolute_path+ "/lib/library.so"
absolute_path_windows = absolute_path+ "/lib/library.dll"

try:
# # Load the shared library
    lib = ctypes.CDLL(absolute_path_windows)
except:
    lib = ctypes.CDLL(absolute_path_ubuntu)

get_community_assignment = lib.get_community_assignment
get_community_assignment.restype = ctypes.POINTER(ctypes.c_int)

def get_community(nodes, edges):

    arr = (ctypes.c_int * (len(edges)*2))()
    for i,[u,v] in enumerate(edges):
        arr[(i*2)] = u
        arr[i*2+1] = v
    
    nrows = len(edges)
    nodeCount = len(nodes)

    res = get_community_assignment(
        arr,
        ctypes.c_int(nrows),
        ctypes.c_int(nodeCount))
    
    
    res = [res[i] for i in range(len(nodes))]
    
    return res




