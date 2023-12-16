import sys
import pprint
from copy import deepcopy


debug_level = 0

def debug_print(s = '', level = 1, end = '\n'):
  if level > debug_level: return
  print(s, end=end)

#
# Print a more readable version of our maps
#
def debug_pretty_print(x, level = 1):
  if level > debug_level: return
  pp = pprint.PrettyPrinter(indent = 4)
  pp.pprint(x)


def new_xy(x, y, direction):
  delta_x = { 'N' : 0, 'E' : 1, 'S' : 0, 'W' : -1 }
  delta_y = { 'N' : -1, 'E' : 0, 'S' : 1, 'W' : 0 }
  return x + delta_x[direction], y + delta_y[direction]


def new_direction(mirror, direction):
  map = {
    '/' : { 'N' : 'E', 'E' : 'N', 'S' : 'W', 'W' : 'S' },
    '\\' : { 'N' : 'W', 'E' : 'S', 'S' : 'E', 'W' : 'N' }
  }
  return map[mirror][direction]


def update_grid(grid, start_xy, direction, level = 0):
  x, y = start_xy
  while True:
    if x < 0 or x == len(grid[0]) or y < 0 or y == len(grid):
      debug_print('out of bounds', 2)
      break

    key = (x, y, direction)
    cell = grid[y][x]
    set = cell[2]
    if key in set:
      debug_print('loop', 2)
      break

    set.add(key)
    cell[1] += 1
    c = cell[0]
  
    debug_print(f"{level}: {x}, {y}, {direction} : '{c}'", 2)

    if c == '-' and direction in ('N', 'S'):
      update_grid(grid, new_xy(x, y, 'E'), 'E', level + 1)
      update_grid(grid, new_xy(x, y, 'W'), 'W', level + 1)
      break
    elif c == '|' and direction in ('E', 'W'):
      update_grid(grid, new_xy(x, y, 'N'), 'N', level + 1)
      update_grid(grid, new_xy(x, y, 'S'), 'S', level + 1)
      break
    elif c in ('/', '\\'):
      direction = new_direction(c, direction)
      update_grid(grid, new_xy(x, y, direction), direction, level + 1)
      break
    else:
      x, y = new_xy(x, y, direction)


def debug_print_grid(grid):
  for row in grid:
    for cell in row:
      debug_print(cell[0], end='')
    debug_print()
  debug_print()


def count_energized(grid, start_xy, direction):
  update_grid(grid, start_xy, direction)
  count = 0
  for row in grid:
    for cell in row:
      count += 1 if cell[1] > 0 else 0
  return count


def part_1(file_path):
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    grid = [[[c, 0, set()] for c in row] for row in rows]

    debug_print_grid(grid)

    count = count_energized(grid, (0, 0), 'E')
    print(count)


def part_2(file_path):
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    grid = [[[c, 0, set()] for c in row] for row in rows]

    max_count = 0
    width = len(grid)
    height = len(grid[0])

    for x in range(width):
      grid2 = deepcopy(grid)
      count = count_energized(grid2, (x, 0), 'S')
      debug_print(f'{x}, {0} {count}')
      max_count = max(max_count, count)
      grid2 = deepcopy(grid)
      count = count_energized(grid2, (x, height - 1), 'N')
      debug_print(f'{x}, {height - 1} {count}')
      max_count = max(max_count, count)

    for y in range(height):
      grid2 = deepcopy(grid)
      count = count_energized(grid2, (0, y), 'E')
      debug_print(f'{0}, {y} {count}')
      max_count = max(max_count, count)
      grid2 = deepcopy(grid)
      count = count_energized(grid2, (width - 1, y), 'W')
      debug_print(f'{width - 1}, {y} {count}')
      max_count = max(max_count, count)

    print(max_count)


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
