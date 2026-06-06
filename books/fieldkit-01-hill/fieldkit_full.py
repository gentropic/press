#!/usr/bin/env python3
"""FIELD KIT No.01 -- full ~38-page geostatistics tour, one seeded source."""
import numpy as np, math, sys

LEVELS = 6
W, H = 12, 7
def smooth(a):
    b=a.copy()
    b[1:-1,1:-1]=(a[1:-1,1:-1]*4+a[:-2,1:-1]+a[2:,1:-1]+a[1:-1,:-2]+a[1:-1,2:])/8.0
    return b
def simulate(seed, passes=5, shape=(H,W)):
    r=np.random.default_rng(seed); pad=3
    a=r.standard_normal((shape[0]+2*pad, shape[1]+2*pad))
    for _ in range(passes): a=smooth(a)
    a=a[pad:pad+shape[0], pad:pad+shape[1]]; a=(a-a.min())/(a.max()-a.min())
    return np.clip((a*LEVELS).astype(int),0,LEVELS-1)

def sim_cont(seed,passes=5,shape=(H,W)):
    r=np.random.default_rng(seed); pad=3
    a=r.standard_normal((shape[0]+2*pad, shape[1]+2*pad))
    for _ in range(passes): a=smooth(a)
    a=a[pad:pad+shape[0], pad:pad+shape[1]]
    return (a-a.min())/(a.max()-a.min())
_fn=sim_cont(7,5)
_rr,_cc=np.mgrid[0:H,0:W]
_bump=np.exp(-(((_cc-5.5)/2.8)**2+((_rr-3.0)/2.1)**2))   # centred ore-y anomaly
_w=0.6
_comb=(1-_w)*_fn+_w*_bump
_comb=(_comb-_comb.min())/(_comb.max()-_comb.min())
grade=np.clip((_comb*LEVELS).astype(int),0,LEVELS-1)
grade_stat=np.clip((_fn*LEVELS).astype(int),0,LEVELS-1)   # stationary texture, for the variogram
sample_cols=[1,5,9]
cold=np.array([min(abs(c-s) for s in sample_cols) for c in range(W)])
conf=1.0-(cold/cold.max())*0.82

GX,GY=2.2,4.0; CW,CH=1.13,1.05; gridtop=GY+H*CH
def cx(c): return GX+c*CW+CW/2
def cell_xy(c,r): return GX+c*CW, GY+(H-1-r)*CH
def cell_top(r): return GY+(H-r)*CH
def sy(x):
    t=(x-GX)/(W*CW); dip=0.78+0.46*math.cos(2*math.pi*t*1.25+0.7)+0.16*math.cos(2*math.pi*t*2.6)
    return gridtop-max(dip,0.05)
def rock(c,r): return cell_top(r)<=sy(cx(c))+0.02

RAMP=["F0E7D2","E8C57E","E0A14B","D07B3C","B85535","8F3B2E"]

PRE=r"""\documentclass[12pt]{article}
\usepackage[paperwidth=220mm,paperheight=220mm,margin=0mm]{geometry}
\usepackage{fontspec}\usepackage{tikz}\usetikzlibrary{calc,arrows.meta,decorations.pathreplacing}
\pagestyle{empty}\setlength{\parindent}{0pt}
\hyphenpenalty=10000\exhyphenpenalty=10000\tolerance=9999\emergencystretch=2em
\newfontfamily\dispBlack[Path=./fonts/]{Barlow-Black.ttf}
\newfontfamily\dispSemi[Path=./fonts/]{Barlow-SemiBold.ttf}
\newfontfamily\mono[Path=./fonts/]{SpaceMono-Regular.ttf}
\newfontfamily\monoB[Path=./fonts/]{SpaceMono-Bold.ttf}
\definecolor{bone}{HTML}{F2ECDD}\definecolor{basalt}{HTML}{24272D}
\definecolor{basalt60}{HTML}{6E727B}\definecolor{ground}{HTML}{D7CDB4}
\definecolor{casing}{HTML}{1B1D22}\definecolor{teal}{HTML}{2FA199}
\definecolor{ferrous}{HTML}{C75B39}\definecolor{azure}{HTML}{3B7DD8}
\definecolor{waste}{HTML}{CDC6B5}
"""
for i,h in enumerate(RAMP):
    PRE+=r"\definecolor{g%d}{HTML}{%s}"%(i,h)+"\n"
PRE+=r"""
\newcommand{\scaffold}{%
  \fill[bone] (0,0) rectangle (18,18);
  \draw[basalt60,line width=0.4pt] (0.7,0.7) rectangle (17.3,17.3);
  \foreach \cx/\cy in {0.7/0.7,17.3/0.7,0.7/17.3,17.3/17.3}{
    \draw[basalt,line width=0.9pt] (\cx,\cy)++(-0.25,0)--++(0.5,0);
    \draw[basalt,line width=0.9pt] (\cx,\cy)++(0,-0.25)--++(0,0.5);}}
\newcommand{\header}[2]{%
  \node[anchor=north west,text=basalt,inner sep=0pt] at (1.15,16.95)
     {\monoB\fontsize{8.5}{10}\selectfont FIELD KIT\,\textcolor{basalt60}{$\cdot$}\,No.01};
  \node[anchor=north west,text=basalt60,inner sep=0pt] at (1.15,16.5)
     {\mono\fontsize{7.5}{9}\selectfont #1};
  \node[anchor=north east,text=basalt60,inner sep=0pt] at (16.85,16.95)
     {\mono\fontsize{8.5}{10}\selectfont #2};}
\newcommand{\readaloud}[1]{%
  \node[anchor=south west,align=left,text=basalt,inner sep=0pt,text width=14.6cm] at (1.2,1.95)
     {\dispBlack\fontsize{19}{22}\selectfont #1};}
\newcommand{\gloss}[1]{%
  \node[anchor=south west,align=left,text=basalt60,inner sep=0pt,text width=15.6cm] at (1.2,1.0)
     {\mono\fontsize{7.5}{9.5}\selectfont \textcolor{basalt}{//}\ #1};}
\begin{document}
"""

LANG = sys.argv[1] if len(sys.argv)>1 else "en"
PT = (LANG=="pt")

PREFIX_TR={"BONUS":"BÔNUS","COLOPHON":"COLOFÃO"}
FOLIO_TR={"ACT I":"ATO I","ACT II":"ATO II","ACT III":"ATO III","ACT IV":"ATO IV","ACT V":"ATO V","ACT VI":"ATO VI"}
NAME_TR={
 "THE GROUND":"O TERRENO","IT VARIES":"TUDO VARIA","WE DRILL":"A GENTE FURA",
 "DEEP \\& SHALLOW":"FUNDO \\& RASO","MOSTLY MYSTERY":"QUASE TUDO MISTÉRIO",
 "FAIR PLAY":"JOGO JUSTO","NEAR":"PERTO","FAR":"LONGE","TOUCHING":"ENCOSTADAS",
 "FORGETTING":"ESQUECENDO","THE BIGGEST GAP":"A MAIOR DIFERENÇA","COUNT THE PAIRS":"CONTE OS PARES",
 "THE DIFFERENCE CURVE":"A CURVA DA DIFERENÇA","WITH THE GRAIN":"NO SENTIDO DO VEIO",
 "ONE BLOCK":"UM BLOCO","WHO VOTES":"QUEM VOTA","THE BLEND":"A MISTURA",
 "THE FAIREST BLEND":"A MISTURA MAIS JUSTA","HOW SURE":"QUÃO CERTOS","TOO SMOOTH":"LISO DEMAIS",
 "MANY MAYBES":"MUITOS TALVEZ","ROLL THE DICE":"JOGUE O DADO","WRITE IT DOWN":"ANOTE",
 "DREAM MANY HILLS":"SONHE VÁRIAS COLINAS","ALL FIT THE HOLES":"TODOS PASSAM PELOS FUROS",
 "A SPREAD OF ANSWERS":"UM LEQUE DE RESPOSTAS","BIG CALM, SMALL WILD":"GRANDE CALMO, PEQUENO BRAVO",
 "PICK A LINE":"TRACE UMA LINHA","WORTH IT":"VALE A PENA","CHECK OUR WORK":"CONFIRA O TRABALHO",
 "WHERE TO DIG":"ONDE CAVAR","DECLUSTERING":"DESAGRUPAMENTO","SCREEN EFFECT":"EFEITO DE TELA",
 "THE LOUD ROCK":"A ROCHA BARULHENTA","A CHOICE OF CURVE":"UMA ESCOLHA DE CURVA",
}
RA={
 "THE GROUND":r"O que tem embaixo da colina?\\ \textcolor{basalt60}{A gente não vê por dentro.}",
 "IT VARIES":r"Tem rocha rica. Tem rocha pobre.\\ \textcolor{basalt60}{Muda de lugar pra lugar.}",
 "WE DRILL":r"Não dá pra cavar tudo.\\ \textcolor{basalt60}{Então a gente faz uns furos.}",
 "DEEP \\& SHALLOW":r"Desça pelo furo ---\\ \textcolor{basalt60}{as cores mudam com a profundidade.}",
 "MOSTLY MYSTERY":r"Poucos furos. Uma colina grande.\\ \textcolor{basalt60}{Quase tudo é palpite.}",
 "FAIR PLAY":r"A gente finge que a colina\\ \textcolor{basalt60}{tem os mesmos hábitos em todo lugar.}",
 "NEAR":r"Rochas pertinho uma da outra\\ \textcolor{basalt60}{são parecidas.}",
 "FAR":r"Rochas bem distantes?\\ \textcolor{basalt60}{Aí já não tanto.}",
 "TOUCHING":r"Lado a lado,\\ \textcolor{basalt60}{ainda assim não são \emph{idênticas}.}",
 "FORGETTING":r"Longe o bastante,\\ \textcolor{basalt60}{as rochas se esquecem uma da outra.}",
 "THE BIGGEST GAP":r"Bem afastadas =\\ \textcolor{basalt60}{a maior diferença que existe.}",
 "COUNT THE PAIRS":r"Pegue duas rochas. Que distância? Que diferença?\\ \textcolor{basalt60}{De novo. E de novo.}",
 "THE DIFFERENCE CURVE":r"Pares perto mal diferem. Pares longe diferem muito.\\ \textcolor{basalt60}{Desenhe --- é a curva!}",
 "WITH THE GRAIN":r"Siga o veio e as rochas\\ \textcolor{basalt60}{continuam parecidas por mais longe.}",
 "ONE BLOCK":r"Aqui, um bloco que a gente não furou.\\ \textcolor{basalt60}{O que tem dentro?}",
 "WHO VOTES":r"Pergunte às rochas em volta.\\ \textcolor{basalt60}{As mais perto falam mais alto.}",
 "THE BLEND":r"Misture os votos.\\ \textcolor{basalt60}{O palpite pende pro furo mais perto.}",
 "THE FAIREST BLEND":r"Use a curva da diferença\\ \textcolor{basalt60}{pra dividir os votos do jeito \emph{certo}.}",
 "HOW SURE":r"Perto dos furos: certeza. Longe: borrado.\\ \textcolor{basalt60}{Cada bloco ganha um borrão.}",
 "TOO SMOOTH":r"Nosso único palpite é\\ \textcolor{basalt60}{suave e borrado. A rocha real é mais áspera.}",
 "MANY MAYBES":r"Em cada bloco o palpite não é uma cor ---\\ \textcolor{basalt60}{é um leque de talvez.}",
 "ROLL THE DICE":r"Nem sempre pegue o meio seguro.\\ \textcolor{basalt60}{Jogue o dado --- escolha um.}",
 "WRITE IT DOWN":r"Seu sorteio agora vale.\\ \textcolor{basalt60}{Vá pro próximo bloco --- e o próximo.}",
 "DREAM MANY HILLS":r"A rocha real é áspera.\\ \textcolor{basalt60}{Então a gente sonha várias colinas possíveis.}",
 "ALL FIT THE HOLES":r"Toda colina sonhada\\ \textcolor{basalt60}{ainda passa pelos furos que a gente fez.}",
 "A SPREAD OF ANSWERS":r"Muitos morros $\rightarrow$ muitas respostas.\\ \textcolor{basalt60}{Agora a gente sabe a faixa.}",
 "BIG CALM, SMALL WILD":r"Blocos grandes são calmos.\\ \textcolor{basalt60}{Blocos pequenos são bravos.}",
 "PICK A LINE":r"Rico o bastante pra cavar?\\ \textcolor{basalt60}{Sim, ou não.}",
 "WORTH IT":r"Conte os blocos\\ \textcolor{basalt60}{que valem a pena cavar.}",
 "CHECK OUR WORK":r"Esconda um furo. Adivinhe.\\ \textcolor{basalt60}{A gente chegou perto?}",
 "WHERE TO DIG":r"Agora a gente sabe o melhor ponto ---\\ \textcolor{basalt60}{e o quanto temos certeza.}",
 "DECLUSTERING":r"Um aglomerado divide um voto só.\\ \textcolor{basalt60}{A rocha sozinha não é abafada.}",
 "SCREEN EFFECT":r"Uma rocha na frente\\ \textcolor{basalt60}{bloqueia a que está atrás.}",
 "THE LOUD ROCK":r"Uma rocha grita um número gigante.\\ \textcolor{basalt60}{A gente acredita --- ou abaixa o volume?}",
 "A CHOICE OF CURVE":r"Várias linhas suaves passam pelos pontos.\\ \textcolor{basalt60}{A gente escolhe uma --- é decisão nossa.}",
}
GL={
 "THE GROUND":r"o desconhecido --- uma propriedade que vive no espaço, $Z(x)$",
 "IT VARIES":r"variabilidade espacial --- o valor é diferente em cada ponto",
 "WE DRILL":r"amostragem --- um punhado de observações esparsas",
 "DEEP \\& SHALLOW":r"teores ao longo do furo --- cada trecho do testemunho é uma amostra",
 "MOSTLY MYSTERY":r"o problema de estimativa --- muito a prever, pouco dado",
 "FAIR PLAY":r"estacionariedade --- supõe-se que as regras de variação valem em todo lugar",
 "NEAR":r"correlação espacial --- a primeira lei de Tobler",
 "FAR":r"a correlação some conforme aumenta a distância",
 "TOUCHING":r"o efeito pepita --- variabilidade que sobra até a distância zero",
 "FORGETTING":r"o alcance --- a distância além da qual não há mais correlação",
 "THE BIGGEST GAP":r"o patamar --- a variância total, atingida no alcance",
 "COUNT THE PAIRS":r"pares por distância --- o variograma experimental nasce de cada par",
 "THE DIFFERENCE CURVE":r"o variograma $\gamma(h)$ --- pepita no início, subindo ao patamar no alcance",
 "WITH THE GRAIN":r"anisotropia --- o alcance depende da direção",
 "ONE BLOCK":r"estimativa --- prever um valor onde não há amostra",
 "WHO VOTES":r"ponderação por distância --- amostras mais próximas pesam mais",
 "THE BLEND":r"uma média ponderada --- a estimativa no bloco",
 "THE FAIREST BLEND":r"krigagem --- o melhor estimador linear não-viesado, pesos vindos de $\gamma(h)$",
 "HOW SURE":r"a variância de krigagem --- uma incerteza para cada estimativa",
 "TOO SMOOTH":r"a krigagem suaviza --- porque pega o meio seguro do intervalo de cada bloco",
 "MANY MAYBES":r"a distribuição condicional: centrada no palpite krigado, larga como a incerteza",
 "ROLL THE DICE":r"a simulação sorteia um valor desse leque em vez da média --- é a aspereza voltando",
 "WRITE IT DOWN":r"simulação sequencial: cada valor sorteado vira dado pro próximo, preservando a textura",
 "DREAM MANY HILLS":r"simulação geoestatística --- muitas realizações igualmente prováveis",
 "ALL FIT THE HOLES":r"simulação condicional --- as realizações respeitam os dados",
 "A SPREAD OF ANSWERS":r"incerteza pelas realizações --- a média delas acompanha a estimativa krigada",
 "BIG CALM, SMALL WILD":r"suporte / o efeito volume--variância --- volumes maiores variam menos",
 "PICK A LINE":r"teor de corte --- um indicador separa minério de estéril",
 "WORTH IT":r"teor--tonelagem --- quanta rocha está acima do corte",
 "CHECK OUR WORK":r"validação cruzada --- tire um, preveja, meça o erro",
 "WHERE TO DIG":r"a decisão --- um modelo de blocos virando plano",
 "DECLUSTERING":r"desagrupamento --- a krigagem reparte o peso redundante do aglomerado",
 "SCREEN EFFECT":r"o efeito de tela --- o peso da amostra sombreada despenca (pode até ficar negativo)",
 "THE LOUD ROCK":r"capping (capeamento) --- domar um valor extremo pra uma amostra só não dominar",
 "A CHOICE OF CURVE":r"o modelo de variograma é uma escolha --- pepita, alcance e forma são decisões, não fatos",
}
DIV_T={"I":"O\\\\DESCONHECIDO","II":"COMO O TERRENO SE ENCAIXA","III":"O\\\\PALPITE",
       "IV":"MUITOS\\\\TERRENOS","V":"BLOCOS \\& DECISÕES","VI":"BÔNUS"}
DIV_S={"I":"o problema, e as poucas pistas que temos",
       "II":"correlação espacial, e a curva que a mede",
       "III":"preenchendo as lacunas, do jeito mais justo --- krigagem",
       "IV":"por que um palpite não basta --- simulação",
       "V":"suporte, teores de corte, verificação, e onde cavar",
       "VI":"para o adulto que lê junto --- dois truques da krigagem"}
LBL_TR={
 "shallow":"raso","deep":"fundo","MATCH!":"IGUAIS!","NOT SO MUCH":"NEM TANTO",
 "still a tiny bit different":"ainda um tiquinho diferentes","the range":"o alcance","anchor":"âncora",
 "as different as it gets":"o máximo de diferença","how far apart":"distância","sill":"patamar",
 "range":"alcance","nugget":"pepita","alike farther":"parecidas mais longe","less far":"menos longe",
 "RICH":"RICA","POOR":"POBRE","hole":"furo","near":"perto","far":"longe","GUESS":"PALPITE",
 "shares the votes":"divide os votos","OUR GUESS":"NOSSO PALPITE","REAL ROCK":"ROCHA REAL",
 "the safe middle":"o meio seguro","could be any of these":"pode ser qualquer uma","picked!":"sorteado!",
 "this block":"este bloco","now a peek":"agora é furo","next!":"próximo!",
 "BIG BLOCKS --- calm":"BLOCOS GRANDES --- calmos","TINY BLOCKS --- wild":"BLOCOS PEQUENOS --- bravos",
 "rich = dig   ·   pale = leave":"escuro = cavar   ·   claro = deixar","TRUE (hidden)":"REAL (oculto)",
 "close!":"perto!","how much metal?":"quanto metal?",
 "the guess $\\approx$ the average":"o palpite $\\approx$ a média",
 "ONE SHARED SAY":"UM VOTO SÓ","OWN SAY":"VOTO PRÓPRIO","BEHIND":"ATRÁS","blocked":"bloqueada",
 "IN FRONT":"NA FRENTE","DIG":"CAVAR","close: tiny gap":"perto: pouca diferença","far: big gap":"longe: muita diferença",
 "turn it down":"abaixa o volume","cap":"teto",
}

# ---------- primitives ----------
def surface_path(lw=1.3,color="basalt"):
    xs=[GX+i*(W*CW)/89 for i in range(90)]
    return f"  \\draw[{color},line width={lw}pt] "+" -- ".join(f"({x:.2f},{sy(x):.2f})" for x in xs)+";\n"
def block(c,r,fill,opacity=1.0,outline="basalt60",lw=0.5):
    x,y=cell_xy(c,r)
    return (f"  \\fill[{fill},opacity={opacity:.2f}] ({x:.2f},{y:.2f}) rectangle ({x+CW:.2f},{y+CH:.2f});\n"
            f"  \\draw[{outline},line width={lw}pt] ({x:.2f},{y:.2f}) rectangle ({x+CW:.2f},{y+CH:.2f});\n")
def drillhole(c):
    s="";hw=0.30;xc=cx(c);rr=[r for r in range(H) if rock(c,r)]
    if not rr: return s
    top=sy(xc);bot=cell_xy(c,max(rr))[1]
    for r in rr:
        _,by=cell_xy(c,r);ty=min(by+CH,top)
        if ty<=by: continue
        s+=f"  \\fill[g{grade[r,c]}] ({xc-hw:.2f},{by:.2f}) rectangle ({xc+hw:.2f},{ty:.2f});\n"
        s+=f"  \\draw[casing,line width=0.4pt] ({xc-hw:.2f},{by:.2f}) -- ({xc+hw:.2f},{by:.2f});\n"
    s+=f"  \\draw[casing,line width=1.0pt] ({xc-hw:.2f},{bot:.2f}) rectangle ({xc+hw:.2f},{top:.2f});\n"
    s+=f"  \\draw[basalt,line width=1.0pt] ({xc:.2f},{top:.2f}) -- ({xc:.2f},{top+0.55:.2f});\n"
    s+=f"  \\fill[basalt] ({xc:.2f},{top+0.55:.2f}) circle (0.10);\n"
    return s
def panel(ox,oy,w,h,arr,outline="basalt60",lw=0.35,frame=True,hi_cols=None):
    Hh,Ww=arr.shape;cw=w/Ww;ch=h/Hh;s=""
    for rr in range(Hh):
        for cc in range(Ww):
            x=ox+cc*cw;y=oy+(Hh-1-rr)*ch
            s+=f"  \\fill[g{arr[rr,cc]}] ({x:.2f},{y:.2f}) rectangle ({x+cw:.2f},{y+ch:.2f});\n"
            s+=f"  \\draw[{outline},line width={lw}pt] ({x:.2f},{y:.2f}) rectangle ({x+cw:.2f},{y+ch:.2f});\n"
    if hi_cols:
        for cc in hi_cols:
            x=ox+cc*cw
            s+=f"  \\draw[basalt,line width=1.2pt] ({x:.2f},{oy:.2f}) rectangle ({x+cw:.2f},{oy+h:.2f});\n"
    if frame:
        s+=f"  \\draw[basalt,line width=0.9pt] ({ox:.2f},{oy:.2f}) rectangle ({ox+w:.2f},{oy+h:.2f});\n"
    return s
def lbl(x,y,t,color="basalt",fs=9,font="monoB",anchor="south"):
    if PT: t=LBL_TR.get(t,t)
    return f"  \\node[anchor={anchor},text={color},inner sep=1pt] at ({x:.2f},{y:.2f}) {{\\{font}\\fontsize{{{fs}}}{{{fs+2}}}\\selectfont {t}}};\n"
def page(tag,folio,body,readaloud,gloss):
    if PT:
        if " --- " in tag:
            pre,nm=tag.split(" --- ",1)
            tag=PREFIX_TR.get(pre,pre)+" --- "+NAME_TR.get(nm,nm)
            readaloud=RA.get(nm,readaloud); gloss=GL.get(nm,gloss)
        else:
            tag=PREFIX_TR.get(tag,tag)
        folio=FOLIO_TR.get(folio,folio)
    return (r"\begin{tikzpicture}[x=1cm,y=1cm]\scaffold\header{"+tag+"}{"+folio+"}"+"\n"
            +body+r"\readaloud{"+readaloud+r"}\gloss{"+gloss+r"}\end{tikzpicture}\clearpage")
def divider(roman,title,sub,accent):
    if PT:
        title=DIV_T.get(roman,title); sub=DIV_S.get(roman,sub)
    actw="ATO" if PT else "ACT"
    s=r"\begin{tikzpicture}[x=1cm,y=1cm]"+"\n"
    s+=r"  \fill[basalt] (0,0) rectangle (18,18);"+"\n"
    s+=r"  \draw[bone,line width=0.5pt,opacity=0.5] (0.9,0.9) rectangle (17.1,17.1);"+"\n"
    for cxx,cyy in [(0.9,0.9),(17.1,0.9),(0.9,17.1),(17.1,17.1)]:
        s+=f"  \\draw[bone,line width=1.0pt] ({cxx:.2f},{cyy:.2f})++(-0.25,0)--++(0.5,0);\n"
        s+=f"  \\draw[bone,line width=1.0pt] ({cxx:.2f},{cyy:.2f})++(0,-0.25)--++(0,0.5);\n"
    s+=f"  \\node[anchor=north west,text={accent},inner sep=0pt] at (1.7,16.2) {{\\monoB\\fontsize{{13}}{{15}}\\selectfont {actw} {roman}}};\n"
    s+=f"  \\node[anchor=west,text=bone,align=left,inner sep=0pt,text width=14.5cm] at (1.7,9.6) {{\\dispBlack\\fontsize{{40}}{{42}}\\selectfont {title}}};\n"
    s+=f"  \\draw[{accent},line width=3pt] (1.75,7.7) -- (6.6,7.7);\n"
    s+=f"  \\node[anchor=north west,text=bone,align=left,inner sep=0pt,text width=14.5cm] at (1.75,7.1) {{\\mono\\fontsize{{10}}{{14}}\\selectfont {sub}}};\n"
    s+=r"\end{tikzpicture}\clearpage"
    return s

P=[]

# ===== COVER =====
_ctour = "um tour completo" if PT else "a complete tour"
_ctitle = (r"O QUE TEM EMBAIXO\\DA COLINA?" if PT else r"WHAT'S UNDER\\THE HILL?")
_csub = ("toda a geoestatística, uma frase de cada vez" if PT else "all of geostatistics, one sayable line at a time")
c=r"\begin{tikzpicture}[x=1cm,y=1cm]\scaffold"+"\n"
c+=r"  \node[anchor=north west,text=basalt,inner sep=0pt] at (1.15,16.95)"+"\n"
c+=r"     {\monoB\fontsize{9}{11}\selectfont FIELD KIT\,\textcolor{basalt60}{$\cdot$}\,No.01};"+"\n"
c+=r"  \node[anchor=north east,text=basalt60,inner sep=0pt] at (16.85,16.95)"+"\n"
c+=r"     {\mono\fontsize{8.5}{10}\selectfont "+_ctour+r"};"+"\n"
for r in range(H):
    for cc in range(W):
        if rock(cc,r): c+=block(cc,r,"ground",outline="basalt60",lw=0.0)
c+=surface_path()
for cc in sample_cols: c+=drillhole(cc)
c+=r"  \node[anchor=south west,align=left,text=basalt,inner sep=0pt,text width=15.6cm] at (1.2,1.15)"+"\n"
c+=r"     {\dispBlack\fontsize{30}{31}\selectfont "+_ctitle+r"};"+"\n"
c+=r"  \node[anchor=north west,text=basalt60,inner sep=0pt] at (1.25,3.25)"+"\n"
c+=r"     {\mono\fontsize{8}{10}\selectfont "+_csub+r"};"+"\n"
c+=r"\end{tikzpicture}\clearpage"
P.append(c)

# ===== ACT I =====
P.append(divider("I","THE\\\\UNKNOWN","the problem, and the few clues we get","teal"))

# 2 THE GROUND
b="".join(block(cc,r,"ground",outline="basalt60",lw=0.0) for r in range(H) for cc in range(W) if rock(cc,r))
b+=surface_path()+r"  \node[text=basalt60] at (9,7.0) {\dispBlack\fontsize{64}{64}\selectfont ?};"+"\n"
P.append(page("FIG.01 --- THE GROUND","ACT I",b,
    r"What's under the hill?\\ \textcolor{basalt60}{We can't see inside.}",
    r"the unknown --- a property that lives in space, $Z(x)$"))

# 3 IT VARIES
b="".join(block(cc,r,f"g{grade[r,cc]}",opacity=0.30,lw=0.3) for r in range(H) for cc in range(W) if rock(cc,r))
b+=surface_path(color="basalt60")
# highlight a rich and a poor block far apart
hr,hc=2,6; pr,pc=5,11
for (rr,cc,name,col,acc) in [(hr,hc,"RICH","g5","ferrous"),(pr,pc,"POOR","g0","azure")]:
    x,y=cell_xy(cc,rr)
    b+=f"  \\fill[{col}] ({x:.2f},{y:.2f}) rectangle ({x+CW:.2f},{y+CH:.2f});\n"
    b+=f"  \\draw[basalt,line width=1.4pt] ({x:.2f},{y:.2f}) rectangle ({x+CW:.2f},{y+CH:.2f});\n"
    b+=lbl(x+CW/2,y+CH+0.12,name,acc,11,"dispBlack")
P.append(page("FIG.02 --- IT VARIES","ACT I",b,
    r"Some rock is rich. Some is poor.\\ \textcolor{basalt60}{It changes from place to place.}",
    r"spatial variability --- the value differs everywhere"))

# 4 WE DRILL
b="".join(block(cc,r,"ground",outline="basalt60",lw=0.0) for r in range(H) for cc in range(W) if rock(cc,r))
b+=surface_path()
for cc in sample_cols: b+=drillhole(cc)
P.append(page("FIG.03 --- WE DRILL","ACT I",b,
    r"We can't dig it all up.\\ \textcolor{basalt60}{So we drill a few holes.}",
    r"sampling --- a sparse set of observations"))

# 5 DEEP & SHALLOW (one big core)
b=""
bx=8.2; bw=1.6; ytop=12.0; bandh=1.05; cc=5; rr=[r for r in range(H) if rock(cc,r)]
yy=ytop
for r in rr:
    b+=f"  \\fill[g{grade[r,cc]}] ({bx:.2f},{yy-bandh:.2f}) rectangle ({bx+bw:.2f},{yy:.2f});\n"
    b+=f"  \\draw[casing,line width=0.6pt] ({bx:.2f},{yy-bandh:.2f}) rectangle ({bx+bw:.2f},{yy:.2f});\n"
    yy-=bandh
b+=f"  \\draw[casing,line width=1.4pt] ({bx:.2f},{yy:.2f}) rectangle ({bx+bw:.2f},{ytop:.2f});\n"
b+=lbl(bx-0.4,ytop-0.1,"shallow","basalt60",9,"mono",anchor="north east")
b+=lbl(bx-0.4,yy+0.1,"deep","basalt60",9,"mono",anchor="south east")
b+=f"  \\draw[basalt60,line width=0.9pt,-{{Triangle[length=3mm]}}] ({bx-0.5:.2f},{ytop-0.3:.2f}) -- ({bx-0.5:.2f},{yy+0.3:.2f});\n"
P.append(page("FIG.04 --- DEEP \\& SHALLOW","ACT I",b,
    r"Go down a hole ---\\ \textcolor{basalt60}{the colours change with depth.}",
    r"down-hole assays --- each interval of core is its own sample"))

# 5b THE LOUD ROCK (capping)
b=""
vals=[1.3,1.9,1.1,5.4,1.5,1.0,1.7]; loud=3
nb=len(vals); bw=0.95; gp=0.55; tot=nb*bw+(nb-1)*gp; bx0=(18-tot)/2; yb=4.8; capy=yb+2.3
b+=f"  \\draw[basalt,line width=1.0pt] ({bx0-0.4:.2f},{yb:.2f}) -- ({bx0+tot+0.4:.2f},{yb:.2f});\n"
for i,v in enumerate(vals):
    x=bx0+i*(bw+gp); col="ferrous" if i==loud else "azure"
    if i==loud:
        b+=f"  \\fill[{col},opacity=0.20] ({x:.2f},{capy:.2f}) rectangle ({x+bw:.2f},{yb+v:.2f});\n"
        b+=f"  \\fill[{col}] ({x:.2f},{yb:.2f}) rectangle ({x+bw:.2f},{capy:.2f});\n"
        b+=f"  \\draw[basalt,line width=0.8pt] ({x:.2f},{yb:.2f}) rectangle ({x+bw:.2f},{yb+v:.2f});\n"
        b+=f"  \\draw[basalt,line width=1.4pt,-{{Triangle[length=3.4mm]}}] ({x+bw/2:.2f},{yb+v+0.1:.2f}) -- ({x+bw/2:.2f},{capy+0.18:.2f});\n"
        b+=lbl(x+bw/2,yb+v+0.25,"turn it down","basalt",9,"monoB")
    else:
        b+=f"  \\fill[{col}] ({x:.2f},{yb:.2f}) rectangle ({x+bw:.2f},{yb+v:.2f});\n"
        b+=f"  \\draw[basalt,line width=0.6pt] ({x:.2f},{yb:.2f}) rectangle ({x+bw:.2f},{yb+v:.2f});\n"
b+=f"  \\draw[basalt,line width=1.0pt,dash pattern=on 3pt off 3pt] ({bx0-0.4:.2f},{capy:.2f}) -- ({bx0+tot+0.4:.2f},{capy:.2f});\n"
b+=lbl(bx0+tot+0.4,capy+0.1,"cap","basalt",8,"mono",anchor="south east")
P.append(page("FIG.05 --- THE LOUD ROCK","ACT I",b,
    r"One rock shouts a giant number.\\ \textcolor{basalt60}{Do we believe it --- or turn it down?}",
    r"capping / top-cut --- taming an extreme value so one sample can't dominate"))

# 6 MOSTLY MYSTERY (optional)
b="".join(block(cc,r,"ground",outline="basalt60",lw=0.0) for r in range(H) for cc in range(W) if rock(cc,r))
b+=surface_path()
for cc in sample_cols: b+=drillhole(cc)
for (cc,rr) in [(3,3),(7,4),(11,3),(0,5)]:
    if rock(cc,rr):
        x,y=cell_xy(cc,rr)
        b+=lbl(x+CW/2,y+0.18,"?","basalt60",16,"dispBlack")
P.append(page("FIG.05 --- MOSTLY MYSTERY","ACT I",b,
    r"A few holes. A big hill.\\ \textcolor{basalt60}{Mostly a guess.}",
    r"the estimation problem --- much to predict, little data"))

# ===== ACT II =====
P.append(divider("II","HOW THE GROUND HANGS TOGETHER","spatial correlation, and the curve that measures it","ferrous"))

# 7 FAIR PLAY (stationarity)
b=""
for gx in range(5):
    for gy in range(4):
        ox=3.2+gx*2.3; oy=5.6+gy*1.5
        b+=f"  \\fill[g3] ({ox:.2f},{oy:.2f}) rectangle ({ox+0.7:.2f},{oy+0.7:.2f});\n"
        b+=f"  \\fill[g1] ({ox+0.8:.2f},{oy:.2f}) rectangle ({ox+1.5:.2f},{oy+0.7:.2f});\n"
        b+=f"  \\draw[basalt60,line width=0.4pt] ({ox:.2f},{oy:.2f}) rectangle ({ox+1.5:.2f},{oy+0.7:.2f});\n"
P.append(page("FIG.06 --- FAIR PLAY","ACT II",b,
    r"We pretend the hill keeps\\ \textcolor{basalt60}{the same habits all over.}",
    r"stationarity --- the rules of variation are assumed the same everywhere"))

# 8 NEAR
b=""
b+=f"  \\fill[g3] (6.6,9.0) rectangle (8.1,10.5);\\draw[basalt,line width=1.2pt] (6.6,9.0) rectangle (8.1,10.5);\n"
b+=f"  \\fill[g3] (8.3,9.0) rectangle (9.8,10.5);\\draw[basalt,line width=1.2pt] (8.3,9.0) rectangle (9.8,10.5);\n"
b+=f"  \\draw[basalt,line width=1.2pt,decorate,decoration={{brace,amplitude=6pt,mirror}}] (6.6,8.8) -- (9.8,8.8);\n"
b+=lbl(8.2,7.9,"MATCH!","teal",17,"dispBlack")
P.append(page("FIG.07 --- NEAR","ACT II",b,
    r"Rocks close together\\ \textcolor{basalt60}{are alike.}",
    r"spatial correlation --- Tobler's first law of geography"))

# 9 FAR
b=""
b+=f"  \\fill[g4] (3.0,9.0) rectangle (4.5,10.5);\\draw[basalt,line width=1.2pt] (3.0,9.0) rectangle (4.5,10.5);\n"
b+=f"  \\fill[g0] (13.5,9.0) rectangle (15.0,10.5);\\draw[basalt,line width=1.2pt] (13.5,9.0) rectangle (15.0,10.5);\n"
b+=f"  \\draw[basalt60,line width=1.0pt,dash pattern=on 2.6pt off 2.6pt] (4.6,9.75) -- (13.4,9.75);\n"
b+=lbl(9.0,10.8,"NOT SO MUCH","ferrous",15,"dispBlack")
P.append(page("FIG.08 --- FAR","ACT II",b,
    r"Rocks far apart?\\ \textcolor{basalt60}{Not so much.}",
    r"correlation fades as separation grows"))

# 10 TOUCHING (nugget)
b=""
b+=f"  \\fill[g3] (6.4,9.0) rectangle (8.4,11.0);\\draw[basalt,line width=1.2pt] (6.4,9.0) rectangle (8.4,11.0);\n"
b+=f"  \\fill[g2] (8.4,9.0) rectangle (10.4,11.0);\\draw[basalt,line width=1.2pt] (8.4,9.0) rectangle (10.4,11.0);\n"
b+=f"  \\draw[ferrous,line width=2pt] (8.4,9.0) -- (8.4,11.0);\n"
b+=lbl(8.4,8.7,"still a tiny bit different","ferrous",10,"dispSemi",anchor="north")
P.append(page("FIG.09 --- TOUCHING","ACT II",b,
    r"Side by side,\\ \textcolor{basalt60}{they still aren't \emph{exactly} the same.}",
    r"the nugget --- variability that survives even at zero distance"))

# 11 FORGETTING (range)
b=""
ax=2.8; ay=9.0; bs=1.0
b+=f"  \\fill[g3] ({ax:.2f},{ay:.2f}) rectangle ({ax+bs:.2f},{ay+bs:.2f});\\draw[basalt,line width=1.0pt] ({ax:.2f},{ay:.2f}) rectangle ({ax+bs:.2f},{ay+bs:.2f});\n"
gaps=[0.35,0.7,1.2,1.8,2.4]; tints=["g3","g3","g4","g1","g0"]
cursor=ax+bs; rngmark=cursor
for i,(g,col) in enumerate(zip(gaps,tints)):
    x=cursor+g
    b+=f"  \\fill[{col}] ({x:.2f},{ay:.2f}) rectangle ({x+bs:.2f},{ay+bs:.2f});\\draw[basalt60,line width=0.8pt] ({x:.2f},{ay:.2f}) rectangle ({x+bs:.2f},{ay+bs:.2f});\n"
    if i==2: rngmark=x+bs+gaps[3]/2
    cursor=x+bs
b+=f"  \\draw[basalt,line width=1.2pt,dash pattern=on 3pt off 3pt] ({rngmark:.2f},{ay-0.5:.2f}) -- ({rngmark:.2f},{ay+bs+0.6:.2f});\n"
b+=lbl(rngmark,ay+bs+0.7,"the range","basalt",10,"monoB")
b+=lbl(ax+bs/2,ay-0.3,"anchor","basalt60",8,"mono",anchor="north")
P.append(page("FIG.10 --- FORGETTING","ACT II",b,
    r"Far enough apart,\\ \textcolor{basalt60}{rocks forget each other.}",
    r"the range --- the distance beyond which there is no correlation"))

# 12 BIGGEST GAP (sill)
b=""
b+=f"  \\fill[g0] (3.0,9.0) rectangle (4.8,10.8);\\draw[basalt,line width=1.2pt] (3.0,9.0) rectangle (4.8,10.8);\n"
b+=f"  \\fill[g5] (13.2,9.0) rectangle (15.0,10.8);\\draw[basalt,line width=1.2pt] (13.2,9.0) rectangle (15.0,10.8);\n"
b+=f"  \\draw[basalt,line width=1.0pt,{{Triangle[length=3mm]}}-{{Triangle[length=3mm]}}] (4.9,9.9) -- (13.1,9.9);\n"
b+=lbl(9.0,11.0,"as different as it gets","basalt",13,"dispBlack")
P.append(page("FIG.11 --- THE BIGGEST GAP","ACT II",b,
    r"All the way apart =\\ \textcolor{basalt60}{the biggest difference there is.}",
    r"the sill --- the total variance, reached at the range"))

# 13 COUNT THE PAIRS
b=""
row=grade[H-1]; sw=1.05; sx=(18-W*sw)/2; y0=8.6; y1=y0+1.2
for c in range(W):
    x=sx+c*sw
    b+=f"  \\fill[g{row[c]}] ({x:.2f},{y0:.2f}) rectangle ({x+sw:.2f},{y1:.2f});\\draw[basalt60,line width=0.4pt] ({x:.2f},{y0:.2f}) rectangle ({x+sw:.2f},{y1:.2f});\n"
# a close pair and a far pair brace under
def under(c1,c2,txt,col,yb):
    xa=sx+c1*sw+sw/2; xb=sx+c2*sw+sw/2
    s=f"  \\draw[{col},line width=1.2pt,decorate,decoration={{brace,amplitude=5pt,mirror}}] ({xa:.2f},{yb:.2f}) -- ({xb:.2f},{yb:.2f});\n"
    s+=lbl((xa+xb)/2,yb-0.6,txt,col,9,"monoB",anchor="north")
    return s
b+=under(2,3,"close: tiny gap","teal",y0-0.2)
b+=under(2,10,"far: big gap","ferrous",y0-1.5)
P.append(page("FIG.12 --- COUNT THE PAIRS","ACT II",b,
    r"Pick two rocks. How far? How different?\\ \textcolor{basalt60}{Again. And again.}",
    r"lag pairs --- the experimental variogram is built from every pair"))

# 14 THE DIFFERENCE CURVE (variogram)
b=""
# experimental semivariogram along rows
z=grade_stat.astype(float); gam=[]
for h in range(1,7):
    d=z[:,:-h]-z[:,h:]; gam.append(0.5*np.mean(d*d))
sill=max(gam); rng=4.0; nug=0.12*sill
ax0,ay0,axw,ayh=4.6,5.2,9.0,4.8; hmax=6.0; ymax=1.15*sill
def MX(h): return ax0+ (h/hmax)*axw
def MY(g): return ay0+ (g/ymax)*ayh
b+=f"  \\draw[basalt,line width=1.2pt,-{{Triangle[length=3mm]}}] ({ax0:.2f},{ay0:.2f}) -- ({ax0+axw+0.6:.2f},{ay0:.2f});\n"
b+=f"  \\draw[basalt,line width=1.2pt,-{{Triangle[length=3mm]}}] ({ax0:.2f},{ay0:.2f}) -- ({ax0:.2f},{ay0+ayh+0.5:.2f});\n"
b+=lbl(ax0+axw+0.6,ay0-0.15,"how far apart","basalt60",8,"mono",anchor="north east")
b+=f"  \\node[anchor=south,rotate=90,text=basalt60] at ({ax0-0.35:.2f},{ay0+ayh/2:.2f}) {{\\mono\\fontsize{{8}}{{10}}\\selectfont {('diferença' if PT else 'how different')}}};\n"
# sill line + range tick
b+=f"  \\draw[basalt60,line width=0.8pt,dash pattern=on 3pt off 3pt] ({ax0:.2f},{MY(sill):.2f}) -- ({ax0+axw:.2f},{MY(sill):.2f});\n"
b+=lbl(ax0+axw,MY(sill)+0.1,"sill","basalt60",8,"mono",anchor="south east")
b+=f"  \\draw[basalt60,line width=0.8pt,dash pattern=on 3pt off 3pt] ({MX(rng):.2f},{ay0:.2f}) -- ({MX(rng):.2f},{MY(sill):.2f});\n"
b+=lbl(MX(rng),ay0-0.15,"range","basalt60",8,"mono",anchor="north")
b+=f"  \\fill[ferrous] ({ax0:.2f},{MY(nug):.2f}) circle (0.07); "+lbl(ax0-0.15,MY(nug),"nugget","ferrous",8,"mono",anchor="east")
# model curve (spherical)
def sph(h):
    if h>=rng: return 1.0
    t=h/rng; return 1.5*t-0.5*t**3
pts=[]
hh=0.0
while hh<=hmax+1e-6:
    g=nug+(sill-nug)*sph(hh); pts.append((MX(hh),MY(g))); hh+=0.15
b+=f"  \\draw[teal,line width=2pt] "+" -- ".join(f"({x:.2f},{y:.2f})" for x,y in pts)+";\n"
# experimental points
for i,g in enumerate(gam):
    b+=f"  \\fill[basalt] ({MX(i+1):.2f},{MY(g):.2f}) circle (0.10);\n"
P.append(page("FIG.13 --- THE DIFFERENCE CURVE","ACT II",b,
    r"Close pairs barely differ. Far pairs differ a lot.\\ \textcolor{basalt60}{Draw it --- that's the curve!}",
    r"the variogram $\gamma(h)$ --- nugget at the start, climbing to the sill at the range"))

# 14b A CHOICE OF CURVE (the model is a choice)
b=""
z2=grade_stat.astype(float); gam2=[0.5*float(np.mean((z2[:,:-hh]-z2[:,hh:])**2)) for hh in range(1,7)]
sill2=max(gam2); nug2=0.12*sill2
cx0,cy0,cw0,ch0=4.6,5.2,9.0,4.8; hmx=6.0; ymx=1.15*sill2
def CMX(h): return cx0+(h/hmx)*cw0
def CMY(g): return cy0+(g/ymx)*ch0
b+=f"  \\draw[basalt,line width=1.2pt,-{{Triangle[length=3mm]}}] ({cx0:.2f},{cy0:.2f}) -- ({cx0+cw0+0.6:.2f},{cy0:.2f});\n"
b+=f"  \\draw[basalt,line width=1.2pt,-{{Triangle[length=3mm]}}] ({cx0:.2f},{cy0:.2f}) -- ({cx0:.2f},{cy0+ch0+0.5:.2f});\n"
b+=lbl(cx0+cw0+0.6,cy0-0.15,("distância" if PT else "how far apart"),"basalt60",8,"mono",anchor="north east")
def sphM(h,rng):
    if h>=rng: return 1.0
    t=h/rng; return 1.5*t-0.5*t**3
def expM(h,rng): return 1-math.exp(-3*h/rng)
def curveM(fn,rng,sill,nug,color,lw,op):
    pts=[]; hh=0.0
    while hh<=hmx+1e-6:
        gg=nug+(sill-nug)*fn(hh,rng); pts.append((CMX(hh),CMY(gg))); hh+=0.15
    return f"  \\draw[{color},line width={lw}pt,opacity={op:.2f}] "+" -- ".join(f"({x:.2f},{y:.2f})" for x,y in pts)+";\n"
b+=curveM(sphM,5.2,sill2*1.05,nug2*0.3,"basalt60",1.4,0.5)
b+=curveM(expM,3.6,sill2,nug2*2.4,"basalt60",1.4,0.5)
b+=curveM(sphM,4.0,sill2,nug2,"teal",2.4,1.0)
for i,gg in enumerate(gam2):
    b+=f"  \\fill[basalt] ({CMX(i+1):.2f},{CMY(gg):.2f}) circle (0.10);\n"
b+=lbl(CMX(5.5),CMY(sill2*0.74),("esta!" if PT else "this one"),"teal",10,"dispBlack")
P.append(page("FIG.14 --- A CHOICE OF CURVE","ACT II",b,
    r"Many smooth lines fit the dots.\\ \textcolor{basalt60}{We choose one --- that's our call.}",
    r"the variogram model is a choice --- nugget, range and shape are decisions, not facts"))

# 15 WITH THE GRAIN (anisotropy)
b=""
ctr=(9,8.6)
b+=f"  \\draw[basalt,line width=1.4pt] ({ctr[0]:.2f},{ctr[1]:.2f}) ellipse (4.6 and 1.7);\n"
b+=f"  \\fill[basalt] ({ctr[0]:.2f},{ctr[1]:.2f}) circle (0.13);\n"
b+=f"  \\draw[teal,line width=2pt,-{{Triangle[length=3mm]}}] ({ctr[0]:.2f},{ctr[1]:.2f}) -- ({ctr[0]+4.4:.2f},{ctr[1]:.2f});\n"
b+=f"  \\draw[ferrous,line width=2pt,-{{Triangle[length=3mm]}}] ({ctr[0]:.2f},{ctr[1]:.2f}) -- ({ctr[0]:.2f},{ctr[1]+1.55:.2f});\n"
b+=lbl(ctr[0]+2.3,ctr[1]+0.15,"alike farther","teal",9,"monoB")
b+=lbl(ctr[0]+0.2,ctr[1]+1.1,"less far","ferrous",9,"monoB",anchor="west")
P.append(page("FIG.14 --- WITH THE GRAIN","ACT II",b,
    r"Follow the grain and rocks\\ \textcolor{basalt60}{stay alike farther.}",
    r"anisotropy --- the range depends on direction"))

# ===== ACT III =====
P.append(divider("III","THE\\\\GUESS","filling the gaps, the fairest way --- kriging","azure"))

T=(9.0,9.4)
def srock(x,y,fill,s=0.92,op=1.0,outline="basalt",lw=1.0):
    return (f"  \\fill[{fill},opacity={op:.2f}] ({x-s/2:.2f},{y-s/2:.2f}) rectangle ({x+s/2:.2f},{y+s/2:.2f});\n"
            f"  \\draw[{outline},line width={lw}pt,opacity={op:.2f}] ({x-s/2:.2f},{y-s/2:.2f}) rectangle ({x+s/2:.2f},{y+s/2:.2f});\n")
def tgt(fill=None):
    s=1.12
    if fill:
        return (f"  \\fill[{fill}] ({T[0]-s/2:.2f},{T[1]-s/2:.2f}) rectangle ({T[0]+s/2:.2f},{T[1]+s/2:.2f});\n"
                f"  \\draw[basalt,line width=1.4pt] ({T[0]-s/2:.2f},{T[1]-s/2:.2f}) rectangle ({T[0]+s/2:.2f},{T[1]+s/2:.2f});\n")
    return (f"  \\fill[bone] ({T[0]-s/2:.2f},{T[1]-s/2:.2f}) rectangle ({T[0]+s/2:.2f},{T[1]+s/2:.2f});\n"
            f"  \\draw[basalt,line width=1.3pt,dash pattern=on 3pt off 3pt] ({T[0]-s/2:.2f},{T[1]-s/2:.2f}) rectangle ({T[0]+s/2:.2f},{T[1]+s/2:.2f});\n"
            f"  \\node[text=basalt60] at ({T[0]:.2f},{T[1]:.2f}) {{\\dispBlack\\fontsize{{24}}{{24}}\\selectfont ?}};\n")
def arr(frm,color,lw,so=0.62,eo=0.78,head=4.0,op=1.0,dashed=False):
    dx,dy=T[0]-frm[0],T[1]-frm[1];L=math.hypot(dx,dy);ux,uy=dx/L,dy/L
    sx,sy_=frm[0]+ux*so,frm[1]+uy*so; ex,ey=T[0]-ux*eo,T[1]-uy*eo
    d=",dash pattern=on 2pt off 2pt" if dashed else ""
    return (f"  \\draw[{color},line width={lw}pt,opacity={op:.2f}{d},-{{Triangle[length={head:.1f}mm,width={head*1.4:.1f}mm]}}] ({sx:.2f},{sy_:.2f}) -- ({ex:.2f},{ey:.2f});\n")
A=(6.5,9.4);A2=(4.4,9.4);Bf=(13.8,12.0);Lon=(6.0,6.2);Cl=[(11.6,6.5),(12.4,6.3),(12.0,7.0)]

# 16 ONE BLOCK
b=""
b+=srock(6.0,9.4,"g4",s=1.4)+lbl(6.0,10.25,"hole","basalt60",8,"mono")
b+=srock(13.0,9.4,"g1",s=1.4)+lbl(13.0,10.25,"hole","basalt60",8,"mono")
b+=tgt()
b+=f"  \\draw[basalt60,line width=0.8pt,dash pattern=on 2pt off 2pt] (6.7,8.5) -- ({T[0]-0.6:.2f},8.5);\n"+lbl((6.7+T[0]-0.6)/2,8.4,"near","basalt60",8,"mono",anchor="north")
b+=f"  \\draw[basalt60,line width=0.8pt,dash pattern=on 2pt off 2pt] ({T[0]+0.6:.2f},8.5) -- (12.3,8.5);\n"+lbl((T[0]+0.6+12.3)/2,8.4,"far","basalt60",8,"mono",anchor="north")
P.append(page("FIG.15 --- ONE BLOCK","ACT III",b,
    r"Here's a block we didn't drill.\\ \textcolor{basalt60}{What's inside?}",
    r"estimation --- predicting a value where we have no sample"))

# 17 WHO VOTES
b=""
cast=[(A,"g4"),(A2,"g5"),(Bf,"g1"),(Lon,"g1")]+[(c,"g3") for c in Cl]
for pt,_ in cast:
    d=math.hypot(T[0]-pt[0],T[1]-pt[1]);lw=max(1.0,5.2-d*0.7)
    b+=arr(pt,"basalt60",lw,op=0.8)
for pt,col in cast: b+=srock(*pt,col)
b+=tgt()
P.append(page("FIG.16 --- WHO VOTES","ACT III",b,
    r"Ask the rocks around it.\\ \textcolor{basalt60}{The closer ones speak louder.}",
    r"distance weighting --- nearer samples carry more weight"))

# 18 THE BLEND
b=""
b+=srock(6.0,9.4,"g4",s=1.4)+srock(13.0,9.4,"g1",s=1.4)
b+=tgt(fill="g3")
b+=f"  \\draw[basalt60,line width=1.0pt,-{{Triangle[length=2.6mm]}}] ({T[0]-0.05:.2f},10.2) -- ({T[0]-0.8:.2f},10.2);\n"
b+=lbl(T[0],10.35,"GUESS","basalt",8,"monoB")
P.append(page("FIG.17 --- THE BLEND","ACT III",b,
    r"Mix the votes.\\ \textcolor{basalt60}{The guess leans to the nearer hole.}",
    r"a weighted average --- the estimate at the block"))

# 19 THE FAIREST BLEND (kriging)
b=""
cast2=[(A,"g4",6.0),(Bf,"g1",2.2),(Lon,"g1",4.5)]+[(c,"g3",1.6) for c in Cl]
for pt,_,lw in cast2: b+=arr(pt,"azure",lw,op=0.9)
for pt,col,_ in cast2: b+=srock(*pt,col)
b+=tgt()
b+=f"  \\node[anchor=north east,text=azure,inner sep=1pt] at (16.6,15.4) {{\\dispBlack\\fontsize{{13}}{{14}}\\selectfont $\\gamma(h)$}};\n"
b+=lbl(15.6,14.7,"shares the votes","azure",8,"mono",anchor="north east")
P.append(page("FIG.18 --- THE FAIREST BLEND","ACT III",b,
    r"Use the difference curve\\ \textcolor{basalt60}{to share the votes \emph{just} right.}",
    r"kriging --- the best linear unbiased estimate, weights from $\gamma(h)$"))

# 20 HOW SURE
b="".join(block(cc,r,f"g{grade[r,cc]}",opacity=conf[cc],outline="basalt60",lw=0.4) for r in range(H) for cc in range(W) if rock(cc,r))
for cc in sample_cols:
    for r in range(H):
        if rock(cc,r):
            x,y=cell_xy(cc,r); b+=f"  \\draw[basalt,line width=1.0pt] ({x:.2f},{y:.2f}) rectangle ({x+CW:.2f},{y+CH:.2f});\n"
b+=surface_path()
P.append(page("FIG.19 --- HOW SURE","ACT III",b,
    r"Near holes: sure. Far away: fuzzy.\\ \textcolor{basalt60}{Every block gets a fuzziness.}",
    r"the kriging variance --- an uncertainty for each estimate"))

# ===== ACT IV =====
P.append(divider("IV","MANY\\\\GROUNDS","why one guess isn't enough --- simulation","g4"))

# 21 TOO SMOOTH
sm=simulate(7,9); rg=simulate(7,2)
b=panel(2.2,6.0,6.2,4.6,sm)+lbl(5.3,5.7,"OUR GUESS","basalt",10,"monoB",anchor="north")
b+=panel(9.6,6.0,6.2,4.6,rg)+lbl(12.7,5.7,"REAL ROCK","basalt",10,"monoB",anchor="north")
P.append(page("FIG.20 --- TOO SMOOTH","ACT IV",b,
    r"Our one best guess is\\ \textcolor{basalt60}{gentle and blurry. Real rock is rougher.}",
    r"kriging smooths --- because it takes the safe middle of every block's range"))

# ----- simulation mechanism (maybes -> roll -> write down) -----
scand=[1,2,3,4,5]; sheight=[0.7,1.5,2.3,1.5,0.7]; spick=3
ssx0=7.4; sstep=1.55; sssz=1.0; sy_sw=5.7; sy_bar=6.55
def sim_sw(hi=None):
    s=""
    for i,(gv,hh) in enumerate(zip(scand,sheight)):
        x=ssx0+i*sstep
        s+=f"  \\fill[basalt60,opacity=0.30] ({x-0.32:.2f},{sy_bar:.2f}) rectangle ({x+0.32:.2f},{sy_bar+hh:.2f});\n"
        lw=1.0; oc="basalt"
        if hi is not None and i==hi: lw=2.4; oc="azure"
        s+=f"  \\fill[g{gv}] ({x-sssz/2:.2f},{sy_sw-sssz/2:.2f}) rectangle ({x+sssz/2:.2f},{sy_sw+sssz/2:.2f});\n"
        s+=f"  \\draw[{oc},line width={lw}pt] ({x-sssz/2:.2f},{sy_sw-sssz/2:.2f}) rectangle ({x+sssz/2:.2f},{sy_sw+sssz/2:.2f});\n"
    return s
def sim_die(x,y,sz=1.0):
    s_=f"  \\draw[basalt,fill=bone,line width=1.4pt,rounded corners=3pt] ({x-sz/2:.2f},{y-sz/2:.2f}) rectangle ({x+sz/2:.2f},{y+sz/2:.2f});\n"
    for px,py in [(-0.25,0.25),(0.25,0.25),(0,0),(-0.25,-0.25),(0.25,-0.25)]:
        s_+=f"  \\fill[basalt] ({x+px*sz:.2f},{y+py*sz:.2f}) circle (0.08);\n"
    return s_
def sim_tb(x,y,sz,fill=None):
    if fill:
        return (f"  \\fill[{fill}] ({x-sz/2:.2f},{y-sz/2:.2f}) rectangle ({x+sz/2:.2f},{y+sz/2:.2f});\n"
                f"  \\draw[basalt,line width=1.4pt] ({x-sz/2:.2f},{y-sz/2:.2f}) rectangle ({x+sz/2:.2f},{y+sz/2:.2f});\n")
    return (f"  \\fill[bone] ({x-sz/2:.2f},{y-sz/2:.2f}) rectangle ({x+sz/2:.2f},{y+sz/2:.2f});\n"
            f"  \\draw[basalt,line width=1.3pt,dash pattern=on 3pt off 3pt] ({x-sz/2:.2f},{y-sz/2:.2f}) rectangle ({x+sz/2:.2f},{y+sz/2:.2f});\n"
            f"  \\node[text=basalt60] at ({x:.2f},{y:.2f}) {{\\dispBlack\\fontsize{{20}}{{20}}\\selectfont ?}};\n")

# MANY MAYBES
b=sim_tb(3.4,8.6,1.7)+sim_sw()
b+=lbl(ssx0+2*sstep, sy_sw-sssz/2-0.25,"the safe middle","basalt60",8,"mono",anchor="north")
b+=f"  \\draw[basalt60,line width=1.0pt,-{{Triangle[length=3mm]}}] (4.35,8.6) -- ({ssx0-sssz/2-0.3:.2f},7.1);\n"
b+=lbl(ssx0+2*sstep, sy_bar+2.6,"could be any of these","basalt",11,"dispSemi")
P.append(page("FIG.21 --- MANY MAYBES","ACT IV",b,
    r"At each block the guess isn't one colour ---\\ \textcolor{basalt60}{it's a range of maybes.}",
    r"the conditional distribution: centred on the kriged guess, as wide as the kriging fuzziness"))

# ROLL THE DICE
b=sim_tb(3.4,8.6,1.7,fill=f"g{scand[spick]}")+sim_sw(hi=spick)+sim_die(3.4,11.4)
b+=f"  \\draw[azure,line width=1.6pt,-{{Triangle[length=3.4mm]}}] ({ssx0+spick*sstep:.2f},{sy_bar+sheight[spick]+0.2:.2f}) -- ({ssx0+spick*sstep:.2f},{sy_bar+sheight[spick]+1.1:.2f});\n"
b+=lbl(ssx0+spick*sstep, sy_bar+sheight[spick]+1.2,"picked!","azure",10,"dispBlack")
b+=lbl(3.4,8.6-1.05,"this block","basalt60",8,"mono",anchor="north")
P.append(page("FIG.22 --- ROLL THE DICE","ACT IV",b,
    r"Don't always take the safe middle.\\ \textcolor{basalt60}{Roll the dice --- pick one.}",
    r"simulation draws a value from that bell instead of its mean --- that is the roughness coming back"))

# WRITE IT DOWN
b=""
wxs=[3.6,6.6,9.6,12.6]; wyb=9.0; wsz=1.6
b+=sim_tb(wxs[0],wyb,wsz,fill=f"g{scand[spick]}")
b+=lbl(wxs[0],wyb+wsz/2+0.2,"now a peek","teal",9,"monoB")
ckx=wxs[0]+1.05; cky=wyb+wsz/2+0.28
b+=f"  \\draw[teal,line width=2.2pt] ({ckx-0.18:.2f},{cky:.2f}) -- ({ckx-0.03:.2f},{cky-0.17:.2f}) -- ({ckx+0.24:.2f},{cky+0.20:.2f});\n"
for x in wxs[1:]: b+=sim_tb(x,wyb,wsz)
b+=f"  \\draw[basalt,line width=1.4pt,-{{Triangle[length=4mm]}}] ({wxs[0]+wsz/2+0.1:.2f},{wyb:.2f}) -- ({wxs[1]-wsz/2-0.1:.2f},{wyb:.2f});\n"
b+=lbl((wxs[0]+wxs[1])/2,wyb-0.2,"next!","basalt",9,"monoB",anchor="north")
P.append(page("FIG.23 --- WRITE IT DOWN","ACT IV",b,
    r"Your pick counts now.\\ \textcolor{basalt60}{On to the next block --- and the next.}",
    r"sequential simulation: each drawn value becomes data for the next, preserving the texture"))

# 22 DREAM MANY HILLS
b=""
for i,sd in enumerate([11,23,31]):
    ox=1.9+i*5.0; b+=panel(ox,7.2,4.4,3.6,simulate(sd,3))
    b+=lbl(ox+2.2,6.9,f"{('colina' if PT else 'hill')} {i+1}","basalt60",8,"mono",anchor="north")
P.append(page("FIG.21 --- DREAM MANY HILLS","ACT IV",b,
    r"Real rock is rough.\\ \textcolor{basalt60}{So we dream up lots of possible hills.}",
    r"geostatistical simulation --- many equally-likely realizations"))

# 23 ALL FIT THE HOLES
b=""
sc=[1,5,9]
for i,sd in enumerate([11,23,31]):
    ox=1.9+i*5.0; a=simulate(sd,3)
    for cc in sc: a[:,cc]=grade[:,cc]
    b+=panel(ox,7.2,4.4,3.6,a,hi_cols=sc)
P.append(page("FIG.22 --- ALL FIT THE HOLES","ACT IV",b,
    r"Every dreamed hill\\ \textcolor{basalt60}{still matches the holes we drilled.}",
    r"conditional simulation --- realizations honour the data exactly"))

# 24 A SPREAD OF ANSWERS
b=""
tots=[int(simulate(sd,3).sum()) for sd in range(40,80)]
import numpy as _np
hist,edges=_np.histogram(tots,bins=7)
bx0=4.0;bw=1.5;baseY=6.0;hmaxv=max(hist)
for i,hh in enumerate(hist):
    x=bx0+i*bw; ht=0.4+ (hh/hmaxv)*4.2
    b+=f"  \\fill[azure,opacity=0.8] ({x:.2f},{baseY:.2f}) rectangle ({x+bw*0.8:.2f},{baseY+ht:.2f});\n"
    b+=f"  \\draw[basalt,line width=0.5pt] ({x:.2f},{baseY:.2f}) rectangle ({x+bw*0.8:.2f},{baseY+ht:.2f});\n"
meanx=bx0+ (len(hist)/2)*bw
b+=f"  \\draw[ferrous,line width=2pt,dash pattern=on 3pt off 3pt] ({meanx:.2f},{baseY-0.2:.2f}) -- ({meanx:.2f},{baseY+4.9:.2f});\n"
b+=lbl(meanx,baseY+5.0,"the guess $\\approx$ the average","ferrous",9,"monoB")
b+=f"  \\draw[basalt,line width=1.0pt] ({bx0-0.2:.2f},{baseY:.2f}) -- ({bx0+len(hist)*bw:.2f},{baseY:.2f});\n"
b+=lbl(bx0+len(hist)*bw/2,baseY-0.3,"how much metal?","basalt60",8,"mono",anchor="north")
P.append(page("FIG.23 --- A SPREAD OF ANSWERS","ACT IV",b,
    r"Many hills $\rightarrow$ many answers.\\ \textcolor{basalt60}{Now we know our range.}",
    r"uncertainty from realizations --- their average tracks the kriged estimate"))

# ===== ACT V =====
P.append(divider("V","BLOCKS \\& DECISIONS","support, cutoffs, checking, and where to dig","teal"))

# 25 BIG CALM, SMALL WILD (support)
fine=grade
coarse=np.zeros((H//1, W//2),dtype=int)
for cc in range(W//2):
    coarse[:,cc]=np.clip(np.round(grade[:,2*cc:2*cc+2].mean(axis=1)).astype(int),0,LEVELS-1)
b=panel(2.2,6.0,6.2,4.6,coarse)+lbl(5.3,5.7,"BIG BLOCKS --- calm","basalt",9,"monoB",anchor="north")
b+=panel(9.6,6.0,6.2,4.6,fine)+lbl(12.7,5.7,"TINY BLOCKS --- wild","basalt",9,"monoB",anchor="north")
P.append(page("FIG.24 --- BIG CALM, SMALL WILD","ACT V",b,
    r"Big blocks are calm.\\ \textcolor{basalt60}{Tiny blocks are wild.}",
    r"support / the volume--variance effect --- larger volumes vary less"))

# 26 PICK A LINE (cutoff)
cut=3
b=""
for r in range(H):
    for cc in range(W):
        if rock(cc,r):
            if grade[r,cc]>=cut: b+=block(cc,r,f"g{grade[r,cc]}",lw=0.5)
            else: b+=block(cc,r,"waste",lw=0.4)
b+=surface_path()
b+=lbl(9,3.4,"rich = dig   ·   pale = leave","basalt",10,"monoB")
P.append(page("FIG.25 --- PICK A LINE","ACT V",b,
    r"Rich enough to dig?\\ \textcolor{basalt60}{Yes, or no.}",
    r"cutoff grade --- an indicator splits ore from waste"))

# 27 WORTH IT (grade-tonnage)
b=""
ore=0
for r in range(H):
    for cc in range(W):
        if rock(cc,r):
            if grade[r,cc]>=cut:
                b+=block(cc,r,f"g{grade[r,cc]}",lw=0.5); ore+=1
                x,y=cell_xy(cc,r); b+=f"  \\draw[basalt,line width=1.0pt] ({x:.2f},{y:.2f}) rectangle ({x+CW:.2f},{y+CH:.2f});\n"
            else: b+=block(cc,r,"waste",opacity=0.5,lw=0.3)
b+=surface_path()
b+=lbl(9,3.3,(f"{ore} blocos para cavar" if PT else f"{ore} blocks worth digging"),"ferrous",11,"dispBlack")
P.append(page("FIG.26 --- WORTH IT","ACT V",b,
    r"Count the blocks\\ \textcolor{basalt60}{worth digging.}",
    r"grade--tonnage --- how much rock sits above the cutoff"))

# 28 CHECK OUR WORK (cross-validation)
b=""
tc,tr=5,2; true_v=grade[tr,tc]; guess_v=min(LEVELS-1,max(0,true_v-1))
b+=srock(6.2,9.2,f"g{true_v}",s=1.7)+lbl(6.2,10.4,"TRUE (hidden)","basalt",9,"monoB")
b+=srock(11.0,9.2,f"g{guess_v}",s=1.7)+lbl(11.0,10.4,"OUR GUESS","azure",9,"monoB")
b+=f"  \\node[text=teal] at (8.6,9.2) {{\\dispBlack\\fontsize{{34}}{{34}}\\selectfont $\\approx$}};\n"
b+=lbl(8.6,7.7,"close!","teal",13,"dispBlack")
P.append(page("FIG.27 --- CHECK OUR WORK","ACT V",b,
    r"Hide a hole. Guess it.\\ \textcolor{basalt60}{Were we close?}",
    r"cross-validation --- leave one out, predict it, measure the error"))

# 29 WHERE TO DIG
best=None
for r in range(H):
    for cc in range(W):
        if rock(cc,r):
            k=(grade[r,cc],-abs(cc-(W-1)/2))
            if best is None or k>best[0]: best=(k,cc,r)
_,dc,dr=best
b="".join(block(cc,r,f"g{grade[r,cc]}",lw=0.5) for r in range(H) for cc in range(W) if rock(cc,r))
b+=surface_path()
bx,by=cell_xy(dc,dr);bxc=bx+CW/2;byc=by+CH/2
b+=f"  \\draw[basalt,line width=2.4pt] ({bx+0.18:.2f},{by+0.18:.2f}) -- ({bx+CW-0.18:.2f},{by+CH-0.18:.2f});\n"
b+=f"  \\draw[basalt,line width=2.4pt] ({bx+0.18:.2f},{by+CH-0.18:.2f}) -- ({bx+CW-0.18:.2f},{by+0.18:.2f});\n"
b+=f"  \\draw[basalt,line width=1.6pt] ({bxc:.2f},{byc:.2f}) circle (0.62);\n"
tx=cx(dc);ty=sy(tx)
b+=f"  \\draw[casing,line width=1.0pt] ({tx:.2f},{byc:.2f}) -- ({tx:.2f},{ty+0.6:.2f});\n  \\fill[basalt] ({tx:.2f},{ty+0.6:.2f}) circle (0.11);\n"
b+=lbl(tx,ty+0.78,"DIG","basalt",8,"monoB")
P.append(page("FIG.28 --- WHERE TO DIG","ACT V",b,
    r"Now we know the best spot ---\\ \textcolor{basalt60}{and how sure we are.}",
    r"the decision --- a block model turned into a plan"))

# ===== ACT VI BONUS =====
P.append(divider("VI","BONUS","for the grown-up reading along --- two kriging quirks","ferrous"))

# 30 DECLUSTERING
b=""
cxm=sum(c[0] for c in Cl)/3; cym=sum(c[1] for c in Cl)/3
b+=f"  \\draw[basalt,line width=1.1pt,dash pattern=on 2.5pt off 2.5pt] ({cxm:.2f},{cym:.2f}) ellipse (1.25 and 1.05);\n"
for c in Cl: b+=f"  \\draw[basalt60,line width=0.8pt,opacity=0.5] ({c[0]:.2f},{c[1]:.2f}) -- ({cxm:.2f},{cym:.2f});\n"
for c in Cl: b+=srock(*c,"g3",s=0.8)
b+=arr((cxm,cym),"ferrous",4.0,so=1.15)+arr(Lon,"teal",4.0)
b+=srock(*Lon,"g1")+tgt()
b+=lbl(cxm,cym+1.3,"ONE SHARED SAY","ferrous",11,"dispBlack")
b+=lbl(Lon[0],Lon[1]-0.95,"OWN SAY","teal",11,"dispBlack",anchor="north")
P.append(page("BONUS --- DECLUSTERING","ACT VI",b,
    r"A huddle shares one say.\\ \textcolor{basalt60}{The lonely rock isn't drowned out.}",
    r"declustering --- kriging splits redundant clustered weight"))

# 31 SCREEN EFFECT
b=""
dx,dy=T[0]-A2[0],T[1]-A2[1];L2=math.hypot(dx,dy);ux,uy=dx/L2,dy/L2
bxp,byp=A[0]-ux*0.66,A[1]-uy*0.66
b+=f"  \\draw[basalt60,line width=2.0pt,opacity=0.55,dash pattern=on 2pt off 2pt,-{{Triangle[length=2.6mm,width=3.2mm]}}] ({A2[0]+ux*0.62:.2f},{A2[1]+uy*0.62:.2f}) -- ({bxp:.2f},{byp:.2f});\n"
b+=arr(A,"teal",6.0)+srock(*A2,"g5",op=0.55)+srock(*A,"g4")+tgt()
b+=lbl(A2[0],A2[1]+0.62,"BEHIND","basalt60",8,"monoB")+lbl(A2[0],A2[1]-0.62,"blocked","basalt60",9,"dispSemi",anchor="north")
b+=lbl(A[0],A[1]+0.62,"IN FRONT","teal",9,"monoB")
P.append(page("BONUS --- SCREEN EFFECT","ACT VI",b,
    r"A rock in front\\ \textcolor{basalt60}{blocks the one behind it.}",
    r"the screen effect --- a shadowed sample's weight collapses (it can even go negative)"))

# ===== GLOSSARY =====
if PT:
    GLOSS=[("variável regionalizada","valor que depende de onde você está"),
      ("amostra","uma espiada medida no terreno"),
      ("testemunho","a rocha trazida ao longo do furo"),
      ("estacionariedade","supor que as regras de variação valem em todo lugar"),
      ("correlação espacial","coisas perto tendem a ser parecidas"),
      ("variograma","a curva de diferença versus distância"),
      ("pepita","variabilidade que sobra até na distância zero"),
      ("alcance","distância além da qual não há correlação"),
      ("patamar","a variabilidade total, atingida no alcance"),
      ("anisotropia","correlação que alcança mais longe em certas direções"),
      ("krigagem","a melhor estimativa ponderada, via variograma"),
      ("variância de krigagem","a incerteza de cada estimativa"),
      ("suporte","volumes maiores variam menos (volume--variância)"),
      ("simulação","muitos terrenos que respeitam os dados"),
      ("realização","um desses terrenos possíveis"),
      ("desagrupamento","repartir o peso de amostras amontoadas"),
      ("efeito de tela","amostra perto sombreia uma mais distante"),
      ("teor de corte","a linha entre minério e estéril"),
      ("validação cruzada","esconder uma amostra, prever e conferir o erro"),
      ("capping","domar um valor extremo (outlier)"),
      ("tendência","uma deriva suave e ampla no teor")]
    gtitle="GLOSSÁRIO"; gsub="as palavras de verdade, pro adulto"
else:
    GLOSS=[("regionalized variable","a value that depends on where you are"),
      ("sample","one measured peek at the ground"),
      ("core","the rock pulled up along a drillhole"),
      ("stationarity","assuming the rules of variation hold everywhere"),
      ("spatial correlation","near things tend to be alike"),
      ("variogram","the curve of difference versus distance"),
      ("nugget","variability left even at zero distance"),
      ("range","the distance beyond which there's no correlation"),
      ("sill","the total variability, reached at the range"),
      ("anisotropy","correlation reaching farther in some directions"),
      ("kriging","the best weighted estimate, using the variogram"),
      ("kriging variance","the uncertainty attached to each estimate"),
      ("support","bigger volumes vary less (volume--variance)"),
      ("simulation","many possible grounds that fit the data"),
      ("realization","one such possible ground"),
      ("declustering","sharing the weight of bunched-up samples"),
      ("screen effect","a near sample shadowing a farther one"),
      ("cutoff grade","the line between ore and waste"),
      ("cross-validation","hide a sample, predict it, check the error"),
      ("capping / top-cut","taming an extreme outlier value"),
      ("trend","a smooth, large-scale drift in grade")]
    gtitle="GLOSSARY"; gsub="the real words, for the grown-up"
g=r"\begin{tikzpicture}[x=1cm,y=1cm]\scaffold\header{"+gtitle+r"}{$\cdot$}"+"\n"
g+=lbl(1.2,15.4,gsub,"basalt60",8,"mono",anchor="north west")
half=(len(GLOSS)+1)//2; colx=[1.3,9.2]; topy=14.4; dyg=1.22
for ci in range(2):
    for k,(term,defn) in enumerate(GLOSS[ci*half:(ci+1)*half]):
        yy=topy-k*dyg
        g+=f"  \\node[anchor=north west,text=basalt,inner sep=0pt,text width=7.4cm] at ({colx[ci]:.2f},{yy:.2f}) {{\\monoB\\fontsize{{8}}{{10}}\\selectfont {term}}};\n"
        g+=f"  \\node[anchor=north west,text=basalt60,inner sep=0pt,text width=7.4cm] at ({colx[ci]:.2f},{yy-0.42:.2f}) {{\\mono\\fontsize{{7}}{{8.5}}\\selectfont {defn}}};\n"
g+=r"\end{tikzpicture}\clearpage"
P.append(g)

# ===== REFERENCES =====
REFS=[
 r"W. Tobler (1970). A computer movie simulating urban growth in the Detroit region. Economic Geography 46: 234--240.",
 r"G. Matheron (1971). The Theory of Regionalized Variables and Its Applications. Cahiers du CMM, Fontainebleau.",
 r"A. Journel \& C. Huijbregts (1978). Mining Geostatistics. Academic Press.",
 r"E. Isaaks \& R. Srivastava (1989). An Introduction to Applied Geostatistics. Oxford Univ. Press.",
 r"N. Cressie (1993). Statistics for Spatial Data. Wiley.",
 r"P. Goovaerts (1997). Geostatistics for Natural Resources Evaluation. Oxford Univ. Press.",
 r"C. Deutsch \& A. Journel (1998). GSLIB: Geostatistical Software Library. Oxford Univ. Press.",
 r"H. Wackernagel (2003). Multivariate Geostatistics, 3rd ed. Springer.",
 r"J.-P. Chilès \& P. Delfiner (2012). Geostatistics: Modeling Spatial Uncertainty, 2nd ed. Wiley.",
 r"M. Rossi \& C. Deutsch (2014). Mineral Resource Estimation. Springer.",
]
rtitle="PARA APRENDER MAIS" if PT else "TO LEARN MORE"
rsub=("a prateleira do adulto --- em ordem cronológica" if PT else "the grown-up's shelf --- in chronological order")
rr=r"\begin{tikzpicture}[x=1cm,y=1cm]\scaffold\header{"+rtitle+r"}{$\cdot$}"+"\n"
rr+=lbl(1.2,15.4,rsub,"basalt60",8,"mono",anchor="north west")
yref=13.9
for ref in REFS:
    rr+=f"  \\node[anchor=north west,text=basalt,inner sep=0pt,text width=15.2cm] at (1.3,{yref:.2f}) {{\\mono\\fontsize{{8.5}}{{12}}\\selectfont {ref}}};\n"
    yref-=1.16
rr+=r"\end{tikzpicture}\clearpage"
P.append(rr)

# ===== COLOPHON =====
if PT:
    _cl1=r"Um tour completo de geoestatística para os bem pequenos e os apenas curiosos: a gente não vê o terreno, então faz uns furos, mede como a rocha se liga, adivinha o resto do jeito mais justo e --- porque um palpite só é arrumado demais --- sonha vários terrenos possíveis pra saber o quanto temos certeza."
    _cl2=r"\textbf{Como ler este livro:} a frase grande é pra ler em voz alta. A linha pequena \textcolor{basalt60}{// nomeia} a ideia de verdade, pro adulto."
    _cl3=r"FIELD KIT No.01 --- ``O Que Tem Embaixo da Colina?''\\ Geoscientific Chaos Union $\cdot$ domínio público (CC0) $\cdot$ terreno simulado da semente 7\\ Barlow \& Space Mono $\cdot$ desenhado em Ti\,kZ $\cdot$ prova, ainda não imposta para impressão"
else:
    _cl1=r"A complete tour of geostatistics for the very young and the merely curious: we cannot see the ground, so we drill a few holes, measure how the rock hangs together, guess the rest the fairest way, and --- because one guess is too tidy --- dream up many possible grounds to learn how sure we really are."
    _cl2=r"\textbf{How to read this book:} the big line is to say out loud. The small \textcolor{basalt60}{// line} names the real idea, for the grown-up."
    _cl3=r"FIELD KIT No.01 --- ``What's Under the Hill?''\\ Geoscientific Chaos Union $\cdot$ public domain (CC0) $\cdot$ ground simulated from seed 7\\ Barlow \& Space Mono $\cdot$ drawn in Ti\,kZ $\cdot$ proof edition, not yet imposed for print"
col=r"\begin{tikzpicture}[x=1cm,y=1cm]\scaffold\header{"+("COLOFÃO" if PT else "COLOPHON")+r"}{$\cdot$}"+"\n"
col+=r"  \node[anchor=north west,align=left,text=basalt,inner sep=0pt,text width=15.4cm] at (1.3,13.8) {\dispSemi\fontsize{14}{18}\selectfont "+_cl1+r"};"+"\n"
col+=r"  \node[anchor=south west,align=left,text=basalt,inner sep=0pt,text width=15.4cm] at (1.3,3.0) {\mono\fontsize{8}{12}\selectfont "+_cl2+r"};"+"\n"
col+=r"  \node[anchor=south west,align=left,text=basalt60,inner sep=0pt,text width=15.4cm] at (1.3,1.2) {\mono\fontsize{8}{12}\selectfont "+_cl3+r"};"+"\n"
col+=r"\end{tikzpicture}"
P.append(col)

# --- bleed/trim pass: scale each 18-unit (180mm) design to 210mm trim,
#     centre on a 220mm page, flood matching bg into the 5mm bleed ring ---
def wrap_bleed(pg):
    cp = pg.endswith(r"\clearpage")
    inner = pg[:-len(r"\clearpage")] if cp else pg
    bg = "basalt" if r"\fill[basalt] (0,0) rectangle (18,18)" in inner else "bone"
    out = (r"\noindent\begin{tikzpicture}[x=1mm,y=1mm]\fill["+bg+r"] (0,0) rectangle (220,220);"
           r"\node[inner sep=0pt] at (110,110) {\resizebox{210mm}{210mm}{"+inner+r"}};"
           r"\end{tikzpicture}")
    return out + (r"\clearpage" if cp else "")
# ---- front matter (mirrors Playback: half-title, frontispiece, title, copyright+dedication verso) ----
_FM_TITLE = "O QUE TEM EMBAIXO DA COLINA?" if PT else "WHAT'S UNDER THE HILL?"
_FM_SUB   = (r"geoestatística para os bem pequenos --- e o adulto curioso" if PT
             else r"geostatistics for the very young --- and the curious grown-up")
_FM_FRONTCAP = r"o chão, antes da pergunta" if PT else r"the ground, before we ask"
_FM_DED = (r"Para toda criança que já se perguntou\\ o que tem embaixo da colina."
           if PT else r"For every kid who ever wondered\\ what's under the hill.")
_FM_ISBN = r"ISBN [ a ser atribuído ]" if PT else r"ISBN [ to be assigned ]"
_FM_FICHA = r"[ ficha catalográfica --- CBL ]"
if PT:
    _FM_CR = (r"Escrito e ilustrado por Arthur Endlein Correia.\\[4pt] Primeira edição --- Belo Horizonte, 2026.\\ Geoscientific Chaos Union.\\[4pt] "
              + _FM_ISBN + r"\\[4pt] "
              r"Este livro é livre. O texto e as figuras estão sob CC0; o código é MIT. Copie, imprima, modifique, venda.\\[4pt] "
              r"Composto em Barlow e Space Mono (SIL Open Font License). Reconstrói, idêntico, a partir de fieldkit\_full.py e da semente aleatória 7.")
else:
    _FM_CR = (r"Written and drawn by Arthur Endlein Correia.\\[4pt] First edition --- Belo Horizonte, 2026.\\ Geoscientific Chaos Union.\\[4pt] "
              + _FM_ISBN + r"\\[4pt] "
              r"This book is free. The text and figures are released under CC0; the code is MIT. Copy it, print it, remix it, sell it.\\[4pt] "
              r"Set in Barlow and Space Mono (SIL Open Font License). Rebuilds, identically, from fieldkit\_full.py and random seed 7.")

def _fm_open(): return r"\begin{tikzpicture}[x=1cm,y=1cm]\scaffold"+"\n"
def _fm_close(): return r"\end{tikzpicture}\clearpage"

fm_half = (_fm_open()
  + r"  \node[text=basalt60] at (9,10.5) {\mono\fontsize{9}{11}\selectfont FIELD KIT \textcolor{basalt}{$\cdot$} No.01};"+"\n"
  + r"  \node[text=basalt,align=center,text width=15cm] at (9,9.2) {\dispBlack\fontsize{18}{21}\selectfont "+_FM_TITLE+r"};"+"\n"
  + _fm_close())

fm_front = (_fm_open()
  + r"  \foreach \i in {0,...,5}{\foreach \j in {0,...,3}{\fill[g\i] ({6+\i},{7+\j}) rectangle ++(0.96,0.96);}}"+"\n"
  + r"  \node[text=basalt60] at (9,5.5) {\mono\fontsize{7.5}{9}\selectfont "+_FM_FRONTCAP+r"};"+"\n"
  + _fm_close())

fm_title = (_fm_open()
  + r"  \node[text=basalt60] at (9,13.4) {\mono\fontsize{9}{11}\selectfont FIELD KIT \textcolor{basalt}{$\cdot$} No.01};"+"\n"
  + r"  \node[text=basalt,align=center,text width=15.5cm] at (9,11.6) {\dispBlack\fontsize{30}{32}\selectfont "+_FM_TITLE+r"};"+"\n"
  + r"  \draw[ferrous,line width=1.2pt] (6.8,9.95) -- (11.2,9.95);"+"\n"
  + r"  \node[text=basalt60,align=center,text width=14cm] at (9,9.1) {\mono\fontsize{9}{12}\selectfont "+_FM_SUB+r"};"+"\n"
  + r"  \foreach \i in {0,...,5}{\fill[g\i] ({6.9+\i*0.7},6.55) rectangle ++(0.64,0.64);}"+"\n"
  + r"  \node[text=basalt] at (9,4.7) {\dispSemi\fontsize{12}{14}\selectfont Arthur Endlein Correia};"+"\n"
  + r"  \node[text=basalt] at (9,3.3) {\monoB\fontsize{9}{11}\selectfont GEOSCIENTIFIC CHAOS UNION};"+"\n"
  + r"  \node[text=basalt60] at (9,2.6) {\mono\fontsize{8}{10}\selectfont Belo Horizonte \textcolor{basalt}{$\cdot$} 2026};"+"\n"
  + _fm_close())

fm_cr = (_fm_open()
  + r"  \node[text=basalt,align=center,text width=13cm] at (9,13.2) {\dispSemi\fontsize{11}{15}\selectfont "+_FM_DED+r"};"+"\n"
  + r"  \node[anchor=north west,align=left,text=basalt,inner sep=0pt,text width=14.6cm] at (1.7,9.4) {\mono\fontsize{8}{12.5}\selectfont "+_FM_CR+r"};"+"\n"
  + r"  \draw[basalt60,line width=0.4pt,dash pattern=on 2pt off 2pt] (1.7,1.6) rectangle (16.3,4.2);"+"\n"
  + r"  \node[text=basalt60] at (9,2.9) {\mono\fontsize{8}{10}\selectfont "+_FM_FICHA+r"};"+"\n"
  + _fm_close())

# cover art now opens the book as the illustrated title page; lean front matter
cover_page = P.pop(0)
P = [cover_page, fm_cr] + P

P=[wrap_bleed(p) for p in P]

import re
body="\n".join(P)
_n=[0]
def _ren(m):
    _n[0]+=1; return f"FIG.{_n[0]:02d}"
body=re.sub(r"FIG\.\d+", _ren, body)
out = "fieldkit_full_pt" if PT else "fieldkit_full"
with open(out+".tex","w") as fh:
    fh.write(PRE+body+"\n\\end{document}\n")
print("lang:",LANG,"pages:",len(P),"figs:",_n[0],"->",out+".tex")
