import sys
import pprint


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


def debug_print_surface(surface, inside_coordinates, outside_coordinates, level = 1):
  if level > debug_level: return
  for coordinate in inside_coordinates:
    x, y = list(map(int, coordinate.split(',')))
    surface[y][x] = 'I'
  for coordinate in outside_coordinates:
    x, y = list(map(int, coordinate.split(',')))
    surface[y][x] = 'O'
  for row in surface:
    for cell in row:
      print(cell, end = '')
    print()
  

moves = {
  'N' : [  0, -1 ],
  'E' : [  1,  0 ],
  'S' : [  0,  1 ],
  'W' : [ -1,  0 ]
}


pipes = {
  '|' : { 'valid_from_moves' : [ 'N', 'S' ], 'to_moves' : { 'N' : 'N', 'S' : 'S' } },
  '-' : { 'valid_from_moves' : [ 'E', 'W' ], 'to_moves' : { 'E' : 'E', 'W' : 'W' } },
  'L' : { 'valid_from_moves' : [ 'S', 'W' ], 'to_moves' : { 'S' : 'E', 'W' : 'N' } },
  'J' : { 'valid_from_moves' : [ 'S', 'E' ], 'to_moves' : { 'S' : 'W', 'E' : 'N' } },
  '7' : { 'valid_from_moves' : [ 'E', 'N' ], 'to_moves' : { 'E' : 'S', 'N' : 'W' } },
  'F' : { 'valid_from_moves' : [ 'W', 'N' ], 'to_moves' : { 'W' : 'S', 'N' : 'E' } }
}


def init(file_path):
  with open(file_path, 'r') as lines:
    start_x = 0
    start_y = 0
    surface = []
    lines = (line.rstrip('\n') for line in lines)
    for y, line in enumerate(lines):
      debug_print(line)
      row = []
      for x, c in enumerate(line):
        row.append(c)
        if c == 'S':
          start_x = x
          start_y = y
      surface.append(row)
    return surface, start_x, start_y


def calc_valid_moves(surface, start_x, start_y):
  valid_moves = []
  surface_width, surface_height = len(surface[0]), len(surface)
  x, y = start_x, start_y
  for move, offset in moves.items():
    new_x = x + offset[0]
    new_y = y + offset[1]
    if new_x < 0 or new_x >= surface_width: continue
    if new_y < 0 or new_y >= surface_height: continue
    new_cell = surface[new_y][new_x]
    if new_cell == '.': continue
    if new_cell == 'S': continue   # Shouldn't happen
    pipe = pipes[new_cell]
    valid_from_moves = pipe['valid_from_moves']
    if move in valid_from_moves:
      valid_moves.append(move)

  return valid_moves


def follow_pipe(surface, start_x, start_y, initial_move):
  x, y = start_x, start_y
  cell = surface[y][x]
  distance = 0
  path = []
  distances = {}
  move = initial_move

  debug_print('\nfollow_pipe ...', 2)
  done = False
  while not done:
    coordinate = f'{x},{y}'
    element = { 'x' : x, 'y' : y, 'coordinate' : coordinate, 'cell' : cell, 'distance' : distance }
    debug_print(element, 2)
    path.append(element)
    distances[coordinate] = distance
    offset = moves[move]
    new_x = x + offset[0]
    new_y = y + offset[1]
    new_cell = surface[new_y][new_x]
    if new_cell == 'S': break
    move = pipes[new_cell]['to_moves'][move]
    x, y, cell = new_x, new_y, new_cell
    distance += 1

  return distances


def part_n(file_path, fn):
  surface, start_x, start_y = init(file_path)
  debug_print(f'start_x = {start_x}, start_y  = {start_y}')

  valid_moves = calc_valid_moves(surface, start_x, start_y)
  debug_print(f'valid_moves: {valid_moves}')

  distances = follow_pipe(surface, start_x, start_y, valid_moves[0])

  fn(surface, start_x, start_y, valid_moves, distances)


def part_1_fn(surface, start_x, start_y, valid_moves, distances):
  path_length = len(distances)
  max_distance = path_length / 2
  print(max_distance)


def part_1(file_path):
  part_n(file_path, part_1_fn)

    
def replace_s(surface, valid_moves, start_x, start_y):
  m = {
    'N' : { 'E' : 'L', 'S' : '|', 'W' : 'J'},
    'E' : { 'N' : 'L', 'S' : 'F', 'W' : '-'},
    'S' : { 'N' : '|', 'E' : 'F', 'W' : '7'},
    'W' : { 'N' : 'J', 'E' : '-', 'S' : '7'}
  }
  surface[start_y][start_x] = m[valid_moves[0]][valid_moves[1]]


def part_2_fn(surface, start_x, start_y, valid_moves, distances):
  # Replace the starting 'S' with the appropriate pipe character to simplify the calcs below
  replace_s(surface, valid_moves, start_x, start_y)
  
  count = 0
  outside_coordinates = []
  inside_coordinates = []
  for y, row in enumerate(surface):
    is_inside = False
    for x, cell in enumerate(row):
      coordinate = f'{x},{y}'
      if coordinate in distances.keys():
        if cell in ('|', 'J', 'L'):
          is_inside = not is_inside
      else:
        if is_inside:
          count += 1
          inside_coordinates.append(coordinate)
        else:
          outside_coordinates.append(coordinate)

  debug_print_surface(surface, inside_coordinates, outside_coordinates)

  print(count)


def part_2(file_path):
  part_n(file_path, part_2_fn)


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
