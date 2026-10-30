import json, re, itertools, sys, os
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from items import UNITS
import glob, importlib, hashlib, datetime
sys.path.insert(0, BASE + '/units')
for f in sorted(glob.glob(BASE + '/units/u[0-9][0-9].py')):
    mod = importlib.import_module(os.path.basename(f)[:-3])
    UNITS[mod.UNIT['n']] = mod.UNIT
UNITS = dict(sorted(UNITS.items()))

DEB = {'1s': ['debería', 'debí', 'debiera'], '2s': ['deberías', 'debiste', 'debieras'],
       '3s': ['debería', 'debió', 'debiera'], '1p': ['deberíamos', 'debimos', 'debiéramos'],
       '2p': ['deberíais', 'debisteis', 'debierais'], '3p': ['deberían', 'debieron', 'debieran']}
HAB = {'habría': 'hubiera', 'habrías': 'hubieras', 'habríamos': 'hubiéramos',
       'habríais': 'hubierais', 'habrían': 'hubieran'}
CL = r'(me|te|se|nos|os|los|las|les|lo|la|le)'


def cap(s):
    s = re.sub(r'^([¡¿]?)(\w)', lambda m: m.group(1) + m.group(2).upper(), s)
    s = re.sub(r'([.!?] [¡¿]?)(\w)', lambda m: m.group(1) + m.group(2).upper(), s)
    return s


def expand_deb(s):
    toks = re.findall(r'\{([dD])(\w\w)\}', s)
    if not toks:
        return [s]
    out = []
    # all placeholders in one string share the same form index (same tense choice)
    for i in range(3):
        t = s
        for kind, per in toks:
            forms = DEB[per] if kind == 'd' else [DEB[per][1], DEB[per][0], DEB[per][2]]
            t = t.replace('{%s%s}' % (kind, per), forms[i], 1)
        out.append(t)
    return out


def invert(s):
    if '. ' in s or '?' in s or '!' in s:
        return []
    m = re.match(r'^Si (.+?), (.+)\.$', s)
    return [cap(m.group(2)) + ' si ' + m.group(1) + '.'] if m else []


def hub(s):
    t = re.sub(r'\b(habría|habrías|habríamos|habríais|habrían)\b', lambda m: (HAB[m.group(1).lower()].capitalize() if m.group(1)[0].isupper() else HAB[m.group(1)]), s, flags=re.I)
    return [t] if t != s else []


def proclitic(s):
    pat = re.compile(r'\b(deb\w+) hab[eé]r' + CL + r'(lo|la|los|las)?\b', re.I)
    def rep(m):
        cl = m.group(2) + (' ' + m.group(3) if m.group(3) else '')
        return cl + ' ' + m.group(1).lower() + ' haber'
    t = pat.sub(rep, s)
    return [t] if t != s else []


def variants(a):
    base = [cap(x) for x in expand_deb(a)]
    out = list(base)
    for x in base:
        out += invert(x)
    for x in list(out):
        out += hub(x)
    for x in list(out):
        out += proclitic(x)
    seen, res = set(), []
    for x in out:
        x = cap(x)
        if x not in seen:
            seen.add(x); res.append(x)
    return res


def gapvariants(a):
    out = expand_deb(a)
    for x in list(out):
        out += hub(x)
    return list(dict.fromkeys(out))


data = []
for u, unit in UNITS.items():
    for n, it in enumerate(unit['items'], 1):
        key = it.get('p') or it.get('s')
        d = {'id': f'{u}-' + hashlib.sha1(key.encode()).hexdigest()[:6], 'u': u, 't': it['t'], 'note': it.get('note') or unit['note'],
             'w': it.get('w', False)}
        cue = it.get('cue', '')
        if unit.get('cue') and it['t'] == 'tr':
            cue = unit['cue'] + (' · ' + cue if cue else '')
        d['cue'] = cue
        if it['t'] == 'tr':
            d['p'] = it['p']
            acc = []
            for a in it['a']:
                acc += variants(a)
            d['acc'] = list(dict.fromkeys(acc))
            d['show'] = d['acc'][0]
            d['alts'] = [cap(expand_deb(a)[0]) for a in it['a'][1:]]
            if '{' in it['a'][0]:
                forms = expand_deb(it['a'][0])
                d['alts'] = list(dict.fromkeys([cap(f) for f in forms[1:]] + d['alts']))
            fs, fe = it.get('fs', ''), it.get('fe', '')
            if fs or fe:
                keep = [a for a in d['acc'] if a.startswith(fs) and a.endswith(fe)]
                assert keep, d['id']
                d['fs'], d['fe'] = fs, fe
                d['acc'] = [a[len(fs):len(a) - len(fe)].strip() for a in keep]
                d['alts'] = [a for a in d['alts'] if a.startswith(fs) and a.endswith(fe)]
        elif it['t'] == 'gap':
            acc = []
            for a in it['a']:
                acc += gapvariants(a)
            d['acc'] = list(dict.fromkeys(acc))
            d['s'] = it['s']
            d['show'] = cap(re.sub(r'___ \([^)]*\)', d['acc'][0], it['s']))
        else:
            d['s'] = it['s']
            d['o'] = it['o']
            d['acc'] = [it['o'][0]]
            d['show'] = it['o'][0] if '___' not in it['s'] else cap(it['s'].replace('___', it['o'][0]))
        data.append(d)

# Lexicon of real Spanish words near the course vocabulary. A one-letter slip is forgiven as a
# typo only when what was typed is NOT a real word here (hanria → typo; había → real error).
import os, unicodedata
LEMMAS = '''saber venir llamar recoger ir buscar salir perder llover comer almorzar reservar estudiar aprobar
abrir estar ser cometer hacer ver saludar decir enfadar poner cerrar quemar retrasar llegar tener comprar
romper correr pagar escribir contestar responder dormir quedar pasar aceptar ofrecer pedir volver regresar
traer descubrir seguir avisar llevar tomar beber preguntar encontrar creer sufrir conocer coger escuchar
ocurrir gastar poder levantar ladrar despertar invitar deber haber pensar decantar confiar apuntar anotar
esperar devolver resolver comprobar mirar revisar terminar acabar dejar ayudar vender ganar explicar
encantar dar querer adelantar recibir vivir hablar trabajar viajar mandar enviar subir bajar entrar
morir caer leer oír sentir mentir servir vestir elegir empezar jugar contar mover probar costar
preferir desear pedir aconsejar exigir recomendar prohibir permitir alegrar molestar temer sentir doler
importar gustar odiar preocupar extrañar sorprender parecer dudar negar suponer imaginar opinar
necesitar intentar conseguir lograr cambiar arreglar limpiar cocinar preparar cenar desayunar merendar
invitar celebrar casar divorciar mudar alquilar aparcar conducir traducir producir reducir ofrecer
agradecer merecer parecer nacer crecer obedecer pertenecer aparecer desaparecer conocer reconocer
caber valer oír huir construir destruir incluir concluir sustituir distribuir contribuir
llegar pagar jugar entregar negar apagar cargar colgar rogar tocar sacar buscar explicar practicar
indicar publicar aparcar equivocar acercar colocar dedicar marcar secar pescar atacar empezar comenzar
cruzar organizar realizar utilizar analizar almorzar gozar abrazar rezar avanzar
dormir morir pedir servir repetir seguir conseguir elegir corregir medir reír sonreír freír vestir
sentir mentir preferir divertir convertir advertir sugerir hervir herir
contar encontrar mostrar recordar acordar costar soñar volar sonar probar aprobar comprobar
mover volver devolver resolver llover doler soler oler morder torcer cocer
pensar cerrar empezar despertar sentar calentar negar regar fregar nevar gobernar recomendar
entender perder defender encender querer tener venir mantener obtener detener contener prevenir convenir
hacer deshacer satisfacer decir predecir poner suponer proponer componer disponer imponer
traer atraer distraer caer salir valer saber haber ir ser estar dar ver prever
tirar echar meter sacar poner quitar dejar soltar coger recoger escoger proteger elegir dirigir exigir
ganar perder vender comprar gastar ahorrar prestar cobrar deber costar valer
hablar charlar contar callar gritar llorar reír bromear quejar discutir pelear
andar caminar correr nadar bailar cantar tocar jugar ganar entrenar
estudiar aprender enseñar leer escribir dibujar pintar
abrir cerrar subir bajar entrar salir llegar partir quedar faltar sobrar
lavar duchar bañar peinar afeitar maquillar vestir desnudar acostar levantar sentar
enfadar enojar cansar aburrir divertir preocupar tranquilizar calmar relajar
casar enamorar separar mudar instalar acostumbrar
ayudar cuidar curar operar enfermar mejorar empeorar
avisar llamar contestar responder mandar enviar recibir
reservar cancelar confirmar retrasar adelantar
probar catar beber brindar servir pedir tomar'''.split()
LEMMAS = list(dict.fromkeys(LEMMAS))
def deacc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')
LEXF = BASE + '/lex.json'
if os.path.exists(LEXF) and json.load(open(LEXF)).get('lemmas') == LEMMAS:
    verbwords = set(json.load(open(LEXF))['words'])
else:
    import logging; logging.disable(logging.CRITICAL)
    from verbecc import CompleteConjugator
    cg = CompleteConjugator(lang='es'); verbwords = set()
    def walk(o):
        if isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
        elif isinstance(o, str):
            for w in re.findall(r'[^\W\d_]+', o): verbwords.add(deacc(w))
    for L in LEMMAS:
        try:
            walk(json.loads(str(cg.conjugate(L))))
        except Exception as e:
            # regular -ar fallback
            st = L[:-2]
            for e2 in '''o as a amos ais an aba abas abamos abais aban e aste o amos asteis aron are aras ara aremos
                areis aran aria arias ariamos ariais arian e es emos eis en ara aras aramos arais aran ase ases asemos
                aseis asen ando ado ada ados adas ad'''.split():
                verbwords.add(st + e2)
        verbwords.add(L)
    # "ir" by hand (the conjugator chokes on two-letter verbs)
    verbwords |= set('''voy vas va vamos vais van iba ibas ibamos ibais iban fui fuiste fue fuimos fuisteis fueron
    ire iras ira iremos ireis iran iria irias iriamos iriais irian vaya vayas vayamos vayais vayan fuera fueras
    fueramos fuerais fueran fuese fueses fuesemos fueseis fuesen ve id idos yendo ido ida idas idos'''.split())
    # participles inflect for gender and number
    for w in list(verbwords):
        if re.search(r'(ad|id|iert|uest|ech|ich|uelt|ist|ot|it)o$', w):
            for e in ('a', 'os', 'as'): verbwords.add(w[:-1] + e)
    json.dump({'lemmas': LEMMAS, 'words': sorted(verbwords)}, open(LEXF, 'w'), ensure_ascii=False)
EXTRA = '''el la los las lo le les al del se me te nos os mi tu su mis tus sus que qué si sí no ni ya
mas más menos muy mucho mucha muchos muchas poco poca tanto tanta tan antes despues ahora aqui
alli este esta esto ese esa eso aquel aquella aquello un una uno unos unas como cuando donde cual
quien para por con sin sobre entre hasta desde hacia contra mismo misma mismos mismas otro otra
nada algo todo toda todos todas nadie alguien tarde temprano pronto siempre nunca ayer hoy manana'''.split()
corpus = set()
for d in data:
    for a in d.get('acc', []) + [d.get('show', ''), d.get('fs', ''), d.get('fe', '')]:
        for w in re.findall(r'[^\W\d_]+', a): corpus.add(deacc(w))
LEX = sorted(verbwords | corpus | set(deacc(w) for w in EXTRA))

ids = [d['id'] for d in data]
assert len(ids) == len(set(ids)), 'duplicate item ids'
meta = {str(u): {'title': un['title'], 'struct': un['struct'], 'count': len(un['items'])} for u, un in UNITS.items()}
course = []
while len(course) + 1 in UNITS: course.append(len(course) + 1)
DATA = {'meta': meta, 'items': data, 'lex': LEX, 'course': course,
        'build': datetime.date.today().isoformat()}
json.dump(DATA, open(BASE + '/data.json', 'w'), ensure_ascii=False, indent=1)
sys.path.insert(0, BASE + '/app')
from assemble import build
ver = build(DATA)
print(len(data), 'items · course units', course, '· version', ver)
