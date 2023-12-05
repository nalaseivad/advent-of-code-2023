import sys
import re
import pprint
from collections import deque


debug = 0

def debug_print(s):
  if debug:
    print(s)


def debug_pretty_print(x):
  if debug:
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(x)


maps = {}


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
# Partition a list into a list of sublists of a certain size.  The last list may be incomplete.
# Examples
#   partition([1, 2, 3, 4, 5, 6, 7], 2) -> [[1, 2], [3, 4], [5, 6], [7]]
#
def partition(iterable, bucket_size):
  return partition_impl(iterable, bucket_size, bucket_size)


#
# Partition a list into a list of sublists of a certain size with a specific offset.  The last list may be incomplete.
# Examples
#   partition([1, 2, 3, 4, 5, 6], 3, 2) -> [[1, 2, 3], [3, 4, 5], [5, 6]]
#
#def partition(iterable, bucket_size, offset):
#  return partition_impl(iterable, bucket_size, offset)


def split_list(iterable, separator_fn):
  list = []
  for item in iterable:
    if separator_fn(item):
      yield list
      list.clear()
      continue
    list.append(item)
  yield list


def a_to_b(a, b, x):
  debug_print(f'{a}-to-{b}')
  ranges = maps[f'{a}-to-{b}']['ranges']
  debug_print(f'x: {x}')
  for range in ranges:
    source_start = range['source_start']
    source_end = range['source_end']
    dest_start = range['dest_start']
    debug_print(f'source_start: {source_start}, source_end: {source_end}, dest_start: {dest_start}')
    if x >= source_start and x < source_end:
      ret = dest_start + (x - source_start)
      slop = source_end - x
      debug_print(f'in range, ret: {ret}, slop: {slop}')
      return ret, slop
  ret = x
  slop = 1_000_000_000_000
  debug_print(f'not in range, ret: {ret}, slop: {slop}')
  return ret, slop


def process_block(block):
  block_iter = iter(block)
  first = next(block_iter)
  map_name, _ = first.split(' ')
  source_name, dest_name = map_name.split('-to-')
  ranges = []
  
  for elem in block_iter:
    dest_start, source_start, length = list(map(lambda x: int(x), elem.split(' ')))
    source_end = source_start + length
    range = {
      'source_start' : source_start,
      'source_end' : source_end,
      'dest_start' : dest_start
    }
    ranges.append(range)

  ranges = sorted(ranges, key = lambda x: x['source_start'])
  maps[map_name] = { 'source_name' : source_name, 'dest_name' : dest_name, 'ranges' : ranges }


def part_1(file_path):
  with open(file_path, 'r') as lines:
    line = next(lines).rstrip('\n')
    parts = re.split(r':\s*', line)
    seeds = list(map(lambda seed: int(seed), re.split(r'\s+', parts[1])))
    _ = next(lines)

    stripped_lines = (line.rstrip('\n') for line in lines)
    for block in split_list(stripped_lines, lambda line: re.match(r'^\s*$', line)):
      process_block(block)

    debug_pretty_print(maps)

    things = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
    locations = []
    for seed in seeds:
      x = seed
      for n in range(len(things) - 1):
        x, _ = a_to_b(things[n], things[n + 1], x)  
      locations.append(x)

    print(min(locations))


def generate_seeds_iterator(start_len_list):
  for start, len in start_len_list:
    for n in range(start, start + len):
      yield n


def part_2(file_path):
  with open(file_path, 'r') as lines:
    line = next(lines).rstrip('\n')
    parts = re.split(r':\s*', line)
    seeds = list(map(lambda seed: int(seed), re.split(r'\s+', parts[1])))
    _ = next(lines)

    stripped_lines = (line.rstrip('\n') for line in lines)
    for block in split_list(stripped_lines, lambda line: re.match(r'^\s*$', line)):
      process_block(block)

    debug_pretty_print(maps)

    things = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
    min_location = -1
    for seed_start, length in partition(seeds, 2):
      seed_end = seed_start + length
      seed = seed_start
      while seed < seed_end:
        debug_print(f'\nseed: {seed}')
        x = seed
        min_slop = -1
        for n in range(len(things) - 1):
          x, slop = a_to_b(things[n], things[n + 1], x)
          if min_slop == -1:
            min_slop = x
          min_slop = min(min_slop, slop)
        
        location = x
        debug_print(f'location: {location}, min_slop: {min_slop}')
        if min_location == -1:
          min_location = location
        min_location = min(min_location, location)

        seed += min_slop

    print(min_location)


if len(sys.argv) != 3:
  print("Usage: python3 day5.py <part> <file_path>")
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
