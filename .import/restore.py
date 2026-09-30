#!/usr/bin/env python3
"""One-time, hash-locked reconstruction of the delivered component corpus.

Transport is never executed. Copies are read from pinned public checkouts;
external assets must match the bytes already delivered to the owner.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import io
import json
import lzma
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import time
import urllib.request
import zipfile

PREFIX_SHA = '099fb11c1cf11aae8006b890944f1dce404f6acdeb64d2cf0b81e98852d14aa6'
RECOVERED_SHA = '8564462ee5b16ea4c9fb9ac55c39facaf4ff33d1aed24d518a62126915b00ce2'
COMPLETION_SHA = '2c0b0dbea569c2cb906d6fd3d3f8fdf8fcaffd44fb8e93d50d2f1b993ae19274'
MAX_DOWNLOAD = 32 * 1024 * 1024


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(root: Path, name: str) -> Path:
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name or '.git' in p.parts:
        raise ValueError(f'Unsafe source path: {name!r}')
    result = root.joinpath(*p.parts)
    result.resolve().relative_to(root.resolve())
    if any(parent.is_symlink() for parent in [result, *result.parents] if parent != root.parent):
        raise ValueError(f'Symlink not allowed: {name}')
    return result


def load_payload(transport: Path) -> tuple[dict, dict]:
    encoded = ''.join((transport / 'payload' / f'{i:02}.b64').read_text().strip() for i in range(15))
    if len(encoded) != 180000 or sha(encoded.encode()) != PREFIX_SHA:
        raise ValueError('The recovered first 15 transport chunks differ from the reviewed bytes')
    text = lzma.LZMADecompressor().decompress(base64.b64decode(encoded, validate=True)).decode('utf-8')
    decoder = json.JSONDecoder()
    pos = 1
    recovered = {}
    while pos < len(text):
        key, pos = decoder.raw_decode(text, pos)
        if text[pos] != ':':
            raise ValueError('Malformed recovered key')
        pos += 1
        if text[pos] == '[':
            pos += 1
            items = []
            while pos < len(text) and text[pos] != ']':
                try:
                    item, next_pos = decoder.raw_decode(text, pos)
                except json.JSONDecodeError:
                    break
                items.append(item)
                pos = next_pos
                if pos < len(text) and text[pos] == ',':
                    pos += 1
            recovered[key] = items
            if pos >= len(text) or text[pos] != ']':
                break
            pos += 1
        else:
            recovered[key], pos = decoder.raw_decode(text, pos)
        if pos < len(text) and text[pos] == ',':
            pos += 1
        else:
            break
    canonical = json.dumps(recovered, separators=(',', ':'), ensure_ascii=False).encode()
    if sha(canonical) != RECOVERED_SHA or len(recovered['copy']) != 628 or len(recovered['write']) != 75:
        raise ValueError('Recovered record count or canonical hash differs')
    completed = ''.join((transport / 'completion' / f'{i:02}.b64').read_text().strip() for i in range(6))
    raw = base64.b64decode(completed, validate=True)
    if sha(raw) != COMPLETION_SHA:
        raise ValueError('Completion transport hash mismatch')
    completion = json.loads(lzma.decompress(raw))
    return recovered, completion


def identities(first: dict, final: dict) -> list[str]:
    paths = [row['path'] for key in ('copy', 'write') for row in first[key]]
    paths += [row['path'] for key in ('write', 'download', 'derive') for row in final[key]]
    if len(paths) != len(set(paths)) or len(paths) != final['expected']['files']:
        raise ValueError('Duplicate or missing source paths')
    return sorted(paths)


def fetch_bytes(url: str, cache: Path) -> bytes:
    if not url.startswith('https://'):
        raise ValueError('Only HTTPS sources are permitted')
    path = cache / sha(url.encode())
    if path.exists():
        return path.read_bytes()
    errors = []
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'ComponentCorpusSourceRestore/1.0'})
            with urllib.request.urlopen(request, timeout=45) as response:
                if not response.url.startswith('https://'):
                    raise ValueError('Non-HTTPS redirect')
                data = response.read(MAX_DOWNLOAD + 1)
            if len(data) > MAX_DOWNLOAD:
                raise ValueError('Source exceeds bounded download limit')
            path.write_bytes(data)
            return data
        except Exception as error:
            errors.append(f'{type(error).__name__}: {error}')
            time.sleep(attempt + 1)
    raise RuntimeError(f'Cannot retrieve {url}: {errors}')


def restore(args, first: dict, final: dict) -> None:
    roots = {'instrument': args.instrument.resolve(), 'framework': args.framework.resolve()}
    for name, root in roots.items():
        actual = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != first['upstream'][name]:
            raise ValueError(f'{name} is not the pinned source commit')
    for item in first['copy']:
        source = safe_path(roots[item['source']], item['source_path'])
        dest = safe_path(args.target, item['path'])
        if not source.is_file():
            raise FileNotFoundError(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    for item in first['write'] + final['write']:
        dest = safe_path(args.target, item['path'])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(item['content'].encode('utf-8'))
    args.cache.mkdir(parents=True, exist_ok=True)
    for item in final['download']:
        raw = fetch_bytes(item['url'], args.cache)
        if 'archive_member_basename' in item:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                # Vendors may rename a readme or duplicate it in several folders.
                # Select exact retained bytes, never a guessed filename alone.
                matches = []
                for info in archive.infolist():
                    if info.is_dir() or info.file_size != item['size']:
                        continue
                    if info.file_size > MAX_DOWNLOAD:
                        raise ValueError('Oversized archive member')
                    candidate = archive.read(info)
                    if sha(candidate) == item['sha256']:
                        matches.append((info.filename, candidate))
                if not matches:
                    raise ValueError(f"No exact retained member for {item['path']}; names={archive.namelist()}")
                data = matches[0][1]
                print('ARCHIVE MEMBER', matches[0][0], '->', item['path'], flush=True)
        else:
            data = raw
        if len(data) != item['size'] or sha(data) != item['sha256']:
            raise ValueError(f"Exact source bytes mismatch: {item['path']} (got {len(data)} / {sha(data)})")
        dest = safe_path(args.target, item['path'])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print('RESTORED', item['path'], sha(data), flush=True)
    print('628 pinned copies, 146 authored/restored text files, and 21 exact downloaded assets restored.')
    print('Three derived meshes must be regenerated and verified before committing.')


def verify(args, first: dict, final: dict) -> None:
    for item in final['derive']:
        file = safe_path(args.target, item['path'])
        if sha(file.read_bytes()) != item['sha256']:
            raise ValueError(f"Re-derived mesh differs from delivered model: {item['path']}")
    # The derivation script writes a new receipt. Keep the reviewed original
    # receipt only after proving all derived mesh bytes match it exactly.
    receipt = next(i for i in final['write'] if i['path'] == 'provenance/step-derivation.json')
    safe_path(args.target, receipt['path']).write_bytes(receipt['content'].encode())
    manifest = []
    for name in identities(first, final):
        file = safe_path(args.target, name)
        manifest.append({'path': name, 'sha256': sha(file.read_bytes()), 'size_bytes': file.stat().st_size})
    digest = sha(''.join(f"{r['path']}\0{r['sha256']}\n" for r in manifest).encode())
    if digest != final['expected']['source_tree_sha256']:
        raise ValueError(f'Source baseline mismatch: {digest}')
    provenance = args.target / 'provenance/repository-import.json'
    provenance.write_text(json.dumps({
        'schema_version': 1,
        'destination': 'Takazudo/gh-zudo-synth-components',
        'delivery_archive': 'zudo-modular-component-corpus-v0.1.0.zip',
        'delivery_archive_sha256': final['expected']['input_zip_sha256'],
        'upstream': first['upstream'],
        'restored_source_file_count': len(manifest),
        'restored_source_tree_sha256': digest,
        'hash_rule': final['expected']['source_manifest_rule'],
        'method': 'Pinned upstream copies plus hash-locked authored overlay, exact source recovery and deterministic STEP tessellation',
        'package_only_not_imported': final['package_only'],
        'generated_output': 'Rebuilt through package-pinned circuit-doc and corpus generators; build output and dependencies not source-controlled',
        'physical_fit_and_electrical_tests': 'NOT RUN',
        'source_manifest': manifest,
    }, indent=2) + '\n')
    print('PASS: 798 restored source files match the delivered corpus source-tree hash:', digest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['inspect', 'restore', 'verify'])
    parser.add_argument('--transport', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--instrument', type=Path)
    parser.add_argument('--framework', type=Path)
    parser.add_argument('--cache', type=Path)
    args = parser.parse_args()
    first, final = load_payload(args.transport)
    identities(first, final)
    if args.action == 'inspect':
        print(json.dumps({'copy': len(first['copy']), 'write': len(first['write']) + len(final['write']),
                          'download': len(final['download']), 'derive': len(final['derive']), 'expected': final['expected']}, indent=2))
    elif args.action == 'restore':
        if not all((args.instrument, args.framework, args.cache)):
            parser.error('restore requires --instrument, --framework, --cache')
        restore(args, first, final)
    else:
        verify(args, first, final)

if __name__ == '__main__':
    main()
