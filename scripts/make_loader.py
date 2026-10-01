"""Generate an external-source GH loader and print its ready-to-copy code."""
import argparse
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys


def validate_rhino_path(path):
    if path is not None and not (PurePosixPath(str(path)).is_absolute()
                                or PureWindowsPath(str(path)).is_absolute()):
        raise ValueError('Explicit Rhino source must be an absolute path on the Rhino host.')


def make_loader(source, rhino_source=None):
    source = Path(source).expanduser().resolve(strict=True)
    if not source.is_file() or source.suffix.lower() != '.py':
        raise ValueError('Source must be an existing Python file.')
    validate_rhino_path(rhino_source)
    target = str(source) if rhino_source is None else str(rhino_source)
    if not target.strip():
        raise ValueError('Rhino source path cannot be empty.')
    return (f'SOURCE_PATH = {target!r}\n'
            'with open(SOURCE_PATH, "r", encoding="utf-8") as source_file:\n'
            '    source = source_file.read()\n'
            'exec(compile(source, SOURCE_PATH, "exec"), globals(), globals())\n')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--rhino-source', help='Path visible to Rhino when hosts differ; not verified locally')
    args = parser.parse_args()
    source = args.source.expanduser().resolve(strict=True)
    code = make_loader(source, rhino_source=args.rhino_source)
    output = (args.output or source.with_name(source.stem + '_loader.py')).expanduser().resolve()
    if output == source:
        raise ValueError('The loader must not overwrite its implementation source.')
    if output.exists() and output.read_text(encoding='utf-8') != code:
        raise FileExistsError('Output already contains different code; choose the intended loader path explicitly.')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(code, encoding='utf-8')
    print(code, end='')
    print(f'Loader file: {output}', file=sys.stderr)
    if args.rhino_source:
        print('Rhino-side path is explicit but unverified; confirm it reads the same current source.', file=sys.stderr)


if __name__ == '__main__':
    main()
