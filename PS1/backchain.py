from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES
import string

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis,rbridge = ''):
    #print hypothesis
    for s in string.split(hypothesis)[1:-1]:
        rbridge += ' ' + s
    #print rbridge
    srule = "(?x)" + rbridge + " (?y)"

    
    for i in rules:
        consequent = i.consequent()
        
        #print consequent[0]
        #print type(consequent[0])
        #print string.split(hypothesis)[1:-1]
        
        mdict = match(srule,hypothesis)
        #print mdict
        
        if type(mdict['y']) == None or type(mdict['x']) == None:
            #print "empty mdict"
            return
        
        if mdict['y'] in consequent[0]:
            #print consequent[0]
            ante = i.antecedent()
##            for j in ante:
##            #print populate(j,mdict)
            for k in ante:
                backchain_to_goal_tree(rules,populate(k,mdict))
# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
