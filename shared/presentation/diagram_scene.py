"""Validate a diagram scene and compile it to editable inline SVG + Reveal fragments."""
from copy import deepcopy
import argparse
import html
import json
import math
from pathlib import Path
import re

KINDS = {'container', 'chip', 'memory', 'storage', 'callout', 'label'}
NODE_KEYS = {'id', 'kind', 'x', 'y', 'w', 'h', 'label', 'stroke', 'fill', 'color', 'fontSize', 'opacity'}
LINK_KEYS = {'id', 'from', 'to', 'stroke', 'opacity', 'label', 'labelOffset', 'dashed'}
DEFAULTS = {'stroke': '#a5a5a5', 'fill': '#111111', 'color': '#fafafa', 'fontSize': 28, 'opacity': 1}
IDENTIFIER = re.compile(r'[a-z][a-z0-9-]*\Z')
COLOR = re.compile(r'#[0-9a-fA-F]{6}\Z')


def number(value, name, low=None, high=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name}: expected a finite number')
    if (low is not None and value < low) or (high is not None and value > high):
        raise ValueError(f'{name}: outside allowed range')


def identifier(value, name):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError(f'{name}: use a lowercase identifier beginning with a letter')


def text(value, name, required=False):
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f'{name}: expected {"nonempty " if required else ""}text')


def validate_node(node, width, height):
    if set(node) - NODE_KEYS:
        raise ValueError(f'Unknown node fields: {set(node) - NODE_KEYS}')
    identifier(node['id'], 'node.id')
    if node['kind'] not in KINDS:
        raise ValueError(f'Unknown node kind: {node["kind"]}')
    for field in ['x', 'y', 'w', 'h', 'fontSize', 'opacity']:
        number(node[field], f'{node["id"]}.{field}', 0)
    if node['w'] < 24 or node['h'] < 24 or not 12 <= node['fontSize'] <= 64 or node['opacity'] > 1:
        raise ValueError(f'{node["id"]}: invalid dimensions, font size, or opacity')
    # Storage has a 6px rear outline; chip pins extend 7px beyond its frame.
    extension = 7 if node['kind'] == 'chip' else 6 if node['kind'] == 'storage' else 0
    if node['x'] < (7 if node['kind'] == 'chip' else 0) or node['y'] < (7 if node['kind'] == 'chip' else 0) or node['x'] + node['w'] + extension > width or node['y'] + node['h'] + extension > height:
        raise ValueError(f'{node["id"]}: node extends outside the viewBox')
    text(node['label'], f'{node["id"]}.label')
    for field in ['stroke', 'fill', 'color']:
        if not isinstance(node[field], str) or not COLOR.fullmatch(node[field]):
            raise ValueError(f'{node["id"]}.{field}: use #RRGGBB')


def validate_link(link, nodes):
    if set(link) - LINK_KEYS:
        raise ValueError(f'Unknown link fields: {set(link) - LINK_KEYS}')
    identifier(link['id'], 'link.id')
    for field in ['from', 'to']:
        port = link[field]
        if not isinstance(port, dict) or set(port) - {'node', 'side', 'at'}:
            raise ValueError(f'{link["id"]}.{field}: expected node, side, at')
        if port.get('node') not in nodes or port.get('side') not in {'left', 'right', 'top', 'bottom'}:
            raise ValueError(f'{link["id"]}.{field}: unknown node or side')
        number(port.get('at', 0.5), 'port.at', 0, 1)
    if not COLOR.fullmatch(link['stroke']):
        raise ValueError('Link stroke must be #RRGGBB')
    number(link['opacity'], 'link.opacity', 0, 1)
    number(link['labelOffset'], 'link.labelOffset')
    text(link['label'], 'link.label')
    if not isinstance(link['dashed'], bool):
        raise ValueError('link.dashed must be boolean')


def resolve_scene(scene):
    """Resolve sparse stage overrides to complete independent snapshots."""
    if set(scene) - {'id', 'title', 'description', 'width', 'height', 'duration', 'nodes', 'links', 'stages'}:
        raise ValueError('Unknown scene field')
    identifier(scene['id'], 'scene.id')
    text(scene['title'], 'scene.title', True)
    text(scene['description'], 'scene.description', True)
    width, height = scene.get('width', 1250), scene.get('height', 470)
    number(width, 'width', 100); number(height, 'height', 100)
    duration = scene.get('duration', 380)
    number(duration, 'duration', 0, 1500)
    if not isinstance(scene.get('nodes'), list) or not scene['nodes']:
        raise ValueError('Scene needs nodes')
    nodes = {}
    for raw in scene['nodes']:
        node = {**DEFAULTS, **raw}
        validate_node(node, width, height)
        if node['id'] in nodes:
            raise ValueError('Duplicate node ID')
        nodes[node['id']] = node
    links = {}
    for raw in scene.get('links', []):
        link = {'stroke': '#a5a5a5', 'opacity': 1, 'label': '', 'labelOffset': -18, 'dashed': False, **raw}
        validate_link(link, nodes)
        if link['id'] in links:
            raise ValueError('Duplicate link ID')
        links[link['id']] = link
    stages = scene.get('stages')
    if not isinstance(stages, list) or not stages:
        raise ValueError('Scene needs at least one stage')
    result = []; names = set()
    for stage in stages:
        if set(stage) - {'name', 'heading', 'emphasis', 'description', 'nodes', 'links'}:
            raise ValueError('Unknown stage field')
        identifier(stage['name'], 'stage.name')
        if stage['name'] in names:
            raise ValueError('Duplicate stage name')
        names.add(stage['name'])
        text(stage['heading'], 'stage.heading', True)
        text(stage.get('emphasis', ''), 'stage.emphasis')
        if stage.get('emphasis') and stage['emphasis'] not in stage['heading']:
            raise ValueError('Stage emphasis must be a substring of its heading')
        text(stage['description'], 'stage.description', True)
        for key, collection, allowed in [('nodes', nodes, NODE_KEYS - {'id', 'kind'}), ('links', links, LINK_KEYS - {'id'} )]:
            for item_id, changes in stage.get(key, {}).items():
                if item_id not in collection or set(changes) - allowed:
                    raise ValueError(f'{stage["name"]}: unknown {key} ID or override field')
                collection[item_id].update(deepcopy(changes))
        for node in nodes.values(): validate_node(node, width, height)
        for link in links.values(): validate_link(link, nodes)
        result.append({'name': stage['name'], 'heading': stage['heading'], 'emphasis': stage.get('emphasis', ''), 'description': stage['description'], 'nodes': deepcopy(nodes), 'links': deepcopy(links)})
    return {'id': scene['id'], 'title': scene['title'], 'description': scene['description'], 'width': width, 'height': height, 'duration': duration, 'stages': result}


def esc(value):
    return html.escape(str(value), quote=True)


def compile_scene(scene):
    """Markup stays stable across stages; runtime updates the same SVG objects."""
    config = resolve_scene(scene)
    prefix = config['id']; initial = config['stages'][0]
    defs = f'<pattern id="{prefix}-dots" width="7" height="7" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="1.2" height="2" fill="#747474"/></pattern><pattern id="{prefix}-red-dots" width="7" height="7" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="1.2" height="2" fill="#6b282c"/></pattern>'
    links = []
    for link in initial['links'].values():
        key = link['id']; marker = f'{prefix}-arrow-{key}'
        defs += f'<marker id="{marker}" viewBox="0 0 10 10" markerWidth="7" markerHeight="7" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path data-arrow="{key}" d="M0 0L10 5L0 10Z" fill="{esc(link["stroke"])}"/></marker>'
        def endpoint(port):
            n=initial['nodes'][port['node']]; at=port.get('at',0.5)
            return {'left':(n['x'],n['y']+n['h']*at),'right':(n['x']+n['w'],n['y']+n['h']*at),'top':(n['x']+n['w']*at,n['y']),'bottom':(n['x']+n['w']*at,n['y']+n['h'])}[port['side']]
        a,b=endpoint(link['from']),endpoint(link['to'])
        horizontal=link['from']['side'] in {'left','right'}; end_horizontal=link['to']['side'] in {'left','right'}
        if horizontal != end_horizontal:
            path=f'M{a[0]} {a[1]}H{b[0]}V{b[1]}' if horizontal else f'M{a[0]} {a[1]}V{b[1]}H{b[0]}'
        else:
            middle=(a[0]+b[0])/2 if horizontal else (a[1]+b[1])/2
            path=f'M{a[0]} {a[1]}H{middle}V{b[1]}H{b[0]}' if horizontal else f'M{a[0]} {a[1]}V{middle}H{b[0]}V{b[1]}'
        label_x=(a[0]+b[0])/2; label_y=(a[1]+b[1])/2+link['labelOffset']; dash='7 7' if link['dashed'] else 'none'
        links.append(f'<g data-link="{key}" opacity="{link["opacity"]}"><path data-part="line" d="{path}" fill="none" stroke="{link["stroke"]}" stroke-width="2" stroke-dasharray="{dash}" marker-end="url(#{marker})"/><text data-part="label" x="{label_x}" y="{label_y}" fill="{link["stroke"]}" text-anchor="middle" font-size="20">{esc(link["label"])}</text></g>')
    nodes = []
    for node in initial['nodes'].values():
        key = node['id']; kind = node['kind']
        x, y, w, h = (node[field] for field in ['x', 'y', 'w', 'h'])
        def rectangle(part, left, top, width, height, fill, opacity=1):
            return f'<rect data-part="{part}" x="{left}" y="{top}" width="{width}" height="{height}" fill="{fill}" stroke="{node["stroke"]}" stroke-width="1.5" opacity="{opacity}"/>'
        fill = f'url(#{prefix}-red-dots)' if kind == 'callout' else f'url(#{prefix}-dots)' if kind == 'storage' else node['fill']
        pieces = '' if kind == 'label' else rectangle('frame', x, y, w, h, fill)
        if kind == 'container': pieces += rectangle('detail', x+7, y+7, w-14, h-14, 'none', 0.4)
        if kind == 'storage': pieces += rectangle('detail', x+8, y+8, w-16, h-16, node['fill'])
        icon = ''
        if kind == 'storage':
            ix, iy = x+26, y+h/2-30
            icon = f'M{ix} {iy}h42v60h-42Z ' + ' '.join(f'M{ix+8} {iy+offset}h26' for offset in [12,24,36,48])
        if kind in {'chip', 'memory'}:
            for i in range(1, 7):
                px = x+w*i/7
                icon += f'M{px} {y+h}v7 '
                if kind == 'chip': icon += f'M{px} {y}v-7 '
            if kind == 'chip':
                for i in range(1, 5):
                    py = y+h*i/5
                    icon += f'M{x} {py}h-7 M{x+w} {py}h7 '
        if kind in {'chip', 'memory', 'storage'}: pieces += f'<path data-part="icon" d="{icon}" fill="none" stroke="{node["stroke"]}" stroke-width="1.5"/>'
        font = node['fontSize']
        tx = x+24 if kind == 'container' else x+w*0.60 if kind == 'storage' else x+w/2
        ty = y+42 if kind == 'container' else y+h/2+font*0.34
        lines = node['label'].split('\n')
        spans = ''.join(f'<tspan x="{tx}" y="{ty+(i-(len(lines)-1)/2)*font*1.3}">{esc(line)}</tspan>' for i,line in enumerate(lines))
        anchor = 'start' if kind == 'container' else 'middle'
        pieces += f'<text data-part="label" x="{tx}" y="{ty}" text-anchor="{anchor}" font-size="{font}" fill="{node["color"]}">{spans}</text>'
        nodes.append(f'<g data-node="{key}" data-kind="{kind}" opacity="{node["opacity"]}" aria-hidden="{str(node["opacity"]==0).lower()}">{pieces}</g>')
    metadata = esc(json.dumps(config, ensure_ascii=False, separators=(',', ':')))
    steps = ''.join(f'<span class="fragment custom ps-diagram-step" data-fragment-index="{i-1}" data-diagram-step="{i}" aria-hidden="true"></span>' for i in range(1, len(config['stages'])))
    heading = esc(initial['heading'])
    if initial['emphasis']:
        before, after = initial['heading'].split(initial['emphasis'], 1)
        heading = esc(before) + '<span class="accent">' + esc(initial['emphasis']) + '</span>' + esc(after)
    # Nodes precede links to keep paths visible; links attach to explicit outer ports.
    return f'<div class="ps-diagram" data-ps-scene="{prefix}" data-ps-state="0"><h2 data-ps-heading>{heading}</h2><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {config["width"]} {config["height"]}" role="img" aria-labelledby="{prefix}-title {prefix}-description"><title id="{prefix}-title">{esc(config["title"])}</title><desc id="{prefix}-description">{esc(initial["description"])}</desc><metadata data-ps-config="" aria-hidden="true" style="display:none">{metadata}</metadata><defs>{defs}</defs>{"".join(nodes)}{"".join(links)}</svg>{steps}<noscript>This animated diagram requires JavaScript.</noscript></div>'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = compile_scene(json.loads(args.source.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output)
    print(f'Compiled diagram: {args.output}')
