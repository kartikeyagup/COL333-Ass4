import copy
# DictMapping = {}

n=40
DealerProb = [1.0/n for i in xrange(n)]

AllStatePolicies={}

class State:
	def __init__(self,numace,fixedval):
		self.NumAce=numace
		self.FixedCardVal = fixedval

	def __eq__(self,othr):
		return (self.NumAce,self.FixedCardVal)==(othr.NumAce,othr.FixedCardVal)

	def __hash__(self):
		return hash((self.NumAce,self.FixedCardVal)) 

	def __str__(self):
		return ",".join(map(str,[self.NumAce, self.FixedCardVal]))

def PossibleScores(inputState):
	posscores=[inputState.FixedCardVal]
	for i in xrange(inputState.NumAce):
		temp = copy.deepcopy(posscores)
		for i in xrange(len(temp)):
			temp[i]+=11
			posscores[i]+=1
		posscores += temp
	return posscores



dpstate={}

def addlist(lista,listb,prob):
	for i in xrange(0,len(lista)):
		lista[i]+=listb[i]*prob
	return lista


def EvaluateProb(p):
	statei=[]
	# p=float(4)/13
	def calcprob(a):
		#print a
		if a in dpstate:
			return dpstate[a]
		else:
			posval=PossibleScores(a)
			valarray=[0]*40
			if(max(posval)>=17):
				maxvalret=-1
				for b in posval:
					if(b<=21):
						maxvalret=max(maxvalret,b)
				if(maxvalret==-1):
					valarray[22]=1
					dpstate[a]=valarray
					#print valarray,22
					return valarray
				else:
					valarray[maxvalret]=1
					dpstate[a]=valarray
					#print valarray,maxvalret
					return valarray
			else:
				for i in xrange(2,12):
					if(i==11):
						statetemp=State(a.NumAce+1,a.FixedCardVal)
						calcprob(statetemp)
						valarray=addlist(valarray,dpstate[statetemp],float(1-p)/9)
					else:
						# print a,i
						statetemp=State(a.NumAce,a.FixedCardVal+i)
						calcprob(statetemp)
						if(i==10):
							#print "10000LOL1000",p
							valarray=addlist(valarray,dpstate[statetemp],float(p))
						else:
							valarray=addlist(valarray,dpstate[statetemp],float(1-p)/9)
			dpstate[a]=valarray
			#print a,valarray	
		return valarray
	statei.append([0]*40)
	statei.append([0]*40)
	for i in xrange(2,12):
		if(i==11):
			a=State(1,0)
			statei.append(calcprob(a))
		else:
		 	a=State(0,i)
			statei.append(calcprob(a))

	# print dpstate 	

	firstfacethenace=(1-p)/9
	firstacethenface=p
	return statei[2:]

	# for a in statei:
	# 	sum=0
	# 	for b in xrange(0,len(a)):
	# 		sum+=a[b]
	# 	print sum

