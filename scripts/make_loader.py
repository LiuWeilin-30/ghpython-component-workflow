"""Generate an external-source GH loader and print its ready-to-copy code."""
import argparse
from pathlib import Path
import sys


def make_loader(source):
    source = Path(source).expanduser().resolve(strict=True)
    if not source.is_file() or source.suffix.lower() != '.py':
        raise ValueError('Source must be an existing Python file.')
    return (f'SOURCE_PATH = {str(source)!r}\n'
            'with open(SOURCE_PATH, "r", encoding="utf-8") as source_file:\n'
            '    source = source_file.read()\n'
            'exec(compile(source, SOURCE_PATH, "exec"), globals(), globals())\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    source = args.source.expanduser().resolve(strict=True)
    code = make_loader(source)
    output = (args.output or source.with_name(source.stem + '_loader.py')).expanduser().resolve()
    if output == source:
        raise ValueError('The loader must not overwrite its implementation source.')
    if output.exists() and output.read_text(encoding='utf-8') != code:
        raise FileExistsError('Output already contains different code; choose the intended loader path explicitly.')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(code, encoding='utf-8')
    print(code, end='')
    print(f'Loader file: {output}', file=sys.stderr)


if __name__ == '__main__':
    main()
