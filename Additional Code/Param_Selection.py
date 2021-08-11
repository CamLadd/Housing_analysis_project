import statsmodels.api as sm
from itertools import combinations
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate, KFold
from sklearn import metrics
import random

def forward_steps(data,Y,X):
    dependent=data[Y]
    Models=[[]]
    features=X.copy()
    lr=LinearRegression()
    def r_score_margin(original,new_f):
        Y_X=(dependent,data[original+[new_f]])
        lr.fit(*Y_X)
        return lr.score(*Y_X)
    while len(features)>0:
        M=Models[-1]
        new_f=max(features,key=lambda f: r_score_margin(M,f))
        features.remove(new_f)
        Models.append([new_f]+M)
    Models.remove([])
    return Models

def backward_steps(data,Y,X):
    dependent=data[Y]
    steps=len(X)
    Models=[X.copy()]
    lr=LinearRegression()
    def r_score_exmargin(original,new_f):
        ins=original.copy()
        ins.remove(new_f)
        Y_X=(dependent,data[ins])
        lr.fit(*Y_X)
        return lr.score(*Y_X)
    while steps>1:
        M=Models[-1].copy()
        worse_f=max(M,key=lambda f: r_score_exmargin(M,f))
        M.remove(worse_f)
        Models.append(M)
        steps-=1
    return Models

def subset_steps(data,Y,X):
    dimensions=X
    M=[]
    lr=LinearRegression()
    dependent=data[Y]
    def r_score_margin(inputs):
        Y_X=(dependent,data[inputs])
        lr.fit(*Y_X)
        return lr.score(*Y_X)
    for d in range(1,len(dimensions)+1):
        combos=[list(c) for c in combinations(dimensions,d)]
        top_model=max(combos,key=r_score_margin)
        M.append(top_model)
    return M


def CV_compare(data,Y,models,folds=5):
    scores={}
    lr=LinearRegression()
    state=random.randint(1,1000)
    SPLIT=KFold(folds,random_state=state,shuffle=True)
    for m in models:
        k='+'.join(m)
        scores[k]=cross_validate(lr,data[Y],data[m])['test_score']
    return scores
        
        