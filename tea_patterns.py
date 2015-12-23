# coding: utf-8

import re
import regex


PATTERNS = []

SUURTAHED = "A-ZÕÄÖÜ"
VAIKETAHED = "a-zõäöü"

# '<s>   1.   </s> <s>' --> '<s> 1.'
PATT_1 = re.compile(r'''
    <s>\s+     # lause algus
    (\d+)\s*   # vähemalt 1 number
    \.\s+      # punkt
    </s>\s<s>  # lause lõpp ja uue algus
''', re.X)
PATT_1_REPLACE = r'<s> \1.'


# '2. 4. 6. </s> <s> 1. ' --> '2.4.6.1. '
# '2. 4. 6. </s> <s> ' --> '2.4.6. '
# '2. 4. 6. ' --> '2.4.6. '
# '2. 4. ' --> '2.4. '
PATT_2 = regex.compile(r'''
    (?P<algus><s>\s)
    (?P<a>\d+\.)\s?     # numbrid, millele võib järgneda tühik
    (?P<b>\d+\.)\s?     # numbrid, millele võib järgneda tühik
    ((?P<c>\d+\.)\s?)?  # numbrid, millele võib järgneda tühik või mitte midagi
    ((?P<d>\d+\.)\s?)?  #
    (</s>\s<s>\s?)?     # lause lõpp ja algus või mitte midagi
    (?P<e>(\d+\.|\s\w+)\s)
''', regex.X)
PATT_2_REPLACE = r'\g<algus>\g<a>\g<b>\g<c>\g<d>\g<e>'



# '20 000' --> '20_000'
PATT_3 = re.compile(r'''
    (\s\d+)  # tühik, millele järgnevad numbrid
    \s       # tühik
    (\d+\s)  # numbrid, millele järgneb tühik
''', re.X)
PATT_3_REPLACE = r'\1<+/>\2'



# "20 %ga " --> "20%ga"
PATT_4 = re.compile(r'''
    (\d+)\s        # numbrid, millele järgneb tühik
    (              # grupi 2 algus
        %          # protsendimärk
        [^\s]*     # 0 või rohkem mittetühikut
        \s         # tühik
    )              # grupi 2 lõpp
''', re.X)
PATT_4_REPLACE = r'\1\2'



# " AS -le " --> " AS-le "
# ' koera" -ga ' --> ' koera"-ga '
# "4000 -le" "4000-le"
# "1,75 -ni " --> "1,75-ni"
PATT_5 = re.compile(r'''
    (\s[%s]{2}| [\"\”\'\]§0-9)])  # lühend (nt AS) või jutumärk, kaldkriips, § või arv
    \s                        # tühik kahe grupi vahel
    ([-–][a-z]{1,3}([0-9])?\s)         # kuni kolmetäheline käändelõpp
''' % SUURTAHED, re.X)
PATT_5_REPLACE = r'\1\2'



# "Teatriankeet ... </s> <s> 2001 " --> "Teatriankeet_..._2001 "
PATT_6 = re.compile(r'''
    ([^\s]+)\s\.\.\.   # kolmele punktile
    \s</s>\s<s>\s      # järgneb lause lõpu ja alguse märk
    ([^\s]+\s)         # mille järgi tulevad numbrid, nt aastaarv
''', re.X)
PATT_6_REPLACE = r'\1<+/>...<+/>\2'

#1 ... </s> <s> 34 --> 1...34
# 60 ... </s> <s> 70 --> 60...70
PATT_41 = re.compile(r'''
    (\d)\s(\.\.\.|…)\s</s>\s<s>\s([0-9])
''', re.X)
PATT_41_REPLACE = r'\1\2\3'


# " 100.5 ... 140,74°C" --> " 100.5_..._140,74°C"
# " 0,96 ... 1 " --> " 0,96_..._1 "
PATT_7 = re.compile(r'''
    (\s\d+[\.,\+]?\d*)   # täis- või murdarv
    \s(\.\.\.?|…)\s            # vahemiku tähistus
    (\d+[,\.\+]?[^\s]*)  # täis- või murdarv (võimalik, te tühikuga)
''', re.X)
PATT_7_REPLACE = r'\1<+/>\2<+/>\3'



# "123 , 123" --> "123,123"

PATT_8 = re.compile(r'''
    (\d+)          # ujukomaarv, kus komakoha
    \s?(,)\s?  # eraldaja ümber on
    (\d+)          # tühikud
''', re.X)
PATT_8_REPLACE = r'\1\2\3'

PATT_36 = re.compile(r'''
    ([0-9]{4})\s(\.\s)
''', re.X)
PATT_36_REPLACE = r'\1\2'


# "8 - 16%" --> "8-16%"

PATT_37 = re.compile(r'''
    ([0-9]+)\s?
    ([–-])\s?
    ([0-9]+%?)
''', re.X)
PATT_37_REPLACE = r'\1\2\3'

# "15. 04. 2005" --> "15.04.2005"
PATT_33 = re.compile(r'''
    (\d+)\s?    # arv
    \.\s?     # eraldaja ümber on tühikud
    (\d+)\s?    # arv
    \.\s?     # eraldaja ümber on tühikud
    (\d+\s?)    # arv
''', re.X)
PATT_33_REPLACE = r'\1.\2.\3'


# "( 123a )" --> "(123a)"
# "( a )" --> "(a)"; "( 1 )" --> "(1)"; "( 1a )" --> "(1a)"
PATT_9 = re.compile(r'''
    \(\s         # sulud algavad
    (\d*[a-z]?)  # loetelu sulgude sees
    \s\)         # sulud lõpevad
''', re.X)
PATT_9_REPLACE = r'(\1)'

PATT_38 = re.compile(r'''
    (<ignore>\s<ignore>\s)
    (\(\s?([A-ZÕÜÖÄ]+|[a-zõüöä][a-zõüöä]?)(\/[^\s]+)?\s?\))
    (\s</ignore>\s</ignore>)
''', re.X)
PATT_38_REPLACE = r'<ignore> \2 </ignore>'



# " 1 ), 1a ), 12b )" --> " 1), 1a), 12b)"
PATT_10 = re.compile(r'''
    (\s\d*[%s]?)  # loetelu nummerdus, nt 1, 1a, 12b,
    \s\)           # millele järgneb tühik ja sulg
''' % VAIKETAHED, re.X)
PATT_10_REPLACE = r'\1)'



# "p &gt" --> "p&gt"
PATT_11 = re.compile(r'''
    ([^\s]*)   # mistahes mittetühik
    \s         # kuni tühik
    (&[^\s]*)  # ampersand ja kogu järgnev tühikuni
''', re.X)
PATT_11_REPLACE = r'\1\2'



# "( Finck , 1979 ; Kuldkepp , 1994)" --> "<ignore> ( Finck , 1979 ; Kuldkepp , 1994) </ignore>"
# "( vt tabel 2 )" --> "<ignore> ( vt tabel 2 ) </ignore>"
_reference_year = r'''
    \s?\d+,?\s?[a-zõüöäA-ZÕÜÖÄ%'\]!]*  # arv (aasta)
    (/\d+)?[-']?\s               # valikuline kaldkriipsuga aastaarv
    (                       # valikulise grupi 2 algus
        :\s                 # koolon
        \d+                 # arvud, nt lk nr
        ([-–]\d+[\.,]?)\s     # kuni-märk ja arvud, nt lk 5-6
    )?                      # grupi 2 lõpp
    \w*\s?                     # lõpus tühik
'''
PATT_12 = regex.compile(r'''
    (\([^\)]+\))?
    (\(              # viide algab suluga
        (            # viite sees võivad olla
            [^\(\)]  # sümbolid, mis pole sulud
            |        # või
            (?R)     # rekursiivselt analoogiline struktuur
            |
            (?1)
        )*           # 0 või enam korda
        {end}        # viide lõpeb aastaarvuga
    \))              # viide lõpeb suluga
'''.format(end=_reference_year), regex.X)
PATT_12_REPLACE = r'<ignore> \2 </ignore>'

PATT_BRACS = regex.compile(r'''
    (<ignore>\s)?
    (\(\s
        (
            ([A-ZÕÜÖÄa-zõüöä0-9,-<>[]\/]{1,3}|\+)\s?
            |
            (?R)
        )*
    \s\))
    (\s</ignore>)?
''', regex.X)
PATT_BRACS_REPLACE = r'<ignore> \2 </ignore>'

PATT_REMOVE_NESTED_IGNORES = re.compile(r'''
    (<ignore>[^>]+?)
        <ignore>\s([^>]+?)\s</ignore>
    ([^>]+?</ignore>)
''', re.X)
PATT_REMOVE_NESTED_IGNORES_SUB = r'\1\2\3'


# "/ ... /" --> "/.../"
PATT_13 = re.compile(r'''
    (\/|\()\s         # kaldkriips(/) ja tühik
    (\.\.\.)\s  # vahemik(...) ja tühik
    (\/|\))           # kaldkriips(/)
''', re.X)
PATT_13_REPLACE = r'\1\2\3'



# "60 km / h" --> "60_km/h" ; "2,3 h / m" --> "2,3_h/m"; "110 m/h" --> "110_m/h"
PATT_14 = re.compile(r'''
    (\s?\d+,?\d*)\s  # algab arvuga, mis võib olla täis- või ujukomaarv,
    ([^\s<]{1,3})\s?       # millele järgneb vähemalt ühe korra miskit
    /\s?              # ja millele omakorda järgneb kaldkriips(/)
    ([^\s]{1,3}\s)       # ja millele järgneb omakorda miskit
''', re.X)
PATT_14_REPLACE = r'\1<+/>\2/\3'



# "1884. a." --> "1884.a. "
# "1884 . a" --> "1884.a "
PATT_15 = re.compile(r'''
    (\d+)\s?(\.)\s  # number, mille järel on punkt ja tühik
    (a\.?\s)  # täht a (millele võib järgneda punkt) ja tühik
''', re.X)
PATT_15_REPLACE = r'\1\2\3'


# "2004 a. " --> "2004a."
PATT_27 = re.compile(r'''
    (\d+)\s?  # number, mille järel on punkt ja tühik
    (a\.?\s)  # täht a (millele võib järgneda punkt) ja tühik
''', re.X)
PATT_27_REPLACE = r'\1\2'


# "21. </s> <s> 12. 2001" --> "21.12.2001"
# 15. </s> <s> 11. 1995.a.
PATT_22 = regex.compile(r'''
    (?P<n>\d+\.)\s
    <\/s>\s<s>\s
    (?P<n1>\d+\.\s)
    (?P<n2>\d{4}\.?(\s|a\.\s))?
''', regex.X)
PATT_22_REPLACE = r'\g<n>\g<n1>\g<n2>'


# "1945 . aasta" --> "1945. aasta"
PATT_23 = re.compile(r'''
    (\d+)\s\.
    (\saasta)
''', re.X)
PATT_23_REPLACE = r'\1.\2'


# " ajal. </s>" --> " ajal . </s>"
# " jne. </s> " --> " jne . </s>"
# "50. </s>" --> "50 . </s>"
# "1995.a. </s>" --> "1995.a . </s>"
# "kogu<+/>=<+/></s>" --> "kogu<+/>=<+/> </s>"
_PATT_16_1 = re.compile(r'''
    ((\s|<\+\/>)[%s0-9]+)\.  # sõna, millele järgneb punkt
    ((\s|<\/\+>)</s>)        # lauselõpp
''' % VAIKETAHED, re.X)
_PATT_16_2 = re.compile(r'''
    (<\+\/>)(</s>)
''', re.X)
_PATT_16_3 = re.compile(r'''
    (\s|\.)(a)(\.\s</s>)
''', re.X)

def PATT_16(s):
    while _PATT_16_1.search(s):
        s = _PATT_16_1.sub(r'\1 .\3', s, count=1)
    while _PATT_16_2.search(s):
        s = _PATT_16_2.sub(r'\1 \2', s, count=1)
    while _PATT_16_3.search(s):
        s = _PATT_16_3.sub(r'\1\2 \3', s, count=1)
    return s


# "( -0,09 )" --> "(-0,09)"
# "( 2.13 )" --> "(2.13)"
PATT_17 = re.compile(r'''
    \(\s                # algab suluga
        ([-–]?\d+[\.,]\d+) # (pos või neg) ujukomaarv
    \s\)                # lõppeb suluga
''', re.X)
PATT_17_REPLACE = r' (\1) '


# "A . </s> <s> J. Sjögren" --> "A . J. Sjögren"
# "J. Fr . </s> <s> Blumenbach " --> "J. Fr . Blumenbach"
PATT_19 = re.compile(r'''
    (?![EB]d|[NV]t|I{2,3}|Hz|Mg)                     # ei ole Ed, Bd, Nt, Vt, II, III, Hz
    (\s[^\(\)a-zõüöäY0-9%\$"\)”;:!\]\?\+-][a-zõüöä]?\s?\.\s) # ükskõik mis (va nurksulgude vahelolev) ja järgneb punkt
    </s>\s<s>\s                                        # lauselõpp ja uue algus
    ([A-ZÕÜÖÄ][a-zõüöä]?\.?\s?[A-ZÕÜÖÄ]?[a-zõüöä]+\s)  # eesnime initsiaalid ja lõpuks perenimi
''', re.X)
PATT_19_REPLACE = r'\1\2'


PATT_20_1 = regex.compile(r'''
    ([A-ZÕÜÖÄ][a-zõüöä]?)   # initsiaalid, millele võib
    \s?\.\s                 # tühikute vahel järgneda punkt
    ([A-ZÕÜÖÄ][a-zõüöä]?)   # initsiaalid, millele võib
    \s?\.\s                 # tühikute vahel järgneda punkt
    ([A-ZÕÜÖÄ][a-zõüöä]+)   # perekonnanimi
''', regex.X)
PATT_20_1_REPLACE = r'\1.\2.<+/>\3'


PATT_20_2 = regex.compile(r'''
    ([A-ZÕÜÖÄ][a-zõüöä]?)   # initsiaalid, millele võib
    \s?\.\s                 # tühikute vahel järgneda punkt
    ([A-ZÕÜÖÄ][a-zõüöä]+)   # perekonnanimi
''', regex.X)
PATT_20_2_REPLACE = r'\1.<+/>\2'


# "294 ha-lt" --> "294<+/>ha-lt"
# "1 ha" ..> "1<+/>ha"
# "1,0 mM" --> "1,0<+/>mM"

# 740 kHz-ni
PATT_21 = re.compile(r'''
    ((<\+\/>)?\d+([,–\.]|<\+\/>)?\d*)\s
    (?!ja|[oO]n|ca\s|\d{4}|a|e\.|ei|ta|me|ka\s|Nr\s|vs\s)
    (([a-zõüöäμ]{1,2}[0-9\.]?%?|[a-zõüöä][A-ZÕÜÖÄ]{1,2}[a-zõüöä]?|[A-ZÕÜÖÄ][a-zõüöä]|[°0o]C|min|mM|μM|MJ)(\s|\s?-[a-zõüöä]{1,2}\s))
''', re.X)
PATT_21_REPLACE = r'\1<+/>\4'


# Y = AY + BX + e 
# "25 x 1,2 x 1,2 x 1,2 x 1,0 x 1,2 x 1,0 x 1,2" --> "25<+/>x<+/>1,2<+/>x<+/>1,2<+/>x<+/>1,2<+/>x<+/>1,0<+/>x<+/>1,2<+/>x<+/>1,0<+/>x<+/>1,2"
# "3 [+-] 3 " --> "3<+/>[+-]<+/>3"
# "108 ± 3.6" --> "108<+/>±<+/>3.6"
# "a 23 a 12" --> "a<+/>23<+/>a<+/>12"

_PATT_24_1= re.compile(r'''
    (\d+[\.,]?|(\s|<\+\/>|\s[A-ZÕÜÖÄ])\s[a-zõüöä](\s|<\+\/>)?|\s[A-ZÕÜÖÄ]\s)\s
    (x|\+|±|-|×)\s?
    (?!\s?ja|\s?l\s|\s?i\s|\s?d\s|\s?KON)
    ((\d+([\.,]\d*)?|[a-zõüöä]|[A-ZÕÜÖÄ]+|[A-ZÕÜÖÄa-zõüöä]{2})(\s|<\+\/>|\.?))
''', re.X)
_PATT_24_2 = re.compile(r'''
    (?!\sca|\sja|\son|\set|\s[lL]k|\ska|\sNr\s)
    ((<\+\/>|\s|\d+)[a-zõüöä]{1,2})\s
    ([a-zõüöä]{1,2}(\)|<\+\/>)|\d+\s)
''', re.X)

def PATT_24(s):
    while _PATT_24_1.search(s):
        s = _PATT_24_1.sub(r'\1<+/>\4<+/>\5', s, count=1)
    while _PATT_24_2.search(s):
        s = _PATT_24_2.sub(r'\1<+/>\3', s, count=1)
    return s

# "0 , 01 " --> " 0,001 "
# "1998. - 2000" --> "1998.-2000"
PATT_26 = re.compile(r'''
    (\d+\.?)\s
    ([–,-])\s?
    (\d+)
''', re.X)
PATT_26_REPLACE = r'\1\2\3'

PATT_27 = re.compile(r'''
    ([xXY]|\s(Mg|Fe|B|Cu|Mn|Zn|Mo|Se)|\sR|\sa|\se|[\s0-9]b|\sC|\sr|\sy)\s
    ((\d+|nn?\s|i\s|\s?y|\s?d\s|m\s|\sC)+\s?)
''', re.X)
PATT_27_REPLACE = r'\1<+/>\3'

# "a 12Y 2" --> "a<+/>12Y<+/>2"
# "b 11 X 1 K" --> "b<+/>11<+/>X<+/>1<+/>K"
PATT_28 = re.compile(r'''
    ([0-9]|y\s?|Y\s?)\s
    (([xXyYC]|\sK|\s?a|\s?d)\s)
''', re.X)
PATT_28_REPLACE = r'\1<+/>\2'

# "1 = a" --> "1_=_a"
PATT_29 = re.compile(r'''
    \s?
    (=)\s
    (-?(\w{,2}|\+|\d+[\.,]?\d*)(\s|<\+\/>))
''', re.X)
PATT_29_REPLACE = r'<+/>\1<+/>\2'

#Hetkel väljakommenteeritud
# '" tegur "'' --> '"tegur"'
PATT_30 = re.compile(r'''
    ([“"])\s
    ([^”"/]+)\s
    ([”"])
''', re.X)
PATT_30_REPLACE = r'\1\2\3'

# "[ du ]"" --> "[du]"
# "[ � , â ]" --> "[� , â]"
PATT_31 =re.compile(r'''
    (\[)\s
    ([^:\]]+)\s
    (\])
''', re.X)
PATT_31_REPLACE = r'\1\2\3'

# [ swi : t ] --> "[swi:t]"
PATT_32 = re.compile(r'''
    (\[)\s
    ([a-zõüöä]+|[0-9]+)\s(\:)\s
    ([a-zõüöä]+|[0-9]+)?\s
    (\])
''', re.X)
PATT_32_REPLACE = r'\1\2\3\4\5'

PATT_34 = re.compile(r'''
    (\()\s
    ([A-ZÕÜÖÄ]+|%)
    \s(\))
''', re.X)
PATT_34_REPLACE = r'<ignore> \1\2\3 </ignore>'


# "<s> Tabel 1. </s> <s> Saagikus" --> <s> Tabel 1. Saagikus"
# "<s> Joonis 23. </s> <s> Mesimuraka" --> "<s> Joonis 23. Mesimuraka"
PATT_35 = re.compile(r'''
    (<s>\s[A-ZÕÜÖÄ][a-zõüöä]+\s[0-9]+([a-z]?|\.[0-9]))\s?
    \.\s</s>\s<s>\s
    ((\d+\.|[A-ZÕÜÖÄ]([a-zõüöä]+|[A-ZÕÜÖÄ]+)?(-?[a-zõüöä]+)?)\s)
''', re.X)
PATT_35_REPLACE = r'\1. \3'


PATT_39 = re.compile(r'''
    (käimas)\s(olev)
''', re.X)
PATT_39_REPLACE = r'\1\2'


PATT_40 = re.compile(r'''
    (ül)\s(dse)
''', re.X)
PATT_40_REPLACE = r'\1\2'


_PATT_42_1= re.compile(r'''
    (\d{4}\.?)(,)(\d{4})
''', re.X)
def PATT_42(s):
    while _PATT_42_1.search(s):
        s = _PATT_42_1.sub(r'\1 \2 \3', s, count=1)
    return s


# "<ignore> ( 2 . </s> <s> 8) </ignore>" --> <ignore> (2 . 8) </ignore>
PATT_43 = regex.compile(r'''
    (?P<algus>\s<ignore>\s\()
    (?P<a>[^<]+)
    </s>\s<s>\s
    (?P<b>[^<]+)?
    (</s>\s<s>\s)?
    (?P<c>[^<]+)?
    (</s>\s<s>\s)?
    (?P<d>[^<]+)?
    (</s>\s<s>\s)?
    (?P<e>[^<]+)?
    (</s>\s<s>\s)?
    (?P<f>[^<]+)?
    (</s>\s<s>\s)?
    (?P<g>[^<]+)?
    (</s>\s<s>\s)?
    (?P<h>[^\)]+)
    (?P<lopp>\)\s</ignore>)
''', regex.X)
PATT_43_REPLACE = r'\g<algus>\g<a>\g<b>\g<c>\g<d>\g<e>\g<f>\g<g>\g<h>\g<lopp>'


# ( x<+/>1 , x<+/>2 , K , x<+/>n)
_PATT_44_1 = re.compile(r'''
    (\(\sx<\+\/>1\s,\sx<\+\/>2\s,\sK\s,\sx<\+\/>n\))
''', re.X)
_PATT_44_2 = re.compile(r'''
    (1-\s-\s-\s5\s6-8-\s10\s11-13\s14-16-\s-\s19-21-\s-\s24\s25-27<\+\/>28<\+\/>29<\+\/>30\s31-33-\s35-37-
    \s-\s-\s-\s-\s43\s44-46\s47-\s-\s-\s51-\s-\s-\s-\sjne)
''', re.X)
# B <ignore> ( 01 ; <ignore> (x) </ignore> ; 0) </ignore> C ( -x ; <ignore> (0) </ignore> ; x)
_PATT_44_3 = re.compile(r'''
    (B\s<ignore>\s)
    (\(\s01\s;\s)<ignore>\s
    (\(x\))\s<\/ignore>
    (\s;\s0\))\s<\/ignore>
    (\sC\s\(\s-x\s;\s)<ignore>
    (\s\(0\)\s)<\/ignore>
    (\s;\sx\))
''', re.X)
# klassikalise e . </s> <s> Batesi
_PATT_44_4 = re.compile(r'''
    (\se)\s(\.\s)<\/s>\s<s>\s
''', re.X)

def PATT_44(s):
    if _PATT_44_1.search(s):
        s = _PATT_44_1.sub(r'<ignore> \1 </ignore>', s)
    if _PATT_44_2.search(s):
        s = _PATT_44_2.sub(r'<ignore> \1 </ignore>', s)
    if _PATT_44_3.search(s):
        s = _PATT_44_3.sub(r'\1\2\3\4\5\6\7 </ignore>', s)
    if _PATT_44_4.search(s):
        s = _PATT_44_4.sub(r'\1\2', s)
    return s

PATT_45 = re.compile(r'''
    (\[(\d+(,\d+)?|[^\s]+)\])
''', re.X)
PATT_45_REPLACE = r'<ignore> \1 </ignore>'



PATTERNS = [
  (PATT_12, PATT_12_REPLACE),
  (PATT_BRACS, PATT_BRACS_REPLACE),
  (PATT_REMOVE_NESTED_IGNORES, PATT_REMOVE_NESTED_IGNORES_SUB),
  (PATT_35, PATT_35_REPLACE),
  (PATT_37, PATT_37_REPLACE),
  (PATT_41, PATT_41_REPLACE),
  (PATT_22, PATT_22_REPLACE),
  (PATT_34, PATT_34_REPLACE),
  (PATT_1, PATT_1_REPLACE),
  (PATT_2, PATT_2_REPLACE),
  (PATT_3, PATT_3_REPLACE),
  (PATT_4, PATT_4_REPLACE),
  (PATT_5, PATT_5_REPLACE),
  (PATT_6, PATT_6_REPLACE),
  (PATT_7, PATT_7_REPLACE),
  (PATT_8, PATT_8_REPLACE),
  (PATT_33, PATT_33_REPLACE),
  (PATT_36, PATT_36_REPLACE),
  (PATT_9, PATT_9_REPLACE),
  (PATT_38, PATT_38_REPLACE),
  (PATT_10, PATT_10_REPLACE),
  (PATT_11, PATT_11_REPLACE),
  (PATT_13, PATT_13_REPLACE),
  (PATT_14, PATT_14_REPLACE),
  (PATT_15, PATT_15_REPLACE),
  (PATT_17, PATT_17_REPLACE),
  (PATT_21, PATT_21_REPLACE),
  (PATT_24, None),
  (PATT_19, PATT_19_REPLACE),
  (PATT_23, PATT_23_REPLACE),
  (PATT_26, PATT_26_REPLACE),
  (PATT_27, PATT_27_REPLACE),
  (PATT_28, PATT_28_REPLACE),
  (PATT_29, PATT_29_REPLACE),
  (PATT_20_1, PATT_20_1_REPLACE),
  (PATT_20_2, PATT_20_2_REPLACE),
  (PATT_16, None),
  (PATT_31, PATT_31_REPLACE),
  (PATT_32, PATT_32_REPLACE),
  (PATT_39, PATT_39_REPLACE),
  (PATT_40, PATT_40_REPLACE),
  (PATT_42, None),
  (PATT_43, PATT_43_REPLACE),
  (PATT_44, None),
  (PATT_45, PATT_45_REPLACE)
]


