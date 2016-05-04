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
def createStatement(statements,rule):
    """ This is where the magic happens.  This function encapsulates the results from
    each rule recursion with the typing required by the backchaining algorithm."""
    if isinstance(rule,AND):
        return AND(statements)
    if isinstance(rule,OR):
        return OR(statements)

def backchain_to_goal_tree(rules, hypothesis, toprint = 0):
    #  Found git entry from junoon53.  Outlined flow.  Recreating from flow.

    goal_tree = [hypothesis]

    for rule in rules:
        consequent = rule.consequent()
        for expr in consequent:
            bindings = match(expr,hypothesis)

            # if bindings is not equal to None, which is return by match when no match is made,
            # or if the expression retrieved from the consequent of the rule is equal to the
            # hypothesis, retrieve the antecedents of the rule for tests and recursion.  Otherwise,
            # fetch the next expression.
            
            if bindings or expr == hypothesis:
                antecedent = rule.antecedent()

                # Is the antecedent a string?  If so we can recurse on it as a new hypothesis.
                #  If not it must be a list of expressions that we will have to parse.
                if isinstance(antecedent,str):
                    new_hypo = populate(antecedent,bindings)
                    goal_tree.append(backchain_to_goal_tree(rules,new_hypo))
                    # Once recursion completes and the results of that recursion are
                    # appended to the goal tree, we can append the new_hypo to the goal tree.
                    goal_tree.append(new_hypo)
                else:
                    # Assuming antecedent is a list of expressions, retrieve them and assemble a list
                    # of statements to be acted on
                    #  junoon53 used a list comprehension here but I'm going to write out the whole for
                    # loop just to make sure I know what is going on.
                    statements = []
                    new_goal_tree=[]
                    for anteEx in antecedent:
                        statements.append(populate(anteEx,bindings))
                    for statement in statements:
                        new_goal_tree.append(backchain_to_goal_tree(rules,statement))
                    goal_tree.append(createStatement(new_goal_tree,antecedent))
                        

                    

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
