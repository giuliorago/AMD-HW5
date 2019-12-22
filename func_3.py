######################find the shortest ordered route functionality#########################

#to preapre the adjacnet matrix for graph
def add_edge_3(from_node, to_node,weight):
    global edges,weight_3
    graph3[from_node].append(to_node)
    graph3[to_node].append(from_node)
    graph3[from_node]=list(dict.fromkeys(graph3[from_node]))
    graph3[to_node] = list(dict.fromkeys(graph3[to_node]))
    weight_3[(from_node, to_node)] = weight
    weight_3[(to_node, from_node)] = weight

def printAllPathsUtil(u, d, visited, path,posi_data):

    # Mark the current node as visited and store in path
    visited[u] = True
    path.append(u)

    # If current vertex is same as destination, then print
    # current path[]
    if u == d:
        #print (path)
        data_to_append=path

        posi_data.append(data_to_append[:])
        #print(posi_data)
            #print(path)
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for i in graph3[u]:
            if visited[i] == False:
                if i in input_node_3:
                    printAllPathsUtil(i, d, visited, path,posi_data)

    path.pop()

    visited[u] = False

def printAllPaths(s, d,V3,posi_data):

    # Mark all the vertices as not visited
    visited = [False] * (V3)

    # Create an array to store paths
    path = []

    # Call the recursive helper function to print all paths
    printAllPathsUtil(s, d, visited, path,posi_data)

def create_graph_3():

    global tree, neighbour_node, edges_dist_cost, edges_time_cost, input_node, V2, graph2, graph_2_data,input_node_3,weight_3
    node_id_total = []
    edges = []

    # get the input parameters
    input_node_3 = []
    print("Enter the source node..")
    source_node_3 = input()
    print("Enter the list of input nodes")
    input_node_3_data = input()
    function_type_str = "Enter the type of function t(x,y), d(x,y) or network distance \n 1 for t(x,y) \n 2 for d(x,y) \n 3 for network distance"
    print(function_type_str)
    filter_fnc = input()
    print ("Network analysis has been started....Please wait...")
    with open(dist_graph_file, "r") as f:
        dist_data = f.readlines()
    for lines in dist_data:
        current_edges = []
        if "a" in lines.split(' ')[0]:
            node_id_total.append(int(lines.split(' ')[1]))
            node_id_total.append(int(lines.split(' ')[2]))
            current_edges.append(int(lines.split(' ')[1]))
            current_edges.append(int(lines.split(' ')[2]))
            edges.append(current_edges)
            edges_dist_cost.append(int(lines.split(' ')[3]))
    with open(time_graph_file, "r") as f:
        dist_data = f.readlines()
    for lines in dist_data:
        if "a" in lines.split(' ')[0]:
            edges_time_cost.append(int(lines.split(' ')[3]))
    node_id = list(set(list(node_id_total)))
    #total_node_3=len(node_id)+1
    total_node_3=max(node_id)+1

    #to find connected components
    mylist_new = []
    for item in edges:
        item.sort()
        mylist_new.append(item)
    #print(mylist_new)
    mylist_new.sort()
    mylist_new=list(mylist_new for mylist_new, _ in itertools.groupby(mylist_new))
    #print (len(mylist_new))
    #print (len(edges))
    #graph = nx.from_edgelist(mylist_new)
    #nodes_connected_fromsrc=list(nx.node_connected_component(graph,int(source_node_3)))
    #print("connected components",nodes_connected_fromsrc)

    #if (list(set(input_node_3)-set(nodes_connected_fromsrc))) ==[]:
        #connected_st=True
    #else:
        #connected_st = False

    if filter_fnc == '3':
        for data in edges:
            add_edge_3(data[0],data[1],1)

    elif filter_fnc == '2':
        for index,data in enumerate(edges):
            add_edge_3(data[0],data[1],edges_dist_cost[index])

    else:
        for index,data in enumerate(edges):
            add_edge_3(data[0],data[1],edges_time_cost[index])


    #getting the input nodes and conevrting them to a list from string
    input_node_3_data=input_node_3_data.split(",")
    input_node_3.append(int(source_node_3))
    for item in input_node_3_data:
        if item !="":
            input_node_3.append(int(item))
        #input_node_2.remove(',')
    #print (input_node_3)
    #preparing a combo list or pairing the input nodes based on permutations
    combo_list3=[]
    for index3,item in enumerate(input_node_3):
        try:
            combo_lits_3_data=[]
            combo_lits_3_data.append(item)
            combo_lits_3_data.append(input_node_3[index3+1])
            combo_list3.append(combo_lits_3_data)
        except:
            pass

    #get all possible paths between source H and list of input nodes
    #print ("combo_list",combo_list3)
    possible_paths_3=[]
    for item in combo_list3:
        posi_data_1=[]
        posi_data=[]
        printAllPaths(item[0], item[1],total_node_3,posi_data)
        #print ("posi_list",posi_data)
        for item_r in posi_data:
            posi_data_1.append(item_r)
        possible_paths_3.append(posi_data)

    #get all possible paths eligible
    #print ("possible_path_list",possible_paths_3)
    data_to_be_removed=[]
    for index, item in enumerate(possible_paths_3):
        data_to_be_removed_dummy=[]
        for cnt in item:
            #print (cnt)
            diff_data=list ((set(cnt)- set(input_node_3)))
            #print ("diff_data",diff_data)
            if diff_data != []:
                data_to_be_removed_dummy.append(cnt)
            else:
                data_to_be_removed_dummy.append([])
        data_to_be_removed.append(data_to_be_removed_dummy)
    #print ("data to be removed ",data_to_be_removed)
    for index_de,item_in in enumerate(data_to_be_removed):
        for item_de in item_in:
            if item_de !=[]:
                possible_paths_3[index_de].remove(item_de)

    #print("filtered possible paths",possible_paths_3)

    #get the shortest path between source H covering all input nodes
    shortes_ordered_path_array=[]
    for index, item in enumerate(possible_paths_3):
        if filter_fnc==3:
            short_list_array_index=find_shortest_path(item,3,weight_3)
            if short_list_array_index!=[]:
                shortes_ordered_path_array.append(item[short_list_array_index])
        elif filter_fnc==2:
            short_list_array_index = find_shortest_path(item, 2,weight_3)
            if short_list_array_index != []:
                shortes_ordered_path_array.append(item[short_list_array_index])
        else:
            short_list_array_index = find_shortest_path(item, 1,weight_3)
            if short_list_array_index != []:
                shortes_ordered_path_array.append(item[short_list_array_index])
    #print (shortes_ordered_path_array)



    shortes_ordered_path_list=[]
    for item in shortes_ordered_path_array:
        if len(item)>2:
            cnt = 0
            for i in range(len(item) - 1):
                split_list = []
                split_list.append(item[cnt])
                split_list.append(item[cnt + 1])
                shortes_ordered_path_list.append(split_list)
                cnt = cnt + 1
        else:
            shortes_ordered_path_list.append(item)
    #print ("Final shortested order path is ",shortes_ordered_path_list)

    # prepare the node_list for graph
    #this is plot the intermediate nodes separately which will be traversed while reaching the destination
    #for example to if the input nodes are 1,2,3,4
    #to reach 3 from 1 if 4 has to be traversed then 4 will be a intermediate node which will again be traversed after visting 3
    shortes_ordered_node_list = []
    shortest_ordered_value_list = []
    shortested_ordered_array_new = []
    replace_no = 0
    for item_node in shortes_ordered_path_array:
        if len(item_node) > 2:
            replace_elements = item_node[1:len(item_node) - 1]
            for item_replace in replace_elements:
                str_replace = str(item_replace) + "_dummy_" + str(replace_no)
                replace_no = replace_no + 1
                item_node = [str_replace if x == item_replace else x for x in item_node]
            cnt = 0
            for i in range(len(item_node) - 1):
                split_list = []
                split_list.append(item_node[cnt])
                split_list.append(item_node[cnt + 1])
                shortested_ordered_array_new.append(split_list)
                shortes_ordered_node_list.append(split_list[0])
                shortes_ordered_node_list.append(split_list[1])
                shortest_ordered_value_list.append(str(split_list[0]).split("_")[0])
                shortest_ordered_value_list.append(str(split_list[1]).split("_")[0])
                cnt = cnt + 1
        else:
            shortested_ordered_array_new.append(item_node)
            shortes_ordered_node_list.append(item_node[0])
            shortes_ordered_node_list.append(item_node[1])
            shortest_ordered_value_list.append(item_node[0])
            shortest_ordered_value_list.append(item_node[1])

    #print("node_list", shortes_ordered_node_list)
    #print("value list", shortest_ordered_value_list)
    # input()
    #print("Final shortested order path is ", shortes_ordered_path_list)
    #print("Final shortested order node path is ", shortested_ordered_array_new)


    #find if graph is possible
    #i.e if the possible path /shortest walkable streets contains all the input nodes or not
    nodes_3 = []
    for item in shortes_ordered_path_list:
        for data in item:
            nodes_3.append(data)
    nodes_3 = list(set(nodes_3))
    possible_st=list(set(input_node_3)-set(nodes_3))
    if possible_st==[]:
        possible_status=True
    else:
        possible_status=False
    #print ("Possible status ",possible_status)

    if possible_status==True:
        draw_graph_3(shortested_ordered_array_new,input_node_3,source_node_3)
    else:
        draw_graph_3("", input_node_3, source_node_3)

#draw the graph
def draw_graph_3(edges_3_draw,graph3_nodes,input_node_draw3):

    if edges_3_draw=="":
        plt.suptitle("No Routes possible")
    #since it is a directed graph
    options = {

        'arrowstyle': '-|>',
        'arrowsize': 10,
    }
    G = nx.MultiDiGraph()#directed graph
    nodes_color = []
    nodes_size = []
    graph3_nodes_4 = []
    graph3_nodes_4_value = []
    graph3_nodes_4_final = []
    for item in edges_3_draw:
        for item2 in item:
            if "_dummy" in str(item2): #finding intermediate nodes
                graph3_nodes_4.append(item2)
                graph3_nodes_4_value.append(str(item2).split("_")[0])
            else:
                graph3_nodes_4.append(item2)
                graph3_nodes_4_value.append(item2)

    for index, item in enumerate(graph3_nodes_4):
        G.add_node(item, value=graph3_nodes_4_value[index]) #adding nodes
    for item in G.nodes:
        if str(item) == str(input_node_draw3):
            nodes_color.append('yellow')
            nodes_size.append(200)
        elif "_dummy" in str(item):
            nodes_color.append('red')
            nodes_size.append(50)
        else:
            nodes_color.append('green')
            nodes_size.append(100)
    #print(nodes_color)
    #print(G.nodes)

    G.add_edges_from(edges_3_draw)
    labels = {}
    for i in G:
        labels[i] = G.nodes[i]['value'] #adding labels to nodes
    #print(labels)
    pos = nx.circular_layout(G)
    nx.draw_circular(G, node_size=nodes_size, node_color=nodes_color, with_labels=False)
    nx.draw_networkx_labels(G, pos, labels, font_size=12)

    #adding legends to graph
    red_patch = mpatches.Patch(color='green', label='Destination nodes')
    yellow_patch = mpatches.Patch(color='yellow', label='Input Node')
    green_patch = mpatches.Patch(color='red', label='Bypass nodes')
    plt.legend(handles=[red_patch, yellow_patch,green_patch], loc='lower right')
    plt.show()

#to find the shortest walkable path between two nodes in the graph
#these two nodes are framed from the input nodes
#cost of the nodes also considered
#if it is based o network distance cost will be considered as 1
def find_shortest_path(path_array,flt_fnc3,weight_array):
    if flt_fnc3==3:
        len_array=[]
        for item_path in path_array:
            len_array.append(len(item_path))
        #print (len_array.index(min(len_array)))
        if len_array!=[]:
            return len_array.index(min(len_array))
        else:
            return []

    else:
        cost_array=[]
        for item_path in path_array:
            cost=0
            combo_lit_flt = []
            #print (item_path)
            if len(item_path) > 2:
                cnt = 0
                for i in range(len(item_path) - 1):
                    split_list = []
                    split_list.append(item_path[cnt])
                    split_list.append(item_path[cnt + 1])
                    spliy=split_list
                    combo_lit_flt.append(spliy[:])
                    cnt = cnt + 1
            else:
                combo_lit_flt.append(item_path[:])
            #print (combo_lit_flt)
            for item in combo_lit_flt:
                cost=weight_array[(item[0], item[1])]+cost

            cost_array.append(cost)
        #print (cost_array)
        if cost_array != []:
            return cost_array.index(min(cost_array))
        else:
            return []
