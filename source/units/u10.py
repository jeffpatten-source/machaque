from items import T, G, M
UNIT = {
    "n": 10,
    "title": "Te lo explico para que lo entiendas",
    "struct": "para que / a fin de que / con el fin de que + subjuntivo; para + infinitivo si el sujeto es el mismo",
    "note": "Sujetos distintos: para que + subjuntivo. Mismo sujeto: para + infinitivo (también a fin de / con el fin de + infinitivo).",
    "items": [
        T("I'm explaining it to you so that you understand it.",
          ["Te lo explico para que lo entiendas.", "Te lo estoy explicando para que lo entiendas.",
           "Estoy explicándotelo para que lo entiendas.",
           "Te lo voy a explicar para que lo entiendas.", "Voy a explicártelo para que lo entiendas."],
          cue="tú", note="Dos sujetos (yo explico, tú entiendes): para que + subjuntivo."),
        T("I'm going to the market to buy fish.",
          ["Voy al mercado para comprar pescado.", "Me voy al mercado para comprar pescado.",
           "Voy a la plaza para comprar pescado.", "Voy a ir al mercado para comprar pescado.",
           "Voy al mercado a comprar pescado."],
          cue="para + infinitivo", note="Mismo sujeto (yo voy, yo compro): para + infinitivo, sin «que»."),
        G("Os he traído el mapa para que ___ (encontrar, vosotros) el camino.", "encontréis",
          note="En vosotros no hay diptongo: encontréis."),
        M("He venido ___ ayudarte.", ["para", "para que", "a fin de que", "con el fin de que"],
          note="Mismo sujeto: para + infinitivo, sin «que»."),
        T("I'll leave the keys with the neighbour so that you can get in.",
          ["Le dejaré las llaves al vecino para que entréis."]
          + [f"{a} para que {b}."
             for a in [f"{v} las llaves {p}"
                       for v in ("Dejaré", "Voy a dejar", "Dejo")
                       for p in ("con el vecino", "con la vecina", "al vecino", "a la vecina",
                                 "en casa del vecino", "en casa de la vecina")]
                      + [f"{v} las llaves {p}"
                         for v in ("Le dejaré", "Le voy a dejar", "Voy a dejarle", "Le dejo")
                         for p in ("al vecino", "a la vecina")]
             for b in ("entréis", "podáis entrar")
             if f"{a} para que {b}." != "Le dejaré las llaves al vecino para que entréis."],
          cue="vosotros", note="Entrar → entréis (acento en vosotros)."),
        T("Turn down the music so that the baby can sleep.",
          [f"{a} para que {b}."
           for a in ("Baja la música", "Baja el volumen", "Baja el volumen de la música")
           for b in ("el bebé duerma", "duerma el bebé", "el bebé pueda dormir", "pueda dormir el bebé")],
          cue="tú", note="Dormir → duerma (o → ue)."),
        G("Hablo despacio con el fin de que todos me ___ (entender, ellos).", "entiendan",
          note="Entender → entiendan (e → ie)."),
        T("She studies every night to pass the exam.",
          [f"{a} para {b} el examen."
           for a in ("Estudia todas las noches", "Estudia cada noche", "Todas las noches estudia", "Cada noche estudia")
           for b in ("aprobar", "pasar", "superar")],
          note="Mismo sujeto: para + infinitivo.", fe="el examen."),
        T("I'm telling you this so that you don't worry.",
          [f"{a} para que no se preocupe."
           for a in ("Se lo digo", "Le digo esto", "Le digo eso", "Se lo cuento", "Le cuento esto",
                     "Le cuento eso", "Se lo estoy diciendo", "Le estoy diciendo esto", "Le estoy diciendo eso",
                     "Estoy diciéndoselo", "Se lo estoy contando")],
          cue="usted", note="Preocuparse → no se preocupe (subjuntivo de usted)."),
        M("Te llamo ___ me cuentes cómo fue la entrevista.", ["para que", "para", "a fin de", "con el fin"],
          note="Sujetos distintos (yo llamo, tú cuentas): para que + subjuntivo."),
        T("We're moving to the centre so that the kids can walk to school.",
          [f"{a} al centro para que los niños {v} {x} {y}."
           for a in ("Nos mudamos", "Nos vamos a mudar", "Nos vamos a vivir", "Nos estamos mudando")
           for v in ("vayan", "puedan ir")
           for m in ("andando", "a pie", "caminando")
           for d in ("al colegio", "a la escuela", "al cole")
           for x, y in ((m, d), (d, m))],
          note="Ir → vayan; «mudarse» = cambiar de casa."),
        G("Escribo el menú en la pizarra para que los clientes lo ___ (leer, ellos) desde la calle.", "lean",
          note="Leer → lean."),
        T("Bring a jacket so that you don't get cold.",
          [f"{a} {b} para que no {c} frío."
           for a in ("Traed", "Llevad", "Traeos", "Llevaos", "Coged")
           for b in ("una chaqueta", "chaqueta", "una cazadora", "un abrigo")
           for c in ("tengáis", "paséis")],
          cue="vosotros · para que", note="Tener → tengáis."),
        T("I'm leaving early to avoid the traffic.",
          [f"{a} {b} para {c}."
           for a in ("Salgo", "Me voy", "Voy a salir", "Me voy a ir")
           for b in ("pronto", "temprano")
           for c in ("evitar el atasco", "evitar el tráfico", "evitar los atascos",
                     "no pillar atasco", "no pillar tráfico", "no pillar el atasco")],
          note="Mismo sujeto (yo salgo, yo evito): para + infinitivo."),
        T("I'm leaving early so you can use the car, okay?",
          [f"{a} {b} para que {c} el coche, ¿vale?"
           for a in ("Salgo", "Me voy", "Voy a salir")
           for b in ("pronto", "temprano")
           for c in ("uses", "puedas usar", "cojas", "puedas coger", "utilices", "puedas utilizar")],
          cue="(a un amigo, coloquial)", note="Sujetos distintos (yo salgo, tú usas): para que + subjuntivo."),
        G("Te presto mi paraguas para que no te ___ (mojar, tú).", "mojes",
          note="Mojar → mojes (cambio de -a- a -e-)."),
        M("Hemos comprado una mesa grande para que ___ todos en la cena de Navidad.",
          ["quepamos", "cabemos", "caber", "cupimos"],
          note="Caber es irregular: quepa, quepamos."),
        T("I'm calling the plumber so that he can fix the sink today.",
          [f"{a} al fontanero para que {v} {x} {y}."
           for a in ("Llamo", "Voy a llamar", "Estoy llamando")
           for v in ("arregle", "repare", "pueda arreglar", "pueda reparar")
           for o in ("el fregadero", "la pila", "el lavabo")
           for x, y in ((o, "hoy"), ("hoy", o))],
          note="Dos sujetos (yo llamo, él arregla): para que + subjuntivo. «Fontanero» en España."),
        T("Speak slowly so that we can understand you.",
          [f"{a} para que {b}."
           for a in ("Hable despacio", "Hable más despacio")
           for p in ("le", "lo", "la")
           for v in ("entender", "comprender")
           for b in (f"{p} {v[:-2]}amos", f"podamos {v}{p}", f"{p} podamos {v}")],
          cue="usted", note="Hablar → hable (mandato de usted)."),
        G("Pongo el despertador a las seis para ___ (llegar, yo) a tiempo al aeropuerto.", "llegar",
          note="Mismo sujeto (yo pongo, yo llego): para + infinitivo."),
        T("Come on, I'll pay for the taxi so you don't have to walk.",
          [f"Venga, {a} el taxi para que no tengas que {b}."
           for a in ("pago yo", "yo pago", "te pago", "te pago yo")
           for b in ("ir andando", "ir a pie", "andar", "caminar")]
          + [f"Venga, el taxi lo pago yo para que no tengas que {b}."
             for b in ("ir andando", "ir a pie", "andar", "caminar")],
          cue="(a un amigo, coloquial)", note="«Venga» es muy coloquial. Tener que → tengas."),
        T("I'm taking Friday off to be with my parents.",
          ["Me tomo el viernes libre para estar con mis padres.", "Me cojo el viernes libre para estar con mis padres.",
           "Voy a tomarme el viernes libre para estar con mis padres.", "Voy a cogerme el viernes libre para estar con mis padres.",
           "Me voy a tomar el viernes libre para estar con mis padres.", "Me voy a coger el viernes libre para estar con mis padres.",
           "Me cojo el viernes de vacaciones para estar con mis padres.",
           "Me tomo el viernes de vacaciones para estar con mis padres.",
           "Me tomo libre el viernes para estar con mis padres.", "Me cojo libre el viernes para estar con mis padres.",
           "Me estoy tomando el viernes libre para estar con mis padres.",
           "Me cojo el viernes para estar con mis padres.", "Me tomo el viernes para estar con mis padres."],
          note="Mismo sujeto: para + infinitivo. En España, «coger» es muy normal.", fe="para estar con mis padres."),
        M("Os lo repito para que no lo ___ otra vez.", ["olvidéis", "olvidáis", "olvidaréis", "olvidaríais"],
          note="Para que + presente de subjuntivo: olvidéis."),
        T("He studies law in order to become a judge.",
          ["Estudia Derecho con el fin de ser juez.", "Estudia Derecho para ser juez.",
           "Estudia Derecho a fin de ser juez.", "Estudia Derecho con el fin de convertirse en juez.",
           "Estudia Derecho a fin de convertirse en juez.", "Estudia Derecho para convertirse en juez.",
           "Estudia Derecho con el fin de llegar a ser juez.", "Estudia Derecho para llegar a ser juez."],
          cue="con el fin de", note="Mismo sujeto: con el fin de + infinitivo, sin «que».", fe="juez."),
        T("The company is hiring more staff so that customers wait less.",
          [f"La empresa {a} {b} a fin de que los clientes {c} menos."
           for a in ("contrata", "está contratando", "va a contratar")
           for b in ("más personal", "a más personal", "más empleados", "a más empleados",
                     "más trabajadores", "a más trabajadores")
           for c in ("esperen", "tengan que esperar")],
          cue="a fin de que", note="A fin de que = para que: siempre con subjuntivo."),
        G("Cierro la ventana con el fin de que no ___ (entrar, el ruido).", "entre",
          note="Con el fin de que + subjuntivo: entre."),
        T("I'm writing it down so that I don't forget it.",
          [f"{a} para {b}."
           for a in ("Lo apunto", "Me lo apunto", "Lo anoto", "Me lo anoto", "Lo escribo",
                     "Lo estoy apuntando", "Me lo estoy apuntando", "Estoy apuntándolo",
                     "Lo estoy anotando", "Lo estoy escribiendo")
           for b in ("no olvidarlo", "que no se me olvide")],
          note="Dos opciones: para no olvidarlo (mismo sujeto) o para que no se me olvide (el sujeto es «lo»)."),
        T("We're leaving you the car so that you can go to the coast.",
          [f"{a} el coche para que {b} a la costa."
           for a in ("Os dejamos", "Os vamos a dejar", "Vamos a dejaros", "Os prestamos", "Os vamos a prestar")
           for b in ("vayáis", "podáis ir", "os vayáis")],
          cue="vosotros", note="Ir → vayáis.", fe="a la costa."),
        M("Estudio español ___ hablar con mi suegra.", ["para", "para que", "a fin de que", "con el fin de que"],
          note="Mismo sujeto: para + infinitivo."),
        T("Open the window so that the smoke goes out.",
          ["Abre la ventana para que salga el humo.", "Abre la ventana para que el humo salga.",
           "Abre la ventana para que se vaya el humo.", "Abre la ventana para que el humo se vaya.",
           "Abre la ventana para que pueda salir el humo.", "Abre la ventana para que el humo pueda salir."],
          cue="tú", note="Salir → salga."),
        G("Hemos puesto un cartel grande para que nadie se ___ (perder, nadie).", "pierda",
          note="Perder → pierda (e → ie)."),
        T("I'm saving every month to buy a flat.",
          [f"{a} para {b} un piso."
           for a in ("Ahorro todos los meses", "Ahorro cada mes", "Todos los meses ahorro", "Cada mes ahorro",
                     "Estoy ahorrando todos los meses", "Estoy ahorrando cada mes")
           for b in ("comprar", "comprarme")],
          note="Mismo sujeto: para + infinitivo. «Piso» en España.", fe="un piso."),
        T("Okay, I'll send you the photos so you can see them.",
          [f"Vale, {a} las fotos para que las veas."
           for a in ("te mando", "te envío", "te paso", "te voy a mandar", "te voy a enviar", "te voy a pasar", "te mandaré", "te enviaré")],
          cue="(a un amigo, coloquial)", note="Ver → veas."),
        T("Sit here so that I can see you.",
          ["Sentaos aquí para que os vea.", "Sentaos aquí para que pueda veros.",
           "Sentaos aquí para que os pueda ver."],
          cue="vosotros", note="Sentarse en imperativo de vosotros pierde la -d: sentaos."),
        M("Cierra la puerta ___ no entren los mosquitos.", ["para que", "para", "a", "por"],
          note="Sujetos distintos (tú cierras, los mosquitos entran): para que + subjuntivo."),
        T("My mother always cooks too much so that nobody goes hungry.",
          [f"Mi madre {a} para que nadie {b}."
           for a in ("siempre cocina demasiado", "cocina siempre demasiado", "siempre cocina de más",
                     "cocina siempre de más", "siempre cocina demasiada comida", "cocina siempre demasiada comida",
                     "siempre hace demasiada comida", "hace siempre demasiada comida",
                     "siempre hace comida de más", "hace siempre comida de más")
           for b in ("se quede con hambre", "pase hambre", "se quede sin comer")],
          note="Pasar hambre = quedarse con hambre; para que + subjuntivo.", fs="Mi madre"),
        T("Look, I'm telling you so that you know, okay?",
          [f"{a}, {b} para que {c}, ¿vale?"
           for a in ("Mira", "Oye")
           for b in ("te lo digo", "te lo cuento", "solo te lo digo", "solo te lo cuento")
           for c in ("lo sepas", "te enteres")],
          cue="(a un amigo, coloquial)", note="Saber → sepas; «¿vale?» es muy de España."),
        T("Hey, lend me your charger so I can charge my phone.",
          [f"Oye, {a} {b} cargador para {c} {d}."
           for a in ("déjame", "préstame", "pásame")
           for b in ("tu", "el")
           for c in ("cargar", "poder cargar", "que cargue", "que pueda cargar")
           for d in ("el móvil", "mi móvil")],
          cue="(a un amigo, coloquial)", note="Cargo yo (el «me» de déjame): para + infinitivo, o para que pueda cargar."),
        T("I'm going to book a table for eight so that the whole family can eat together.",
          [f"{a} una mesa para {n} para que {c}."
           for a in ("Voy a reservar", "Reservo", "Reservaré")
           for n in ("ocho", "ocho personas")
           for c in ("toda la familia coma junta", "toda la familia pueda comer junta",
                     "podamos comer todos juntos", "comamos todos juntos")],
          cue="reservar", note="Comer → coma; «para ocho» y «para que» no se confunden."),
        G("Habla más alto para que te ___ (oír, nosotros).", "oigamos",
          note="Oír → oigamos."),
        M("Mis padres trabajan mucho ___ yo pueda estudiar en Madrid.",
          ["para que", "para", "a fin de", "con el fin"],
          note="Sujetos distintos (mis padres / yo): para que + subjuntivo."),
        T("We're opening a second shop to reach more customers.",
          [f"{a} {b} para llegar a más clientes."
           for a in ("Abrimos", "Vamos a abrir", "Estamos abriendo")
           for b in ("una segunda tienda", "otra tienda", "un segundo local", "otro local")],
          note="Mismo sujeto: para + infinitivo.", fe="para llegar a más clientes."),
        T("Sign here so that we can process your order.",
          ["Firme aquí para que tramitemos su pedido.", "Firme aquí para que podamos tramitar su pedido.",
           "Firme aquí para que procesemos su pedido.", "Firme aquí para que podamos procesar su pedido.",
           "Firme aquí para que gestionemos su pedido.", "Firme aquí para que podamos gestionar su pedido."],
          cue="usted", note="Firmar → firme (usted); para que + subjuntivo."),
        T("Study hard so that your parents are proud of you.",
          ["Estudiad mucho para que vuestros padres estén orgullosos de vosotros.",
           "Estudiad mucho para que vuestros padres se sientan orgullosos de vosotros.",
           "Estudiad mucho para que vuestros padres se sientan orgullosos.",
           "Estudiad mucho para que vuestros padres estén orgullosos."],
          cue="vosotros", note="Estar → estén; estudiad: el imperativo de vosotros termina en -d."),
        # weaving with units 1-9
        T("I hope you've brought the photos so that grandma can see them.",
          ["Espero que hayáis traído las fotos para que la abuela las vea.",
           "Espero que hayáis traído las fotos para que la abuela pueda verlas.",
           "Espero que hayáis traído las fotos para que la abuela las pueda ver.",
           "Espero que hayáis traído las fotos para que las vea la abuela.",
           "Espero que hayáis traído las fotos para que pueda verlas la abuela.",
           "Espero que hayáis traído las fotos para que las pueda ver la abuela."],
          cue="vosotros", note="Espero que + haya + participio, y después para que + subjuntivo.", w=True),
        T("I ask you to send me the report today so that I can read it over the weekend.",
          ["Le pido que me mande el informe hoy para poder leerlo el fin de semana."]
          + [s for s in (f"Le pido que {o} para {r} {f}."
                         for v in ("mande", "envíe", "pase")
                         for o in (f"me {v} el informe hoy", f"me {v} hoy el informe", f"hoy me {v} el informe")
                         for r in ("poder leerlo", "leerlo", "que pueda leerlo", "que lo pueda leer")
                         for f in ("el fin de semana", "durante el fin de semana"))
             if s != "Le pido que me mande el informe hoy para poder leerlo el fin de semana."],
          cue="usted", note="Pido que + subjuntivo; leo yo (el «me»): para poder leerlo o para que pueda leerlo.", w=True),
        T("I don't think they'll close the street so that the kids can play.",
          [f"No creo que {a} la calle para que {b}."
           for a in ("cierren", "vayan a cerrar", "corten", "vayan a cortar")
           for b in ("los niños jueguen", "jueguen los niños", "los niños puedan jugar", "puedan jugar los niños")],
          note="No creo que + subjuntivo; para que + subjuntivo. Jugar → jueguen.", w=True),
        G("Es importante que apaguéis el móvil para que no ___ (sonar, él) durante la película.", "suene",
          note="Es importante que + subjuntivo; para que + subjuntivo. Sonar → suene.", w=True),
        G("Necesito un piso que tenga dos cuartos para que mis hijos ___ (tener, ellos) su propio espacio.", "tengan",
          note="Antecedente desconocido: «que tenga»; fin: para que tengan.", w=True),
        M("Espero que ya hayáis comprado el pan para que ___ cenar pronto.",
          ["podamos", "podemos", "podremos", "pudimos"],
          note="Espero que + haya + participio; para que + presente de subjuntivo: podamos.", w=True),
    ],
}
