import AccessControl
from Products.RhaptosRepository.Extensions.ObjectResult import ObjectResult

class SimData:

    # Convert DB arrays into python tuples
    def similarities(self):
        sims = [ x.split(',') for x in self.sims.strip('{}').split('},{')]
        return map(lambda l: (l[0], l[1], int(l[2])), sims)

    def simobjs(self,repository):
        sims = [ x.split(',') for x in self.sims.strip('{}').split('},{')]
	
        return map(ObjectResult, *zip(*[s+[repository] for s in sims]))

