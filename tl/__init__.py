#!/usr/bin/python

import sys;
import re;

import tl.units;

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

def rel_dist(bucket_u, delta_u, time_u):
    import math

    L = bucket_u.size * bucket_u.amount
    v = delta_u.size * delta_u.amount / time_u.size
    c = 299792458.0
    
    if (v == c):
      delta_u.size = 0.0;
      return;
    
    if (v > c):
      print 'Speed more than the speed of light, cannot use relativistic math.'
      print
      return;

    Lp = L*math.sqrt(1 - v**2/c**2)

    if (v > 0.1*c):
      print 'Speed is %.2f%% the speed of light.' % round(float(v)/float(c)*100, 2)
      print 'Distance gets shortened by %.2f%%.' % round(100-float(Lp)/float(L)*100, 2)
      print
    
    bucket_u.size = Lp / bucket_u.amount;

def main_command(command):
  if command == "list":
    print "===List of all units==="
    for family in tl.units.units:
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
  
  delta = argv[1];
  
  bucket_u = tl.units.parse_bucket(argv[0]);
  delta_u, time_u = tl.units.parse_delta(argv[1]);
  
  if not (bucket_u and delta_u and time_u):
    return 1;
  
  if bucket_u.family != delta_u.family:
    print "Family type mismatch"
    print bucket_u.family, "!=", delta_u.family;
    return 1;
  
  if bucket_u.family == 'distance':
    rel_dist(bucket_u, delta_u, time_u);
  
  prettyprint_time(int(round((bucket_u.size * bucket_u.amount * time_u.size) / (delta_u.size * delta_u.amount))));
  return 0;

def entrypoint():
  sys.exit(main(sys.argv[1:]));
