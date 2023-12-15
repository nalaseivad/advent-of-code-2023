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


#
# Split a list into an iterable of sublists based on a test of whether a given list element is a separator
# Examples
#   [1, 2, sep, 3, sep, sep, 4, 5, 6] -> [[1, 2], [3], [], [4, 5, 6]]
#
def split_list(iterable, separator_fn):
  list = []
  for item in iterable:
    if separator_fn(item):
      yield list
      list.clear()
      continue
    list.append(item)
  yield list


#
# num_cols = 8
# vv        test_col = 0, num_cols - test_col - 2 = 6, test_width = 0
# xxxxxxxx
# -vv-      test_col = 1, num_cols - test_col - 2 = 5, test_width = 1
# xxxxxxxx
# --vv--    test_col = 2, num_cols - test_col - 2 = 4, test_width = 2
# xxxxxxxx
# ---vv---  test_col = 3, num_cols - test_col - 2 = 3, test_width = 3
# xxxxxxxx
#   --vv--  test_col = 4, num_cols - test_col - 2 = 2, test_width = 2
# xxxxxxxx
#     -vv-  test_col = 5, num_cols - test_col - 2 = 1, test_width = 1
# xxxxxxxx
#       vv  test_col = 6, num_cols - test_col - 2 = 0, test_width = 0
# xxxxxxxx
#
def find_reflection_col(grid_rows, target_diff_count):
  num_rows = len(grid_rows)
  num_cols = len(grid_rows[0])
  for test_col in range(num_cols - 1):
    diff_count = 0
    test_width = min(test_col, num_cols - test_col - 2)
    for n in range(0, test_width + 1):
      for row_n in range(num_rows):
        l, r = test_col - n, test_col + n + 1
        lc, rc = grid_rows[row_n][l], grid_rows[row_n][r]
        if lc != rc:
          diff_count += 1
    if diff_count == target_diff_count:
      return test_col
  return -1


def part_n(file_path, target_diff_count):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    answer = 0
    for grid in split_list(lines, lambda line: len(line) == 0):
      grid_rows = [[c for c in line] for line in grid]
      grid_cols = [[c for c in col] for col in zip(*grid_rows)]
      col = find_reflection_col(grid_rows, target_diff_count)
      if col != -1: answer += (col + 1)
      row = find_reflection_col(grid_cols, target_diff_count)
      if row != -1: answer += 100 * (row + 1)
    print(answer)


def part_1(file_path):
  part_n(file_path, 0)


def part_2(file_path):
  part_n(file_path, 1)


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
