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

def ruleParse(hypothesis,haction = '',hsub='',hobj='',toprint = 1):
    
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

def backchain_to_goal_tree(rules, hypothesis,chainlist = [],toprint=1):

    srule = ruleParse(hypothesis)
    if toprint >= 1: print "\n\n srule is:  ",srule,' at line ',getframeinfo(currentframe()).lineno
    
    if chainlist == []:
        chainlist = [hypothesis]
        if toprint >= 1: print "\n\n Chainlist init is:  ",chainlist,' at line ',getframeinfo(currentframe()).lineno

    # Get variable bindings from hypothesis

    bindings = match(srule,hypothesis)
    if toprint >= 1:
        print "\n\n bindings are:  ",bindings,' at line ',getframeinfo(currentframe()).lineno
        print "\n"
    
    

    for i in rules:
        cons = i.consequent()
        if toprint >= 1: print "Consequent is:  ",cons

        # Compare consequent of rule with hypothesis...

        if hypothesis == populate(cons[0],bindings):
            if toprint >= 1:
                print "\n\nGot a match:  ",cons[0]
                print "\n"
            #  Ok, how to handle recursive antecedent hypotheses...1)  Changes to the chain list
            #  should not be made unless there is a match between the antecedent hypothesis and
            #  a rule.  This if: block would be where to make the change.  Not real sure how to do that yet though.
            #  I guess I need to take the a.h. and encapsulate it in another sublist and replace it's original.

            ante = i.antecedent()
            alist = []
            
            if hypothesis not in chainlist:
                """ Need to account for the difference between the initial run and a recursive run"""
                for j in range(len(ante)):
                    alist.append(populate(ante[j],bindings))
                chainlist.append(alist)
            else:
                """ this would then be the recursive case """
                for i in range(len(chainlist)):
                    print i
                    print chainlist[i]
                    try:
                            sdex = chainlist[i].index('opus flies')
                            hindex = (i,sdex)
                            print "\n Hypothesis index is:  ",hindex,' at line ',getframeinfo(currentframe()).lineno
                    except ValueError:
                            print "target not found in ",chainlist[i]
                            continue
        else:
            #  If the current rule does not match, recycle to next rule.
            if toprint >= 1: print "\n No match found, move to next rule",getframeinfo(currentframe()).lineno
            continue

        #  Once a matching rule is found, its antecedents must be retrieved and added to the chain list as
        #  a sublist.


        

        

    return chainlist
    
    
# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
