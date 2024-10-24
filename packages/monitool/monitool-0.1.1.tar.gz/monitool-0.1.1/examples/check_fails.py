import monitool

class Plugin(monitool.Plugin):
    def check(self, args):
        raise SystemError('oops')

if __name__ == '__main__':
    Plugin().main()
