import monitool
from monitool import Info, Perf
from functools import reduce

class Plugin(monitool.Plugin):
    def check(self, args):
        infos = [Info(
            head='This is headline {}'.format(i),
            extended = ['This is extended info {}'.format(i)],
            perf=Perf('metric_{}'.format(i), i),
        ) for i in range(3)]
        # This would better be operator.bor, but this is to demonstrate the syntax
        info = reduce(lambda a, b: a | b, infos)
        return info

if __name__ == '__main__':
    Plugin().main()
