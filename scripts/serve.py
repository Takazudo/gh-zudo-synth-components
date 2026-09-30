#!/usr/bin/env python3
"""Serve the prebuilt read-only corpus on loopback. No installation required."""
import argparse, functools, http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",type=int,default=8765)
    args=parser.parse_args()
    directory=ROOT/"doc/dist"
    if not (directory/"index.html").is_file():
        parser.error("Prebuilt doc/dist is missing. Run pnpm build first.")
    if not 1024<=args.port<=65535:parser.error("Choose a port between 1024 and 65535")
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(directory))
    with http.server.ThreadingHTTPServer(("127.0.0.1",args.port),handler) as server:
        print(f"Open http://127.0.0.1:{args.port}/docs/project/")
        print("Bound to this computer only. Stop with Ctrl-C.")
        try:server.serve_forever()
        except KeyboardInterrupt:pass
if __name__=="__main__":main()
