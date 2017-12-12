class Predicate(object):
    
    
    def __init__(self, attribute_name, operation, value):
        self.attribute = attribute_name
        self.operation = operation
        self.value = value
        self.negation_dict = {
            '=': '!=',
            '!=': '=',
            '>=': '<',
            '<': '>=',
            '<=': '>',
            '>': '<=',
        }
    
        
    def __repr__(self):
        return "{} {} {}".format(self.attribute, self.operation, self.value or 'any')
    
    def negate(self):
        return Predicate(self.attribute, self.negation_dict[self.operation], self.value)
    
    def __eq__(self, other):
        return self.operation == other.operation and self.attribute == other.attribute and self.value == other.value
    
    def __hash__(self):
        return hash(repr(self))
        
class ApplicationRequirement(object):
    '''
    Lists out application requirement with predicates
    '''
    
    def __init__(self, relation, predicate):
        self.relation = relation
        self.predicate = predicate
        
    def __repr__(self):
        return 'Database {}, Relation {} :- {}'.format(self.database, self.relation, self.predicate)
    
    
    

class Application(object):
    
    
    def __init__(self, requirements):
        self.requirements = requirements
        
    def get_predicates(self):
        return list(map(lambda x: x.predicate , self.requirements))
    

def group_predicates_by_attribute(predicates):
        grouped = {}
        for predicate in predicates:
            if grouped.get(predicate.attribute, None): grouped[predicate.attribute].append(predicate)
            else: grouped[predicate.attribute] = [predicate]
            
        return grouped
    
def minimal(pr_prime):
    pr_prime = list(pr_prime) ## since changing set in for loop raises RuntimeError
    for predicate in pr_prime:
        if type(predicate.value) == int and predicate.negate() in pr_prime: pr_prime.remove(predicate)
    return set(pr_prime)

def minimal_final(pr_prime):
    pr_prime = list(pr_prime)
    grouped = group_predicates_by_attribute(pr_prime)
    for group in grouped:
        for predicate in grouped[group]:
            if type(predicate.value) == str and len(grouped[group]) > 1: pr_prime.remove(predicate); break
                
    return set(pr_prime)
