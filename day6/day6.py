import sys
import re
import pprint
from functools import reduce
from math import sqrt


debug = 0

def debug_print(s):
  if debug:
    print(s)

#
# Print a more readable version of our maps
#
def debug_pretty_print(x):
  if debug:
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(x)


#
# Let's use math!
#
# If we wait t milliseconds before starting then the boat will move off at t millimeters / millisecond and will run for
# total_time - t milliseconds.  The total distance travelled will be d where d = t * (total_time - t).  In order for
# this to beat record_distance then we need d > record_distance or t * (total_time - t) > record_distance.  This is a
# quadratic inequality in t ...
#
# -t^2 + (total_time * t) - record_distance > 0
#
# This is an inverted parabola.  There will be two times, t1 and t2, between which the parabola will be above the x axis
# given by ...
#
# t1 = (- total_time / 2) + (sqrt(total_time^2 - (4 * record_distance)) / (-2))
# t2 = (- total_time / 2) - (sqrt(total_time^2 - (4 * record_distance)) / (-2))
#
# Equivalently ...
#
# t1 = (total_time / 2) + (sqrt(total_time^2 - (4 * record_distance)) / 2)
# t2 = (total_time / 2) - (sqrt(total_time^2 - (4 * record_distance)) / 2)
#
# The start wait times that we can employ and still beat the record are [ int(t1) + 1, ..., int(t2) ] unless t2 is an
# integer in which case it's [ int(t1) + 1, ..., int(t2) - 1 ]
#
def process_race(race):
  total_time, record_distance = race

  delta = sqrt(pow(total_time, 2) - (4 * record_distance)) / 2
  mid_t = total_time / 2
  t1 = mid_t - delta
  t2 = mid_t + delta
  debug_print(f't1 = {t1}, t2 = {t2}')

  t1 = int(t1) + 1
  t2 = int(t2) - 1 if t2 % 10 == 0 else int(t2)
  count = t2 - t1 + 1
  debug_print(f't1 = {t1}, t2 = {t2}, count = {count}')
  
  return count


def parse_line(line):
  _, s = re.split(r':\s*', line.rstrip('\n'))
  return list(map(int, re.split(r'\s+', s)))


def part_1(file_path):
  with open(file_path, 'r') as lines:
    times = parse_line(next(lines))
    distances = parse_line(next(lines))
  races = list(zip(times, distances))
  counts = []
  for race in races:
    counts.append(process_race(race))
  debug_print(counts)
  print(reduce(lambda accumulator, x: accumulator * x, counts))


def part_2(file_path):
  with open(file_path, 'r') as lines:
    times = parse_line(next(lines))
    distances = parse_line(next(lines))
  time = int(''.join(map(str, times)))
  distance = int(''.join(map(str, distances)))
  print(process_race((time, distance)))


if len(sys.argv) != 3:
  print(f'Usage: python3 {sys.argv[0]} <part> <file_path>')
  exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

if part == '1':
  part_1(file_path)
elif part == '2':
  part_2(file_path)
else:
  print('Unknown part')
  exit(1)
