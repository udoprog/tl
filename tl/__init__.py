#!/usr/bin/python

import sys;
import re;
import collections;

Family = collections.namedtuple('Family', 'type units')
Unit = collections.namedtuple('Unit', 'suffix long size')

units = [
  Family('net', (
    Unit('B', "byte", 1),
    Unit('kB', "kilobyte", 1000),
    Unit('MB', "megabyte", 1000 ** 2),
    Unit('GB', "gigabyte", 1000 ** 3),
    Unit('TB', "terabyte", 1000 ** 4),
    Unit('PB', "petabyte", 1000 ** 5),
    Unit('EB', "exabyte", 1000 ** 6),
    Unit('ZB', "zetabyte", 1000 ** 7),
    Unit('YB', "yottabyte", 1000 ** 8),
    Unit('KiB', "kibibyte", 1024),
    Unit('MiB', "mebibyte", 1024 ** 2),
    Unit('GiB', "gibibyte", 1024 ** 3),
    Unit('TiB', "tebibyte", 1024 ** 4),
    Unit('PiB', "pebibyte", 1024 ** 5),
    Unit('EiB', "exbibyte", 1024 ** 6),
    Unit('ZiB', "zebibyte", 1024 ** 7),
    Unit('YiB', "yobibyte", 1024 ** 8),
  )),
  Family('weight', (
    Unit('g', "gram", 1),
    Unit('kg', "kilogram", 1000),
    Unit('ton', "ton", 1000**2),
  )),
  Family('volume', (
    Unit('ml', "millilitre", 1e-3),
    Unit('l', "litre", 1),
  )),
  Family('time', (
    Unit('ms', "second", 1e-3),
    Unit('s', "second", 1),
    Unit('m', "minute", 60),
    Unit('H', "minute", 60 * 60),
  ))
];

def match_unit(arg):
  bucket = bucket_m.match(arg);
  
  if not bucket:
    return None, None, None;
  
  amount, _, suffix = bucket.groups();
  
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

bucket_m = re.compile("^([0-9]+(\.[0-9]+)?)([a-zA-Z]+)$");
time_m = re.compile("^(.*)/([a-zA-Z]+)$");

def main(argv):
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
  
  prettyprint_time(int((a_unit.size * a_amount * time_u.size) / (b_unit.size * b_amount)));
  return 0;

def entrypoint():
  sys.exit(main(sys.argv[1:]));
