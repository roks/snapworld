import random
import sys

import swlib

#distmean = 150
#distvar  = 22.5
distmean = 8
#distmean = 3
distvar  = 1

def StdDist(mean,dev):
    x = 0.0
    for i in range(0,12):
        x += random.random()

    x -= 6.0
    x *= dev
    x += mean

    return int(x + 0.5)

def GenStubs(sw):
    """
    determine degrees for all the nodes, generate the stubs and distribute them
    """

    taskname = sw.GetName()

    msglist = sw.GetMsgList()
    sw.log.debug("msglist " + str(msglist))

    for item in msglist:
        dmsg = sw.GetMsg(item)
        d = dmsg["body"]
        sw.log.debug("task %s, args %s" % (taskname, str(d)))

        ns = d["s"]
        ne = ns + d["r"]

        sw.log.debug("task %s, start %d, end %d" % (taskname, ns, ne))

        # determine node degrees
        i = ns
        ddeg = {}
        while i <= ne:
            deg = StdDist(distmean,distvar)
            #deg = 3
            ddeg[i] = deg
            sw.log.debug("task %s, node %s, degree %s" % (taskname, str(i), str(deg)))
            i += 1

    sw.log.debug("ddeg " + str(ddeg))

    # distribute the stubs randomly to the tasks
    ntasks = int(sw.GetVar("gen_tasks"))
    sw.log.debug("__tasks__ %s\t%s" % (taskname, str(ntasks)))

    # each task has a list of stubs
    dstubs = {}
    for key,value in ddeg.iteritems():
        for i in range(0,value):
            t = int(random.random() * ntasks)
            if not dstubs.has_key(t):
                dstubs[t] = []
            dstubs[t].append(key)

    sw.log.debug("dstubs " + str(dstubs))

    dmsgout = {}
    dmsgout["src"] = taskname
    dmsgout["cmd"] = "stubs"

    for tdst, msgout in dstubs.iteritems():
        sw.log.debug("sending task %d, msg %s" % (tdst, str(msgout)))
        dmsgout["body"] = msgout
        sw.Send(tdst, dmsgout)

def Worker(sw):
    GenStubs(sw)

if __name__ == '__main__':
    
    sw = swlib.SnapWorld()
    sw.Args(sys.argv)

    fname = "swwork-%s.log" % (sw.GetName())

    sw.SetLog(fname)
    sw.GetConfig()

    Worker(sw)

    sw.log.info("finished")

