import copy
from Dealer import EvaluateProb

p = 0.35
n=40
DealerProb = EvaluateProb(p)
# print DealerProb
# 2 is 0th element and so on

AllStatePolicies={}
# State -> (Move, Probability Winning)

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

	def __repr__(self):
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

def GetMaxValidScore(inputState):
	posscores = PossibleScores(inputState)
	msofar=0
	for elem in posscores:
		if elem <=21:
			msofar = max(msofar,elem)
	return msofar

def CalculateWinningStatic(arr,elem):
	ans=0
	for i in xrange(0,elem):
		ans+=arr[i]
	return ans

def MakeChildren(inputState):
	ns1 =State(inputState.NumCards+1, inputState.NumAce +1, inputState.FixedCardVal, inputState.BetVal)
	ans=[]
	if GetMaxValidScore(ns1):
		ans.append((ns1,(1.0-p)/9))
	for i in xrange(1,10):
		newstate=(State(inputState.NumCards+1, inputState.NumAce,i+inputState.FixedCardVal, inputState.BetVal),(1.0-p)/9.0)
		if GetMaxValidScore>0:
			ans.append(newstate)
	newstate=(State(inputState.NumCards+1, inputState.NumAce,10+inputState.FixedCardVal, inputState.BetVal),p)
	if GetMaxValidScore>0:
		ans.append(newstate)
	return ans

Allcount=0

def DecideMove(s):
	# print s, GetMaxValidScore(s)
	global AllStatePolicies
	if s in AllStatePolicies:
		global Allcount
		Allcount+=1
		return AllStatePolicies[s]
	elif GetMaxValidScore(s)==0:
		AllStatePolicies[s]=("H",0.0)
		return AllStatePolicies[s]
	else:
		possibilities= ["H","S"]
		# Considering S
		presscore = GetMaxValidScore(s)
		WinningAmountS = CalculateWinningStatic(DealerProb, presscore)

		# Considering H
		AllChildren = MakeChildren(s)
		if len(AllChildren):
			MovesDecided = map(lambda x: x[1]*DecideMove(x[0])[1], AllChildren)
			WinningAmountH = sum(MovesDecided)

			if WinningAmountH>WinningAmountS:
				AllStatePolicies[s]= ("H",WinningAmountH)
			else:
				AllStatePolicies[s]=("S",WinningAmountS) 
		else:
			AllStatePolicies[s]=("S",WinningAmountS) 	
		return AllStatePolicies[s]

p=State(2,0,6,1)
q=State(2,0,6,1)
print PossibleScores(p)
# print p==q
a={}
a[p]="H"
a[q]="D"
# print str(q)
# print MakeChildren(p)
# print p in a
# print DecideMove(p)
# print Allcount
# print len(ans)

for elem in DealerProb:
	print elem