import sys
import os
import time
import syslog

NUM_ATTEMPTS = 3
PAUSE_TIME = 3

def storeSimilarity(id, version):
    global app

    syslog.openlog("ExtSimilarity[%d]" % os.getpid())
    syslog.syslog("Storing similarity for %s, %s" % (id, version))
    for n in range(NUM_ATTEMPTS):
        # FIXME: This is crap.  Someday we will have a single API call that won't depend on the id string
        if id.startswith('m'):
            try:
                data = app.plone.portal_moduledb.sqlGetModule(id=id, version=version)[0]
            except IndexError:
                syslog.syslog("Couldn't find %s, %s (attempt %d)" % (id, version, n+1))
                time.sleep(PAUSE_TIME)
                continue
            o = app.plone.content.getRhaptosObject(id, version, data=data)
            break
        else:
            try:
                o = app.plone.content.getRhaptosObject(id, version)
                break
            except KeyError:
                syslog.syslog("Couldn't find %s, %s (attempt %d)" % (id, version, n+1))
                time.sleep(PAUSE_TIME)
                continue
    else:
        syslog.syslog(syslog.LOG_ERR, "Failed after %d attempts to get %s, %s" % (NUM_ATTEMPTS, id, version))
        sys.exit(-1)
        
    try:
        app.plone.portal_similarity._storeSimilarity(o)
    except Exception, e:
        syslog.syslog(syslog.LOG_ERR, "Similarity storage failure for %s, %s" % (id, version))
        raise
        
    get_transaction().commit()
    syslog.closelog()


if __name__ == '__main__':
    try:
        id = sys.argv[1]
        version = sys.argv[2]
    except KeyError:
        sys.exit(-1)

    storeSimilarity(id, version)
