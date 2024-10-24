import monitool
from monitool import Info, Perf

class Plugin(monitool.Plugin):
    def configure_parser(self, parser):
        parser.add_argument('value', type=float, default=0.0, help='The value to check')
        parser.add_argument('--unit', '-u', default='', help='The unit of that value')

    def check(self, args):
        return Info(
                head='The value is {}{}'.format(args.value, args.unit),
                perf=Perf('value', args.value, args.unit, args.warn, args.crit),
        )

if __name__ == '__main__':
    Plugin().main()
