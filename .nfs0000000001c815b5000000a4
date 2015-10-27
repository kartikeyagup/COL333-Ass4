import copy
from Dealer import EvaluateProb

p = 4.0/13
n=40
DealerProb = EvaluateProb(p)
# print DealerProb
for i in xrange(len(DealerProb)):
	print i+2, DealerProb[i]	
# 2 is 0th element and so on

print "p",p

AllStatePolicies={}
# State -> [(Move, Value winning) list]

def Compress(n):
	if n<=2:
		return n
	else:
		return 3
# Add probability to the state
class State:
	def __init__(self,numcards,numace,fixedval):
		self.NumCards=numcards
		self.NumAce=numace
		self.FixedCardVal = fixedval

	def __eq__(self,othr):
		return (Compress(self.NumCards),self.NumAce,self.FixedCardVal)==(Compress(othr.NumCards),othr.NumAce,othr.FixedCardVal)

	def __hash__(self):
		return hash((Compress(self.NumCards),self.NumAce,self.FixedCardVal)) 

	def __str__(self):
		return ",".join(map(str,[self.NumCards,self.NumAce, self.FixedCardVal]))

	def __repr__(self):
		return ",".join(map(str,[self.NumCards,self.NumAce, self.FixedCardVal]))


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
	# TODO: Check for blackjack
	# TODO: Put in values correctly
	ans=-1
	if (0<elem<=21):
		ans=arr[22]
		for i in xrange(17,elem):
			ans+=arr[i]
		for i in xrange(elem+1,22):
			ans-=arr[i]
	return ans

def MakeChildren(inputState):
	ns1 =State(inputState.NumCards+1, inputState.NumAce +1, inputState.FixedCardVal)
	ans=[]
	if GetMaxValidScore(ns1):
		# print "p",p
		ans.append((ns1,(1.0-p)/9))
	for i in xrange(2,10):
		newstate=(State(inputState.NumCards+1, inputState.NumAce,i+inputState.FixedCardVal),(1.0-p)/9.0)
		if GetMaxValidScore(newstate[0])>0:
			ans.append(newstate)
	newstate=(State(inputState.NumCards+1, inputState.NumAce,10+inputState.FixedCardVal),p)
	if GetMaxValidScore(newstate[0])>0:
		ans.append(newstate)
	return ans

def AddAll(BigArr):
	ans=[0]*len(BigArr[0])
	for elem in BigArr:
		for k in xrange(len(elem)):
			ans[k]+=elem[k][1]
	return ans

Allcount=0

def PutFactor(prob,AllChild):
	# Puts in new probability factor with a given state vector
	ans=[0]*len(AllChild)
	for i in xrange(len(AllChild)):
		ans[i]=(AllChild[i][0],AllChild[i][1]*prob)
	return ans

def DecideMove(s):
	# print s, GetMaxValidScore(s)
	global AllStatePolicies
	if s in AllStatePolicies:
		# global Allcount
		# Allcount+=1
		return AllStatePolicies[s]
	elif GetMaxValidScore(s)==0:
		AllStatePolicies[s]=[("H",0.0) for i in xrange(10)]
		return AllStatePolicies[s]	
	else:
		possibilities= ["H","S"]
		# Considering S
		presscore = GetMaxValidScore(s)
		WinningAmountS = []
		for elem in DealerProb:
			WinningAmountS.append(CalculateWinningStatic(elem, presscore))

		# Considering H
		AllChildren = MakeChildren(s)
		if len(AllChildren):
			MovesDecided = map(lambda x: PutFactor(x[1],DecideMove(x[0])), AllChildren)
			WinningAmountH = AddAll(MovesDecided)
			# print WinningAmountH
			tempans = [0]*10

			for i in xrange(10):
				if WinningAmountH[i]>WinningAmountS[i]:
					tempans[i]= ("H",WinningAmountH[i])
				else:
					tempans[i]=("S",WinningAmountS[i]) 
			AllStatePolicies[s]=tempans
		else:
			AllStatePolicies[s]=[("S",WinningAmountS[i]) for i in xrange(10)]	
		return AllStatePolicies[s]

def CalcWinningAmtDoubled(InputState):
	ans=[0.0]*10
	sc= GetMaxValidScore(InputState[0])
	for i in xrange(10):
		ans[i]=2*InputState[1]*CalculateWinningStatic(DealerProb[i],sc)
	return ans

def CompressD(InputArr):
	ans=[0.0]*10
	for elem in InputArr:
		for i in xrange(len(elem)):
			ans[i]+=elem[i]
	return ans

def DecideMoveWithDouble(s):
	global AllStatePolicies
	if s in AllStatePolicies:
		return AllStatePolicies[s]
	elif GetMaxValidScore(s)==0:
		AllStatePolicies[s]=[("H",0.0) for i in xrange(10)]
		return AllStatePolicies[s]	
	else:
		possibilities= ["H","S","D"]
		# Considering S
		presscore = GetMaxValidScore(s)
		WinningAmountS = []
		for elem in DealerProb:
			WinningAmountS.append(CalculateWinningStatic(elem, presscore))

		# Considering H,D
		AllChildren = MakeChildren(s)
		if len(AllChildren):
			MovesDecided = map(lambda x: PutFactor(x[1],DecideMove(x[0])), AllChildren)
			WinningAmountH = AddAll(MovesDecided)
			
			MovesD = map(CalcWinningAmtDoubled, AllChildren)
			WinningAmountD = CompressD(MovesD)

			tempans = [0]*10

			for i in xrange(10):
				if WinningAmountD[i]>WinningAmountH[i] and WinningAmountD[i]>WinningAmountS[i]:
					tempans[i]= ("D",WinningAmountD[i])	
				elif WinningAmountH[i]>WinningAmountS[i] and WinningAmountH[i]>WinningAmountD[i]:
					tempans[i]= ("H",WinningAmountH[i])
				else:
					tempans[i]=("S",WinningAmountS[i]) 
			AllStatePolicies[s]=tempans
		else:
			AllStatePolicies[s]=[("S",WinningAmountS[i]) for i in xrange(10)]	
		return AllStatePolicies[s]

def MakeChildrenSplit(card):
	ans =[0.0]*10
	for i in xrange(10):
		ans[i]=((card,i+2),(1.0-p)/9)
	ans[8] = ((card,10),p)
	return ans

def NewState(card1,card2):
	numac = 0
	fixval = 0
	if card1==11:
		numac+=1
	else:
		fixval += card1
	if card2==11:
		numac+=1
	else:
		fixval += card2
	return State(2, numac, fixval)

def CalculateWinningSplitA(state):
	ans=[0.0]*10
	# print state
	sc= GetMaxValidScore(NewState(state[0][0],state[0][1]))
	for i in xrange(10):
		ans[i]=state[1]*CalculateWinningStatic(DealerProb[i], sc)
	return ans


def DecideMoveSplit(cards1,cards2):
	if cards1!=cards2:
		return DecideMoveWithDouble(NewState(cards1,cards2))
	else:
		if cards1==11:
			# Case of Ace
			Children = MakeChildrenSplit(cards1)
			TotalSofar = [0.0]*10
			outputamt = map(CalculateWinningSplitA, Children)
			WinningAmountP = CompressD(outputamt)
			NormalAns = DecideMoveWithDouble(State(2,2,0))
			ans =[0]*10
			for i in xrange(10):
				if NormalAns[i][1]>WinningAmountP[i]:
					ans[i]=NormalAns[i]
				else:
					ans[i]=("P",WinningAmountP[i])
			return ans
		else:
			Children = MakeChildrenSplit(cards1)
			TotalSofar = [0.0]*10
			den = 1.0
			for elem in Children:
				if elem[0][0]== elem[0][1]:
					den -= 2*elem[1]
				else:
					TempEval = DecideMoveSplit(elem[0][0],elem[0][1])
					for i in xrange(10):
						TotalSofar[i] += 2*elem[1]*TempEval[i][1]
			expscore = []
			if den!=0:
				expscore = map (lambda x: x/den, TotalSofar)
			else:
				# TODO change
				expscore = [9999]*10	
			NormalMoves = DecideMoveWithDouble(NewState(cards1,cards2))
			ans=[0.0]*10
			for i in xrange(10):
				if NormalMoves[i][1]>expscore[i]:
					ans[i] = NormalMoves[i]
				else:
					ans[i] = ("P",expscore[i])
			return ans

# q=State(2,0,6,1)
# print PossibleScores(p)
# print p==q
# a={}
# a[p]="H"
# a[q]="D"
# print str(q)
# print MakeChildren(p)
# print p in a

# print map(lambda x: (NewState(x[0][0],x[0][1]),x[0]) ,MakeChildrenSplit(11))

ArrAns =[]
for i in xrange(5, 20):
	p1=State(2,0,i)
	# print p1,MakeChildren(p1)
	ArrAns.append(DecideMoveWithDouble(p1))
	print p1, "______", ArrAns[-1], len(AllStatePolicies)
for j in xrange(2,10):
	p1 = State(2, 1, j)
	ArrAns.append(DecideMoveWithDouble(p1))
	print p1, "______", ArrAns[-1], len(AllStatePolicies)
for j in xrange(2,12):
	ArrAns.append(DecideMoveSplit(j,j))
	print j,j,"______", ArrAns[-1], len(AllStatePolicies)

	# break
# p2 = State(2,0, 6)
# print p2, "______", DecideMove(p2), len(AllStatePolicies)

# print MakeChildren(p1)
# print Allcount
# print len(ans)

# for elem in AllS	tatePolicies:
	# print elem

# for elem in DealerProb:
# 	print elem