from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES
import string
from inspect import currentframe, getframeinfo
import sys

sys.setrecursionlimit(20000)
frameinfo = getframeinfo(currentframe())


# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

ACTIONS = [" has ",\
           " is an ",\
           " is a ",\
           " is ",\
           " gives ",\
           " chews ",\
           " could not ask for ",\
           " could not ask ",\
           " could not ",\
           " could ",\
           " does not ",\
           " does ",\
           " lays "\
           ]

def ruleParse(hypothesis,haction = '',hsub='',hobj='',toprint = 0):
    
    hwords = hypothesis.split()    
    for i in ACTIONS:
        if i in hypothesis:
            haction = i
            hsub = hypothesis.split()[0]
            replacer = hsub+i
            hobj = hypothesis.replace(replacer,'')
            
            if toprint ==1: print "subject is:  ",hsub
            if toprint ==1: print "predicate is:  ",haction
            if toprint ==1: print "object is:  ",hobj
            
            break
        
    if haction == '':
        hsub = hwords[0]
        haction = ' '+ hwords[-1] + ' '
        
        if toprint == 2:  print "hypothesis has no explicit object" + ' at line ', getframeinfo(currentframe()).lineno
        if toprint == 2: print "subject is:  ",hsub
        if toprint == 2: print "predicate is:  ",haction

    srule = "(?x)" + haction + "(?y)"
    
    if toprint ==2: print "srule is:  ",srule

    return srule
    

def backchain_to_goal_tree(rules,hypothesis,chains='',toprint=1):
    """ bogus!  I've been sending the whole chain through the recursion every time.  Maybe I should just be
    sending the antecedent through each time and collecting the leaves into the chain on the head of each next recursion"""

##    if backchain == '':
##        backchain = OR(hypothesis)
##    if permathesis == '':
##        permathesis = hypothesis

  
##    if chains != '':
##        chains=OR(chains)
##        if toprint >=1:  print "chains: ", chains,' at line ', getframeinfo(currentframe()).lineno

        
    achain = []

    srule = ruleParse(hypothesis)
    if toprint >=1: print "srule is: ",srule,' at lineno ',getframeinfo(currentframe()).lineno
    
    for i in rules:
        consequent = i.consequent()
        
        if toprint >=1: print consequent[0]
        if toprint ==2: print type(consequent[0])
        if toprint ==2: print string.split(hypothesis)[1:-1]
        
        if match(consequent[0],hypothesis) != None:
            if chains == '':
                chains = OR(hypothesis)
                
                if toprint >=1: print "initializing goal tree:  ",chains,' at line ', getframeinfo(currentframe()).lineno
            else:
                if toprint >=1: print "\n\n Appending hypothesis to chains: ",hypothesis,' at line ', getframeinfo(currentframe()).lineno
                chains.append(OR(hypothesis))
                if toprint >=1: print "\n\naChains contains:  ",chains,' at line ', getframeinfo(currentframe()).lineno
                
            bindings = match(srule,hypothesis)
            
        else:
            if toprint == 2:  print "The rule in question does not match the current hypothesis, recycling for loop to next rule"
            continue

        if toprint == 2: print "variable bindings: ",bindings, ' at line ', getframeinfo(currentframe()).lineno

        if bindings == None:
            continue
        
        if bindings['y'] in consequent[0]:
            
            if toprint >=1: print consequent[0] + ' at line ', getframeinfo(currentframe()).lineno
            
            ante = i.antecedent()
            
            for j in ante:
                if toprint >=1: print "\n\nFound Antecedent:  ",j,' at line ', getframeinfo(currentframe()).lineno
                achain.append(populate(j,bindings))
                
            chains.append(AND(achain))

            for k in achain:
                if toprint >=1: print "\n\nRecursingh on:  ",k,' at line ', getframeinfo(currentframe()).lineno
                backchain_to_goal_tree(rules,k,AND(chains))
                if toprint >=1: print "\n\nachain contains:  ",achain,' at line ', getframeinfo(currentframe()).lineno

            if toprint >=1: print "\n\nachains contains:  ",achain,' at line ', getframeinfo(currentframe()).lineno

              

                
    if toprint >=1: print "\n\nhypothesis is:  ",hypothesis + ' at line ', getframeinfo(currentframe()).lineno
    
    if chains=='':
        chains = [hypothesis]

    if toprint >=1: print "\n\nchains contains:  ",chains,' at line ', getframeinfo(currentframe()).lineno
    return chains

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'alice is an albatross')
