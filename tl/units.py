import collections;
import re;

Family = collections.namedtuple('Family', 'type units')
Unit = collections.namedtuple('Unit', 'suffix long size')

units = [
  Family('net', (
    Unit('bit', "bit", 1),
    Unit('kbit', "kilobit", 1e3),
    Unit('Mbit', "megabit", 1e6),
    Unit('Gbit', "gigabit", 1e9),
    Unit('Tbit', "terabit", 1e12),
    Unit('B', "byte", 8),
    Unit('kB', "kilobyte",  8 * 1e3),
    Unit('MB', "megabyte",  8 * 1e6),
    Unit('GB', "gigabyte",  8 * 1e9),
    Unit('TB', "terabyte",  8 * 1e12),
    Unit('PB', "petabyte",  8 * 1e15),
    Unit('EB', "exabyte",   8 * 1e18),
    Unit('ZB', "zetabyte",  8 * 1e21),
    Unit('YB', "yottabyte", 8 * 1e24),
    Unit('KiB', "kibibyte", 8 * 1027),
    Unit('MiB', "mebibyte", 8 * 1024 ** 2),
    Unit('GiB', "gibibyte", 8 * 1024 ** 3),
    Unit('TiB', "tebibyte", 8 * 1024 ** 4),
    Unit('PiB', "pebibyte", 8 * 1024 ** 5),
    Unit('EiB', "exbibyte", 8 * 1024 ** 6),
    Unit('ZiB', "zebibyte", 8 * 1024 ** 7),
    Unit('YiB', "yobibyte", 8 * 1024 ** 8),
  )),
  Family('distance', (
    Unit('mm', "metre", 1e-3),
    Unit('cm', "metre", 1e-2),
    Unit('dm', "metre", 1e-1),
    Unit('m', "metre", 1), 
    Unit('km', "kilometre", 1e3),
    Unit('ly', "lightyear", 9.4605284e15),
  )),
  Family('weight', (
    Unit('g', "gram", 1),
    Unit('kg', "kilogram", 1e3),
    Unit('ton', "ton", 1e6),
  )),
  Family('volume', (
    Unit('ml', "millilitre", 1e-3),
    Unit('cl', "centilitre", 1e-2),
    Unit('dl', "decilitre", 1e-1),
    Unit('l', "litre", 1),
  )),
  Family('time', (
    Unit('ms', "millisecond", 1e-3),
    Unit('s', "second", 1),
    Unit('m', "minute", 60),
    Unit('H', "hour", 60 * 60),
    Unit('d', "day", 60 * 60 * 24),
    Unit('w', "week", 60 * 60 * 24 * 7),
    Unit('y', "year", 60 * 60 * 24 * 365),
  ))
];

class UnitRepr:
  def __init__(self, family, unit, amount):
    self.family = family.type;
    self.suffix = unit.suffix;
    self.long = unit.long;
    self.size = unit.size;
    self.amount = amount;

bucket_m = re.compile("^([0-9]+(\.[0-9]+)?(e[1-9][0-9]*)?)([a-zA-Z]+)$");
time_m = re.compile("^(.*)/([a-zA-Z]+)$");

def parse_bucket(arg):
  bucket = bucket_m.match(arg);
  
  if not bucket:
    return None;
  
  amount, _, _, suffix = bucket.groups();
  family, unit = find_unit_by_suffix(suffix);
  
  if not family:
    print "No family for suffix:", suffix;
    return None;
  
  return UnitRepr(family, unit, float(amount));

def parse_delta(arg):
  delta = time_m.match(arg);
  
  if not delta:
    print "Argument is not a valid delta:", delta
    return 1;
  
  delta_left, delta_right = delta.groups();
  
  left_u = parse_bucket(delta_left);
  
  if not left_u:
    print "Bad unit:", delta_left;
    return None, None;
  
  time_f, time_u = find_unit_by_type('time', delta_right);

  if not time_f:
    print "No unit matching:", delta_right
    return None, None;
  
  return left_u, UnitRepr(time_f, time_u, 0);

def find_unit_by_suffix(suffix):
  for family in units:
    for unit in family.units:
      if unit.suffix == suffix:
        return family, unit;
  
  return None, None;

def find_unit_by_type(family_type, suffix):
  for family in units:
    if family.type == family_type:
      for unit in family.units:
        if unit.suffix == suffix:
          return family, unit;
  
  return None, None;
