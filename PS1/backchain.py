from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES
import string
from inspect import currentframe, getframeinfo

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

def backchain_to_goal_tree(rules,\
                           hypothesis='',\
                           permathesis = '',\
                           chains='',\
                           haction = '',\
                           hsub='',\
                           hobj = '',\
                           toprint = 1,\
                           hwords = []):
    """ bogus!  I've been sending the whole chain through the recursion every time.  Maybe I should just be
    sending the antecedent through each time and collecting the leaves into the chain on the head of each next recursion"""

##    if backchain == '':
##        backchain = OR(hypothesis)
    if permathesis == '':
        permathesis = hypothesis

  
##    if chains != '':
##        chains = OR(chains)
##        if toprint >=1:  print "chains: ", chains,' at line ', getframeinfo(currentframe()).lineno

        
    andAnte = []

    if toprint >= 2: print "andAnte type is ",str(type(andAnte))        
    if toprint ==2: print "permathesis is:  ",permathesis
    if toprint >=1: print "hypothesis is:  ",hypothesis + ' at line ', getframeinfo(currentframe()).lineno

    hwords = hypothesis.split()
    
    for i in ACTIONS:
        if i in hypothesis:
            haction = i
            hsub = hypothesis.split()[0]
            replacer = hsub+i
            hobj = hypothesis.replace(replacer,'')
            
            if toprint ==2: print "subject is:  ",hsub
            if toprint ==2: print "predicate is:  ",haction
            if toprint ==2: print "object is:  ",hobj
            
            break
        
    if haction == '':
        hsub = hwords[0]
        haction = ' '+ hwords[-1] + ' '
        
        if toprint == 2:  print "hypothesis has no explicit object" + ' at line ', getframeinfo(currentframe()).lineno
        if toprint == 2: print "subject is:  ",hsub
        if toprint == 2: print "predicate is:  ",haction

    srule = "(?x)" + haction + "(?y)"
    
    if toprint ==2: print "srule is:  ",srule

    
    for i in rules:
        consequent = i.consequent()
        
        if toprint >=1: print consequent[0]
        if toprint ==2: print type(consequent[0])
        if toprint ==2: print string.split(hypothesis)[1:-1]
        
        if match(consequent[0],hypothesis) != None:
            if chains == '':
                chains = OR(permathesis)
                
                if toprint >=1: print "initializing goal tree:  ",chains,' at line ', getframeinfo(currentframe()).lineno
                
            mdict = match(srule,hypothesis)
            
        else:
            if toprint == 2:  print "The rule in question does not match the current hypothesis, recycling for loop to next rule"
            continue

        if toprint == 2: print "variable bindings: ",mdict, ' at line ', getframeinfo(currentframe()).lineno

        if mdict == None:
            continue
        elif mdict['y'] in consequent[0]:
            
            if toprint >=1: print consequent[0] + ' at line ', getframeinfo(currentframe()).lineno
            
            ante = i.antecedent()
            
            for j in ante:
                andAnte.append(populate(j,mdict))
                
            if toprint >=1: print "andAnte contains:  ",andAnte,' at line ', getframeinfo(currentframe()).lineno
            if toprint >=1: print "\n\nchains contains:  ",chains,' at line ', getframeinfo(currentframe()).lineno

            if hypothesis == permathesis:
                chains.append(AND(andAnte))
                
                if toprint >=2: print "\n\nhypothesis is:  ",hypothesis + ' at line ', getframeinfo(currentframe()).lineno
                if toprint >=2: print "\n\nchains contains:  ",chains,' at line ', getframeinfo(currentframe()).lineno

            else:
                chains.append(OR(hypothesis,AND(andAnte)))
                if toprint >=1: print "\n\nhypothesis is:  ",hypothesis + ' at line ', getframeinfo(currentframe()).lineno
                if toprint >=1: print "\n\nchains contains:  ",chains,' at line ', getframeinfo(currentframe()).lineno


                
            if toprint >=2: print "chains contains:  ",chains,' at line ', getframeinfo(currentframe()).lineno
            for k in ante:
                
                if toprint>=1: print "\n\nrecursing on: ",k + ' at line ', getframeinfo(currentframe()).lineno
                
                backchain_to_goal_tree(rules,populate(k,mdict),permathesis,chains)
        else:
            continue
                
    if toprint >=1: print "\n\nhypothesis is:  ",hypothesis + ' at line ', getframeinfo(currentframe()).lineno
    
    if chains=='':
        chains = [hypothesis]

    if toprint >=1: print "\n\nchains contains:  ",chains,' at line ', getframeinfo(currentframe()).lineno
    return simplify(chains)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'alice is an albatross')
