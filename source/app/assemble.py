# Assembles the deployable site in /home/claude/machaque/site from the pilot template pieces.
import json, re, hashlib, os, sys
import os as _os
APP = _os.path.dirname(_os.path.abspath(__file__))
SP = APP
# the site is written to the repository root (the folder above source/)
OUT = _os.environ.get('MACHAQUE_OUT') or _os.path.dirname(_os.path.dirname(APP))

def build(data):
    head = open(SP + '/head.html').read()
    body = open(SP + '/body.html').read().split('\n')
    css = head.split('<style>')[1]
    css = css.replace('--font-text:"Literata", Georgia, "Times New Roman", serif;', '--font-text:ui-serif, "New York", Georgia, "Times New Roman", serif;')
    css = css.replace('--font-ui:"Atkinson Hyperlegible", -apple-system, "Segoe UI", Roboto, sans-serif;', '--font-ui:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;')
    css += '\n'.join(body[0:9]) + '\n' + open(APP + '/extra.css').read()
    # checking code from the pilot (lines 21-133 of body.html), unchanged
    whole = '\n'.join(body)
    check_js = whole[whole.index('// ---------- answer checking'):whole.index('// ---------- session')]
    js = ('const DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n'
          "const KEY = 'machaque.app.v1';\n"
          'function defaults(){ return {items:{}, units:{}, notes:[], newDay:null, newCount:0, answered:0, backup:null} }\n'
          'function load(){ try{ return JSON.parse(localStorage.getItem(KEY)) || {} }catch(e){ return {} } }\n'
          'function save(){ try{ localStorage.setItem(KEY, JSON.stringify(store)) }catch(e){} }\n'
          'const store = Object.assign(defaults(), load());\n'
          + check_js + '\n' + open(APP + '/app.js').read())
    html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Machaque</title>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Machaque">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#f3f4f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121514" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png">
<style>{css}
</head>
<body>
<div class="wrap" id="app"></div>
<script>
{js}
</script>
</body>
</html>
'''
    os.makedirs(OUT, exist_ok=True)
    open(OUT + '/index.html', 'w').write(html)
    ver = hashlib.sha1(html.encode()).hexdigest()[:10]
    sw = open(APP + '/sw.js').read().replace('__VERSION__', ver)
    open(OUT + '/sw.js', 'w').write(sw)
    json.dump({"name": "Machaque", "short_name": "Machaque", "start_url": "./", "scope": "./",
               "display": "standalone", "background_color": "#f3f4f1", "theme_color": "#f3f4f1", "lang": "es",
               "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]},
              open(OUT + '/manifest.webmanifest', 'w'), indent=1)
    if not os.path.exists(OUT + '/icon-512.png'):
        from PIL import Image, ImageDraw, ImageFont
        for size, name in [(512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')]:
            im = Image.new('RGB', (size, size), '#1f4e8c'); d = ImageDraw.Draw(im)
            fp = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
            f = ImageFont.truetype(fp, int(size * 0.62)) if os.path.exists(fp) else ImageFont.load_default()
            bb = d.textbbox((0, 0), 'M', font=f)
            d.text(((size - (bb[2] - bb[0])) / 2 - bb[0], (size - (bb[3] - bb[1])) / 2 - bb[1]), 'M', fill='#f3f4f1', font=f)
            im.save(OUT + '/' + name)
    open(OUT + '/.nojekyll', 'w').write('')
    return ver
