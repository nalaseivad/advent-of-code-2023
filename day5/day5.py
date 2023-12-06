import sys
import re
import pprint
from collections import deque


#
# This is chosen to be larger than any of the lengths of seed ranges in the input data. I do like that I can use '_' as
# a thousands separator in integer constants in Python.  Very nice.
#
LARGE_VALUE = 1_000_000_000_000


debug = 0

def debug_print(s):
  if debug:
    print(s)

#
# Print a more readable version of our maps
#
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
# Partition a list into an iterable of sublists of a certain size.  The last list may be incomplete.
# Examples
#   partition([1, 2, 3, 4, 5, 6, 7], 2) -> [[1, 2], [3, 4], [5, 6], [7]]
#
def partition(iterable, bucket_size):
  return partition_impl(iterable, bucket_size, bucket_size)


#
# Partition a list into an iterable of sublists of a certain size with a specific offset.  The last list may be
# incomplete.
# Examples
#   partition([1, 2, 3, 4, 5, 6], 3, 2) -> [[1, 2, 3], [3, 4, 5], [5, 6]]
#
#def partition(iterable, bucket_size, offset):
#  return partition_impl(iterable, bucket_size, offset)


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
# A generic function for mappings from 'a' to 'b'.
# Find the range that the input value is in and determine the mapped value.  Also calculate, and return, the amount of
# 'slop' there is in the range, i.e. the distance of the input value from the top end of the range that it's in.  If
# the input value is not in any of the ranges then consider 'slop' to be some arbitrary large value scaled to be larger
# than any of the lengths in the input data.
#
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
  slop = LARGE_VALUE
  debug_print(f'not in range, ret: {ret}, slop: {slop}')
  return ret, slop


#
# For part 2 I enhanced this to sort the ranges stored in the maps.  This would then ensure that I could easily test
# those ranges in increasing seed order in the a_to_b fn above.
#
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

  # Ensure that the ranges are sorted by starting value
  ranges = sorted(ranges, key = lambda x: x['source_start'])
  maps[map_name] = { 'source_name' : source_name, 'dest_name' : dest_name, 'ranges' : ranges }


def part_n(file_path, part_fn):
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
    print(part_fn(seeds, things))


def part_1_fn(seeds, things):
  min_location = -1
  for seed in seeds:
    debug_print(f'\nseed: {seed}')
    x = seed
    for n in range(len(things) - 1):
      x, _ = a_to_b(things[n], things[n + 1], x)

    location = x
    debug_print(f'location: {location}')
    if min_location == -1:
      min_location = location
    min_location = min(min_location, location)

  return min_location


def part_1(file_path):
  part_n(file_path, part_1_fn)


#
# Part 2 changed the interpretation of the initial list.  Whereas in part 1 the list was a list of actual seed values,
# in part 2 it's a list of seed ranges [[start, length], ...].  What's more the length values in the input data are huge
# and so the total number of seed values to process is now orders of magniture more.  I started with a naive strategy of
# generating all the seed values in turn and then going through all the map tables as in part1, but it immediately
# became clear that this was computationally a non-starter.  So we needed another approach.
#
# It occured to me that the vast majority of sequential seed values would end up taking the same path through the map
# tables, and so I wanted to calculate how much wiggle room (or 'slop' as I called it) there was for each seed's path
# through the maps.  The idea was that I could assume that any new seed values in the range of [prev_seed_value,
# prev_seed_value + prev_min_slop] would end up at the same final location, and so there was no need to generate those
# values and run them through all the maps.  Instead I could jump ahead and only test new seed values that were min_slop
# ahead of the previously tested seed value.  Here min_slop is the smallest amount of slop I saw in any of the ranges
# across all the map tables for the last seed value.
#
# This worked and I could very efficiently process all the seed ranges and find the minimum final location.
#
def part_2_fn(seeds, things):
  min_location = -1
  for seed_start, length in partition(seeds, 2):
    seed_end = seed_start + length
    seed = seed_start
    while seed < seed_end:
      debug_print(f'\nseed: {seed}')
      x = seed
      min_slop = -1   # The minimum amount of slop across all the map tables for this seed value
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

      seed += min_slop  # Jump ahead

  return min_location


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
