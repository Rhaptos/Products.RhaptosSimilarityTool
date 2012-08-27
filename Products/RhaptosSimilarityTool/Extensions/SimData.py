import AccessControl
from Products.RhaptosRepository.Extensions.ObjectResult import ObjectResult

class SimData:

    # Convert DB arrays into python tuples
    def similarities(self):
        return map(lambda l: (l[0], l[1], int(l[2])), self.sims)

    def simobjs(self,repository):
        return map(ObjectResult, *zip(*[s+[repository] for s in self.sims]))

