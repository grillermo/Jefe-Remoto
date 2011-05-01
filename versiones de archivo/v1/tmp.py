from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--firstIP", dest="firstIP",
                  help="the starting IP for the desired range")
parser.add_option("-l", "--lastIP", dest="lastIP",
                  help="the last IP for the desired range")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

args = ["-f", "192.168.1.102"]
(options, args) = parser.parse_args()
