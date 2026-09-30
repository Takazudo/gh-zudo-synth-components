#!/usr/bin/env python3
"""Opt-in local source downloads. Never promote evidence or change reviewed records."""
from __future__ import annotations
import argparse, datetime, hashlib, ipaddress, json, socket, urllib.request, urllib.parse, urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAX_BYTES=30*1024*1024

def public_url(url: str) -> str:
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or not p.hostname or p.username or p.password or p.port not in (None,443):
        raise ValueError("Only public HTTPS source URLs without credentials are permitted")
    for answer in socket.getaddrinfo(p.hostname,443,type=socket.SOCK_STREAM):
        ip=ipaddress.ip_address(answer[4][0])
        if not ip.is_global:raise ValueError("Private/reserved network source refused")
    return url

class PublicRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        public_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id",action="append",default=[],help="Queue item ID (repeatable)")
    parser.add_argument("--apply",action="store_true",help="Actually download selected PDF leads; default lists only")
    args=parser.parse_args()
    queue=json.loads((ROOT/"corpus/acquisition-queue.json").read_text())
    selected=[r for r in queue if not args.id or r["id"] in args.id]
    if args.id and set(args.id)-{r["id"] for r in selected}:parser.error("Unknown queue ID")
    if args.apply and not args.id:parser.error("--apply requires explicit --id selections")
    out=ROOT/"sources/incoming";receipts=ROOT/"provenance/acquisitions"
    opener=urllib.request.build_opener(PublicRedirect())
    failed=0
    for item in selected:
        print(item["id"],item["expected_kind"],item.get("url") or "exact source not identified")
        if not args.apply:continue
        if item["expected_kind"]!="pdf" or not item.get("url"):
            print("MANUAL REVIEW: not an established direct PDF source");failed+=1;continue
        when=datetime.datetime.now(datetime.timezone.utc).isoformat()
        receipt={"queue_id":item["id"],"requested_url":item["url"],"attempted_at":when,
                 "status":"FAILED","evidence_promotion":"NOT PERFORMED"}
        try:
            req=urllib.request.Request(public_url(item["url"]),headers={"User-Agent":"ModularComponentCorpus/0.1 source-review"})
            with opener.open(req,timeout=25) as response:
                final=public_url(response.url);data=response.read(MAX_BYTES+1)
                if len(data)>MAX_BYTES:raise ValueError("Source exceeds 30 MiB")
                if not data.lstrip().startswith(b"%PDF-"):raise ValueError("Response is not PDF bytes")
                sha=hashlib.sha256(data).hexdigest()
                out.mkdir(parents=True,exist_ok=True)
                path=out/(sha+".pdf")
                if path.exists() and path.read_bytes()!=data:raise ValueError("Hash-address collision")
                if not path.exists():path.write_bytes(data)
                receipt.update(status="RETAINED_UNREVIEWED",final_url=final,sha256=sha,bytes=len(data),
                    path=str(path.relative_to(ROOT)),content_type=response.headers.get("Content-Type"))
                print("RETAINED_UNREVIEWED",path.relative_to(ROOT))
        except Exception as exc:
            receipt["error"]=f"{type(exc).__name__}: {exc}";failed+=1;print(receipt["error"])
        receipts.mkdir(parents=True,exist_ok=True)
        slug=item["id"].replace("/","-")
        stamp=when.replace(":","").replace("+","_")
        (receipts/(slug+"--"+stamp+".json")).write_text(json.dumps(receipt,indent=2)+"\n")
    return 1 if failed else 0
if __name__=="__main__":raise SystemExit(main())
