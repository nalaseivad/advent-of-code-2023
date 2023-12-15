import sys
import pprint
from collections import deque


debug_level = 0

def debug_print(s, level = 1):
  if level > debug_level: return
  print(s)

#
# Print a more readable version of our maps
#
def debug_pretty_print(x, level = 1):
  if level > debug_level: return
  pp = pprint.PrettyPrinter(indent = 4)
  pp.pprint(x)


def partition_impl(iterable, bucket_size, offset):
  buckets = deque()
  n = 0
  for item in iterable:
    if n % offset == 0:
      buckets.append([])
    for bucket in buckets:
      bucket.append(item)
    if len(buckets[0]) == bucket_size:
      yield buckets.popleft()
    n += 1
  while len(buckets) > 0:
    yield buckets.popleft()


#
# Partition a list into an iterable of sublists of a certain size with a specific offset.  The last list may be
# incomplete.
# Examples
#   partition([1, 2, 3, 4, 5, 6, 7], 2)    -> [[1, 2], [3, 4], [5, 6], [7]]
#   partition([1, 2, 3, 4, 5, 6, 7], 3, 2) -> [[1, 2, 3], [3, 4, 5], [5, 6, 7], [7]]
#
def partition(iterable, bucket_size, offset = None):
  if offset == None: offset = bucket_size
  return partition_impl(iterable, bucket_size, offset)


#
# For each column, move 'O' rocks to the North far as they can go
#
# For each column from left to right
#   For each row from top to bottom
#     Continue until we find a 'O' *
#     Walk back up the column until we find a '#' or a 'O'
#       Move the 'O' from * up to the cell just below the found '#' or a 'O'
#       Replace the 'O' from * with '.'
#
def tilt_platform_north(platform):
  platform_height = len(platform)
  platform_width = len(platform[0])
  for col_n in range(platform_width):
    for row_n in range(0, platform_height, 1):
      cell = platform[row_n][col_n]
      if cell in ('.', '#'): continue

      blockage_n = -1
      for n in range(row_n - 1, -1, -1):
        if platform[n][col_n] in ('#', 'O'):
          blockage_n = n
          break

      if row_n == blockage_n + 1: continue

      platform[blockage_n + 1][col_n] = cell
      platform[row_n][col_n] = '.'

#
# For each row, move 'O' rocks to the East as far as they can go
#
# For each row from top to bottom
#   For each row from right to left
#     Continue until we find a 'O' *
#     Walk back across the row to the right until we find a '#' or a 'O'
#       Move the 'O' from * across to the cell just to the left of the found '#' or a 'O'
#       Replace the 'O' from * with '.'
#
def tilt_platform_east(platform):
  platform_height = len(platform)
  platform_width = len(platform[0])

  for row_n in range(platform_height):
    for col_n in range(platform_width - 1, -1, -1):
      cell = platform[row_n][col_n]
      if cell in ('.', '#'): continue

      blockage_n = -1
      for n in range(col_n + 1, platform_width, 1):
        if platform[row_n][n] in ('#', 'O'):
          blockage_n = n
          break

      if blockage_n == -1: blockage_n = platform_width
      if col_n == blockage_n - 1: continue

      platform[row_n][blockage_n - 1] = cell
      platform[row_n][col_n] = '.'


#
# For each column, move 'O' rocks to the South far as they can go
#
# For each column from left to right
#   For each row from bottom to top
#     Continue until we find a 'O' *
#     Walk back down the column until we find a '#' or a 'O'
#       Move the 'O' from * down to the cell just above the found '#' or a 'O'
#       Replace the 'O' from * with '.'
#
def tilt_platform_south(platform):
  platform_height = len(platform)
  platform_width = len(platform[0])
  for col_n in range(platform_width):
    for row_n in range(platform_height - 1, -1, -1):
      cell = platform[row_n][col_n]
      if cell in ('.', '#'): continue

      blockage_n = -1
      for n in range(row_n + 1, platform_height, 1):
        if platform[n][col_n] in ('#', 'O'):
          blockage_n = n
          break

      if blockage_n == -1: blockage_n = platform_height
      if row_n == blockage_n - 1: continue

      platform[blockage_n - 1][col_n] = cell
      platform[row_n][col_n] = '.'


#
# For each row, move 'O' rocks to the West as far as they can go
#
# For each row from top to bottom
#   For each row from left to right
#     Continue until we find a 'O' *
#     Walk back across the row to the left until we find a '#' or a 'O'
#       Move the 'O' from * across to the cell just to the right of the found '#' or a 'O'
#       Replace the 'O' from * with '.'
#
def tilt_platform_west(platform):
  platform_height = len(platform)
  platform_width = len(platform[0])

  for row_n in range(platform_height):
    for col_n in range(0, platform_width, 1):
      cell = platform[row_n][col_n]
      if cell in ('.', '#'): continue

      blockage_n = -1
      for n in range(col_n - 1, -1, -1):
        if platform[row_n][n] in ('#', 'O'):
          blockage_n = n
          break

      if col_n == blockage_n + 1: continue
      
      platform[row_n][blockage_n + 1] = cell
      platform[row_n][col_n] = '.'


def calc_load(platform):
  load = 0
  platform_height = len(platform)
  for row_n, row in enumerate(platform):
    for cell in row:
      if cell == 'O':
        load += platform_height - row_n
  return load


def part_1(file_path):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    platform = [[c for c in row] for row in lines]
    tilt_platform_north(platform)
    print(calc_load(platform))


def cycle_platform(platform):
  tilt_platform_north(platform)
  tilt_platform_west(platform)
  tilt_platform_south(platform)
  tilt_platform_east(platform)


def print_platform(platform):
  for row in platform:
    print(''.join(row))
  print()


#
# We have to determine the load on the platform after 1,000,000,000 cycles!  It's computationally infeasible to actually
# simulate that so we have to be clever.  I assume that the load on the platform will fall into a loop of it's own as we
# cycle through tilts of the platform.  So let's sample some cycles and see what the loads are.
#
# For test-input.txt we get these results ...
#
# 87: 1 []            Cycle  1
# 69: 2 [1, [1, 6]+]  Cycles 2 + 7n, cycles 3 + 7n for n = 0, 1, 2, ...
# 65: 5 [[2, 5]+]     Cycles 4 + 7n, cycles 6 + 7n for n = 0, 1, 2, ...
# 64: 6 [[7]+]        Cycles 5 + 7n                for n = 0, 1, 2, ...
# 63: 8 [[7]+]        Cycles 0 + 7n                for n = 0, 1, 2, ...
# 68: 9 [[7]+]        Cycles 8 + 7n                for n = 0, 1, 2, ...
# 
# 1,000,000,000 % 7 == 6 so after a billion cycles the load will be 64 as the problem says.
# 
# Now for input.txt.  We get these results ...
#
# 96258:    1 []
# 96283:    2 []
# ...
# 102727:  82 []
# 102696:  83 [[42]+]  Cycles  83 + 42n for n = 0, 1, 2, ...   = 41 + 42n for n = 1, 2, 3, ...
# 102660:  84 [[42]+]  Cycles  84 + 42n for n = 0, 1, 2, ...   =  0 + 42n for n = 2, 3, 4, ...
# 102625:  85 [[42]+]  Cycles  85 + 42n for n = 0, 1, 2, ...   =  1 + 42n for n = 2, 3, 4, ...
# ...
# 102943: 118 [[42]+]  Cycles 118 + 42n for n = 0, 1, 2, ...   = 34 + 42n for n = 2, 3, 4, ...
# ...
# 102747: 123 [[42]+]  Cycles 123 + 42n for n = 0, 1, 2, ...   = 39 + 42n for n = 2, 3, 4, ...
# 102726: 124 [[42]+]  Cycles 124 + 42n for n = 0, 1, 2, ...   = 40 + 42n for n = 2, 3, 4, ...
#
# 1,000,000,000 % 42 == 34 so after a billion cycles the load will be 102943.  That is the right answer.
#
def part_2(file_path):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    platform = [[c for c in row] for row in lines]

    #
    # Sample 1,000 cycles ...
    #
    loads = {}
    for n in range(1, 1000, 1):
      cycle_platform(platform)
      load = calc_load(platform)
      if load not in loads:
        loads[load] = {}
        loads[load]['cycles'] = [n]
      else:
        loads[load]['cycles'].append(n)

    #
    # Let's look for loops in the load ...
    #
    for k, v in loads.items():
      cycles = loads[k]['cycles']
      loads[k]['start_cycle'] = min(cycles)
      deltas = []
      if len(cycles) > 1:
        for pair in partition(cycles, 2, 1):
          if len(pair) == 2:
            delta = pair[1] - pair[0]
            deltas.append(delta)
      loads[k]['cycle_deltas'] = deltas

    #
    # Print some stats ...
    #
    for k, v in loads.items():
      start_cycle = v['start_cycle']
      cycle_deltas = v['cycle_deltas']
      cycles = v['cycles']
      print(f'{k}: {start_cycle} {cycle_deltas[0:10]} {cycles[0:15]}')


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
