from items import T, G, M
UNIT = {
    "n": 11,
    "title": "Cuando llegues, llámame",
    "struct": "cuando, en cuanto, tan pronto como, hasta que, mientras + subjuntivo (futuro) vs indicativo (hábito / pasado)",
    "note": "Cuando, en cuanto, tan pronto como, después de que, hasta que y mientras llevan subjuntivo si hablan del futuro; si es un hábito o algo pasado, indicativo. Nunca futuro ni condicional después de «cuando».",
    "items": [
        T("When you get there, call me.",
          ["Cuando llegues, llámame.", "Cuando llegues allí, llámame.", "Cuando llegues ahí, llámame.",
           "Llámame cuando llegues.", "Llámame cuando llegues allí.", "Llámame cuando llegues ahí."],
          cue="tú", note="Llegar → llegues: futuro, subjuntivo después de «cuando»."),
        G("Cuando ___ (tener, yo) tiempo, te ayudaré con la mudanza.", "tenga",
          note="Acción futura después de «cuando»: subjuntivo."),
        T("I'll tell him as soon as he gets home.",
          ["Se lo diré en cuanto llegue a casa.", "Se lo digo en cuanto llegue a casa.",
           "Se lo voy a decir en cuanto llegue a casa.", "En cuanto llegue a casa, se lo diré.",
           "En cuanto llegue a casa, se lo digo.", "En cuanto llegue a casa, se lo voy a decir.",
           "Voy a decírselo en cuanto llegue a casa.", "En cuanto llegue a casa, voy a decírselo."],
          cue="en cuanto", note="«En cuanto» + subjuntivo cuando se refiere al futuro."),
        M("Mañana te llamo en cuanto ___ del médico.", ["salga", "salgo", "saldré", "salía"],
          note="Futuro después de «en cuanto»: subjuntivo, nunca futuro."),
        T("I always call my mother when I get home.",
          ["Siempre llamo a mi madre cuando llego a casa.", "Cuando llego a casa, siempre llamo a mi madre.",
           "Siempre llamo a mi madre al llegar a casa.", "Llamo siempre a mi madre cuando llego a casa.",
           "Cuando llego a casa, llamo siempre a mi madre.", "Al llegar a casa, siempre llamo a mi madre."],
          note="Hábito: «cuando» + indicativo."),
        T("Wait here until the waiter brings the menu.",
          ["Esperad aquí hasta que el camarero traiga la carta.", "Esperad aquí hasta que el camarero traiga el menú.",
           "Esperad aquí hasta que el camarero os traiga la carta.", "Esperad aquí hasta que el camarero os traiga el menú.",
           "Esperad aquí hasta que traiga la carta el camarero.", "Esperad aquí hasta que traiga el menú el camarero."],
          cue="vosotros", note="Traer → traiga; «hasta que» + subjuntivo."),
        G("No te muevas de aquí hasta que yo ___ (volver).", "vuelva",
          note="Volver → vuelva (o → ue)."),
        M("Mientras yo ___ en esta casa, nadie pasará hambre.", ["viva", "vivo", "vivía", "vivir"],
          note="«Mientras» = «siempre que»: subjuntivo para el futuro."),
        T("As long as you keep paying the rent, you can stay in the flat.",
          [f"Mientras {v}, {r} en el piso." for v in ("sigas pagando el alquiler", "pagues el alquiler")
           for r in ("puedes quedarte", "te puedes quedar", "podrás quedarte", "te podrás quedar")],
          cue="tú · mientras", note="Seguir → sigas; «mientras» como condición futura lleva subjuntivo.", fe="en el piso."),
        T("After we eat, we'll go for a walk.",
          [f"Después de que comamos, {r}." for r in (
              "daremos un paseo", "iremos a dar un paseo", "vamos a dar un paseo", "nos daremos un paseo",
              "iremos a pasear", "vamos a pasear", "saldremos a pasear", "saldremos a dar un paseo",
              "daremos una vuelta", "vamos a dar una vuelta", "iremos a dar una vuelta")]
          + [f"{r} después de que comamos." for r in (
              "Daremos un paseo", "Iremos a dar un paseo", "Vamos a dar un paseo", "Iremos a pasear",
              "Vamos a pasear", "Saldremos a pasear", "Daremos una vuelta", "Vamos a dar una vuelta")],
          cue="nosotros · después de que", note="«Después de que» + subjuntivo si es futuro."),
        T("When I was a kid, I used to go to the village every summer.",
          [f"{s} {k}, {v} al pueblo todos los veranos." for s in ("Cuando era", "De")
           for k in ("pequeño", "pequeña", "niño", "niña", "crío", "cría") for v in ("iba", "solía ir")],
          note="Pasado habitual: indicativo (era, iba).", fe="al pueblo todos los veranos."),
        G("Cuando ___ (conocer, yo) a Ana, trabajaba en un banco.", "conocí",
          note="Pasado: indicativo."),
        T("As soon as I know something, I'll let you know.",
          [f"Tan pronto como sepa algo, {v}." for v in (
              "os aviso", "os avisaré", "os voy a avisar", "voy a avisaros", "os lo digo", "os lo diré",
              "os lo voy a decir", "voy a decíroslo", "os lo haré saber")]
          + [f"{v} tan pronto como sepa algo." for v in (
              "Os aviso", "Os avisaré", "Os voy a avisar", "Voy a avisaros", "Os lo digo", "Os lo diré",
              "Os lo voy a decir", "Voy a decíroslo", "Os lo haré saber")],
          cue="vosotros · tan pronto como", note="Saber → sepa."),
        T("I'll pay you guys when I get paid, okay?",
          [f"{p} cuando {c}, ¿vale?" for p in ("Os pago", "Os pagaré", "Os lo pago", "Os lo pagaré",
                                               "Os voy a pagar", "Os lo voy a pagar", "Os lo devuelvo")
           for c in ("cobre", "me paguen")]
          + [f"Cuando {c}, {p}, ¿vale?" for c in ("cobre", "me paguen")
             for p in ("os pago", "os pagaré", "os lo pago", "os lo pagaré", "os voy a pagar")],
          cue="vosotros · (a unos amigos, coloquial)", note="Cobrar → cobre; «vale» es muy de España."),
        G("Cuando ___ (venir, vosotros) a Madrid, os enseñaremos el Retiro.", "vengáis",
          note="Venir → vengáis."),
        T("Don't open the oven until the cake is ready.",
          [f"No abra el horno {h} {x}." for h in ("hasta que", "hasta que no")
           for c, e in (("la tarta", "esté lista"), ("la tarta", "esté hecha"), ("el pastel", "esté listo"),
                        ("el pastel", "esté hecho"), ("el bizcocho", "esté listo"), ("el bizcocho", "esté hecho"))
           for x in (f"{c} {e}", f"{e} {c}")],
          cue="usted", note="Abrir → abra (negativo de usted); estar → esté."),
        M("Normalmente, cuando ___ frío, me pongo la bufanda.", ["hace", "haga", "hará", "hiciera"],
          note="Hábito: indicativo."),
        T("I'll come as soon as I finish work.",
          [f"{v} en cuanto {s}." for v in ("Vendré", "Vengo", "Voy a venir")
           for s in ("termine de trabajar", "acabe de trabajar", "termine el trabajo", "salga del trabajo",
                     "salga de trabajar")]
          + [f"En cuanto {s}, {v}." for s in ("termine de trabajar", "acabe de trabajar", "termine el trabajo",
                                              "salga del trabajo", "salga de trabajar")
             for v in ("vendré", "vengo", "voy a venir")],
          cue="venir · en cuanto", note="Terminar → termine."),
        T("We'll wait for you until you're ready.",
          ["Os esperaremos hasta que estéis listos.", "Os esperaremos hasta que estéis listas.",
           "Os esperamos hasta que estéis listos.", "Os esperamos hasta que estéis listas.",
           "Os vamos a esperar hasta que estéis listos.", "Os vamos a esperar hasta que estéis listas."],
          cue="vosotros", note="Estar → estéis (con tilde)."),
        G("Mañana, en cuanto ___ (poner, yo) la lavadora, saldré a comprar el pan.", "ponga",
          note="Poner → ponga."),
        T("When I retire, I'm going to live by the sea.",
          [f"Cuando me jubile, {v} {d} mar." for v in ("voy a vivir", "viviré", "me voy a ir a vivir",
                                                      "me iré a vivir", "voy a irme a vivir")
           for d in ("cerca del", "junto al", "al lado del", "a la orilla del")],
          fs="Cuando me jubile,", note="Jubilarse → me jubile."),
        T("We'll start dinner when everybody sits down.",
          [f"{m} cuando {s}." for m in ("Empezaremos a cenar", "Empezamos a cenar", "Vamos a empezar a cenar",
                                        "Empezaremos la cena", "Cenaremos")
           for s in ("todos se sienten", "se sienten todos", "todo el mundo se siente", "se siente todo el mundo",
                     "todos estén sentados", "estén todos sentados")],
          note="Sentarse → se sienten (e → ie)."),
        T("Dude, as soon as I get paid, we're going out for some beers.",
          [f"{a} {b}" for a in ("Tío, en cuanto cobre,", "Tío, en cuanto me paguen,", "En cuanto cobre, tío,",
                                "En cuanto me paguen, tío,")
           for b in ("nos vamos de cañas.", "nos vamos de cervezas.", "salimos de cañas.", "nos tomamos unas cañas.",
                     "nos tomamos unas cervezas.", "nos vamos a tomar unas cañas.", "salimos a tomar unas cañas.",
                     "salimos a tomar unas cervezas.", "nos vamos a tomar unas cervezas.", "vamos a salir de cañas.",
                     "vamos a ir de cañas.", "salimos de cervezas.", "nos vamos de birras.",
                     "nos tomamos unas birras.")],
          cue="(a un amigo, coloquial) · en cuanto", note="Cobrar → cobre; pagar → paguen (g → gu)."),
        M("No te vayas hasta que te ___ el cambio.", ["den", "dan", "dieron", "darán"],
          note="Dar → den (sin tilde en «den»); «hasta que» + subjuntivo."),
        T("Don't worry, man, I'll fix it as soon as I get back home.",
          [f"{t}, tío, {f} en cuanto {v} a casa." for t in ("Tranquilo", "Tranquila", "No te preocupes")
           for f in ("lo arreglo", "lo arreglaré", "lo voy a arreglar", "voy a arreglarlo")
           for v in ("vuelva", "llegue", "regrese")],
          cue="(a un amigo, coloquial) · en cuanto", note="Volver → vuelva; «tío» es muy de España."),
        T("Whenever I finish work, I go for a run.",
          [f"{s} {v} de trabajar, {r}." for s in ("Siempre que", "Cada vez que", "Cuando")
           for v in ("termino", "acabo") for r in ("salgo a correr", "me voy a correr", "voy a correr")],
          cue="hábito", note="Hábito: indicativo (termino)."),
        G("Mientras no ___ (llover) esta tarde, jugaremos al fútbol en el parque.", "llueva",
          note="«Mientras no» = siempre que no: subjuntivo."),
        T("We'll buy a house when we have enough money.",
          [f"{v} una casa cuando tengamos {d}." for v in ("Compraremos", "Nos compraremos", "Vamos a comprar",
                                                           "Nos vamos a comprar")
           for d in ("suficiente dinero", "bastante dinero", "dinero suficiente")]
          + [f"Cuando tengamos {d}, {v} una casa." for d in ("suficiente dinero", "bastante dinero", "dinero suficiente")
             for v in ("compraremos", "nos compraremos", "vamos a comprar", "nos vamos a comprar")],
          cue="nosotros", note="Tener → tengamos."),
        M("Cuando ___ a Sevilla, visitaremos la Giralda.", ["vayamos", "vamos", "iremos", "íbamos"],
          note="Ir → vayamos: futuro, subjuntivo."),
        T("Let me know when the doctor tells you something, okay?",
          ["Venga, avísame cuando el médico te diga algo, ¿vale?", "Avísame cuando el médico te diga algo, ¿vale?",
           "Venga, avísame cuando te diga algo el médico, ¿vale?", "Avísame cuando te diga algo el médico, ¿vale?"],
          cue="(a un amigo, coloquial)", note="Decir → diga.", fe="¿vale?"),
        T("When you hear the bell, open the door.",
          ["Cuando oigas el timbre, abre la puerta.", "Cuando escuches el timbre, abre la puerta.",
           "Cuando suene el timbre, abre la puerta."],
          cue="tú", note="Oír → oigas.", fe="abre la puerta."),
        G("Cuando ___ (ver, vosotros) lo caro que es el hotel, no vais a querer quedaros.", "veáis",
          note="Ver → veáis."),
        T("When I go to Madrid next week, I'll have lunch with them.",
          [f"Cuando vaya a Madrid {s}, {c} con ellos." for s in ("la semana que viene", "la semana próxima",
                                                                 "la próxima semana")
           for c in ("comeré", "almorzaré", "voy a comer", "voy a almorzar", "como")]
          + [f"{c} con ellos cuando vaya a Madrid {s}." for s in ("la semana que viene", "la semana próxima",
                                                                  "la próxima semana")
             for c in ("Comeré", "Almorzaré", "Voy a comer", "Voy a almorzar", "Como")],
          note="Ir → vaya."),
        T("They won't give us the keys until we pay the deposit.",
          [f"No nos {v} las llaves hasta que {n}paguemos la fianza." for v in ("darán", "van a dar", "dan")
           for n in ("", "no ")],
          note="Pagar → paguemos (g → gu).", fe="la fianza."),
        M("¿Cuál es correcta?",
          ["Cuando termines, cierra la puerta.", "Cuando terminarás, cierra la puerta.",
           "Cuando terminaras, cierra la puerta.", "Cuando terminarías, cierra la puerta."],
          note="Después de «cuando», nunca futuro ni condicional: termines."),
        T("As long as it's cold, we won't open the windows.",
          [f"Mientras haga frío, no {v} las ventanas." for v in ("abriremos", "abrimos", "vamos a abrir")],
          note="Hacer → haga.", fe="las ventanas."),
        T("I'll water the plants when I come back from the trip.",
          ["Regaré las plantas cuando vuelva del viaje.", "Regaré las plantas cuando regrese del viaje.",
           "Voy a regar las plantas cuando vuelva del viaje.", "Voy a regar las plantas cuando regrese del viaje.",
           "Riego las plantas cuando vuelva del viaje.", "Riego las plantas cuando regrese del viaje."],
          note="Volver → vuelva; regresar → regrese.", fe="del viaje."),
        M("Cuando era joven, ___ mucho en bici.", ["montaba", "monte", "montaré", "montara"],
          note="Pasado habitual: imperfecto de indicativo."),
        T("You can order dessert once you finish the main course.",
          [f"{p} {k} {v} {c}." for p in ("Podéis pedir el postre", "Podéis pedir postre")
           for k in ("cuando", "una vez que", "en cuanto")
           for v in ("terminéis", "acabéis", "hayáis terminado", "hayáis acabado")
           for c in ("el segundo plato", "el segundo", "el plato principal")],
          cue="vosotros", note="Terminar → terminéis; «cuando» + subjuntivo."),
        G("Cuando ___ (poder, usted), pase por recepción para recoger la llave.", "pueda",
          note="Poder → pueda (usted)."),
        T("He's going to cry when he finds out.",
          [f"{a} {b}" for a in ("Va a llorar", "Llorará", "Se va a poner a llorar", "Se pondrá a llorar")
           for b in ("cuando se entere.", "cuando lo sepa.")]
          + [f"Cuando {c}, {d}." for c in ("se entere", "lo sepa")
             for d in ("va a llorar", "llorará", "se va a poner a llorar", "se pondrá a llorar")],
          note="Enterarse → se entere; saber → sepa."),
        G("Te lo explicaré todo tan pronto como ___ (conocer, nosotros) los resultados.", "conozcamos",
          note="Conocer → conozcamos."),
        T("We'll stay until they close the bar.",
          [f"{v} hasta que {c} el bar." for v in ("Nos quedaremos", "Nos quedamos", "Nos vamos a quedar")
           for c in ("cierren", "cierre")],
          note="Cerrar → cierren (e → ie).", fe="el bar."),
        # weaving with units 1-10
        T("When you see her, tell her to call me.",
          ["Cuando la veas, dile que me llame.", "Dile que me llame cuando la veas."],
          cue="tú", note="«Cuando la veas» y «dile que me llame»: subjuntivo en los dos.", w=True),
        T("I hope you'll call me as soon as you land.",
          ["Espero que me llaméis en cuanto aterricéis.", "En cuanto aterricéis, espero que me llaméis.",
           "Espero que en cuanto aterricéis me llaméis."],
          cue="vosotros · en cuanto", note="«Esperar que» y «en cuanto»: subjuntivo en los dos.", w=True),
        T("I don't think he'll say anything until he talks to his lawyer.",
          [f"No creo que {v} nada hasta que {n}{h} con su {a}." for v in ("diga", "vaya a decir")
           for n in ("", "no ") for h in ("hable", "haya hablado") for a in ("abogado", "abogada")],
          note="«No creo que» + subjuntivo; «hasta que» + subjuntivo.", w=True),
        M("No creo que se ___ hasta que alguien le ofrezca otra cosa.", ["vaya", "va", "irá", "fue"],
          note="«No creo que» + subjuntivo.", w=True),
        T("I may wait a bit longer, until the rain stops.",
          [f"{q} espere {u} más hasta que {p}." for q in ("Quizás", "Quizá") for u in ("un rato", "un poco")
           for p in ("pare de llover", "deje de llover", "pare la lluvia")],
          cue="quizás + subjuntivo", note="«Quizás» y «hasta que»: subjuntivo en los dos.", w=True),
        T("I'm looking for a flat that has a terrace; when I find it, I'll call you.",
          [f"{b} un piso que tenga {t}; cuando lo encuentre, {c}." for b in ("Busco", "Estoy buscando")
           for t in ("terraza", "una terraza") for c in ("te llamo", "te llamaré", "te aviso", "te avisaré")],
          cue="tú", note="Antecedente desconocido (que tenga) y «cuando lo encuentre»: subjuntivo.", w=True),
        G("Es mejor que no cenemos hasta que ___ (venir, ellos) tus padres.", "vengan",
          note="«Es mejor que» y «hasta que»: subjuntivo.", w=True),
    ],
}
