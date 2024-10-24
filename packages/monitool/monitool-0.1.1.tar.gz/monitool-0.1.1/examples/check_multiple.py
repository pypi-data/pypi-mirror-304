import monitool
from monitool import Info, Perf, Status

class Plugin(monitool.Plugin):
    def check_a(self, args):
        return Info(head='Check a passed')

    def check_b(self, args):
        return Info(status=Status.WARNING, head='Check b has some trouble')

    def check_c(self, args):
        return Info(head='Check c passed as well')

    def check_d(self, args):
        return Info(head='And finally check d passes too')

if __name__ == '__main__':
    Plugin().main()
