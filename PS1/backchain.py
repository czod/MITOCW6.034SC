from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES
import string
from inspect import currentframe, getframeinfo
import sys, copy

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

def funcDebug(mesg,clno):
    """ mesg is a dictionary of the form:
        {"mesg":var}
        clno =  current line number        """
    # debug template  if toprint >= :clno = getframeinfo(currentframe()).lineno;funcDebug({"":,"":},clno)
    for i in mesg.iterkeys():
        print i,mesg[i],' at line ',clno

def ruleParse(hypothesis,haction = '',hsub='',hobj='',toprint = 0):
    
    hwords = hypothesis.split()    
    for i in ACTIONS:
        if i in hypothesis:
            haction = i
            hsub = hypothesis.split()[0]
            replacer = hsub+i
            hobj = hypothesis.replace(replacer,'')

            #Debug
            if toprint ==1:clno = getframeinfo(currentframe()).lineno;funcDebug({"subject is: ":hsub,"predicate is:  ":haction,"object is:  ":hobj},clno)
            
            break
        
    if haction == '':
        hsub = hwords[0]
        haction = ' '+ hwords[-1] + ' '
        
        #Debug
        if toprint ==1:
            clno = getframeinfo(currentframe()).lineno + 1
            funcDebug({"subject is: ":hsub,"predicate is:  ":haction,"object is:  ":hobj},clno)


    srule = "(?x)" + haction + "(?y)"

    if toprint ==2: print "srule is:  ",srule

    return srule
    

def backchain_to_goal_tree(rules,hypothesis,chains='',rchains='', toprint=0):
        
       
    srule = ruleParse(hypothesis)
    if toprint >=1: print "srule is: ",srule,' at lineno ',getframeinfo(currentframe()).lineno

    bindings = match(srule,hypothesis)

    
    for i in rules:
        """ Iterate through each rule, extract the consequent (the OR node) and match it to the hypothesis.  If they match
            retrieve the antecedent (the AND()) and recurse on each element of the antecedent. """

        #  The OR() Node
        consequent = i.consequent()

        #Debug
        if toprint >=1: print consequent[0]
        if toprint >=2:clno = getframeinfo(currentframe()).lineno;funcDebug({"consequent type: ":type(consequent[0]),"hypothesis split is":string.split(hypothesis)[1:-1]},clno)

        # Make sure the match isn't a NoneType object since that makes the program barf.
        if match(consequent[0],hypothesis) != None:
            
            # Compare the predicate ('y') of the rule consequent to the predicate of the hypothesis.
            # If they match, grab the antecedents (AND() nodes) of the rule, append and recurse on each individually.
            if bindings['y'] in consequent[0]:
                
                #Debug
                if toprint >=1: clno = getframeinfo(currentframe()).lineno;funcDebug({"\n Found a match for ":hypothesis,"\n The consequent is ":consequent[0]},clno)

                if chains == '':
                    # If this is our first rodeo, initialize chains with an OR() node containing the hypothesis.
                    chains = OR(hypothesis)
                    rchains = AND()

                    #Debug
                    if toprint >=1: print "initializing goal tree:  ",chains,' at line ', getframeinfo(currentframe()).lineno
                else:
                    #Debug
                    if toprint >=1: print "\n\n Appending hypothesis to chains: ",hypothesis,' at line ', getframeinfo(currentframe()).lineno

                    # If chains is not a null string it means that we're hear on a recursion.  Create an OR() node
                    # and append it to the current chain
                    if AND(hypothesis) in rchains:rchains.remove(AND(hypothesis))                        
                    if OR(hypothesis) not in rchains:rchains.append(OR(hypothesis))

                    


                if toprint >=1: print "\n\n rchains contains:  ",rchains,' at line ', getframeinfo(currentframe()).lineno

                ante = i.antecedent()


                #Iterating over each antecedent
                for j in ante:
                    #Debug
                    if toprint >=1: print "\n\nFound Antecedent:  ",j,' at line ', getframeinfo(currentframe()).lineno


                    # Since I'm no longer trying to capture the return from the recurse, I can append the AND() nodes for
                    # the antecedents here prior to recursing them.  Also, I no longer need to create a copy of chains to hand off
                    # to the recurse since ignoring the function return from backchain avoids the infinite recursion.
                    rchains.append(AND(populate(j,bindings)))

                    # For each iterated antecedent, call backchain with antecedent as hypothesis argument to the
                    # next recursion.  Then append the output to chains.  The first recursion will not append to chains until
                    # every recursion below it in the goal tree has recursed and appended.  This sounds like order will
                    # get all whacked since the nodes are supposed to be in chains in order of occurrence as the
                    # recursion decends but I'm hoping simplify() on the function return will suss this out.
                    # Actually, now that I think about it, this could well be the source of my problem.  For example, if
                    # I recurse on the antecedent "(?x) is a bird", there are two rules with matching consequents.  backchain will
                    # hit the first rule in order of appearance and then recurse.  backchain will then match the second occurrence of
                    # the antecedent and recurse.  Since there are no more rules to match, it will fail and return, appending the second
                    # occurrence onto chains, followed by the first occurrence thus chaining them out of order.  I think the way to fix this
                    # might be to iterate the rules backward but continue to iterate the antecedents forward.
                    #
                    # Technically this violates the protocol for backward chaining since you're supposed to follow the left
                    # branch of the goal tree all the way down in DFS but in this case, I'm not tasked with eliminating anything
                    # so it's not an issue.  Just need to bear this in mind in the future.
                    
                    backchain_to_goal_tree(rules,populate(j,bindings),chains,rchains)



                    # Ok, new plan.  I don't actually *have* to catch the return from the function in order to build the
                    # chain.  It is simple enough to make all the appends in the body of the rule and antecedent iterations.

                    #Debug
                    if toprint >=3: print "\n\nachain contains:  ",achain,' at line ', getframeinfo(currentframe()).lineno

                    #chains.append(AND(achain))                


                if toprint >=3: print "\n\nachain contains:  ",achain,' at line ', getframeinfo(currentframe()).lineno                
                

    # Since recursed antecedents that don't match rules will not have OR() nodes created for them, it
    # should be safe to create their AND() nodes here just before they exit their recursion.
    goal_tree = AND()
    gchains = copy.copy(chains)
    gchains.append(rchains)
    goal_tree.append(gchains)
    if chains == '':
        goal_tree = [hypothesis]

    return goal_tree


# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'alice is an albatross')
