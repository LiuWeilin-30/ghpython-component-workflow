"""Verify loader path quoting, shared globals and fresh disk reads; no Rhino needed."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from make_loader import make_loader


class LoaderTests(unittest.TestCase):
    def test_explicit_rhino_path_is_not_resolved_on_agent_host(self):
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/'component.py'
            source.write_text('Result = 1\n',encoding='utf-8')
            remote="Z:/shared/space ' 功能.py"
            code=make_loader(source,rhino_source=remote)
            namespace={}
            exec(code.split('\n',1)[0],namespace,namespace)
            self.assertEqual(namespace['SOURCE_PATH'],remote)
            with self.assertRaises(ValueError):make_loader(source,rhino_source='relative.py')

    def test_quoted_unicode_path_inputs_outputs_and_fresh_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "space ' \u529f\u80fd.py"
            source.write_text('Result = Data + 1\n', encoding='utf-8')
            code = make_loader(source)
            namespace = {'Data': 3}
            exec(compile(code, '<loader>', 'exec'), namespace, namespace)
            self.assertEqual(namespace['Result'], 4)
            source.write_text('Result = Data + 2\n', encoding='utf-8')
            exec(compile(code, '<loader>', 'exec'), namespace, namespace)
            self.assertEqual(namespace['Result'], 5)

    def test_cli_writes_the_same_copyable_code_and_protects_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'component.py'
            source.write_text('Result = 1\n', encoding='utf-8')
            script = Path(__file__).with_name('make_loader.py')
            command = [sys.executable, '-X', 'utf8', str(script), str(source)]
            run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(run.returncode, 0, run.stderr)
            loader = source.with_name('component_loader.py')
            self.assertEqual(loader.read_text(encoding='utf-8'), run.stdout)
            run = subprocess.run(command + ['--output', str(source)], capture_output=True,
                                 text=True, encoding='utf-8')
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(source.read_text(encoding='utf-8'), 'Result = 1\n')


if __name__ == '__main__':
    unittest.main()
