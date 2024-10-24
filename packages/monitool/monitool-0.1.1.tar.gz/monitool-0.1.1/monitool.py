'''
monitool -- A monitoring plugin framework for Nagios, Icinga, and so forth
'''

__version__ = '0.1.1'

from argparse import ArgumentParser
from enum import Enum
from functools import total_ordering, reduce
import operator
import sys
import traceback

# An opinionated ordering as to which status is "more important"
# As of now, CRITICAL > UNKNOWN > WARNING > OK
STATUS_ORDERING = {k: v for k, v in enumerate([0, 1, 3, 2])}

# Suffixes, by default, applied to headlines corresponding to certain statuses
STATUS_SUFFIX = {0: '', 1: '(!)', 2: '(!!)', 3: '(?)'}

@total_ordering
class Status(Enum):
    '''
    Corresponds to the Plugin statuses. Each is named for the "standard" name
    of the Plugin Return Codes; these are the standards used in the
    monitoring-plugins package.

    Statuses are comparable, a greater value is "more important". This does not
    use the return code, but an opinion based on monitool.STATUS_ORDERING; in
    particular CRITICAL is "more important" than UNKNOWN.
    '''
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __eq__(self, other):
        return isinstance(other, Status) and self.value == other.value

    def __lt__(self, other):
        return isinstance(other, Status) and \
                STATUS_ORDERING[self.value] < STATUS_ORDERING[other.value]

    def suffix(self):
        '''
        Get the "suffix" of this Status. See Info's constructor.

        This is simply an index into STATUS_SUFFIX, which can be used to assign
        different suffixes globally.
        '''
        return STATUS_SUFFIX[self.value]

class Range:
    '''
    A (Threshold) Range, as defined by the Nagios plugin standard. The range is
    always interpreted as inclusive, so lower <= x <= upper for some value x.
    If interior is False (the default), the sense is inverted (so x < lower or
    x > upper); this is the norm for most such specifications.
    '''
    def __init__(self, lower=None, upper=None, interior=False):
        if (lower is not None) and (upper is not None) and (lower > upper):
            raise ValueError(
                    'Invalid bounds (lower > upper): {} > {}'.format(lower, upper)
            )
        self.lower, self.upper, self.interior = \
                lower, upper, interior

    @classmethod
    def parse(cls, spec):
        '''
        Parse a Nagios range, using the plugin standard. The syntax is approximately

            [@][low:][high]

        where low is assumed to be 0, and high infinity, if omitted. If the
        range starts with @, it is an interior range. Low may also be `~` (the
        tilde character) to represent negative infinity.
        '''
        # Based on https://nagios-plugins.org/doc/guidelines.html#THRESHOLDFORMAT
        interior = False
        if spec.startswith('@'):
            interior = True
            spec = spec[1:]

        lower, _, upper = spec.rpartition(':')

        if not lower:
            lower = 0
        elif lower == '~':
            lower = None
        else:
            lower = float(lower)

        if not upper:
            upper = None
        else:
            upper = float(upper)

        return cls(lower, upper, interior)

    def __contains__(self, value):
        '''
        True if the value matches the range spec.
        '''
        contained = True
        if self.lower is not None and value < self.lower:
            contained = False
        if self.upper is not None and value > self.upper:
            contained = False
        if self.interior:
            return contained
        return not contained

    def __repr__(self):
        return 'Bounds({!r}, {!r}, {!r})'.format(self.lower, self.upper, self.interior)

    def __str__(self):
        '''
        Renders this range in a manner that can be understood by Range.parse.
        '''
        pfx = ''
        if self.interior:
            pfx = '@'

        lower = str(self.lower)
        if self.lower == 0:
            lower = ''
        if self.lower is None:
            lower = '~'

        upper = str(self.upper)
        if self.upper is None:
            upper = ''

        delim = ':'
        if not lower:
            delim = ''

        return '{}{}{}{}'.format(
                pfx, lower, delim, upper,
        )

# Convenient constants for Ranges:
Range.NOWHERE = Range()  # Never contains any value
Range.EVERYWHERE = Range(interior=True)  # Contains every value
Range.NONNEGATIVE = Range(0, interior=True)  # Contains every non-negative value
Range.UNIT = Range(0, 1, interior=True)  # Contains [0, 1]

class Perf:
    '''
    A single performance metric. Constructor arguments are largely as for the
    Performance Data part of the Nagios Plugin specification, with the note
    that bounds must always be an interior=True range (due to limitations).

    When used with Info, this class can automatically determine a Status if one
    is not already assigned.
    '''
    def __init__(self, label, value, unit='', warn=None, crit=None, bounds=None):
        if bounds is not None and (not bounds.interior):
            raise ValueError(
                    'Perfdata only understands interior lower/upper bounds, got {!r}'.format(bounds)
            )
        self.label, self.value, self.unit, self.warn, self.crit, self.bounds = \
                label, value, unit, warn, crit, bounds

    @property
    def status(self):
        '''
        The status implied by this performance metric.

        If this metric has a critical range and the value matches it, this is
        Status.CRITICAL. An analogous check is done for WARNING. Otherwise, the
        status is OK.
        '''
        if self.crit is not None and self.value in self.crit:
            return Status.CRITICAL
        if self.warn is not None and self.value in self.warn:
            return Status.WARNING
        return Status.OK

    def __repr__(self):
        return'Perf({!r}, {!r}, {!r}, warn={!r}, crit={!r}, bounds={!r})'.format(
                self.label, self.value, self.unit, self.warn, self.crit, self.bounds,
        )

    def __str__(self):
        '''
        Formats a Perf as a single item of Nagios performance data.
        '''
        return '{}={}{};{};{};{};{}'.format(
                self.label, self.value, self.unit,
                '' if self.warn is None else self.warn,
                '' if self.crit is None else self.crit,
                '' if self.bounds is None else self.bounds.lower,
                '' if self.bounds is None else self.bounds.upper,
        )

class Info:
    '''
    Represents (possibly combined) plugin output. A check returns such a value.

    It is recommended that all values are passed as keywords; this way, code is
    not sensitive to reordering. All values have sensible defaults.

    status gives the status of this check. If set, this overrides any default,
    including one surmised from perf. If unset and no perf is given, this
    defaults to OK.

    head represents a headline string. This should contain no internal
    newlines, and be as succinct as possible.

    extended is a sequence of lines that are ordered after the headline. This
    is the correct place for more details than can fit in the headline.

    perf is either a Perf object, or a sequence thereof, giving performance
    metrics. Aside from being collected, an unset status is implied to be the
    "most important" status from this set (see Perf.status).

    meta is a metadata dictionary. This isn't rendered in plugin output, but is
    preserved; its main intent is to pass information between checks, or to
    check middleware that might transform the results.

    suffix may be a string, or None. If a string, it is appended to head; if
    None, a suffix is derived from the status (as given or computed) is used.
    See Status.suffix for details. Once combined, this acts as if head
    contained this string all along for the purposes of combination; see
    combine.
    '''
    def __init__(self, status=None, head='', extended=(), perf=(), meta={}, suffix=None):
        if isinstance(perf, Perf):
            perf = (perf,)
        if status is None:
            status = max((p.status for p in perf), default=Status.OK)
        if suffix is None:
            suffix = status.suffix()
        self.status, self.head, self.extended, self.perf, self.meta = \
                status, head + suffix, extended, perf, meta

    @classmethod
    def combine(cls, *each):
        '''
        Produce a combined Info from one or more Info objects. Attributes are
        combined as follows:

        - status: Set to the "most important" (see Status).
        - head: Joined with commas.
        - extended: Joined in order.
        - perf: Joined in order.
        - meta: Combined, last wins.
        '''
        status = max(i.status for i in each)
        head = ', '.join(filter(None, (i.head for i in each)))
        extended = reduce(operator.add, (tuple(i.extended) for i in each), ())
        perf = reduce(operator.add, (tuple(i.perf) for i in each), ())
        meta = reduce(lambda a, b: {**a, **b}, (i.meta for i in each), {})
        return cls(
                status=status,
                head=head,
                extended=extended,
                perf=perf,
                meta=meta,
                suffix='',
        )

    def __or__(self, other):
        '''
        Combines two Info objects. See Info.combine for details.
        '''
        return self.combine(self, other)

    def __repr__(self):
        return 'Info(status={!r}, head={!r}, extended={!r}, perf={!r}, meta={!r})'.format(
                self.status, self.head, self.extended, self.perf, self.meta,
        )

    def __str__(self):
        '''
        Renders this Info as a valid Nagios plugin output.
        '''
        perf_sep = ' | ' if self.perf else ''
        return '{}: {}{}{}{}'.format(
            self.status.name,
            self.head,
            perf_sep,
            ' '.join(map(str, self.perf)),
            '\n' + '\n'.join(self.extended) if self.extended else '',
        )

class Plugin:
    '''
    A plugin. This class is meant to be derived in a script.

    Each plugin must have at least one check; each check may produce zero or
    more Info objects, which are combined and rendered as output.

    Some influential class variables:

    - description: Gives the ArgumentParser description for this plugin.

    - single_valued: If True (the default), defines -w/--warn and -c/--crit
      arguments, as is typically the case for a check written against a single
      value. If your check is more complex than this, set this to False, and
      prefer adding more appropriate arguments in configure_parser.
    '''
    description = 'A monitoring plugin'
    single_valued = True

    def main(self, use_exit=True):
        '''
        Main entry point. Intended to be called from `if __name__ == '__main__'`.

        If use_exit is True (the default), calls sys.exit with the returned
        Status code, and thus does not return.
        '''
        parser = self.get_parser()
        result = self.run(parser.parse_args())
        print(result)
        if use_exit:
            sys.exit(result.status.value)
        else:
            return result

    def run(self, args):
        '''
        Run all checks. Returns the combined Info object.
        '''
        checks = self.all_checks
        if not checks:
            return Info(
                    status=Status.UNKNOWN,
                    head='No checks to run!',
            )

        self.setup(args)
        info = []
        for check in checks:
            result = self.run_check(check, args)
            if result is None:
                continue
            try:
                i = iter(result)
                info.extend(i)
            except TypeError:
                info.append(result)

        self.cleanup(args)
        return Info.combine(*info)

    @property
    def all_checks(self):
        '''
        Enumerates all checks. You can set this to a class variable
        representing the names of methods to call. The default implementation
        looks for a `check` method and/or methods starting with `check_`.
        '''
        return [name for name in dir(self) if name.startswith('check_') or name == 'check']

    def run_check(self, name, args):
        '''
        Run a single check, returning an Info object.

        The check is assumed to be a method with the given name. args is passed
        directly, and should be an argparse.Namespace from an ArgumentParser.
        '''
        try:
            return getattr(self, name)(args)
        except Exception as e:
            tb_lines = list(filter(None, ''.join(traceback.format_exception(e)).split('\n')))
            return Info(
                    status=Status.UNKNOWN,
                    head='Failed to run {}: {!r}'.format(name, e),
                    extended=['{}: {}'.format(name, line) for line in tb_lines],
                    meta={'exception': e},
            )

    def get_parser(self):
        '''
        Produce an ArgumentParser for this Plugin.
        '''
        parser = ArgumentParser(description=self.description)

        if self.single_valued:
            parser.add_argument('-w', '--warn', type=Range.parse,
                                help='Warning if value matches this range specification')
            parser.add_argument('-c', '--crit', type=Range.parse,
                                help='Critical if value matches this range specification')

        self.configure_parser(parser)
        return parser

    def configure_parser(self, parser):
        '''
        Extend the ArgumentParser given as parser. This is intended to allow
        plugin authors to add further arguments; the default implementation
        does nothing.
        '''
        pass

    def setup(self, args):
        '''
        Called from run(), before checks are run. This is intended to allow
        plugin authors to initialize state shared between checks; the default
        implementation does nothing.
        '''
        pass

    def cleanup(self, args):
        '''
        Called from run(), after all checks are run. This is intended to allow
        plugin authors to clean any setup() state; the default implementation
        does nothing.
        '''
        pass
