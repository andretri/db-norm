# if there is a higher number than the no. of rows then its not valid
def ValidCheck(cols, board):
    flag = False
    tmp = board
    tmp = tmp.translate(None, ' -')
    for value in tmp:
        if int(value) > int(cols):
            print "Input not valid"
            flag = True
            break
    return flag


def SplitInput(inpt):
	deps = {}
	dps =  inpt.split(' ')
	for dp in dps:
		key, res = dp.split('-')
		for k in list(key):
			res = [tmp for tmp in list(res)]
			try:
				deps[k] = deps[k].union(set(res))
				#print deps
			except KeyError as err:
				deps[k] = set(res)
	return deps


def BuildGraph(grh, cols):
	graph = SplitInput(grh)
	for i in range(cols):
		try:
			graph[str(i+1)].union(set())
		except KeyError as err:
			graph[str(i+1)] = set()
	return graph


def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


def CalCands(graph):
	candsTmp = {}
	for vct in graph:
		tmp = dfs(graph, vct)
		candsTmp[vct] = tmp
		#print "DFS(",vct,"): ", candsTmp[vct]
	#print candsTmp
	return __CalCands(candsTmp)


def __CalCands(tmp):	
	board = set([str(i+1) for i in range(len(tmp))])
	cands = []
	for key in list(tmp):
		lst = tmp[key]
		if(lst == board):
			cands.append(set(key))
		else:
			k = __CalCands__(board, tmp, key)
			cands.append(k)
	cand = min(cands, key=len)
	cands = [cnd for cnd in cands if (len(cnd)==len(cand) and cnd != cand)]
	cands.append(cand)
	return cands


def __CalCands__(board, dfs_lst, dfs_key):
	board = board - dfs_lst[dfs_key]
	dfs_lst.pop(dfs_key, None)
	cnd = set(dfs_key)
	for key, value in sorted(dfs_lst.iteritems(), key=lambda (k,v): len(dfs_lst[k]), reverse=True):
		if (value <= board):
			#print value
			board = board - value
			cnd = cnd.union(set(str(key)))
	if (len(board) != 0):
		cnd = cnd.union(board)
	return cnd


def CatNF(cands, deps):
	#keys = [set(list(tmp.split('-')[0])) for tmp in deps.split(' ')]
	#results = [set(list(tmp.split('-')[1])) for tmp in deps.split(' ')]
	
	#print keys
	#print results
	
	deps = SplitInput(deps)
	cand = cands[0]
# 1-NF Check is redundant
	nf2 = True
	nf3 = True
	bcnf = True
	cause = None

# 2-NF Check
	for key in deps:
		if (set(key) < cand and len(cand.intersection(deps[key])) == 0 ):
			nf2 = False
			cause = "%s -> %s" %(key, deps[key])
			break

# 3-NF Check
	if(nf2):
		nf3, cause = __3NF__(cand, deps)

# Boyce-Codd Normal Form Check
	if(nf2 and nf3):
		print cands
		for key in deps:
			if (set(key) not in cands):
				bcnf = False
				cause = "%s -> %s" %(key, deps[key])
				break

# Final Conclusion
	if nf2:
		if nf3:
			if bcnf:
				return "Boyce-Codd Normal Form (BCNF)", None
			else:
				return "3rd Normal Form (3NF)", cause
		else:
			return "2nd Normal Form (2NF)", cause
	else:
		return "1st Normal Form (1NF)", cause


def __3NF__(candKey, deps):
	res = deps[next(iter(candKey))]
	for key in res:
		try:
			tmp = deps[key].union(set(key))
			if (tmp < res):
				return False, "%s -> %s" %(key, deps[key])
				break
		except KeyError as err:
			pass
	return True, None
