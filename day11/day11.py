import sys
import pprint
from itertools import combinations


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


def debug_print_image(image, level = 1):
  if level > debug_level: return
  for row in image:
    for c in row:
      print(c, end = '')
    print('')


def init_image(file_path):
  image = []
  rows_with_galaxy = set()
  cols_with_galaxy = set()
  galaxies = {}
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    galaxy_number = 1
    for y, line in enumerate(lines):
      row = []
      for x, c in enumerate(line):
        if c == '#':
          cols_with_galaxy.add(x)
          rows_with_galaxy.add(y)
          galaxies[galaxy_number] = (x, y)
          galaxy_number += 1
        row.append(c)
      image.append(row)

  image_height = len(image)
  image_width = len(image[0])
  rows_without_galaxy = set(range(image_height)) - rows_with_galaxy
  cols_without_galaxy = set(range(image_width)) - cols_with_galaxy

  return image, rows_without_galaxy, cols_without_galaxy, galaxies
  

def part_n(file_path, expansion_factor):
  _, rows_without_galaxy, cols_without_galaxy, galaxies = init_image(file_path)
  num_galaxies = len(galaxies.keys())
  galaxy_pairs = combinations(range(1, num_galaxies + 1), 2)

  #
  # .1. .1.. .1... .1.... .1..... .1...... .1....... .1........
  # .x. .xx. .xx.. .xx... .xx.... .xxx.... .xxx..... .xxxx.....
  # .2. ..2. ..x2. ..xx2. ..xxx2. ...xxx2. ...xxxx2. ....xxxx2.
  # 
  # .1. .1.. .1... .1.... .1..... .1......
  # .x. .x.. .x... .xx... .xx.... .xx.....
  # .x. .xx. .xxx. ..xx.. ..xx... ..xx....
  # .2. ..2. ...2. ...x2. ...xx2. ...xxx2.
  #
  # .1. .1.. .1... .1.... .1..... .1...... .1....... .1........ .1............. .1xxxxxxxxxxxx. 
  # .x. .x.. .x... .xx... .xx.... .xx..... .xx...... .xx....... .x............. .............x.
  # .x. .x.. .xx.. ..x... ..x.... ..xx.... ..xx..... ..xx...... .x............. .............x.
  # .x. .xx. ..xx. ..xx.. ..xx... ...xx... ...xx.... ...xx..... .x............. .............x.
  # .2. ..2. ...2. ...x2. ...xx2. ....xx2. ....xxx2. ....xxxx2. .xxxxxxxxxxxx2. .............2.
  #
  # It seems that the shortest path is just delta_x + delta_y
  #
  shortest_paths = []
  for pair in galaxy_pairs:
    galaxy0 = galaxies[pair[0]]
    galaxy1 = galaxies[pair[1]]
    min_x, max_x = min(galaxy0[0], galaxy1[0]), max(galaxy0[0], galaxy1[0])
    min_y, max_y = min(galaxy0[1], galaxy1[1]), max(galaxy0[1], galaxy1[1])
    col_count = row_count = 0
    for x in range(min_x + 1, max_x):
      if x in cols_without_galaxy: col_count += 1
    for y in range(min_y + 1, max_y):
      if y in rows_without_galaxy: row_count += 1

    delta_x = max_x - min_x + (col_count * (expansion_factor - 1))
    delta_y = max_y - min_y + (row_count * (expansion_factor - 1))
    distance = delta_x + delta_y
    shortest_paths.append(distance)
  
  print(sum(shortest_paths))
  

def part_1(file_path):
  part_n(file_path, 2)


def part_2(file_path):
  part_n(file_path, 1_000_000)


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
