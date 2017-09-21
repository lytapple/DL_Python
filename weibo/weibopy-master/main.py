import sys

from action.Grabber import Grabber


# Test for Grabber
if __name__ == '__main__':

    Grabber.start()

    Grabber.connect(sys.argv[1])
    print 'Getting Information from account {0}'.format(sys.argv[1])
    for j in range(3):
        Grabber.getStatuses(1 + j)

    Grabber.close()
