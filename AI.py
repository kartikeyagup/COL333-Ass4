import copy
# DictMapping = {}

n=40
DealerProb = [1.0/n for i in xrange(n)]

# def GetMove():


# def Calcval(initset):


# def MakeProbabilities(initset,probface):
# 	global DictMapping
# 	if Calcval(initset)<=21:
# 		probnormal = (1 - probface)/

# a=[[]]
# b=[i+1 for i in xrange(11)]

# ans=[]
# while len(a):
# 	s=a.pop()
# 	if sum(s)>=21:
# 		ans.append(s)
# 	else:
# 		for elem in b:
# 			a+=[s+[elem]]

AllStatePolicies={}
# State -> (Move, Neutral Score Beyond This Point, )

def GetExpectedScore(l1,l2,amt):
	ans=0.0
	for i in xrange(len(l1)):
		for j in xrange(i):
			ans+= amt*l1[i]*l2[j]
	return ans	

# Add probability to the state
class State:
	def __init__(self,numcards,numace,fixedval,betval):
		self.NumCards=numcards
		self.NumAce=numace
		self.FixedCardVal = fixedval
		self.BetVal = betval

	def __eq__(self,othr):
		return (self.NumCards,self.NumAce,self.FixedCardVal)==(othr.NumCards,othr.NumAce,othr.FixedCardVal)

	def __hash__(self):
		return hash((self.NumCards,self.NumAce,self.FixedCardVal)) 

	def __str__(self):
		return ",".join(map(str,[self.NumCards,self.NumAce, self.FixedCardVal,self.BetVal]))

def PossibleScores(inputState):
	posscores=[inputState.FixedCardVal]
	for i in xrange(inputState.NumAce):
		temp = copy.deepcopy(posscores)
		for i in xrange(len(temp)):
			temp[i]+=11
			posscores[i]+=1
		posscores += temp
	return posscores

def DecideMove(s):
	global AllStatePolicies
	if s in AllStatePolicies:
		return AllStatePolicies[s]
	else:
		possibilities= ["H","S"]
		# Considering S


p=State(2, 0, 6,1)
q=State(2,0,6,1)
print PossibleScores(p)
# print p==q
a={}
a[p]="H"
a[q]="D"
print str(q)
print p in a
# print len(ans)