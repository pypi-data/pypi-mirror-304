import monitool
from monitool import Info, Perf

class Plugin(monitool.Plugin):
    def check(self, args):
        return Info(
                head='This is the headline',
                extended = [
                    'This is a bunch',
                    'of extended information',
                    'usually rendered as separate lines',
                ],
        )

if __name__ == '__main__':
    Plugin().main()
