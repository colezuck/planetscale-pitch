"""Meaningful compiler boundaries: geometry, evidence text, namespaces, and state isolation."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('diagram_scene', ROOT / 'diagram_scene.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


class SceneTests(unittest.TestCase):
    def setUp(self):
        self.scene = json.loads((ROOT / 'examples/capacity-model.json').read_text())

    def test_states_are_independent_and_resolution_does_not_mutate_author_source(self):
        original = deepcopy(self.scene); config = module.resolve_scene(self.scene)
        self.assertEqual(config['stages'][0]['nodes']['cpu']['w'], 145)
        self.assertEqual(config['stages'][1]['nodes']['cpu']['w'], 182)
        config['stages'][1]['nodes']['cpu']['w'] = 999
        self.assertEqual(config['stages'][2]['nodes']['cpu']['w'], 182)
        self.assertEqual(self.scene, original)

    def test_missing_connection_target_and_typo_are_rejected(self):
        self.scene['links'][0]['to']['node'] = 'missing'
        with self.assertRaises(ValueError): module.resolve_scene(self.scene)
        self.setUp(); self.scene['stages'][1]['nodes']['cpu']['width'] = 200
        with self.assertRaises(ValueError): module.resolve_scene(self.scene)

    def test_nonfinite_geometry_and_out_of_bounds_growth_are_rejected(self):
        self.scene['nodes'][0]['x'] = float('nan')
        with self.assertRaises(ValueError): module.resolve_scene(self.scene)
        self.setUp(); self.scene['stages'][1]['nodes']['cpu']['w'] = 2000
        with self.assertRaises(ValueError): module.resolve_scene(self.scene)

    def test_compiled_svg_has_visible_initial_geometry_and_safe_metadata(self):
        self.scene['nodes'][1]['label'] = 'CPU <fast> & reliable'
        markup = module.compile_scene(self.scene)
        svg = ET.fromstring(markup[markup.index('<svg'):markup.index('</svg>') + 6])
        cpu = next(e for e in svg.iter() if e.get('data-node') == 'cpu')
        frame = next(e for e in cpu if e.get('data-part') == 'frame')
        self.assertEqual(float(frame.get('width')), 145)
        self.assertIn('CPU <fast> & reliable', ''.join(cpu.itertext()))
        metadata = next(e for e in svg if e.tag.endswith('metadata'))
        self.assertEqual(json.loads(metadata.text)['id'], 'capacity-model')
        ids = [e.get('id') for e in svg.iter() if e.get('id')]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(i.startswith('capacity-model-') for i in ids))


if __name__ == '__main__': unittest.main()
