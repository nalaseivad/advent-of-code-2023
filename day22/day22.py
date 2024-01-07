import sys
import pprint
from collections import deque


debug_level = 0

def debug(level = 1):
  if level > debug_level: return False
  return True

def debug_print(s = '', level = 1, end = '\n'):
  if level > debug_level: return
  print(s, end=end)

def debug_pretty_print(x, level = 1):
  if level > debug_level: return
  pp = pprint.PrettyPrinter(indent = 4)
  pp.pprint(x)

def debug_print_grid(grid, level = 1):
  if level > debug_level: return
  for row in grid:
    print(''.join(row))
  print()


def init_empty_rows(bricks):
  max_x = max(map(lambda brick: brick[2][0], bricks))
  max_z = max(map(lambda brick: brick[2][2], bricks))
  rows = []
  for z in range(max_z + 1):
    row = []
    for x in range(max_x + 1):
      row.append('.')
    rows.append(row)
  return rows


def projection(bricks, range_fn):
  rows = init_empty_rows(bricks)
  for brick in bricks:
    name, (_, _, z1), (_, _, z2) = brick
    for z in range(z1, z2 + 1):
      for axis in range_fn(brick):
        if rows[z][axis] == '.':
          rows[z][axis] = name
  return rows


def x_projection(bricks):
  return projection(bricks, lambda brick: range(brick[1][0], brick[2][0] + 1))


def y_projection(bricks):
  return projection(bricks, lambda brick: range(brick[1][1], brick[2][1] + 1))


def print_projection(rows, label):
  print(f' {label} ')
  print('012')
  for z in range(len(rows) - 1, -1, -1):
    row = ''.join(rows[z])
    print(f'{row} {z}')


def print_projections(bricks):
  print('-----'  )
  print_projection(x_projection(bricks), 'x')
  print()
  print_projection(y_projection(bricks), 'y')
  print()


#
# Assume that x11 <= x12 and x21 <= x22
#
# No             Yes            Yes          Yes       Yes        Yes       Yes         Yes           No
# x11 x12        x11 x12        x11 x12      x11 x12    x11 x12     x11 x12     x11 x12       x11 x12         x11 x12
# v   v          v   v          v   v        v   v      v   v       v   v       v   v         v   v           v   v
# xxxxx          xxxxx          xxxxx        xxxxx      xxxxx       xxxxx       xxxxx         xxxxx           xxxxx
#       xxxxxxx      xxxxxxx       xxxxxxx   xxxxxxx   xxxxxxx    xxxxxxx   xxxxxxx     xxxxxxx       xxxxxxx
#       ^     ^      ^     ^       ^     ^   ^     ^   ^     ^    ^     ^   ^     ^     ^     ^       ^     ^
#       x21   x22    x21   x22     x21   x22 x21   x22 x21   x22  x21   x22 x21   x22  x21   x22     x21   x22
#
# They overlap iff x12 >= x21 and x11 <= x22
#
def lines_overlap(x11, x12, x21, x22):
  return x12 >= x21 and x11 <= x22


#
# brick:  [<bottom-left-coord>, <top-right-coord>]
#
# brick1: [[x11, y11, z11], [x12, y12, z12]]
# brick2: [[x21, y21, z21], [x22, y22, z22]]
#
# Assume that x11 <= x12, y11 <= y12 and z11 <= z12
# and that    x21 <= x22, y21 <= y22 and z21 <= z22
#
# In the x-y plane ...
#
#     xxxxx <- brick2
#     x   x
#     x   x xxxxx
#     x   x x   x
#     xxxxx x   x
#           x   x
#           xxxxx <- brick1
#   
#     xxxxx <- brick2
#     x   x
#   xxxxx x
#   x x x x
#   x xxxxx
#   x   x
#   xxxxx <- brick1
#
def bricks_overlap(brick1, brick2):
  _, (x11, y11, _), (x12, y12, _) = brick1
  _, (x21, y21, _), (x22, y22, _) = brick2
  return lines_overlap(x11, x12, x21, x22) and lines_overlap(y11, y12, y21, y22)


def fall(bricks):
  for n, brick in enumerate(bricks):
    base_z = 0
    if n > 0:
      # Examine all the bricks that are lower than 'brick' ...
      for lower_brick in bricks[:n]:
        if bricks_overlap(brick, lower_brick):
          # lower_brick's upper corner will be the floor
          base_z = max(base_z, lower_brick[2][2])
    fall_distance = brick[1][2] - (base_z + 1)
    brick[2][2] -= fall_distance
    brick[1][2] -= fall_distance


def init_dict(bricks):
  return { n : set() for n in range(len(bricks))}


def calc_support_network(bricks):
  supports = init_dict(bricks)
  rests_on = init_dict(bricks)
  for brick_n, brick in enumerate(bricks):
    for m, upper_brick in enumerate(bricks[(brick_n + 1)::]):
      upper_brick_n = m + brick_n + 1
      if bricks_overlap(upper_brick, brick):
        z_offset = upper_brick[1][2] - brick[2][2]
        if z_offset == 1:
          rests_on[upper_brick_n].add(brick_n)
          supports[brick_n].add(upper_brick_n)
  return supports, rests_on


def init_bricks(file_path):
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    bricks = []
    for r, row in enumerate(rows):
      name = chr(ord('A') + r) if r <= 6 else ''
      brick = [name, *[[int(n) for n in coordinate.split(',')] for coordinate in row.split('~')]]
      bricks.append(brick)
    return bricks


def part_n(file_path, fn):
  bricks = init_bricks(file_path)

  # Sort so that the bricks are in increasing order of first corner z coordinate
  bricks.sort(key = lambda brick: brick[1][2])
  
  if(debug(2)): print_projections(bricks)
  fall(bricks)
  if(debug()): print_projections(bricks)

  # Some of the bricks may have fallen past lower bricks so we need to sort again
  bricks.sort(key = lambda brick: brick[1][2])

  supports, rests_on = calc_support_network(bricks)
  debug_print(f'{supports=}\n{rests_on=}')
  fn(bricks, supports, rests_on)


#
# We can disintegrate a brick provided that all the bricks it supports rest on at least two bricks, i.e. if there's one
# other supporting brick as well as the brick we are considering for disintegration.  We need to calc the total number
# of bricks we can disintegrate.
#
def part1_fn(bricks, supports, rests_on):
  count = 0
  for n in range(len(bricks)):
    if all(len(rests_on[m]) >= 2 for m in supports[n]):
      count += 1
  print(f'result = {count}')


#
# For each brick we have to figure out how many other bricks would fall, in a chain reaction, if it were disintegrated.
# We need to calc the sum of that over all bricks.
#
def part2_fn(bricks, supports, rests_on):
  count = 0
  for n in range(len(bricks)):
    will_fall = deque(m for m in supports[n] if len(rests_on[m]) == 1)
    falling = set(will_fall)
    falling.add(n)                          # Add the brick that disintegrates too

    while will_fall:
      m = will_fall.popleft()
      for k in supports[m]:
        if k in falling: continue           # Don't double count
        if rests_on[k].issubset(falling):   # If all the bricks this brick rests on are falling (or disinegrated)
          will_fall.append(k)
          falling.add(k)

    count += len(falling) - 1               # Don't count the brick that disintegrated

  print(f'result = {count}')


#
# * Each line is a pair of (x, y, z) coordinates that describe the extremes (opposite corners) of a 3D block/brick.
# * In each pair only one of the coordinates is different so each of the bricks they describe are 1 unit wide and long
#   and n units high, potentially reoriented of course.
# * In each pair the coordinate that differs is always larger in the second element of the pair.  This means that the
#   first corner coordinates are always <= the cooresponding coordinate of the second corner.
#


def part_1(file_path):
  part_n(file_path, part1_fn)


def part_2(file_path):
  part_n(file_path, part2_fn)


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
