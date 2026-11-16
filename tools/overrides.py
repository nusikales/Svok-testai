# -*- coding: utf-8 -*-
"""Corrections, explanations and references layered on top of the workbook data.

FIN: keyed by the final-test question number. Fields:
  q / o / a  - replacement question text, options, correct option indexes (0 = A)
  conflict   - shown as a warning: what the workbook says and why it was changed
  why        - short explanation of the principle ("Kodėl?")
  refs       - extra references (the workbook itself is always added automatically)
Edits are also applied to identical questions in the module tests.
"""

# --- standard references by topic -------------------------------------------
R_VAND = ['STR 2.07.01:2003 „Vandentiekis ir nuotekų šalintuvas“', 'LST EN 806 (pastato vidaus vandentiekis)']
R_NUOT = ['STR 2.07.01:2003 „Vandentiekis ir nuotekų šalintuvas“', 'LST EN 12056 (savitakės nuotekų sistemos pastatuose)']
R_SILD = ['STR 2.09.02:2005 „Šildymas, vėdinimas ir oro kondicionavimas“']
R_PAVIRS = R_SILD + ['LST EN 1264 (įrengtosios paviršinio šildymo ir vėsinimo sistemos)']
R_RAD = R_SILD + ['LST EN 442 (radiatoriai ir konvektoriai)', 'Radiatorių gamintojo montavimo instrukcija']
R_AUKST = ['Darbų aukštyje saugos ir sveikatos taisyklės', 'Lietuvos Respublikos darbuotojų saugos ir sveikatos įstatymas']
R_GAISR = ['LST EN 2 (gaisrų klasės)', 'LST EN 3 (gesintuvai)', 'Gaisrinės saugos pagrindiniai reikalavimai (PAGD)']
R_BREZ = ['LST EN ISO 5455 (brėžinių masteliai)', 'STR 1.04.04:2017 „Statinio projektavimas, projekto ekspertizė“']
R_SAUGA = ['Lietuvos Respublikos darbuotojų saugos ir sveikatos įstatymas', 'Darbuotojų instruktavimo, mokymo ir atestavimo bendrieji nuostatai']
R_VED = ['STR 2.09.02:2005 „Šildymas, vėdinimas ir oro kondicionavimas“', 'Vėdinimo įrenginių gamintojo (pvz. Komfovent) montavimo ir priežiūros instrukcijos']
R_ORT = R_VED + ['LST EN 12237 (apvalūs metaliniai ortakiai)', 'LST EN 1507 (stačiakampiai metaliniai ortakiai)']
R_SIURB = ['Šilumos siurblio gamintojo techninė dokumentacija (pvz. Mitsubishi Electric katalogas)', 'Reglamentas (ES) 2024/573 dėl fluorintų šiltnamio efektą sukeliančių dujų']

def topic_refs(n):
    if n in (5, 6, 7, 8): return R_NUOT
    if 1 <= n <= 17 or n in (20, 23, 36): return R_VAND
    if n in (19, 21, 24, 26, 34, 37, 39, 102, 18): return R_PAVIRS
    if n in (27, 28, 31, 38): return R_RAD
    if 18 <= n <= 39: return R_SILD
    if n in (40, 99): return R_AUKST
    if n == 42: return R_GAISR
    if n in (43, 44): return R_BREZ
    if 40 <= n <= 47 or n in (100, 101): return R_SAUGA
    if n in (49, 51, 53, 54, 55, 56, 57, 58, 69, 70, 71, 72, 73, 77): return R_ORT
    if 49 <= n <= 98: return R_VED
    return R_SIURB

FIN = {
 1: dict(
    q='Plastikinio vamzdžio slėgio klasė nurodyta PN10. Kokį vardinį darbinį slėgį jis atlaiko (esant 20 °C vandens temperatūrai)?',
    o=['10 barų', '15 barų', '18 barų'], a=[0],
    conflict='Sąsiuvinyje teigiama, kad visi plastikiniai vamzdžiai atlaiko iki 10 barų. Tai netikslu: leistinas slėgis priklauso nuo medžiagos (PP-R, PEX, PE-RT, PVC, PE), sienelės storio (SDR) ir PN klasės, pvz. PN10, PN16, PN20. Klausimas perrašytas.',
    why='PN skaičius reiškia vardinį slėgį barais, esant 20 °C. Kylant vandens temperatūrai, leistinas slėgis mažėja, todėl karštam vandeniui renkamasi aukštesnės klasės vamzdis (pvz. PP-R PN20) arba žiūrima gamintojo slėgio ir temperatūros lentelė.',
    refs=['LST EN ISO 15874 (PP vamzdžiai)', 'LST EN ISO 15875 (PEX vamzdžiai)', 'Vamzdžių gamintojo techninė dokumentacija']),
 2: dict(why='Išardomus sujungimus galima atsukti ir vėl sujungti nepažeidžiant detalių (sriegiai, kompresinės jungtys, flanšai, movos). Litavimas, klijavimas, suvirinimas ir presavimas sukuria neišardomą jungtį.'),
 3: dict(
    q='Kokiu slėgiu dažniausiai hidrauliškai išbandoma pastato vandentiekio sistema, jei projekte nenurodyta kitaip?',
    conflict='Sąsiuvinyje bandymo slėgis pateiktas kaip vienintelė visoms santechninėms sistemoms taikoma taisyklė. Iš tikrųjų slėgį, trukmę ir leistiną slėgio kritimą nustato projektas, normatyvai ir vamzdžių gamintojas. Plastikiniams vamzdžiams taikoma speciali bandymo procedūra, o nuotekų (savitakės) sistemos tikrinamos kitaip, ne darbinio slėgio padauginimu.',
    why='Bandymo slėgis didesnis už darbinį, kad atsiskleistų silpnos jungtys. Dažniausia taisyklė – 1,5 karto didesnis už darbinį slėgį. Tikslius reikalavimus visada žiūrėk projekte ir gamintojo instrukcijoje.',
    refs=['LST EN 806-4 (vandentiekio įrengimas ir bandymai)', 'Vamzdžių gamintojo bandymo instrukcija']),
 4: dict(why='Saugumo sumetimais vamzdynas apžiūrimas tik sumažinus slėgį iki darbinio. Bandomasis slėgis didesnis, todėl, jei jungtis neatlaikytų, apžiūrintis žmogus galėtų būti sužeistas.'),
 5: dict(why='Sifono skersmuo turi būti ne mažesnis už prietaiso nuotekų angą: praustuvui ~32 mm, voniai ar dušui ~40–50 mm, klozetui ~100 mm (110 mm vamzdis).'),
 6: dict(why='Vėdinimo stovas išlygina slėgį nuotekų sistemoje. Be jo, nuleidus vandenį, sifonai išsiurbiami, o į patalpas ima sklisti kvapai. Nuotekų sistemos negalima jungti su pastato vėdinimo sistema.'),
 9: dict(why='Plieniniai vamzdžiai virinami arba jungiami presuojamomis jungtimis (taip pat sriegiais). Polifuzinis suvirinimas ir klijavimas taikomi tik plastikams.'),
 11: dict(why='Juodasis plienas rūdija, todėl geriamajam vandeniui naudojami cinkuoti, nerūdijančio plieno, variniai ar plastikiniai vamzdžiai.'),
 12: dict(why='Bendra taisyklė: karštas vanduo – kairėje, šaltas – dešinėje (žiūrint į prietaisą). Taip maišytuvai standartizuoti visoje Europoje.'),
 13: dict(why='Dažniausia priežastis – per aukštai sureguliuotas plūdinis vožtuvas, todėl vanduo bėga per perpildymo vamzdelį. Nesandari uždaromoji armatūra taip pat gali būti priežastis, tačiau sąsiuvinyje teisingu laikomas A.'),
 14: dict(
    q='Kaip vandentiekyje turi būti išdėstyti variniai vamzdžiai cinkuoto plieno vamzdžių atžvilgiu, žiūrint vandens tekėjimo kryptimi?',
    o=['Variniai – už (po) plieninių', 'Variniai – prieš plieninius', 'Nesvarbu, galima įvairiai'], a=[0],
    conflict='Sąsiuvinyje parašyta tik „tik po plieninių“, nepaaiškinant, kad turima omenyje vandens tekėjimo kryptis. Klausimas patikslintas.',
    why='Vanduo iš vario išplauna vario jonus. Patekę ant cinkuoto plieno, jie sukelia taškinę (galvaninę) koroziją. Todėl varis montuojamas tik už plieno, kad vanduo pirmiau tekėtų per plieną. Mišrioje sistemoje taip pat naudojamos dielektrinės jungtys.',
    refs=['LST EN 12502 (metalų korozija vandens sistemose)']),
 15: dict(
    q='Iš kokių vamzdžių dažniausiai įrengiami atvirai tiesiami pastato vidaus priešgaisrinio vandentiekio (gaisrinių čiaupų) vamzdynai?',
    conflict='Sąsiuvinyje teigiama, kad priešgaisrinio vandentiekio vamzdynai yra tik plieniniai. Dažniausiai taip ir yra, tačiau projektas gali leisti sertifikuotus plastikinius (pvz. CPVC sprinkleriams) ar PE (požeminiam įvadui) vamzdžius. Klausimas patikslintas.',
    why='Atvirai tiesiamas priešgaisrinis vamzdynas gaisro metu turi išlaikyti vandenį ir slėgį, todėl naudojamas nedegus plienas (juodas arba cinkuotas). Plastikiniai vamzdžiai leidžiami tik ten, kur tai numato projektas ir gamintojo sertifikatas.',
    refs=['Gaisrinės saugos pagrindiniai reikalavimai (PAGD)', 'LST EN 12845 (automatinės sprinklerinės sistemos)']),
 16: dict(why='Polifuzinis suvirinimas – tai to paties plastiko (PP-R) vamzdžio ir jungties išlydymas antgaliu ir sujungimas. Metalams ši technologija netinka.'),
 17: dict(why='Atbulinis vožtuvas praleidžia vandenį tik viena kryptimi ir apsaugo nuo atgalinio srauto (pvz. kad karštas vanduo nepatektų į šalto vandens tinklą).'),
 21: dict(why='Ilgesniame kontūre didėja hidraulinis pasipriešinimas ir temperatūrų skirtumas. 16 mm vamzdžiui įprasta riba – apie 80–100 m, ilgesnius plotus reikia dalyti į kelis kontūrus.'),
 22: dict(why='Plokštelinis šilumokaitis yra kompaktiškas ir efektyvus: per daug plonų plokštelių šiluma perduodama dideliu paviršiumi.'),
 23: dict(why='Purvo gaudiklis (filtras) prieš skaitiklį saugo jį ir armatūrą nuo smėlio ir nuosėdų, kurios iškraipytų matavimus.'),
 24: dict(
    q='Kokios temperatūros šilumnešis (vanduo) dažniausiai naudojamas grindinio, sieninio ar lubinio šildymo sistemose?',
    o=['Aukšto slėgio garas', 'Žemo slėgio garas', 'Žemos temperatūros vanduo, dažniausiai apie 30–45 °C'], a=[2],
    conflict='Sąsiuvinyje atsakymas pateiktas tik kaip „< 41 °C“, be paaiškinimo, kad tai vandens temperatūra. Klausimas ir atsakymas patikslinti.',
    why='Paviršinis šildymas atiduoda šilumą dideliu plotu, todėl užtenka žemos šilumnešio temperatūros. Grindų paviršius gyvenamojoje zonoje neturi viršyti 29 °C (žr. 102 klausimą). Tokia sistema puikiai dera su šilumos siurbliais ir kondensaciniais katilais.'),
 25: dict(why='Neizoliuotas vamzdynas be reikalo atiduoda šilumą, todėl auga nuostoliai, o šalto vandens vamzdžiai rasoja.'),
 27: dict(why='Pirmas skaitmuo – šildymo plokščių skaičius, antras – konvekcinių elementų (briaunų) eilių skaičius. Pvz. 22 tipas: 2 plokštės ir 2 konvektoriai.'),
 28: dict(why='Prijungimo mazgas (pvz. H tipo) jungia radiatorių prie vamzdyno ir leidžia jį atjungti nuo sistemos, todėl nereikia išleisti vandens iš visos sistemos.'),
 31: dict(why='Bent 100 mm tarpas po radiatoriumi reikalingas oro cirkuliacijai (konvekcijai) ir grindų valymui.'),
 32: dict(why='Siauruose plokštelinio šilumokaičio kanaluose iš kieto vandens nusėda kalkės, todėl mažėja pralaidumas ir šilumos perdavimas. Šilumokaitį reikia periodiškai praplauti.'),
 34: dict(why='Šiltas grindų, sienos ar lubų paviršius šildo spinduliavimu, kaip saulė: šiluma pirmiausia šildo žmones ir paviršius, o ne orą.'),
 36: dict(why='Buto skaitikliui įprastas DN15 (½") skersmuo.'),
 37: dict(why='PVC netinka šildymo temperatūroms ir nėra deguoniui nepralaidus. Paviršiniam šildymui naudojami PEX, PE-RT, PB ar daugiasluoksniai vamzdžiai su deguonies barjeru.'),
 38: dict(why='Vienvamzdėje sistemoje vanduo nuosekliai teka per visus prietaisus, todėl kiekvienas paskesnis radiatorius gauna vėsesnį vandenį.'),
 39: dict(why='Srauto matuokliu kiekvienam kontūrui nustatomas projekte apskaičiuotas srautas. Taip sistema subalansuojama, ir trumpi kontūrai „nepasiima“ viso vandens.'),
 40: dict(
    q='Nuo kokio aukščio darbas laikomas darbu aukštyje, kai privaloma taikyti apsaugos nuo kritimo priemones (aptvarus, turėklus ar asmenines apsaugos priemones)?',
    conflict='Sąsiuvinyje klausiama apie „aptverimo aukštį“, tačiau 1,3 m yra aukštis, nuo kurio darbas laikomas darbu aukštyje. Pats aptvaras (turėklas) turi būti apie 1,1 m aukščio. Klausimas perrašytas.',
    why='1,3 m – riba, nuo kurios privalomos apsaugos nuo kritimo priemonės. Pirmiausia renkamos kolektyvinės (aptvarai, turėklai, tinklai), o kai jų įrengti neįmanoma – asmeninės (saugos diržai su lynu).',
    refs=R_AUKST),
 42: dict(
    q='Kuris gesintuvas tinka A (kietųjų medžiagų) ir B (degiųjų skysčių) klasės gaisrams gesinti, bet netinka degiųjų dujų (C klasės) gaisrams?',
    o=['Vandens putų', 'Angliarūgštės (CO₂)', 'Miltelinis ABC'], a=[0],
    conflict='Sąsiuvinyje teisingu atsakymu laikomas angliarūgštės gesintuvas. Tai neteisinga: CO₂ gesintuvas skirtas B klasei ir elektros įrenginiams, A klasės gaisrams jis neefektyvus, nes neatvėsina žarijų. Klausimas perrašytas, teisingas atsakymas – vandens putų gesintuvas.',
    why='Gaisrų klasės: A – kietosios medžiagos (mediena, popierius), B – skysčiai, C – dujos, D – metalai, F – kepimo riebalai. Putų gesintuvas – A ir B klasėms. Miltelinis ABC – A, B ir C klasėms. CO₂ – B klasei ir elektros įrangai.'),
 43: dict(why='Eskizas – ranka, dažnai be tikslaus mastelio padarytas brėžinys. Jame vis tiek pateikiami principiniai konstrukcijos sprendimai ir matmenys, todėl teisingi abu variantai.'),
 44: dict(why='Mastelis 1:100 reiškia, kad 1 cm brėžinyje atitinka 100 cm natūroje, todėl objektas sumažintas. 1:1 – natūralus dydis, o, pvz., 2:1 – padidintas.'),
 45: dict(why='Kolektyvinės priemonės saugo visus darbuotojus iš karto (aptvarai, tinklai, ventiliacija). Asmeninės priemonės (šalmas, diržai, drabužiai) saugo tik jas dėvintį žmogų.'),
 47: dict(why='Prieš pradedant dirbti privalomas įvadinis instruktavimas (bendros įmonės taisyklės) ir pirminis instruktavimas darbo vietoje (konkretaus darbo pavojai).'),
 53: dict(why='Ortakis gali tapti gaisro ir dūmų plitimo keliu, todėl jame ir arti jo negalima tiesti degių medžiagų ar kabelių.'),
 57: dict(why='Minimalus tarpas nuo ortakio ašies iki lubų turi būti ne mažesnis už skersmenį, kad būtų vietos tvirtinimui, izoliacijai ir montavimui.'),
 58: dict(why='Perforuota juosta be guminio tarpiklio perduoda vibraciją ir triukšmą į konstrukcijas, be to, ilgainiui ortakis gali nusvirti. Rekomenduojamos apkabos su guminiu tarpikliu ant sriegto strypo.'),
 61: dict(why='Atbulinis vožtuvas saugo nuo atgalinio oro srauto, gaisrinė sklendė – nuo ugnies ir dūmų plitimo. Diafragma skirta balansavimui, ne apsaugai.'),
 62: dict(why='Prieš ir už vožtuvų, sklendžių ir matavimo įtaisų reikia tiesios ortakio atkarpos, nes už posūkių srautas būna netolygus ir prietaisas veikia netiksliai.'),
 63: dict(why='Atbulinis vožtuvas leidžia orui tekėti tik viena kryptimi. Nuo ugnies ir dūmų saugo gaisrinė sklendė, nuo triukšmo – slopintuvas.'),
 64: dict(why='Dūmų šalinimo sistema ne gesina gaisrą, o šalina dūmus iš evakuacijos kelių, kad žmonės galėtų saugiai išeiti, o ugniagesiai – dirbti.'),
 67: dict(why='Vėdinimo sistema subalansuojama diafragmomis ar reguliavimo sklendėmis, kad kiekviena patalpa gautų projektinį oro kiekį.'),
 69: dict(why='Apvalus ortakis izoliuojamas nedegiais akmens vatos dembliais arba kevalais su aliuminio folija: folija sulaiko garus, o tinklelis laiko formą.'),
 71: dict(why='Oras nuteka per jungtis ir siūles, todėl sandarumas priklauso nuo jungčių ilgio ir viso ortakio paviršiaus ploto. Pagal plotą skaičiuojamas leistinas nuotėkis.'),
 72: dict(
    q='Kokios sandarumo klasės ortakiai parenkami, kai keliami aukščiausi sandarumo reikalavimai (pvz. ištraukiamas oras su toksiškomis ar pavojingomis medžiagomis)?',
    conflict='Sąsiuvinyje D klasė pateikta kaip vienintelis atsakymas „toksiškam orui“. Tikslią klasę nustato projektas pagal technologiją, slėgį ir riziką. D klasė yra aukščiausia (A – žemiausia), tačiau toksiškam orui papildomai taikomi ir kiti reikalavimai, pvz. ortakis turi būti po neigiamu slėgiu pastato viduje. Klausimas patikslintas.',
    why='Sandarumo klasės A, B, C ir D nusako leistiną oro nuotėkį per ortakio paviršiaus plotą. Kiekviena aukštesnė klasė leidžia maždaug 3 kartus mažesnį nuotėkį. Įprastoms sistemoms dažniausiai pakanka C klasės.',
    refs=R_ORT + ['LST EN 16798-3 (negyvenamųjų pastatų vėdinimas)']),
 73: dict(why='Oras nuteka pro jungčių vietas, įskaitant varžtų skyles ir lipnia juosta užklijuotas siūles.'),
 76: dict(why='Oro kiekis apskaičiuojamas dviem būdais: pagal žmonių skaičių ir pagal plotą. Parenkama didesnė reikšmė, kad būtų patenkinti abu reikalavimai.'),
 77: dict(why='Skersmuo parenkamas pagal formulę A = L / v: reikiamas oro kiekis L dalijamas iš leistino oro greičio v. Didesnis greitis leidžia mažesnį ortakį, bet sukelia daugiau triukšmo.'),
 79: dict(
    q='Kokiems pastatams vėdinti gali būti taikomos ortakinės ir beortakinės (decentralizuotos) vėdinimo sistemos?',
    o=['Viešiesiems', 'Gyvenamiesiems', 'Gamybiniams', 'Visiems išvardintiems'], a=[3],
    conflict='Sąsiuvinyje teisingu laikomas tik atsakymas „gyvenamiesiems“. Iš tikrųjų tiek ortakinės, tiek beortakinės (pvz. sieniniai rekuperatoriai) sistemos taikomos ir visuomeniniuose bei gamybiniuose pastatuose. Pridėtas variantas „Visiems išvardintiems“.',
    why='Sistemos tipas parenkamas pagal pastato dydį, paskirtį ir oro poreikį, o ne vien pagal tai, ar pastatas gyvenamasis. Pavyzdžiui, mokyklose dažnai montuojami decentralizuoti klasių įrenginiai.'),
 81: dict(why='Už kliūties (alkūnės, trišakio) srautas netolygus, todėl sklendė su pavara montuojama bent per 2 skersmenis nuo jos, kad reguliuotų tiksliai.'),
 85: dict(why='Įrenginio prijungimo angos žymimos raidėmis pagal gamintojo schemą. Visada tikrink konkretaus modelio instrukciją.'),
 89: dict(why='Rekuperatoriuje šiltas ištraukiamas oras atvėsta, ir iš jo iškrinta kondensatas, kurį reikia nuvesti drenažu.'),
 91: dict(why='Prieš ir už slopintuvo reikia tiesios ortakio dalies, kad srautas būtų tolygus. Kitaip slopintuvas pats kelia triukšmą ir didina pasipriešinimą.'),
 93: dict(why='Didžiausią triukšmą kelia ventiliatorius, todėl slopintuvas montuojamas už jo.'),
 94: dict(
    q='Pagal sąsiuvinį (vėdinimo modulio 15 užduotis), kokiu periodiškumu turi būti tikrinami šilumokaičiai (šildytuvai, vėsintuvai ir šilumogrąžiai)?',
    conflict='Atsakymas „3 kartus per metus“ paimtas tik iš sąsiuvinio (vėdinimo modulio 15 užduotis). Norminio dokumento, nustatančio būtent tokį periodiškumą, sąsiuvinyje nenurodyta. Praktikoje periodiškumą nustato įrenginio gamintojo instrukcija ir pastato priežiūros planas, o šilumokaičiai paprastai tikrinami prieš šildymo ir vėsinimo sezonus.',
    why='Šilumokaičiai užsiteršia dulkėmis, todėl mažėja jų efektyvumas, o žiemą jie gali užšalti. Dėl to juos reikia reguliariai tikrinti ir valyti.',
    refs=['STR 1.07.03:2017 „Statinių techninės ir naudojimo priežiūros tvarka“', 'Vėdinimo įrenginio gamintojo priežiūros instrukcija']),
 95: dict(why='Jei vandeninis šildytuvas ar vėsintuvas būna žemesnėje nei 0 °C aplinkoje (nešildomoje patalpoje ar lauke), vanduo jame gali užšalti ir susprogdinti vamzdelius. Todėl naudojamas glikolio tirpalas.'),
 96: dict(why='Ortakio valymui įrengiami apžiūros liukai, kad būtų galima įkišti valymo įrangą ir patikrinti švarumą.'),
 97: dict(
    q='Koks skystis dažniausiai maišomas su vandeniu, kad mišinys neužšaltų, ir nuo ko priklauso jo kiekis?',
    o=['Propilenas, visada 35 %', 'Etilenglikolis (arba propilenglikolis); koncentracija parenkama pagal reikiamą apsaugos nuo užšalimo temperatūrą', 'Etilenglikolis, visada 15 %'], a=[1],
    conflict='Sąsiuvinyje nurodyta fiksuota 35 % (užduotyje – 30–35 %) koncentracija. Iš tikrųjų koncentracija parenkama pagal žemiausią numatomą temperatūrą ir gamintojo lentelę. Pavyzdžiui, apie 30–35 % etilenglikolio saugo maždaug iki −15…−20 °C.',
    why='Kuo daugiau glikolio, tuo žemesnė užšalimo temperatūra, bet blogesnis šilumos perdavimas ir didesnė klampa. Todėl dedama tiek, kiek reikia. Koncentracija tikrinama refraktometru.'),
 98: dict(why='Balansavimas atliekamas paleidžiant sistemą arba ją rekonstruojant. Tai nėra periodinis priežiūros darbas.'),
 99: dict(why='Dirbant aukštyje šalmas privalomas su smakro dirželiu, kad nukritęs žmogus jo nepamestų.'),
 101: dict(why='Flanšų skylės sulyginamos specialiais laužtuvėliais (kaiščiais). Kišti pirštus tarp flanšų pavojinga.'),
 102: dict(why='Pagal LST EN 1264 grindų paviršius gyvenamojoje zonoje neturi viršyti 29 °C, nes šiltesnės grindys nepatogios kojoms. Pakraščių zonose leidžiama iki 35 °C.'),
 103: dict(
    q='Kokių tipų gali būti „oras–oras“ šilumos siurbliai pagal blokų išdėstymą?',
    o=['Split (vienas išorinis ir vienas vidinis blokas) ir multi-split (keli vidiniai blokai prie vieno išorinio)', 'Tik vandeniniai monoblokai', 'Tik geoterminiai (gruntiniai)'], a=[0],
    conflict='Sąsiuvinyje kaip „oras–oras“ tipas nurodytas „monoblokas (vandeniniai)“. Tai klaidinga: vandeniniai monoblokai yra „oras–vanduo“ siurbliai. „Oras–oras“ siurbliai šildo arba vėsina orą tiesiogiai, freonu. Klausimas perrašytas.',
    why='„Oras–oras“: freonas cirkuliuoja tarp išorinio ir vidinio bloko, o vidinis blokas pučia šiltą arba vėsų orą. „Oras–vanduo“: šiluma perduodama vandeniui (grindims, radiatoriams, karštam vandeniui).'),
 104: dict(why='Vidiniai blokai skirstomi pagal montavimo vietą: sieniniai, lubiniai (kasetiniai), grindiniai (konsoliniai) ir kanaliniai (paslėpti, su ortakiais).'),
 105: dict(why='„Oras–oras“ siurblys šildo ir vėsina orą, filtruoja jį ir sausina, nes vėsinant iš oro iškrinta kondensatas.'),
 107: dict(
    q='Ar yra universali galios riba, skirianti buitinius ir pramoninius „oras–oras“ šilumos siurblius?',
    o=['Taip: buitiniai iki 3 kW, pramoniniai nuo 5 kW', 'Taip: buitiniai 2,5–5 kW, pramoniniai nuo 7 kW', 'Ne: galia parenkama pagal patalpų šilumos ir vėsinimo poreikį; buitiniai dažniausiai būna apie 2–8 kW, komerciniai (pvz. VRF) – iki dešimčių ar šimtų kW'], a=[2],
    conflict='Sąsiuvinyje pateiktos fiksuotos galios ribos tarp buitinių ir pramoninių siurblių. Tokios universalios ribos nėra: gamintojai skirsto modelius skirtingai, o galia parenkama pagal skaičiuojamąjį šilumos poreikį. Klausimas perrašytas.',
    why='Siurblio galia parenkama pagal patalpos šilumos nuostolius ir šilumos pritekėjimą. Per mažas siurblys nepašildys patalpos, o per didelis dažnai įsijungs ir išsijungs (taktuos) ir veiks neefektyviai.'),
 108: dict(
    q='Kokias funkcijas name gali atlikti „oras–vanduo“ (arba „žemė–vanduo“) šilumos siurblio sistema?',
    conflict='Sąsiuvinyje klausiama apskritai apie „šilumos siurblio sistemą“, nors išvardintos funkcijos (grindinis šildymas, radiatoriai, karštas vanduo) būdingos „oras–vanduo“ ir „žemė–vanduo“ siurbliams. „Oras–oras“ siurblys vandens nešildo, jis šildo arba vėsina orą. Klausimas patikslintas.',
    why='„Oras–vanduo“ siurblys šildo vandenį, kuris naudojamas grindiniam šildymui, radiatoriams ir buitiniam karštam vandeniui. Nuo legionelių saugo periodinis vandens pašildymas iki ~60–65 °C (antilegioneline funkcija, dažnai papildomu elektriniu kaitintuvu).'),
 109: dict(why='Išmanieji vidiniai blokai su judesio ar infraraudonųjų spindulių jutikliais nustato, kiek žmonių yra ir kur jie sėdi, mato langų ir durų zonas bei paviršių temperatūras, todėl nukreipia srautą taip, kad nepūstų tiesiai į žmones.'),
 110: dict(why='Pagrindiniai rekuperatorių tipai: plokšteliniai (priešpriešiniai ar kryžminiai), rotaciniai ir atskirų srautų (su tarpiniu šilumnešiu, dažniau pramonėje).'),
 111: dict(why='Filtrai išsiurbiami (išvalomi), prireikus dezinfekuojami, o susidėvėję – pakeičiami. Litavimas su filtrais nesusijęs.'),
}

# pre-test (index = question number)
PRE = {
 1: dict(why='ŠVOK montuotojas montuoja šildymo, vėdinimo, oro kondicionavimo sistemas ir šilumos siurblius. Nuotekų sistemos – santechniko darbas.'),
 8: dict(why='Šiluminį pojūtį lemia keturi aplinkos parametrai: oro temperatūra, santykinis drėgnis, oro judėjimo greitis ir paviršių spinduliuotės temperatūra. Dar svarbūs du asmeniniai veiksniai: apranga ir fizinis aktyvumas.', refs=['HN 42:2009 „Gyvenamųjų ir visuomeninių pastatų patalpų mikroklimatas“']),
 11: dict(conflict='Sąsiuvinio atsakymų lape nurodytas tik C („Valyti orą“). Tačiau „oras–oras“ siurbliai šildo, vėsina, filtruoja ir sausina orą (tai patvirtina ir baigiamojo testo 105 klausimas), todėl įskaitomi visi keturi variantai.',
         why='„Oras–oras“ siurblys yra ir šildytuvas, ir kondicionierius: jis šildo ir vėsina orą, o filtras jį valo. Vėsinant iš oro iškrinta kondensatas, todėl oras sausinamas.', a=[0,1,2,3]),
 12: dict(why='Dažniausi trūkumai: išorinio bloko triukšmas, vidinių blokų išvaizda ir freono poveikis aplinkai, jei jis nuteka.'),
}

# Answers for practice tasks that have no answer in the workbook.
# key: (module index, task number)
TASKS = {
 (0, 1): '''<p><b>1.1 Krovinių kėlimo rankomis saugos reikalavimai</b></p>
<ul><li>Prieš keliant įvertinti krovinio svorį, formą ir kelią. Sunkų ar nepatogų krovinį kelti dviese arba mechanizmais (vežimėliu, kėlikliu).</li>
<li>Laikytis leistinų krovinių masių normų. Jos priklauso nuo darbuotojo lyties, amžiaus ir kėlimo dažnumo. Pavyzdžiui, suaugusiam vyrui dažnai nurodoma ne daugiau kaip 25–30 kg, moteriai – apie 10–15 kg. Konkrečias ribas nustato įmonės rizikos vertinimas.</li>
<li>Dėvėti darbines pirštines ir avalynę su apsauginėmis nosimis.</li>
<li>Pasirūpinti, kad kelias būtų laisvas, neslidus ir gerai apšviestas.</li></ul>
<p><b>1.2 Teisinga kėlimo technika</b></p>
<ul><li>Stovėti arti krovinio, kojas laikyti pečių plotyje.</li>
<li>Pritūpti lenkiant kelius, o ne nugarą. Nugara turi likti tiesi.</li>
<li>Krovinį tvirtai suimti abiem rankomis ir laikyti arti kūno.</li>
<li>Kelti tolygiai, kojų raumenimis, be staigių judesių.</li>
<li>Nesisukti liemeniu laikant krovinį, o pasisukti kojomis.</li>
<li>Padėti krovinį taip pat tiesia nugara, pritūpus.</li></ul>''',
 (0, 2): '''<p><b>2.1 Medžiagų krovimo ir sandėliavimo saugos reikalavimai</b></p>
<ul><li>Medžiagas krauti ant lygaus, tvirto pagrindo arba stelažuose, kad rietuvės būtų stabilios ir neapvirstų.</li>
<li>Vamzdžius krauti horizontaliai, ant padėklų ar stovų su atramomis (kaiščiais), kad neišriedėtų. Rietuvės aukštis ribojamas.</li>
<li>Plastikinius vamzdžius laikyti nuo saulės apsaugotoje vietoje ir neperkrauti, kad nesideformuotų.</li>
<li>Sunkesnius daiktus dėti apačioje, lengvesnius – viršuje. Neperkrauti lentynų.</li>
<li>Tarp rietuvių palikti praėjimus. Neužstatyti evakuacijos kelių ir gesintuvų.</li>
<li>Degias medžiagas (dujų balionus, klijus, dažus) laikyti atskirai, pagal gaisrinės saugos reikalavimus.</li>
<li>Ortakius ir smulkias detales laikyti sausoje vietoje, užkimštais galais, kad vidun nepatektų dulkių.</li></ul>''',
 (0, 6): '''<p><b>6.1 Kas yra tvari statyba?</b></p>
<p>Tai toks pastatų projektavimas, statyba ir naudojimas, kai per visą pastato gyvavimo ciklą tausojami ištekliai, mažinamas energijos suvartojimas ir poveikis aplinkai, o žmonėms užtikrinama sveika aplinka. Tvari statyba svarbi, nes pastatai suvartoja didelę dalį energijos ir išmeta daug CO₂. Ji mažina eksploatacijos išlaidas ir gerina gyvenimo kokybę.</p>
<p><b>6.2 Tvarios statybos principai</b></p>
<ul><li>Energinis efektyvumas: gera šiluminė izoliacija, sandarumas, rekuperacija, A++ klasės pastatai.</li>
<li>Atsinaujinančių šaltinių naudojimas: šilumos siurbliai, saulės kolektoriai ir elektrinės.</li>
<li>Ekologiškos, vietinės, perdirbamos medžiagos su maža įkūnyta energija.</li>
<li>Atliekų mažinimas ir rūšiavimas statybvietėje.</li>
<li>Vandens taupymas (taupi santechnika, lietaus vandens panaudojimas).</li>
<li>Sveikas patalpų mikroklimatas: vėdinimas, natūrali šviesa, mažai teršalų.</li>
<li>Ilgaamžiškumas ir galimybė pastatą pritaikyti kitai paskirčiai.</li></ul>''',
 (3, 8): '''<p><b>8.1 Nestandartinių ortakių detalių gamybos principai</b></p>
<ul><li>Detalė gaminama pagal brėžinį ar išmatavimus vietoje. Pirmiausia nubraižoma išklotinė (atraiža) su užlaidomis sujungimams.</li>
<li>Naudojama tokio pat storio ir dangos (cinkuota) skarda kaip ir standartinių ortakių.</li>
<li>Skarda pjaunama skardos žirklėmis ar gilotina, lankstoma lankstymo staklėmis, siūlės užlenkiamos (falcuojamos) arba kniedijamos.</li>
<li>Nupjautos briaunos apsaugomos nuo korozijos.</li>
<li>Sujungimai užsandarinami hermetiku ar sandarinimo juosta, kad detalė atitiktų sistemos sandarumo klasę.</li>
<li>Vidinis paviršius turi būti lygus, be aštrių briaunų, kad nedidėtų pasipriešinimas ir triukšmas.</li></ul>
<p><b>8.2 Kada prireikia nestandartinių detalių?</b></p>
<p>Kai standartinės jungiamosios dalys netinka: ortakį reikia apvesti aplink sijas ar kitas komunikacijas, sujungti nestandartinių matmenų ar formų ortakius (pvz. stačiakampį su apvaliu), prijungti prie įrenginio angos, rekonstruojant senas sistemas arba kai trūksta vietos.</p>''',
 (3, 9): '''<p><b>9.1 Ortakių ir komunikacijų pravedimas per atitvaras</b></p>
<ul><li><b>Sandarumas:</b> pastato sandarumas tikrinamas slėgio bandymu (n50). Kiekviena prakiaura per sandarinamąjį sluoksnį (garo izoliaciją, vėjo izoliaciją) turi būti užsandarinta specialiomis manžetėmis, juostomis ar sandarikliais. Kuo aukštesnė pastato energinio naudingumo klasė (A+, A++), tuo griežtesni sandarumo reikalavimai.</li>
<li><b>Šiluminė izoliacija:</b> ortakis, einantis per šaltą zoną (pvz. lauko oro ar išmetamo oro ortakis per šildomą patalpą), izoliuojamas, kad nesusidarytų šilumos tiltelis ir kondensatas.</li>
<li><b>Gaisrinė sauga:</b> kertant priešgaisrines sienas ar perdangas, įrengiamos gaisrinės sklendės arba priešgaisrinės manžetės, o tarpai užpildomi nedegiomis medžiagomis, kad būtų išlaikyta konstrukcijos atsparumo ugniai klasė.</li>
<li><b>Garso izoliacija:</b> per konstrukcijas neturi sklisti vibracija ir triukšmas, todėl naudojami elastingi tarpikliai.</li>
<li><b>Konstrukcijų vientisumas:</b> laikančiosiose konstrukcijose angos daromos tik pagal projektą ir suderinus su konstruktoriumi.</li>
<li>Angos dydis parenkamas su atsarga izoliacijai ir sandarinimui, tačiau ne per didelis.</li></ul>''',
 (4, 2): '''<p><b>2.1 Freonų rūšys</b></p>
<ul><li><b>CFC</b> (chlorfluorangliavandeniliai, pvz. R12) – ardo ozono sluoksnį, uždrausti.</li>
<li><b>HCFC</b> (pvz. R22) – mažiau ardo ozoną, bet ES taip pat uždrausti.</li>
<li><b>HFC</b> (pvz. R410A, R134a, R32) – ozono neardo, bet sukelia šiltnamio efektą (didelis GWP). Jų naudojimas palaipsniui mažinamas.</li>
<li><b>HFO</b> (pvz. R1234yf, R1234ze) – labai mažas GWP.</li>
<li><b>Natūralūs šaltnešiai:</b> propanas R290, CO₂ R744, amoniakas R717.</li></ul>
<p><b>2.2 Sudėtis</b></p>
<p>Freonai – tai sočiųjų angliavandenilių (metano, etano) dariniai, kuriuose vandenilio atomus pakeičia fluoras ir (ar) chloras. Mišiniai (pvz. R410A = R32 + R125) sudaryti iš kelių tokių junginių.</p>
<p><b>2.3 Pagrindiniai ES reikalavimai</b> (F dujų reglamentas (ES) 2024/573)</p>
<ul><li>Su F dujomis gali dirbti tik atestuoti specialistai ir įmonės.</li>
<li>Privalomi periodiniai sandarumo patikrinimai, kurių dažnis priklauso nuo kiekio CO₂ ekvivalentu.</li>
<li>Įrangą privaloma ženklinti, o darbus registruoti.</li>
<li>Freonas turi būti surenkamas (rekuperuojamas), jo negalima išleisti į atmosferą.</li>
<li>HFC kiekiai palaipsniui mažinami (kvotos), taikomi draudimai naujoje įrangoje naudoti didelio GWP freonus.</li></ul>
<p><b>2.4 Uždrausti freonai</b></p>
<p>CFC (R11, R12) ir HCFC (R22) uždrausti, nes ardo ozono sluoksnį (Monrealio protokolas). Vis daugiau didelio GWP HFC (pvz. R404A) ribojama naujoje įrangoje dėl klimato šiltėjimo.</p>
<p><b>2.5 Ateitis</b></p>
<p>Pereinama prie mažo GWP šaltnešių: R32, HFO ir natūralių šaltnešių (propano R290, CO₂). Daugelis naujų šilumos siurblių jau naudoja R290.</p>''',
 (4, 6): '''<p><b>6.1 Energinio efektyvumo etiketė</b></p>
<p>Tai ES energijos vartojimo efektyvumo etiketė, kuria privaloma ženklinti oro kondicionierius ir šilumos siurblius, kad pirkėjas galėtų palyginti jų efektyvumą. Etiketėje nurodoma:</p>
<ul><li>gamintojas ir modelis;</li>
<li>energinio efektyvumo klasė vėsinimo ir šildymo režimams (nuo A+++ iki D);</li>
<li>projektinė galia (Pdesign, kW) vėsinimui ir šildymui;</li>
<li>SEER ir SCOP vertės;</li>
<li>metinis elektros suvartojimas (kWh/metus);</li>
<li>vidinio ir išorinio bloko triukšmo lygis (dB(A));</li>
<li>Europos klimato zonų žemėlapis.</li></ul>
<p><b>Kodėl ženklinama?</b> To reikalauja ES teisė (ekologinis projektavimas ir energijos ženklinimas). Ženklinimas skatina gaminti ir pirkti efektyvesnę įrangą bei mažinti energijos suvartojimą.</p>
<p><b>Klimato zonos:</b> šildymo efektyvumas nurodomas trims zonoms. <i>Šilta</i> (Atėnai), <i>vidutinė</i> (Strasbūras) ir <i>šalta</i> (Helsinkis). Lietuva priskiriama šaltesnei zonai, todėl jai aktualesnė vidutinės ar šaltos zonos vertė.</p>
<p><b>Ryšys su zonomis:</b> kuo šaltesnis klimatas, tuo didesnis skirtumas tarp lauko ir patalpos temperatūrų. Tada siurblys dirba sunkiau, todėl jo SCOP ir efektyvumo klasė būna žemesni.</p>
<p><b>SEER</b> (Seasonal Energy Efficiency Ratio) – sezoninis vėsinimo efektyvumas: per sezoną pagamintas vėsumo kiekis, padalytas iš suvartotos elektros energijos.</p>
<p><b>SCOP</b> (Seasonal Coefficient of Performance) – sezoninis šildymo efektyvumas: per šildymo sezoną pagaminta šiluma, padalyta iš suvartotos elektros. Pavyzdžiui, SCOP 4 reiškia, kad iš 1 kWh elektros gaunama apie 4 kWh šilumos.</p>''',
}
