import pybpsapi
from pprint import pprint

api = pybpsapi.API()

print("Latest circular from `general`:")
pprint(api.latest('general'))
print()

print("List of circulars from primary:")
pprint(api.list('primary'))
print()

print("Searching for Grade 12 PB1 syllabus:")
pprint(api.search("XXI pre board 1 syllabus"))
print()

print("Check for new circulars from category general:")
circular_checker = pybpsapi.CircularChecker(category='general')
pprint(circular_checker.check())
