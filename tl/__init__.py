#!/usr/bin/python

import sys;
import re;
import collections;

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

def match_unit(arg):
  bucket = bucket_m.match(arg);
  
  if not bucket:
    return None, None, None;
  
  amount, _, _, suffix = bucket.groups();
  
  if amount:
    amount = float(amount);
  
  family, unit = find_unit_by_suffix(suffix);

  if family:
    return family, unit, amount;
  
  return None, None, None;

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

def prettyprint_time(seconds):
  if seconds < 1:
    print "less than a second"
    return;
  
  timeparts = list();

  mill = 0;
  cent = 0;
  dec = 0;
  y = 0;
  d = 0;
  H = 0;
  m = 0;
  
  if seconds > 60:
    m = seconds / 60;
    seconds -= (m * 60)
  
  if m > 60:
    H = m / 60;
    m -= (H * 60)
  
  if H > 24:
    d = H / 24;
    H -= (d * 24);
  
  if d > 365:
    y = d / 365;
    d -= (y * 365)
  
  if y > 10:
    dec = y / 10;
    y -= (dec * 10)

  if dec > 10:
    cent = dec / 10;
    dec -= (cent * 10);

  if cent > 10:
    mill = cent / 10;
    cent -= (mill * 10);

  if mill > 0:
    if mill == 1:
      timeparts.append(str(mill) + " millenium")
    else:
      timeparts.append(str(mill) + " millenia")
  
  if cent > 0:
    if cent == 1:
      timeparts.append(str(cent) + " century")
    else:
      timeparts.append(str(cent) + " centuries")
  
  if dec > 0:
    if dec == 1:
      timeparts.append(str(dec) + " decade")
    else:
      timeparts.append(str(dec) + " decades")
  
  if y > 0:
    if y == 1:
      timeparts.append(str(y) + " year")
    else:
      timeparts.append(str(y) + " years")

  if d > 0:
    if d == 1:
      timeparts.append(str(d) + " day")
    else:
      timeparts.append(str(d) + " days")
  
  if H > 0:
    if H == 1:
      timeparts.append(str(H) + " hour")
    else:
      timeparts.append(str(H) + " hours")

  if m > 0:
    if m == 1:
      timeparts.append(str(m) + " minute")
    else:
      timeparts.append(str(m) + " minutes")
  
  if seconds > 0:
    if seconds == 1:
      timeparts.append(str(seconds) + " second")
    else:
      timeparts.append(str(seconds) + " seconds")
  
  print ", ".join(timeparts);

def rel_dist(a_unit, a_amount, b_unit, b_amount, time_u):
    import math

    L = a_unit.size * a_amount
    v = b_unit.size * b_amount / time_u.size
    c = 299792458.0

    if (v == c):
      return Unit(a_unit.suffix, a_unit.long, 0.0)
      
    if (v > c):
      print 'Speed more than the speed of light, cannot use relativistic math.'
      print
      return a_unit

    Lp = L*math.sqrt(1 - v**2/c**2)

    if (v > 0.1*c):
      print 'Speed is %.2f%% the speed of light.' % round(float(v)/float(c)*100, 2)
      print 'Distance gets shortened by %.2f%%.' % round(100-float(Lp)/float(L)*100, 2)
      print
    
    return Unit(a_unit.suffix, a_unit.long, Lp / a_amount)

bucket_m = re.compile("^([0-9]+(\.[0-9]+)?(e[1-9][0-9]*)?)([a-zA-Z]+)$");
time_m = re.compile("^(.*)/([a-zA-Z]+)$");

def main_command(command):
  if command == "list":
    print "===List of all units==="
    for family in units:
      print ""
      print family.type
      
      for unit in family.units:
        if unit.size == 1:
          print "%-3s %-20s %s (Base unit)"%(unit.suffix, unit.long, str(unit.size));
        else:
          print "%-3s %-20s %s"%(unit.suffix, unit.long, str(unit.size));

def main(argv):
  if len(argv) == 1:
    return main_command(argv[0]);

  if len(argv) < 2:
    return 1;
  
  bucket = argv[0];
  delta = argv[1];

  a_fam, a_unit, a_amount = match_unit(bucket);

  if not a_fam:
    print "Argument is not a valid bucket:", bucket
    return 1;
  
  time_match = time_m.match(delta);

  if not time_match:
    print "Argument is not a valid delta:", delta
    return 1;
  
  delta_left, delta_right = time_match.groups();
  
  b_fam, b_unit, b_amount = match_unit(delta_left);
  
  if not b_fam:
    print "Bad unit:", delta_left;
    return 1;
  
  if a_fam.type != b_fam.type:
    print "Family type mismatch"
    print a_fam.type, "!=", b_fam.type;
    return 1;
  
  time_f, time_u = find_unit_by_type('time', delta_right);
  
  if not time_f:
    print "Could not find time unit:", delta_right;
    return 1;

  if a_fam.type == 'distance':
    a_unit = rel_dist(a_unit, a_amount, b_unit, b_amount, time_u)
  
  prettyprint_time(int(round((a_unit.size * a_amount * time_u.size) / (b_unit.size * b_amount))));
  return 0;

def entrypoint():
  sys.exit(main(sys.argv[1:]));
