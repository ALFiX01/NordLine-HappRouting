import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/build_dat.py'


class BuildTests(unittest.TestCase):
    def test_wire_format_and_failed_build_preserves_outputs(self):
        self.assertTrue(SCRIPT.exists(), 'converter must exist')
        spec = importlib.util.spec_from_file_location('build_dat', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'txt').mkdir()
            (root / 'txt/geoip.txt').write_text('\ufeff[DIRECT]\n1.2.3.4/32\n', encoding='utf-8')
            (root / 'txt/geosite.txt').write_text('[TEST]\ndomain:example.com\n', encoding='utf-8')
            module.build(root)
            self.assertEqual((root / 'dat/geoip.dat').read_bytes(), bytes.fromhex('0a120a0644495245435412080a04010203041020'))
            self.assertEqual((root / 'dat/geosite.dat').read_bytes(), bytes.fromhex('0a170a0454455354120f0802120b6578616d706c652e636f6d'))
            before = {p.name: p.read_bytes() for p in (root / 'dat').glob('*.dat')}
            (root / 'txt/geoip.txt').write_text('[DIRECT]\n8.8.8.8\n')
            (root / 'txt/geosite.txt').write_text('[TEST]\nunsupported:example.com\n')
            with self.assertRaises(ValueError):
                module.build(root)
            self.assertEqual(before, {p.name: p.read_bytes() for p in (root / 'dat').glob('*.dat')})


if __name__ == '__main__':
    unittest.main()
