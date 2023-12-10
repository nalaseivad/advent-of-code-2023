import sys
import re
import pprint
from collections import deque


debug_level = 0

def debug_print(s, level = 1):
  if level <= debug_level:
    print(s)

#
# Print a more readable version of our maps
#
def debug_pretty_print(x, level = 1):
  if level <= debug_level:
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


def augment_numbers_lists_2(numbers_lists):
  prev_first_number = 0
  for numbers in reversed(numbers_lists):
    first_number = numbers[0]
    new_first_number = first_number - prev_first_number
    numbers.insert(0, new_first_number)
    prev_first_number = new_first_number
  debug_print(f'augmented numbers_lists: {numbers_lists}')
  return numbers_lists


def augment_numbers_lists_1(numbers_lists):
  prev_last_number = 0
  for numbers in reversed(numbers_lists):
    last_number = numbers[-1]
    new_last_number = last_number + prev_last_number
    numbers.append(new_last_number)
    prev_last_number = new_last_number
  debug_print(f'augmented numbers_lists: {numbers_lists}')
  return numbers_lists


def process_numbers(numbers, augment_numbers_lists_fn):
  numbers_lists = [numbers]

  while True:
    pairs = list(filter(lambda pair: len(pair) == 2, partition(numbers, 2, 1)))
    diffs = list(map(lambda pair: pair[1] - pair[0], pairs))
    debug_print(f'diffs: {diffs}')
    numbers_lists.append(diffs)
    if all(map(lambda x: x == 0, diffs)):
      debug_print(f'numbers_lists: {numbers_lists}')
      break
    numbers = diffs

  return augment_numbers_lists_fn(numbers_lists)


def parse_line(line, augment_numbers_lists_fn):
  number_strings = re.split(r'\s+', line)
  numbers = list(map(int, number_strings))
  debug_print(f'\nnumbers: {numbers}')
  return process_numbers(numbers, augment_numbers_lists_fn)


def part_n(file_path, augment_numbers_lists_fn, selector_fn):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    numbers = []
    for line in lines:
      numbers_lists = parse_line(line, augment_numbers_lists_fn)
      number = selector_fn(numbers_lists)
      numbers.append(number)
      debug_print(number)
    print(sum(numbers))


def part_1(file_path):
  part_n(file_path, augment_numbers_lists_1, lambda numbers_lists: numbers_lists[0][-1])

    
def part_2(file_path):
  part_n(file_path, augment_numbers_lists_2, lambda numbers_lists: numbers_lists[0][0])


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
