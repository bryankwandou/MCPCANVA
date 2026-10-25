"""Benchmark: one page with 8 same-style texts, fresh boxes (CANVA_STYLE_REUSE=0) vs copying a styled box.
usage: CANVA_CDP_PORT=9223 python bench_style_reuse.py"""
import json, os, subprocess, sys, time

if len(sys.argv) > 1:  # child: one build in the mode given by the environment
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
    from creative_mcp import canva_native as cn
    els = [{"type": "text", "text": f"Baris uji nomor {i + 1}", "font": "Inter", "size": 40, "color": "#15161A",
            "x": 110, "y": 80 + i * 110, "w": 1200} for i in range(8)]
    t = time.time()
    r = cn.build({"title": f"bench {sys.argv[1]}", "width": 1920, "height": 1080, "elements": els})
    print(json.dumps({"mode": sys.argv[1], "detik": round(time.time() - t), "ok": r["ok"], "added": len(r["added"]),
                      "errors": r["errors"]}, ensure_ascii=False))
else:
    for mode in ("0", "1"):
        env = dict(os.environ, CANVA_STYLE_REUSE=mode)
        subprocess.run([sys.executable, __file__, "lama" if mode == "0" else "salin"], env=env)
