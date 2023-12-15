import sys
import pprint


debug_level = 1

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


def part_1(file_path):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    platform = [[c for c in row] for row in lines]
    platform_cols = [[c for c in col] for col in zip(*platform)]
    platform_height = len(platform)
    platform_width = len(platform[0])

    debug_print(f'platform_width = {platform_width}, platform_height = {platform_height}')
    for line in platform:
      debug_print(''.join(line))

    tilted_platform = []
    for col in platform_cols:
      tilted_col = []
      for row_n in range(platform_height):
        cell = col[row_n]
        tilted_col.append(cell)
        if cell in ('.', '#'): continue
        n = 0
        for n in range(row_n - 1, -2, -1):
          if tilted_col[n] in ('#', 'O'):
            break
        if n + 1 < row_n:
          tilted_col[n + 1] = cell
          tilted_col[row_n] = '.'
      tilted_platform.append(tilted_col)

    debug_print('')
    for line in zip(*tilted_platform):
      debug_print(''.join(line))

    answer = 0
    for row_n, row in enumerate(zip(*tilted_platform)):
      for cell in row:
        if cell == 'O':
          answer += platform_height - row_n
    print(answer)


def part_2(file_path):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
  print('to do')


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
