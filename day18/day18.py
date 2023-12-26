import sys
import pprint


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


class point_t:
  def __init__(self, r, c):
    self.r = r
    self.c = c

  def __repr__(self):
    return f'({self.r}, {self.c})'

  def __str__(self):
    return f'({self.r}, {self.c})'
  

class line_t:
  def __init__(self, start_point, end_point):
    self.start_point = start_point
    self.end_point = end_point

  def __repr__(self):
    return f'({self.start_point}, {self.end_point})'

  def __str__(self):
    return f'({self.start_point}, {self.end_point})'
    

class shape_t:
  def __init__(self):
    self.edges = []
    self.vertexes = []

  def __repr__(self):
    ret = 'edges:\n'
    for edge in self.edges:
      ret += f'{edge}\n'
    ret += 'vertexes:\n'
    for vertex in self.vertexes:
      ret += f'{vertex}\n'
    return ret

  def __str__(self):
    ret = 'edges:\n'
    for edge in self.edges:
      ret += f'{edge}\n'
    ret += 'vertexes:\n'
    for vertex in self.vertexes:
      ret += f'{vertex}\n'
    return ret


def process_instruction(start_r, start_c, direction, distance, shape):
  deltas = { 'U' : (-1, 0), 'R' : (0, 1), 'D' : (1, 0), 'L' : (0, -1) }
  dr, dc = deltas[direction]
  end_r, end_c = start_r + (dr * distance), start_c + (dc * distance)
  start_point = point_t(start_r, start_c)
  end_point = point_t(end_r, end_c)
  line = line_t(start_point, end_point)
  shape.edges.append(line)
  shape.vertexes.append(start_point)
  return end_r, end_c


#
# https://en.wikipedia.org/wiki/Shoelace_formula
#
def calc_area(shape):
  area = 0
  prev_vertex = None
  count = 0
  for vertex in (*(shape.vertexes), shape.vertexes[0]):
    if count > 0:
      x1, y1 = prev_vertex.c, prev_vertex.r
      x2, y2 = vertex.c, vertex.r
      triangle_area = ((x2 * y1) - (x1 * y2)) / 2
      area += triangle_area
    prev_vertex = vertex
    count += 1
  return abs(area)


def calc_perimeter(shape):
  perimiter = 0
  for edge in shape.edges:
    start_point = edge.start_point
    end_point = edge.end_point
    length = abs(end_point.c - start_point.c if start_point.r == end_point.r else end_point.r - start_point.r)
    debug_print(f'({start_point=}, {end_point=}, {length=}')
    perimiter += length
  return perimiter


def part_n(file_path, extract_dir_dist_fn):
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    shape = shape_t()
    r, c = 0, 0
    for row in rows:
      direction, distance = extract_dir_dist_fn(row)
      r, c = process_instruction(r, c, direction, int(distance), shape)

    debug_print()
    debug_print(shape)

    #
    # The answer isn't just the area of the polygon because we also have to account for the thick, blocky edge.  We need
    # to account for the extra space along the straight part of each edge, and also the space around the outside of what
    # I am calling 'outer' vertexes and the space inside what I am calling 'inner' vertextes.  The extra space is shown
    # as '* here ...
    #
    #  *****  **            ##
    #  #####  *##           #*
    #          #           
    #  Edge   Outer vertex  Inner vertex
    #
    area = calc_area(shape)
    perimeter = calc_perimeter(shape)
    num_vertexes = len(shape.vertexes)
    num_inner_vertexes = (num_vertexes - 4) / 2
    num_outer_vertexes = num_vertexes - num_inner_vertexes
    result = int(area + ((perimeter - num_vertexes) / 2) + (num_inner_vertexes / 4) + (num_outer_vertexes * 3 / 4))
    debug_print(f'{area=}, {perimeter=}, {num_vertexes=}, {num_inner_vertexes=}, {num_outer_vertexes=}, {result=}')
    print(result)


def extract_dir_dist_1(row):
  direction, distance, _ = row.split(' ')
  return direction, distance


def part_1(file_path):
  part_n(file_path, extract_dir_dist_1)


def extract_dir_dist_2(row):
  _, _, color = row.split(' ')
  distance_string = color[2:7]
  direction_index = int(color[7])
  distance = int(distance_string, 16)   # Interpret as hex
  direction = ['R', 'D', 'L', 'U'][direction_index]
  return direction, distance


def part_2(file_path):
  part_n(file_path, extract_dir_dist_2)


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
