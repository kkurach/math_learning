#!/usr/bin/python

import os
import re
import sys
import igraph
import pygraphviz as pgv

PLOTS_DIR = 'results/plots'
NUM_VERT = 0
G = None

def Parse(s):
  # pylint: disable=W0602
  global G, NUM_VERT
  v_id = NUM_VERT
  NUM_VERT += 1
  G[v_id] = {}
  if s in ['None', 'A', 'B', '\'A\'', '\'B\'']:
    G[v_id]['child'] = []
    G[v_id]['op'] = s
    return v_id

  tokens = []
  opened = 1  
  assert s[0] == '('
  tok = ""
  for i in xrange(1, len(s)):
    if s[i] == ',' and opened == 1:
      tokens.append(tok)
      tok = ""
      continue

    if s[i] == '(':
      opened += 1
    elif s[i] == ')':
      opened -= 1

    if s[i] != ' ' or (i+1 < len(s) and s[i+1] in ('1', '2')):
      tok += s[i]
  
  tokens.append(tok[:-1])
  assert opened == 0
  assert len(tokens) in (2, 3)
  #assert tokens[0].isdigit()

  G[v_id]['op'] = tokens[0]
  G[v_id]['child'] = [] 
  for i in xrange(1, len(tokens)):
    son = Parse(tokens[i])
    G[v_id]['child'].append(son)

  return v_id

op_to_color = {
  "None": 'black',
  "A": 'black',
  "\'A\'": 'black',
  "B": 'black',
  "\'B\'": 'black',
  "'\\\\sum_0'": 'green',
  "'\\\\sum_1'": 'red',
  "'^T'": 'violet',
  "'*'": 'blue',
  "'.*'": 'yellow'}

def BuildIgraph(filename):
  g = igraph.Graph(directed=True)
  g.add_vertices(len(G))
  labels = []
  colors = []
  for v_id in sorted(G.keys()):
    op = G[v_id]['op']
    labels.append(op)
    assert op in op_to_color, "Missing color for op %s. Please add." % op
    colors.append(op_to_color[op])
    for child in G[v_id]['child']:
      g.add_edge(v_id, child)
  g.vs["label"] = labels
  g.vs["color"] = colors

  print 'Writing file: %s' % filename
  layout = g.layout("circle")
  igraph.plot(g, target=filename, layout=layout)

def BuildGraphvizDot(filename, rankdir):
  g = pgv.AGraph(rankdir=rankdir, directed=True)
  
  op_to_shape = {
    'None': 'circle',
    '\'A\'': 'circle',
    'A': 'circle',
    '\'B\'': 'circle',
    'B': 'circle',
    "'\\\\sum_0'": 'polygon',
    "'\\\\sum_1'": 'box',
    "'^T'": 'diamond',
    "'*'": 'circle',
    "'.*'": 'triangle'}
  
  for i in xrange(len(G)):
    op = G[i]['op']
    g.add_node(
        i, label=op.strip("'"), shape=op_to_shape[op], color=op_to_color[op])

  for v_id in sorted(G.keys()):
    for child in G[v_id]['child']:
      g.add_edge(v_id, child, dir='back')
  g.layout(prog='dot')
  g.draw(filename)

def ProcessLine(line_num, line, tree_dir):
  global G, NUM_VERT
  print "Expression %d: %s" % (line_num, line)
  G = {}
  NUM_VERT = 0

  line_parts = line.split('@@@@@')
  for line_part in line_parts:
    Parse(line_part.strip())

  vert_filename = tree_dir + 'vertical_%d.png' % line_num
  horiz_filename = tree_dir + 'horizontal_%d.png' % line_num
  BuildGraphvizDot(vert_filename, rankdir='TD')
  BuildGraphvizDot(horiz_filename, rankdir='LR')

def main():
  if len(sys.argv) != 2 or not sys.argv[1].endswith(".tree"):
    print 'Usage: %s <path_to_tree_file>' % sys.argv[0]
    sys.exit(1)
  
  tree_file = sys.argv[1]
  with open(tree_file, 'r') as f:
    tree_basename = tree_file.split('/')[-1]
    tree_dir = os.path.join(PLOTS_DIR, re.sub(r'.tree$', '', tree_basename))
    if not os.path.isdir(tree_dir):
      os.makedirs(tree_dir)

    for i, line in enumerate(f):
      ProcessLine(i, line, tree_dir)

if __name__ == '__main__':
  main()
