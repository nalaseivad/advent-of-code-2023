import sys
import pprint
import heapq


debug_level = 1

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


def update_grid_with_path(grid, path, end_key):
  key = end_key
  r, c, _ = key
  while (r, c) != (0, 0):
    prev_key = path[key]
    prev_r, prev_c, _ = prev_key
    if prev_r == r and prev_c < c:
      marker = '>'
    elif prev_r == r and prev_c > c:
      marker = '<'
    elif prev_r < r and prev_c == c:
      marker = 'v'
    elif prev_r > r and prev_c == c:
      marker = '^'
    else:
      marker = '?'
    grid[r][c] = marker
    key = prev_key
    r, c = prev_r, prev_c


def get_next_cells_n(grid, start_r, start_c, state, extra_tests_fn):
  in_dir, straight_count = state
  num_rows = len(grid)
  num_cols = len(grid[0])
  next_cells = []
  for new_dir, (dr, dc) in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]):
    new_r, new_c = start_r + dr, start_c + dc
    new_straight_count = (1 if new_dir != in_dir else straight_count + 1)
    new_state = (new_dir, new_straight_count)
    if (new_dir + 2) % 4 == in_dir:
      continue
    if new_r < 0 or new_r >= num_rows or new_c < 0 or new_c >= num_cols:
      continue
    if extra_tests_fn(state, new_state):
      continue
    next_cells.append((new_r, new_c, (new_dir, new_straight_count)))
  return next_cells


def extra_tests_1(state, new_state):
  _, new_straight_count = new_state
  return new_straight_count > 3


def get_next_cells_1(grid, start_r, start_c, state):
  return get_next_cells_n(grid, start_r, start_c, state, extra_tests_1)


def extra_tests_2(state, new_state):
  in_dir, straight_count = state
  new_dir, new_straight_count = new_state
  if new_dir != in_dir and straight_count < 4:
    return True
  if new_straight_count > 10:
    return True


def get_next_cells_2(grid, start_r, start_c, state):
  return get_next_cells_n(grid, start_r, start_c, state, extra_tests_2)


def modified_dijkstra(grid, start_r, start_c, initial_state, get_next_cells_fn):
  distances = {}
  path = {}
  key = (start_r, start_c, initial_state)
  path[(start_r, start_c)] = (0, -1)
  distances[key] = 0
  min_heap = [(0, *key)]

  while len(min_heap) > 0:
    min_distance, min_r, min_c, state = heapq.heappop(min_heap)
    for new_r, new_c, new_state in get_next_cells_fn(grid, min_r, min_c, state):
      cell_value = int(grid[new_r][new_c])
      distance = min_distance + cell_value
      key = (new_r, new_c, new_state)
      if key not in distances: distances[key] = float('inf')
      if distance < distances[key]:
        distances[key] = distance
        path[key] = (min_r, min_c, state)
        heapq.heappush(min_heap, (distance, *key))
  return distances, path


def part_n(file_path, initial_state, get_next_cells_fn, calc_answer_fn):
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    grid = [[c for c in row] for row in rows]

    debug_print_grid(grid)

    distances, path = modified_dijkstra(grid, 0, 0, initial_state, get_next_cells_fn)
    answer, end_key = calc_answer_fn(grid, distances)

    if debug(): update_grid_with_path(grid, path, end_key)
    debug_print('')
    debug_print_grid(grid)

    print(f'{answer=}')


def calc_answer_n(grid, distances, extra_tests_fn):
  num_rows, num_cols = len(grid), len(grid[0])
  answer = float('inf')
  end_key = None
  for k, v in distances.items():
    row, col, state = k
    if row == num_rows - 1 and col == num_cols - 1 and extra_tests_fn(state):
      if v < answer:
        end_key = k
      answer = min(answer, v)
  return (answer, end_key)


def calc_answer_1(grid, distances):
  return calc_answer_n(grid, distances, lambda state: True)


def part_1(file_path):
  part_n(file_path, (2, 0), get_next_cells_1, calc_answer_1)
    

def calc_answer_2(grid, distances):
  return calc_answer_n(grid, distances, lambda state: state[1] >= 4)


def part_2(file_path):
  part_n(file_path, (2, 0), get_next_cells_2, calc_answer_2)


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
