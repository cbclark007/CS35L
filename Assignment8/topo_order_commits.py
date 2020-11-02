import os
import sys
import zlib

def topo_order_commits():
    #print("helloooo")
    cwd = os.getcwd()
    while(checkForGit(cwd) == False and len(cwd) != 1):
        #lastIndex = cwd.rfind('/')
        cwd = os.path.dirname(cwd)

    #we make it to the / directory
    if(len(cwd) <= 0):
        sys.stderr.write("Not inside a git repository")
        sys.exit(1)

    os.chdir(cwd)
        
    #cwd contains .git
    branch_dir = cwd + '/.git/refs/heads'
    branches = os.listdir(branch_dir)
    #print(branches)
    #print(branches[0])

    objects_dir = cwd + '/.git/objects'

    #print("now we look at the branches?")
    #print(branches)
    latest_commits = []
    hash_dict = dict()
    root_commits = set()
    for item in os.listdir(branch_dir):
        #print(item)
        filename = branch_dir + '/' + item
        if os.path.isdir(filename):
            for branch in os.listdir(filename):
                newpath = filename + '/' + branch
                contents = open(newpath, 'r').read()
                commit = contents[0:len(contents)-1]
                latest_commits.append(contents[0:len(contents)-1])
                branch_name = item + '/' + branch
                if commit in hash_dict:
                    hash_dict[commit].branches.add(branch_name)
                    continue
                commit_node = CommitNode(commit)
                commit_node.add_branch_name(branch_name)
                hash_dict.update({commit:commit_node})
            continue;
        #print(filename)
        contents = open(filename, 'r').read()
        #print(compressed_contents)
        commit = contents[0:len(contents)-1]
        latest_commits.append(contents[0:len(contents)-1])
        if commit in hash_dict:
            hash_dict[commit].branches.add(item)
            continue
        commit_node = CommitNode(commit)
        commit_node.add_branch_name(item)
        hash_dict.update({commit:commit_node})
    #print(latest_commits)


    #ok let's process the branches and the commits and such
    #hash_dict = dict()
    #root_commits = set()
    #branch_iter = 0
    #for commit in latest_commits:
    #    if commit in hash_dict:
    #        hash_dict[commit].branches.add(branches[branch_iter])
    #        branch_iter = branch_iter+1
    #        continue
    #    commit_node = CommitNode(commit)
    #    commit_node.add_branch_name(branches[branch_iter])
    #    hash_dict.update({commit: commit_node})
    #    branch_iter = branch_iter+1

    #let's put together the graph?
    #visited_hashes = set()
    for hashe in list(hash_dict):
        #print(hashe)
        update_hash_dict(hashe, objects_dir, hash_dict, root_commits)

    root_commits = sorted(root_commits)
    #sort everything:                                                                                                                                                       
    for hashe in hash_dict:
        hash_dict[hashe].branches = sorted(hash_dict[hashe].branches)
        hash_dict[hashe].parents = sorted(hash_dict[hashe].parents)
        hash_dict[hashe].children = sorted(hash_dict[hashe].children)

    #now we do dfs because we have our roots and our graph
    #print("dfs time")
    visited = set()
    stack = []
    printstack = []
    for root_commit in root_commits:
        stack.clear()
        stack.append(root_commit)
        while(len(stack)):
            v = stack.pop()
            #print(v)
            printstack.append(v)
            #check if v has been visited. If it has, next loop. Otherwise, we add it to visited
            if v in visited:
                continue
            visited.add(v)

            for child in hash_dict[v].children:
                if child not in visited:
                    stack.append(child)

    #print("printstack")
    #for i in range(len(printstack)):
    #    print(printstack.pop())

    #print("now we do the order")
    order = get_topo_ordered_commits(hash_dict, root_commits)
    #print(order)
    #for o in order:
    #    o_branches = hash_dict[o].branches
    #    print(o, end = " ")
    #    print(o_branches)

    #print()
    #print()
    #print("here we go")
    #print(order)
    #print()
    #sort everything:
    for hashe in hash_dict:
        hash_dict[hashe].branches = sorted(hash_dict[hashe].branches)
        hash_dict[hashe].parents = sorted(hash_dict[hashe].parents)
        hash_dict[hashe].children = sorted(hash_dict[hashe].children)

    #peep the branches
    #print()
    #for hashe in hash_dict:
    #    print(hashe)
    #    print(hash_dict[hashe].children)
    #    print()
    
    #now we go thru
    isFirst = True
    for i in range(len(order)):
        o_branches = hash_dict[order[i]].branches
        #last thing to be printed
        if(i == len(order)-1):
            print(order[i], end = "")
            for b in o_branches:
                print(" ", end=b)
            print()
            break
        #print(order[i], end = "")
        #if current item isn't a parent of previous item and has children, print those children
        if isFirst == False and order[i-1] not in hash_dict[order[i]].children:
            print("=", end = "")
            #print("OK")
            #print("order" + order[i])
            #print(hash_dict[order[i]].children)
            if len(hash_dict[order[i]].children) == 0:
                print()
            else:
                for child in hash_dict[order[i]].children:
                    print(child, end=" ")
                print()
            print(order[i], end = "")
            for b in o_branches:
                print(" ", end=b)
        #if next item is not a parent of current item, print the parents of current item
        elif order[i+1] not in hash_dict[order[i]].parents:
            print(order[i], end = "")
            for b in o_branches:
                print(" ", end=b)
            print()
            last_parent = hash_dict[order[i]].parents.pop()
            for p in hash_dict[order[i]].parents:
                print(p, end=" ")
            print(last_parent, end = "")
            hash_dict[order[i]].parents.append(last_parent)
            hash_dict[order[i]].parents = sorted(hash_dict[order[i]].parents)
            print("=")
        else:
            #print branches otherwise
            print(order[i], end = "")
            for b in o_branches:
                print(" ", end=b)
        print()
        isFirst = False

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()
        self.branches = set()

    def add_branch_name(self, branch_name):
        self.branches.add(branch_name)

def checkForGit(cwd):
    #print(cwd)
    scan = os.scandir()
    for entry in scan:
        if(entry.name == '.git' and entry.is_dir()):
            return True
    #if we make it to the / directory                                                                                                                                      
    if(cwd == '/'):
        sys.stderr.write("Not inside a git repository")
        sys.exit(1)
    return False

def update_hash_dict_recursion(hashe, objects_dir, hash_dict, root_commits):
    print(hashe)
    #we have the hash, now we access the object file that the hash points to and add parent                                                                              
    obj_file_path = objects_dir + '/' + hashe[0:2] + '/' + hashe[2:]
    print(obj_file_path)
    #with the file path, we unpack the object with zlib                                                                                                                  
    compressed_contents = open(obj_file_path, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents)
    decoded = decompressed_contents.decode('cp437')
    print("splitting")
    decoded_list = decoded.splitlines()
    print(decoded_list)
    parent_index = decoded.find('parent ')
    #if we can't find the parent, it hashe is a root node                                                                                                                
    if(parent_index == -1):
        root_commits.add(hashe)
        if hashe not in hash_dict:
            print("root and not in dict")
            hash_dict.update({hashe: CommitNode(hashe)})
        return
    parent_commit = decoded[parent_index+7:decoded.find('author')-1]
    #add parent to the commit we are on                                                                                                                                  
    hash_dict[hashe].parents.add(parent_commit)
    #add child to the parent                                                                                                                                             
    if parent_commit not in hash_dict:
        hash_dict.update({parent_commit: CommitNode(parent_commit)})
    hash_dict[parent_commit].children.add(hashe)
    update_hash_dict_recursion(parent_commit, objects_dir, hash_dict, root_commits)

def update_hash_dict(hashe, objects_dir, hash_dict, root_commits):
    hashe_set = []
    hashe_set.append(hashe)
    visited_hashes = set()
    visited_hashes.add(hashe)
    while(True):
        if len(hashe_set) == 0:
            break
        curr_hashe = hashe_set.pop()
        #print(hashe)
        #we have the hash, now we access the object file that the hash points to and add parent                                                                             
        obj_file_path = objects_dir + '/' + curr_hashe[0:2] + '/' + curr_hashe[2:]
        #print(obj_file_path)
        #with the file path, we unpack the object with zlib                                                                                                                 
        compressed_contents = open(obj_file_path, 'rb').read()
        decompressed_contents = zlib.decompress(compressed_contents)
        decoded = decompressed_contents.decode('cp437')
        #print(decoded)
        decoded_list = decoded.splitlines()
        #print("splititng")
        #print(decoded_list)
        didFindParent = False
        if curr_hashe not in hash_dict:
            hash_dict.update({curr_hash, CommitNode(curr_hash)})
            
        for line in decoded_list:
            parent_index = line.find('parent ')
            if parent_index == -1:
                continue
            didFindParent = True
            parent_commit = line[parent_index+7:]
            #print(parent_commit)
            hash_dict[curr_hashe].parents.add(parent_commit)
            if parent_commit not in hash_dict:
                hash_dict.update({parent_commit: CommitNode(parent_commit)})
            hash_dict[parent_commit].children.add(curr_hashe)
            if parent_commit not in visited_hashes:
                hashe_set.append(parent_commit)
                visited_hashes.add(parent_commit)
            #hashe = parent_commit
            
        #if we can't find the parent, it hashe is a root node                                                                                                               
        if didFindParent == False:
            root_commits.add(curr_hashe)
            if curr_hashe not in hash_dict:
                #print("root and not in dict")
                hash_dict.update({curr_hashe: CommitNode(curr_hashe)})
            if len(hashe_set) == 0:
                break
            else:
                continue
        #we can have more than one parent
        #parent_commit = decoded[parent_index+7:decoded.find('author')-1]
        #print("parent stuff")
        #print(parent_commit)
        #add parent to the commit we are on                                                                                                                                
        #hash_dict[hashe].parents.add(parent_commit)
        #add child to the parent                                                                                                                                                 
        #if parent_commit not in hash_dict:
        #    hash_dict.update({parent_commit: CommitNode(parent_commit)})
        #hash_dict[parent_commit].children.add(hashe)
        #hashe = parent_commit

def get_topo_ordered_commits(hash_dict, root_commits):
    order = []
    visited = set()
    gray_stack = []
    black_nodes = set()
    stack = list(root_commits)
    #print(stack)

    while(stack):
        v = stack.pop()
        if v in visited:
            #do something when v already visited
            #print("v is visited")
            if v in gray_stack:
                gray_stack.remove(v)
                black_nodes.add(v)
                order.append(v)
            continue
        visited.add(v)

        #while v isn't a child of the vertex on top of gray stack
        while len(gray_stack) > 0 and v not in hash_dict[gray_stack[-1]].children:
            g = gray_stack.pop()
            order.append(g)
        gray_stack.append(v)

        for c in hash_dict[v].children:
            #what do you do if v has already been visited?
            stack.append(c)

    #add the rest of the gray stack into order
    for g in range(len(gray_stack)):
        order.append(gray_stack.pop())

    return order

if __name__ == '__main__':
    topo_order_commits()
