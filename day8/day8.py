import sys
import re
import pprint
from functools import cmp_to_key
from math import lcm


debug_level = 1

def debug_print(s, level):
  if level <= debug_level:
    print(s)

#
# Print a more readable version of our maps
#
def debug_pretty_print(x, level):
  if level <= debug_level:
    pp = pprint.PrettyPrinter(indent = 4)
    pp.pprint(x)


#
# Parse each line, build up the network and return the path, network and the names of all the xxA nodes (for part 2)
#
def init(file_path):
  with open(file_path, 'r') as lines:
    network = {}
    a_nodes = []
    lines = (line.rstrip('\n') for line in lines)
    path = next(lines)
    _ = next(lines)
    pattern = r'^([0-9A-Z]{3})\s+=\s+\(([0-9A-Z]{3}),\s+([0-9A-Z]{3})\)$'
    for line in lines:
      result = re.search(pattern, line)
      if result:
        node_name, left, right = result.groups() 
        network[node_name] = { 'L' : left, 'R' : right}
        if node_name[2] == 'A': a_nodes.append(node_name)

    debug_pretty_print(path, 2)
    debug_pretty_print(network, 2)
    debug_print(f'Node names ending in A: {a_nodes}', 2)
    return (path, network, a_nodes)


#
# Follow the path around the network from a given start node until we reach an end condition.
# Return the length of the path and then end node name.
#
def follow_path(network, path, start_node_name, is_end_node_fn):
  node_name = start_node_name
  node = network[node_name]
  debug_print(f'start_node_name: {start_node_name}', 2)
  done = False
  count = 0
  while not done:
    for c in path:
      count += 1
      node_name = node[c]
      node = network[node_name]
      debug_print(f'Step: {c} -> {node_name} : {node}', 3)
      if is_end_node_fn(node_name):
        end_node_name = node_name
        debug_print(f'({count}) end_node: {node_name} : {node}', 2)
        done = True
        break
  return count, end_node_name


def part_1(file_path):
  path, network, _ = init(file_path)
  is_end_fn = lambda node_name: node_name == 'ZZZ'
  path_length, _ = follow_path(network, path, 'AAA', is_end_fn)
  print(path_length)


def part_2(file_path):
  path, network, a_nodes = init(file_path)

  # For each node that ends with 'A' follow the path until we reach a node that ends with 'Z'
  is_end_fn = lambda node_name: node_name[2] == 'Z'
  paths = {node : follow_path(network, path, node, is_end_fn) for node in a_nodes}

  # For each node ending in 'Z' that we reached, follow the path again until we reach another node that ends with 'Z'
  # and add that info to our existing paths object
  for k, v in paths.items():
    info = follow_path(network, path, v[1], is_end_fn)
    paths[k] = ( v[0], { v[1] : info } )

  # Now paths object contains the cycle length to get from xxA to xxZ and then around again to xxZ
  debug_pretty_print(paths, 1)

  #
  # I notice that the path length to get from an xxA node to an zzZ node is the same as to get from the xxZ node back to
  # an xxZ node, and in fact the cycle from each xxZ node takes us back to the same xxZ node in all cases as well.
  # So, we have a number of cycles that we need to synchronize the end points of (the point when they get to an xxZ
  # node).  This is just the Lowest Common Multiple of all the cycle lengths.
  #
  lengths = [v[0] for _, v in paths.items()]
  print(lcm(*lengths))


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
