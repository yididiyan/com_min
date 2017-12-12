import repository
from helpers import Predicate, ApplicationRequirement, Application
from helpers import minimal, minimal_final, group_predicates_by_attribute

def com_min_algo(relation, pr, application):
    f = [] # set of minterm fragments
    pr_prime = set() # set of simple, complete and minimal fragments
    
    pr = set(pr)
       
    
    ## Find pi in pr which is in the application
    app_reqts = set(application.get_predicates())
    
    pr = app_reqts if len(app_reqts) > len(pr) else pr
    
    assert len(app_reqts) > 0 ## Assertion Fails check your application requirements
    assert pr
    assert app_reqts.intersection(pr)
    

    ## pi should be one of the req in app_reqs + the list of predicates: pr
    ## TODO: SELECT Pr FROM INTERSECTION OF PREDICATE + APP_REQS
    intersection = list(app_reqts.intersection(pr))
    pi = intersection[0] if len(intersection) else None
    
    assert pi ## Atleast one element in the intersection of APP_REQS and Pr
    
    ## remove pi from pr
    intersection.remove(pi)
    
    ## Add pi to pr_prime
    pr_prime.add(pi)
    
    
    
    
    ## Get the minterm fragment according to pi
    ## Database connection here 
    repo = repository.Repository()
    f.extend(repo.fragment(relation, pi))
    
    
    
    while True:
        ## find a pj elt of Pr such that p j partitions some fk of Pr0 according to Rule 1;
        
        ## if intersection is empty it is complete
        pj = intersection[0] if len(intersection) else None
        
        if not pj: break
        
        intersection.remove(pj)
        pr_prime.add(pj)
        
        ## Check minimality 
        pr_prime = minimal(pr_prime)
        
        
    pr_prime = minimal_final(pr_prime)
    
    
    return pr_prime


    


if __name__ == '__main__':
    repo = repository.Repository()
    meta = repo.get_meta_data()
    repo.create_schema()
    repo.populate_data()

    ## Example 

    requirements = [ApplicationRequirement('project', Predicate('location', '=' , 'Addis Ababa')),
                    ApplicationRequirement('project', Predicate('location', '=', 'Awassa')),               
                    ApplicationRequirement('project', Predicate('location', '=', 'Bahir Dar')),                
                    ApplicationRequirement('project', Predicate('location', '=', 'Mekelle')),                
                    ApplicationRequirement('project', Predicate('budget', '>=', 200000)),
                    ApplicationRequirement('project', Predicate('budget', '<', 200000))
                ]                
    
    application = Application(requirements)
    print('==============================================================')
    print('============= Application Requirement ========================')
    print('\n'.join(map(lambda x: str(x) ,application.get_predicates()) ) )

    print('==============================================================')

    pr_prime = com_min_algo('project', [Predicate('location', '=' , 'Awassa'), Predicate('a', '=', 'Bahir Dar')], application)

    print('==============================================================')
    print('============= Complete And Minimal Predicates ================')
    print('\n'.join(map(lambda x: str(x) ,pr_prime) ) )

    print('==============================================================')