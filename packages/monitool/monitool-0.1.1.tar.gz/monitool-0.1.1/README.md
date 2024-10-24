# monitool

A little library for writing monitoring plugins for Nagios, Icinga, and
probably others that are ABI-compatible.

## Usage

```python
import monitool
from monitool import Info, Perf, Status

# First: define a Plugin class.
class Plugin(monitools.Plugin):
    # Then: set up some defaults
    description = 'My awesome monitoring plugin'

    # single_valued = False
    # If the above is uncommented, doesn't add args.warn (-w) and args.crit
    # (-c) automatically

    def configure_parser(self, parser):
        parser.add_argument('arg', type=float, help='The value to check')
        parser.add_argument('unit', default='', help='The unit this value has')

    # Finally: define some checks
    # The Plugin automatically finds `check`, and any method starting with
    # `check_`, but you can override `all_checks` to change this
    def check(self, args):
        return Info(
            # status=Status.OK,  # Without this, inferred from the Perf data
            head='The arg is {}{}'.format(args.arg, args.unit),
            perf=Perf('arg', args.arg, args.unit, args.warn, args.crit),
        )

if __name__ == '__main__':
    Plugin().main()  # don't forget to run it!
```

The API is experimental and subject to change. Feedback is welcome!

Further examples are in the `examples/` directory; the one above is by no means
a complete demonstration.

## Specification

This package attempts to conform with [the Nagios plugin guidelines][npdg].
Generally speaking, usage of this library (without malice) that results in an
out-of-spec output is a bug. Feel free to report it as such!

[npdg]: https://nagios-plugins.org/doc/guidelines.html

## License

GPLv3 or later at your option. See LICENSE for details.
