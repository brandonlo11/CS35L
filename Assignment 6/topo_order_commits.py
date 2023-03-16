import os
import sys
import zlib
# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.

# I used strace to test that my code does not use additional commands by searching for exec commands

# Given function
def topo_order_commits():
    directory = findGit()
    branches = getBranches(directory)
    commitNodes, roots = buildGraph(directory, branches)
    sortedCommits = topoSort(commitNodes, roots)
    printGraph(commitNodes, sortedCommits, branches)

# Code given in assignment
class CommitNode:
    def __init__(self, commit_hash):
        """                                                                                    
        :type commit_hash: str                                                                 
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

# Create path to the git directory
def findGit():
    path = os.path.abspath(os.getcwd())
    while True:
        # If you get to root directory you are not in a git repository
        if os.path.dirname(path) == path:
            sys.stderr.write("No git directory found")
            sys.exit(1)
        for i in os.listdir(path):
            if i == ".git":
                return os.path.realpath(os.path.join(path, i))
        path = os.path.abspath(os.path.join(path, os.pardir))

# Create list of branches
def getBranches(path):
    # Add to git path in order to find heads directory
    path += "/refs/heads"
    # Dictionary of branches
    branches = {}
    # Iterate through all directories and subdirectories in heads
    for path, dirs, files in os.walk(path):
        for filename in files:
            # Open files and read commits
            commit = open(os.path.join(path,filename),"r").read().replace("\n", "")
            name = os.path.join(path,filename)[len(path)+1:]
            if commit not in branches:
                branches[commit] = []
                branches[commit].append(name)
    return branches

# Create graph of commits
def buildGraph(path, branches):
    # Add to git path in order to find objects directory
    path += "/objects/"
    roots = set()
    commitNodes = {}
    # Create CommitNode for commit if not in dictionary of nodes already
    for commit in branches:
        if commit not in commitNodes:
            commitNodes[commit] = CommitNode(commit)
        curr = commitNodes[commit]
        while True:
            # Find parents of commits by decompressing contents of the object file
            data = zlib.decompress(open(os.path.join(path, curr.commit_hash[0:2], curr.commit_hash[2:]), 'rb').read())
            text = str(data, 'utf-8', 'strict')
            text = text.split("\n")
            parents = []
            # Find lines with parents
            for line in text:
                if "parent" in line:
                    parents += (line.split()[1:])
            curr.parents = set(sorted(parents))
            # The node is a root node if no children
            if len(curr.parents) == 0:
                roots.add(curr.commit_hash)
                break
            # Add children
            for p in curr.parents:
                if p not in commitNodes:
                    commitNodes[p] = CommitNode(p)
                parent = commitNodes[p]
                parent.children.add(curr.commit_hash)
            curr = commitNodes[next(iter(curr.parents))]

    roots = sorted(roots)
    return commitNodes, roots

# Topological sort
def topoSort(commitNodes, roots):
    checked = set()
    sortedCommits = []
    # Use stack in order to sort topologically
    stack = list(roots)
    while stack:
        node = stack[-1]
        checked.add(node)
        added = False
        # Look at children of node on stack
        for child in sorted(commitNodes[node].children):
            if child not in checked:
                stack.append(child)
                added = True
                break
        if not added:
            sortedCommits.append(stack.pop())
    return sortedCommits

# Print the graph
def printGraph(commitNodes, sortedCommits, branches):
    # Flag to indicate whether the previous commit was a sticky commit
    sticky = False
    for i in range(len(sortedCommits)):
        hashPrint = sortedCommits[i]
        # If the previous commit was a sticky commit, print the children of the current commit with an "=" prefix
        if sticky:
            sticky = False
            stickyHashPrint = " ".join(commitNodes[hashPrint].children)
            print(f"={stickyHashPrint}")
        # If the current commit is a branch head, print the branch name(s) after the commit hash
        if hashPrint in branches:
            sortedBranches = sorted(branches[hashPrint])
        else:
            sortedBranches = []
        if branches:
            print(hashPrint+(" "+" ".join(sortedBranches)))
        else:
            print(hashPrint+("   "))
        # If the next commit is not a parent of the current commit, print a sticky commit
        if len(sortedCommits) > (i+1):
            if sortedCommits[i+1] not in commitNodes[hashPrint].parents:
                sticky = True
                stickyHashPrint = " ".join(commitNodes[hashPrint].parents)
                print(f"{stickyHashPrint}=\n")
            
if __name__ == '__main__':
    topo_order_commits()
