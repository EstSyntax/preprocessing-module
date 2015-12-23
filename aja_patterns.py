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


PATT_2 = regex.compile(r'''
    (\(\s[^\s]+\s)
        (<\/s>\s<s>\s)
    ([^\)]+\))
''', regex.X)
PATT_2_REPLACE = r'\1\3'


# '20 000' --> '20<+/>000'
# 40 000-45 000 --> 40<+/>000-45<+/>000
PATT_3 = regex.compile(r'''
    ((\s|\s[\-\+]|<\+\/>)\d+)  # tühik, millele järgnevad numbrid
    \s            # tühik
    (\d+)  # numbrid, millele järgneb tühik
''', regex.X)
PATT_3_REPLACE = r'\1<+/>\3'


PATT_3_1 = regex.compile(r'''
    (\d+<\+/>\d+)\s
    (\d+(<\+/>\d+(<\+/>\d+)?)?)
''', regex.X)
PATT_3_1_REPLACE = r'\1<+/>\2'


# 1 . 58 , 95 --> 1<+/>.<+/>58<+/>,<+/>95
PATT_3_2 = regex.compile(r'''
    (\d+)\s\.\s(\d+)\s,\s(\d+\s)
''', regex.X)
PATT_3_2_REPLACE = r'\1<+/>.<+/>\2<+/>,<+/>\3'


#5<+/>36-st
PATT_46 = re.compile(r'''
    ([0-9])
    <\+\/>
    ([0-9]+-st)
''', re.X)
PATT_46_REPLACE = r'\1 \2'


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


PATT_4_1 = regex.compile(r'''
    (\d+)\s([,\.])\s(\d+[a-zõüöä%]+)
''', regex.X)
PATT_4_1_REPLACE = r'\1\2\3'


# 0,20 -protsendilise --> 0,20-protsendilise
PATT_4_2 = regex.compile(r'''
    (\d)\s(-protsendi[^\s]+\s)
''', regex.X)
PATT_4_2_REPLACE = r'\1\2'


PATT_4_3 = regex.compile(r'''
    (\d+)\s([,\.])\s(\d+(\sning|\sja|\sseku|\smilj|\sminu|\stun|\speal|\stuha|\skorda|\sprotsen|<\+|\svõrra|\skeskmis|\sruutmeet|\s(Rootsi\s)kroon|\s(Saksa\s)?marga|\sdollar|\-[a-zõüöäšž]{1,3}))
''', regex.X)
PATT_4_3_REPLACE = r'\1\2\3'


#  1 , 5 : 0 , 5 --> 1,5<+/>:<+/>0,5
PATT_4_4 = regex.compile(r'''
    (\d+)\s,\s(\d+<\+[^:]+:<\+\/>\d+)\s,\s(\d+)
''', regex.X)
PATT_4_4_REPLACE = r'\1,\2,\3'


# AS -le --> AS-le
# koera" -ga --> koera"-ga
# 4000 -le --> 4000-le
# 1,75 -ni --> "1,75-ni
PATT_5 = re.compile(r'''
    (\s[%s]{2}| [\"\”\'\]§0-9)])  # lühend (nt AS) või jutumärk, kaldkriips, § või arv
    \s                        # tühik kahe grupi vahel
    ([-–][a-z]{1,3}([0-9])?\s)         # kuni kolmetäheline käändelõpp
''' % SUURTAHED, re.X)
PATT_5_REPLACE = r'\1\2'


# 2,0 ... </s> <s> 3,5 --> 2,0<+/>...<+/>3,5
PATT_6 = re.compile(r'''
    ([0-9])\s(\.\.\.|…)   # kolmele punktile
    \s</s>\s<s>\s      # järgneb lause lõpu ja alguse märk
    ([0-9])         # mille järgi tulevad numbrid, nt aastaarv
''', re.X)
PATT_6_REPLACE = r'\1<+/>\2<+/>\3'


# . . .
PATT_6_1 = regex.compile(r'''
    ([0-9])\s\.\s\.\s\.\s
    ([\+\-]?[0-9])
''', regex.X)
PATT_6_1_REPLACE = r'\1<+/>...<+/>\2'


# 0 , 3 . . . </s> <s> 1% --> 0,3<+/>...<+/>1% 
PATT_6_2 = regex.compile(r'''
    ([0-9])\s,\s([0-9])\s\.\s\.\s\.   # kolmele punktile
    \s</s>\s<s>\s      # järgneb lause lõpu ja alguse märk
    ([0-9])         # mille järgi tulevad numbrid, nt aastaarv
''', regex.X)
PATT_6_2_REPLACE = r'\1,\2<+/>...<+/>\3'


# 0 , 3<\+\/>...<\+\/>0,7% --> 0,3<\+\/>...<\+\/>0,7%
PATT_6_3 = regex.compile(r'''
    ([0-9])\s,\s([0-9]+)(<\+\/>\.\.\.|\/[0-9])
''', regex.X)
PATT_6_3_REPLACE = r'\1,\2\3'


PATT_36 = re.compile(r'''
    ([0-9]{4})\s(\.\s)
''', re.X)
PATT_36_REPLACE = r'\1\2'


# 8 - 16% --> "82,0<+/>...<+/>16%
PATT_37 = re.compile(r'''
    ([0-9]+)\s?
    ([–-])\s?
    ([0-9]+%?)
''', re.X)
PATT_37_REPLACE = r'\1<+/>\2<+/>\3'


# ( 123a ) --> (123a)
# ( a ) --> (a); ( 1 ) --> (1); ( 1a ) --> (1a)
PATT_9 = re.compile(r'''
    \(\s         # sulud algavad
    (\d*[a-z]?)  # loetelu sulgude sees
    \s\)         # sulud lõpevad
''', re.X)
PATT_9_REPLACE = r'(\1)'


# 15. 04. 2005 --> 15.04.2005
PATT_33 = re.compile(r'''
    (\d+)\s?    # arv
    \.\s?     # eraldaja ümber on tühikud
    (\d+)\s?    # arv
    \.\s?     # eraldaja ümber on tühikud
    (\d+\s?)    # arv
''', re.X)
PATT_33_REPLACE = r'\1.\2.\3'


PATT_61 = regex.compile(r'''
    (<s>\s)((\d+[a-z]?|[a-zA-Z])\s?\))
''', regex.X)
PATT_61_REPLACE = r'\1<ignore> \2 </ignore>'


# Simon &amp; Schusteri --> Simon<+/>&amp;<+/>Schusteri
PATT_11 = re.compile(r'''
    (\s[^\s]*)   # mistahes mittetühik
    \s         # kuni tühik
    (&amp;)\s  # ampersand ja kogu järgnev tühikuni
    ([^\s]*)
''', re.X)
PATT_11_REPLACE = r'\1<+/>\2<+/>\3'


# ( Finck , 1979 ; Kuldkepp , 1994) --> <ignore> ( Finck , 1979 ; Kuldkepp , 1994) </ignore>
# ( vt tabel 2 )" --> <ignore> ( vt tabel 2 ) </ignore>
_reference_year = r'''
    \s?\d+,?\s?[a-zõüöäA-ZÕÜÖÄ%'"\]!]*  # arv (aasta)
    (/\d+)?[-']?\s               # valikuline kaldkriipsuga aastaarv
    (                       # valikulise grupi 2 algus
        :\s                 # koolon
        \d+                 # arvud, nt lk nr
        ([-–]\d+[\.,]?)\s     # kuni-märk ja arvud, nt lk 5-6
    )?                      # grupi 2 lõpp
    -?\w*\s?                     # lõpus tühik
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


# 60 km / h --> 60<+/>km/h ; 2,3 h / m --> 2,3<+/>h/m; 110 m/h --> 110<+/>m/h
PATT_14 = re.compile(r'''
    (\s?\d+,?\d*)\s  # algab arvuga, mis võib olla täis- või ujukomaarv,
    ([^\s<]{1,3})\s?       # millele järgneb vähemalt ühe korra miskit
    /\s?              # ja millele omakorda järgneb kaldkriips(/)
    ([^\s]{1,3}\s)       # ja millele järgneb omakorda miskit
''', re.X)
PATT_14_REPLACE = r'\1<+/>\2/\3'



# 1884. a." --> "1884.a.
# 1884 . a" --> "1884.a
PATT_15 = re.compile(r'''
    ([0-9][0-9][0-9][0-9])\s?(\.)\s  # aastaarv, mille järel on punkt ja tühik
    (a\.?\s)                         # täht a (millele võib järgneda punkt) ja tühik
''', re.X)
PATT_15_REPLACE = r'\1\2\3'


# 2004 a. --> 2004a.
PATT_27 = re.compile(r'''
    ([0-9][0-9][0-9][0-9])\s?  # number, mille järel on punkt ja tühik
    (a\.?\s)                   # täht a (millele võib järgneda punkt) ja tühik
''', re.X)
PATT_27_REPLACE = r'\1\2'


# 21. </s> <s> 12. 2001 --> 21.12.2001
# 15. </s> <s> 11. 1995.a.
PATT_22 = regex.compile(r'''
    (?P<n>\d+\.)\s
    <\/s>\s<s>\s
    (?P<n1>\d+\.\s)
    (?P<n2>\d{4}\.?(\s|a\.\s))?
''', regex.X)
PATT_22_REPLACE = r'\g<n>\g<n1>\g<n2>'


# 1945 . aasta --> 1945. aasta
PATT_23 = re.compile(r'''
    (\d+)\s\.
    (\saasta)
''', re.X)
PATT_23_REPLACE = r'\1.\2'


# ajal. </s> --> ajal . </s>
# jne. </s> --> jne . </s>
# 50. </s> --> 50 . </s>
# 1995.a. </s> --> 1995.a . </s>
# Eesti konsulaat Tamperes avati 2000.aastal. </s>
_PATT_16_1 = re.compile(r'''
    ((\s|<\+\/>|\.|\/)[a-zõüöäA-ZÕÜÖÄ0-9]+)\.  # sõna, millele järgneb punkt
    ((\s|<\+\/>)<\/s>)        # lauselõpp
''', re.X)
_PATT_16_2 = re.compile(r'''
    (<\+\/>)(<\/s>)
''', re.X)
_PATT_16_3 = re.compile(r'''
    (\s|\.)(a)(\.\s<\/s>)
''', re.X)

def PATT_16(s):
    while _PATT_16_1.search(s):
        s = _PATT_16_1.sub(r'\1 .\3', s, count=1)
    while _PATT_16_2.search(s):
        s = _PATT_16_2.sub(r'\1 \2', s, count=1)
    while _PATT_16_3.search(s):
        s = _PATT_16_3.sub(r'\1\2 \3', s, count=1)
    return s


# A . </s> <s> J. Sjögren --> A . J. Sjögren
# J. Fr . </s> <s> Blumenbach --> J. Fr . Blumenbach
PATT_19 = re.compile(r'''
    (?![EB]d|[NV]t|I{2,3}|Hz|Mg)                     # ei ole Ed, Bd, Nt, Vt, II, III, Hz
    (\s[^\(\)a-zõüöäY0-9%\$"\)”;:!\]\?\+-[^Ei]][a-zõüöä]?\s?\.\s) # ükskõik mis (va nurksulgude vahelolev) ja järgneb punkt
    <\/s>\s<s>\s                                        # lauselõpp ja uue algus
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


# 294 ha-lt --> 294<+/>ha-lt
# 1 ha ..> 1<+/>ha
# 1,0 mM --> 1,0<+/>mM
# 740 kHz-ni
PATT_21 = re.compile(r'''
    ((<\+\/>)?\d+([,–\.]|<\+\/>)?\d*)\s
    (?!ja|[oO]n|ca\s|\d{4}|a|e\.|[Ee]i|ta|me|ka\s|Nr\s|vs\s)
    (([a-zõüöäμ]{1,2}[0-9\.]?%?³?|[a-zõüöä][A-ZÕÜÖÄ]{1,2}[a-zõüöä]?|[A-ZÕÜÖÄ][a-zõüöä]|[°0o]C|C°|min|μM|spl|MHz)(\s|\s?-[a-zõüöä]{1,2}\s))
''', re.X)
PATT_21_REPLACE = r'\1<+/>\4'


# 1998. - 2000 --> "1998.<+/>-<+/>2000
# 1.- 4. --> 1.<+/>-<+/>4.
PATT_26 = re.compile(r'''
    (\d+\.?)\s?
    ([-–])\s?
    (\d+\.?)
''', re.X)
PATT_26_REPLACE = r'\1<+/>\2<+/>\3'


PATT_26_1 = regex.compile(r'''
    (\d+)\s?(\.?)\s?
    ([-–])\s?
    (\d+)\s?(\.?)
''', regex.X)
PATT_26_1_REPLACE = r'\1\2<+/>\3<+/>\4\5'


PATT_34 = re.compile(r'''
    (?<!<s>\s)(\(\s)
    ([A-ZÕÜÖÄ]+|%)
    (\s\))(?!\s<\/s>)
''', re.X)
PATT_34_REPLACE = r'<ignore> \1\2\3 </ignore>'


# <ignore> ( 2 . </s> <s> 8) </ignore> --> <ignore> (2 . 8) </ignore>
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


# Dove 'i --> Dove'i
PATT_44 = re.compile(r'''
    ([A-ZÕÜÖÄ][a-zõüöä]+)\s
    (\'[a-zõüöä]+\s)
''', re.X)
PATT_44_REPLACE = r'\1\2'


# www. </s> <s> esindus.ee/korteriturg --> www.esindus.ee/korteriturg
# www. </s> <s> kavkazcenter.com
PATT_45 = re.compile(r'''
    (www)\.\s<\/s>\s<s>\s
    ([a-zõüöä]+\.)
''', re.X)
PATT_45_REPLACE = r'\1.\2'


PATT_47 = re.compile(r'''
    ([0-9])\s(\.\.\.|…)   # kolmele punktile
    \s(-?[0-9])           # mille järgi tulevad numbrid, nt aastaarv
    \s(,)\s([0-9])
''', re.X)
PATT_47_REPLACE = r'\1\2\3\4\5'


# 0 : 4 --> 0<+/>:<+/>4
PATT_48 = regex.compile(r'''
    ((\s|>)\d+)\s:\s(\d+)
''', regex.X)
PATT_48_REPLACE = r'\1<+/>:<+/>\3'


# <ignore> (FRA) </ignore> <ignore> (13) </ignore> --> <ignore> (FRA) (13) </ignore> 
PATT_49 = regex.compile(r'''
    (?P<a>\s</ignore>\s)
    (?P<b><ignore>)
''', regex.X)
PATT_49_REPLACE = r''


# <ignore> (17) </ignore> , <ignore> (20) </ignore> isa --> <ignore> (17) , (20) </ignore> isa
PATT_50 = regex.compile(r'''
    (?P<a>\s</ignore>\s,\s)
    (?P<b><ignore>)
''', regex.X)
PATT_50_REPLACE = r','


PATT_51 = re.compile(r'''
    ([0-9a-zõüöäA-ZÕÜÖÄ])(<\/ignore>)
''', re.X)
PATT_51_REPLACE = r'\1 \2'


# <ignore> .* </ignore> ja <ignore> .* </ignore> --> <ignore> .* ja .* </ignore>
PATT_52 = regex.compile(r'''
    (?P<a>\s</ignore>\sja\s)
    (?P<b><ignore>)
''', regex.X)
PATT_52_REPLACE = r' ja'


# ( Venemaa ) --> <ignore> ( Venemaa ) </ignore>
# ( Jaapan , Subaru ) --> <ignore> ( Jaapan , Subaru ) </ignore>
PATT_55 =regex.compile(r'''
    ([a-zõüöäA-ZÕÜÖÄ0-9]+\s)(\(\s[A-ZÕÜÖÄ][a-zõüöä]+(-[A-ZÕÜÖÄ][a-zõüöä]+)?\s?(,\s[A-ZÕÜÖÄ][a-zõüöä]+\s)?\)\s)
''', regex.X)
PATT_55_REPLACE = r'\1<ignore> \2</ignore> '


# ( 85 . </s> <s> Antonov ) --> ( 85 . Antonov )
PATT_60 = regex.compile(r'''
    (\(\s[^\s]+\s?\.\s)<\/s>\s<s>\s([^\)]+\))
''', regex.X)
PATT_60_REPLACE = r'\1\2'


# ( WTA 210. ) --> <ignore> ( WTA 210. ) </ignore>
# Kreekaga ( 57. ) --> Kreekaga <ignore> ( 57. ) </ignore>
PATT_62 = regex.compile(r'''
    ([^>])(\s\(\s(\d+\s?\.(\s[a-zõüöä]+)?|[A-ZÕÜÖÄ]+\s\d+\s?\.)\s\))
''', regex.X)
PATT_62_REPLACE = r'\1 <ignore>\2 </ignore>'


# <p> <s> Lõuna-Aafrika Vabariik <ignore> (4) </ignore> </s> </p>
# <p> <s> Tuneesia <ignore> (5) </ignore> </s> </p>
# p> <s> St.<+/>Louis :
PATT_63 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s
        ([A-ZÕÜÖÄ][a-zõüöä](\s[A-ZÕÜÖÄ][a-zõüöä]+)?+(-[A-ZÕÜÖÄ][a-zõüöä]+(\s[A-ZÕÜÖÄ][a-zõüöä]+)?|\.<\+\/>[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)?|[A-ZÕÜÖÄ]+)
        [^<]+<ignore>[^>]+>\s)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_63_REPLACE = r'\1 <ignore>\3\4\9</ignore> \10'


# <p> <s> Boston : Dafoe <ignore> (24) </ignore> , Skudra <ignore> ( 1 , vahetus 26<+/>:<+/>15 ) </ignore> , Dafoe <ignore> ( vahetus 28<+/>:<+/>23 ) </ignore> , Skudra <ignore> ( vahetus 53<+/>:<+/>49 ) </ignore> </s> </p>
PATT_63_2 = regex.compile(r'''
    (<p>)(\s<s>)
    (\s[A-ZÕÜÖÄŠŽ]([a-zõüöäšž]+|\.<\+\/>[A-ZÕÜÖÄŠŽa-zõüöäšž]+)(\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)?\s:\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+(\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)?((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_63_2_REPLACE = r'\1 <ignore>\2\3\8</ignore> \9'


# <p> <s> 1. Marcus Grönholm/Timo Rautiainen 3<+/>:<+/>23.44 , 8 , </s> </p>
PATT_64 = regex.compile(r'''
    (<p>)(\s<s>)
    ([\sa-zõüöäA-ZšŠÕÜÖÄ0-9\.\-,':;\/\)\(\*&%><\+]{,70}\s(,(\s...)?|-?\d+([,.]\d+)?\s?(punkti\s)?\.?)\s)
    (<\/s>\s)(<\/p>\s)
''', regex.X)
PATT_64_REPLACE = r'\1 <ignore>\2\3\8</ignore> \9'


# valemilaadsed asjad, nt 3 x 15
PATT_65= regex.compile(r'''
    ([0-9]+)\s?
    (x|×)\s?
    ([0-9]+)
''', regex.X)
PATT_65_REPLACE = r'\1<+/>\2<+/>\3'


# <+/>05 . 42 . </s>
PATT_65_1 = regex.compile(r'''
    (<\+\/>\d+)\s\.\s(\d+)(\s\.\s<\/s>)
''', regex.X)
PATT_65_1_REPLACE = r'\1<+/>.<+/>\2\3'


# <p> <s> Kert KÜTT - FC Valga ; </s> </p>
PATT_66_1 = regex.compile(r'''
    (<p>)(\s<s>)(((?!\s\d+\s\)|-)[^;])+)(<\/s>\s)(<\/p>)
''', regex.X)
PATT_66_1_REPLACE = r'\1 <ignore>\2\3\5</ignore> \6'


# <p> <s> TORONTO - NEW JERSEY 3<+/>-<+/>1 <ignore> ( 1<+/>-<+/>0,2<+/>-<+/>1,0<+/>-<+/>0 ) </ignore> </s> </p>
PATT_66_2 = regex.compile(r'''
    (<p>|<\/s>)(\s<s>)
    (\s[A-ZÕÜÖÄŠŽ]+(\s[A-ZÕÜÖÄŠŽ]+)?\s-\s[A-ZÕÜÖÄŠŽ]+(\s[A-ZÕÜÖÄŠŽ]+)?\s((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_66_2_REPLACE = r'\1 <ignore>\2\3\7</ignore> \8'


# David Coulthard McLaren +1 ring </s> </p>
PATT_66 = regex.compile(r'''
    (<p>\s<s>)(\s\d+\.)?((\s[A-ZÕÜÖÄ][a-zõüöäA-Z]+){2,}\s)(\+\d+\sringi?\s)?(<\/s>\s<\/p>)
''', regex.X)
# PATT_66_REPLACE = r'\1 <ignore>\2</ignore> \3'
PATT_66_REPLACE = r'\1 <ignore>\2\3\5</ignore> \6'


# '<p> <s> <ignore> Venemaa <ignore> (13) </ignore> </ignore> </s> </p>'--> '<p> <s> <ignore> Venemaa (13) </ignore> </s> </p>'
PATT_67 = regex.compile(r'''
    (<ignore>[^<]+)
    (<ignore>)
    ([^<]+)
    (<\/ignore>\s)
    (<\/ignore>)
''', regex.X)
PATT_67_REPLACE = r'\1\3\5'


PATT_57 = regex.compile(r'''
    (\))
    \s\s
    (\+?\d)
''', regex.X)
PATT_57_REPLACE = r'\1 \2'


PATT_tyhik = regex.compile(r'''
    (<s>)\s\s([^\s]+)
''', regex.X)
PATT_tyhik_REPLACE = r'\1 \2'


# <+/> 24
PATT_37_1 = regex.compile(r'''
    (<\+\/>)\s(\d)
''', regex.X)
PATT_37_1_REPLACE = r'\1\2'


PATT_37_2 = regex.compile(r'''
    (\d{4})<\+\/>(\d+\.)
''', regex.X)
PATT_37_2_REPLACE = r'\1 \2'


# <p> <s> Rahvamajandus : Abiševa , Maria ; Ahlamtšenkova , Viktoria ; Bakulina , Maria ;
PATT_68 = regex.compile(r'''
    (<p>)(\s<s>)
    (\s[A-ZÕÄÖÜ][a-zõüöä]+-?(\s[a-zõüöä]+)?\s(ja\s[A-ZÕÄÖÜ]?[a-zõüöä]+\s)?:)
    ((\s[A-ZÕÜÖÄŠŽ\*][a-zõüöäšž]+(-[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+|\s\(\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+\s\)|\s[a-zõüöäšž]+)?
        (\s,\s[A-ZÕÜÖÄŠŽ\*][a-zõüöäšž]+(-[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)?)?\s[;\.]?\s?)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_68_REPLACE = r'\1 <ignore>\2\3\6\11</ignore> \12'


# SPORDUUUDISED

# p> <s> 5 km ( v ) : 1. Katerina Neumannova ( pildil , Tshehhimaa ) 12.56 , 1 , 2. </s>
PATT_69 = regex.compile(r'''
    (<p>|<\/s>)(\s<s>)
    (\s\d+)(<[^>]+>[^\s]+\s[^\s]+\s:\s((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_69_REPLACE = r'\1 <ignore>\2\3\4\6</ignore> \7'


# <p> <s> Sprint : 1. Ronny Ackermann <ignore> ( Saksamaa ) </ignore> 18.58 , 2 , 2 . </s>
# # <s> Naiste 1000<+/>m : 1 . </s>
# <p> <s> Mehed : 200<+/>m 1 . </s> <s> 
# <p> <s> <hi rend="rasvane"> 10<+/>000<+/>m : </hi>
PATT_70 = regex.compile(r'''
    (<p>|<\/s>)(\s<s>(\s<hi[^>]+>)?)
    (\s([A-ZÕÄÖÜ][A-ZÕÜÖÄ]?\s?[a-zõüöä]+\s|\d+\s[a-zõüöäšž]+\s|[A-ZÕÜÖÄŠŽ]+[0-9]+\s
        |[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+\s[a-zõüöäšž]+\s[a-zõüöäšž]+\s)?
    (\s?\d+(<\+\/>(\d+<\+\/>)?[a-zõüöäšž]+³?)?\s)?:?(\s<\/hi>)?\s\d+(<\+\/>[a-z]+\s\d+)?\s?\.\s((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_70_REPLACE = r'\1 <ignore>\2\4\12</ignore> \13'


# <p> <s> <hi rend="rasvane"> 4x400<+/>m </hi> 2 . 54 , 29 USA 1993 </s> </p>
# <p> <s> <hi rend="rasvane"> 400<+/>m : </hi> 1 . </s> <s>
# <p> <s> <hi rend="rasvane"> 50<+/>km käim . </hi> 3<+/>:<+/>40 . 53 Hartwig Gauder , SDV 1987 </s>
# <p> <s> <hi rend="rasvane"> Mehed . 50<+/>m vabalt </hi> : 1 . </s>
PATT_71 = regex.compile(r'''
    (<p>|<\/s>)(\s<s>(\s<hi[^>]+>)?)
    (\s([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s\.\s)?(\d+x)?\d+(<\+\/>(\d+<\+\/>)?[a-zõüöäšž]+)?\s
        ([a-zõüöäšž]+\s(\.\s)?)?(<\/hi>)?\s?(:\s)?\d+(\s[\.,]|<\+)
        ((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_71_REPLACE = r'\1 <ignore>\2\4\15</ignore> \16'


# <p> <s> <hi rend="rasvane"> Maraton </hi> 2.25.17 Rosa Mota , Portugal 1987 </s> </p>
# <p> <s> <hi rend="rasvane"> Oda </hi> 90 . 82 Kimmo Kinnunen , Soome 1991 </s> </p>
# <p> <s> <hi rend="rasvane"> 10-võistlus </hi> 8817 Dan OBrien , USA 1993 </s> </p>
PATT_71_1 = regex.compile(r'''
    (<p>|<\/s>)(\s<s>(\s<hi[^>]+>)?)
    (\s[0-9A-ZÕÜÖÄŠŽa-zõüöäšž\-]+\s<\/hi>\s\d+\s?\.((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_71_1_REPLACE = r'\1 <ignore>\2\4\6</ignore> \7'


# <p> <s> Joe Sakic Col 45<+/>25+37= 62<+/>18 </s> </p>
# <p> <s> Peter Forsberg Col 8<+/>4+ 9= 13<+/>4 </s> </p>
# <p> <s> NY Islanders 45<+/>12 4<+/>2 27<+/>30 </s> </p>
PATT_74 = regex.compile(r'''
    (<p>)(\s<s>)
    ((\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+(\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)?(\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)?|
        \s[A-ZÕÜÖÄŠŽ]+\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)
    ((?!(\d+|\*)\s<\/s>\s<\/p>).)+(\d+|\*)\s)
    (<\/s>)(\s<\/p>)
''', regex.X)
PATT_74_REPLACE = r'\1 <ignore>\2\3\10 </ignore>\11'


# ( Tallinna Wado ) --> <ignore> ( Tallinna Wado ) </ignore>
PATT_72 = regex.compile(r'''
    (\s\(\s[A-ZÕÜÖÄ][a-zõüöä]+\s[A-ZÕÜÖÄ][a-zõüöä]+\s\)\s)
''', regex.X)
PATT_72_REPLACE = r' <ignore>\1</ignore> '


# <p> <s> 1-0 Shayne Corson ( Darcy Tucker , Tie Domi ) 14 : 38 </s> </p>
PATT_73 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s\d<\+\/>-<\+\/>\d+((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_73_REPLACE = r'\1 <ignore>\3\4\6</ignore> \7'


# <p> <s> M Safin ( RUS ) - [ 2 ] A Pavel ( ROM ) 4-6 , 6-3 , 6-4 , 7-6 ( 7/5 ) </s> </p>
# <p> <s> K Clijsters ( BEL ) ( 15 ) - A Jidkova ( RUS ) 6-3 , 7-6 </s> </p>
# <p> <s> W Arthurs ( AUS ) - I Heuberger ( SWI ) 6-3 3-6 6-3 3-6 6-1 </s> </p>
PATT_75 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s[A-ZÕÜÖÄŠŽ]([a-zõüöäšž]+)?\s[A-ZÕÜÖÄŠŽ][a-zõüöäšžA-ZÕÜÖÄ-]+\s[\(\[]\s[A-ZÕÜÖÄŠŽ0-9]+\s[\)\]](\s[\(\[]\s[A-ZÕÜÖÄŠŽ0-9]+\s[\)\]])?\s[-\/]
    ((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_75_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


# <p> <s> 1. Hiroshi Masuoka <ignore> ( Jaapan , Misubishi ) </ignore> 6<+/>:<+/>14.34 , 2 . </s> <s> Jean-Louis Schlesser <ignore> ( Prantsusmaa , Schlesser ) </ignore> 6<+/>:<+/>18.55 , 3 . </s> <s> Jose Maria Servia <ignore> ( Hispaania , Schlesser ) </ignore> 6<+/>:<+/>23.01 . </s> </p>
# <p> <s> Mehed . </s> <s> 1. Dvorak 26<+/>476 , 2 . Šebrle 25<+/>184 , 3 . </s>
PATT_76 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    (\s\d\.\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+\s
        ([A-ZÕÜÖÄŠŽ][a-zõüöäšž]+\s)?((?!\d+\s\.\s<\/s>\s<s>).)+\d+\s\.\s<\/s>\s<s>
    ((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_76_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


# <p> <s> 1. Valencia 17<+/>10<+/>5<+/>2 29<+/>:<+/>10<+/>35 </s> </p>
PATT_77 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s\d+(\.|\s-)\s[A-ZÕÜÖÄ]([a-zõüöäšž]+|[A-ZÕÜÖÄŠŽ]+)(\s[A-ZÕÜÖÄ][a-zõüöäšž]+(\s[A-ZÕÜÖÄ][a-zõüöäšž]+)?)?\s[^\s]+(\s[^\s]+)?\s(\.\s)?)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_77_REPLACE = r'\1 <ignore>\3\4\11</ignore> \12'

# <p> <s> Patrick Kluivert <ignore> ( Barcelona ) </ignore> </s> </p>
# <p> <s> Raul Gonzalez <ignore> ( Real Madrid ) </ignore> </s> </p>
# <p> <s> Catanha <ignore> ( Celta Vigo ) </ignore> </s> </p>
# <p> <s> 8 - John Carew <ignore> ( Valencia ) </ignore> </s> </p>
PATT_78 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s(\d+\s-\s)?
        [A-ZÕÜÖÄŠŽ][a-zõüöäšž]+(\s[A-ZÕÜÖÄŠŽ][a-zõüöäšž]+)?\s<ignore>
        ((?!<\/ignore>\s<\/s>\s<s>).)+
        <\/ignore>\s)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_78_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


# <p> <s> 2. Svetlana Tšernoussova Venemaa +1.12 , 8 <ignore> (1) </ignore> </s> </p>
# <p> <s> 3. Liv Grete Skjelbreid-Poiree Norra +1.23 , 0 <ignore> (6) </ignore> </s> </p>
PATT_79 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s\d+\.\s
        ([A-ZÕÜÖÄŠŽ][a-zõüöäšž\-\s]+)+
        \+?\d+\.\d+\s,\s\d+\s<ignore>((?!<\/ignore>).)+<\/ignore>\s)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_79_REPLACE = r'\1 <ignore>\3\4\7</ignore> \8'


# <p> <s> Miami-Detroit 93<+/>-<+/>85 <ignore> ( M : Mason 23/18 , D : Stackhouse 28 , Wallace 8/14 ) </ignore> </s> </p>
PATT_80 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s([A-ZÕÜÖÄŠŽ][a-zõüöäšž\s\-]+)+\d+<\+\/>\-<\+\/>\d+\s<ignore>((?!<\/ignore>).)+<\/ignore>\s(\.\s)?)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_80_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


# <p> <s> CLEVELAND 20<+/>20 . </s> <s> 500<+/>5<+/>1/2 </s> </p>
# <p> <s> NEW JERSEY 14<+/>29 . </s> <s> 326<+/>18<+/>1/2 </s> </p>
PATT_81 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s([A-ZÕÜÖÄŠŽ]+\s)+[^\s]+\s\.\s<\/s>\s<s>\s[^\s]+\s(\-\s)?)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_81_REPLACE = r'\1 <ignore>\3\4\7</ignore> \8'


# <p> <s> MK-sari : 1 . </s> <s> Shmigun 958 , 2 . </s> <s> Larissa Lazutina ( Venemaa ) 815 , 3 . 
# </s> <s> Olga Danilova ( mõl . Venemaa ) 609 . </s> </p>
PATT_82 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>(\s<hi[^>]+>)?)
    (\s[A-ZÕÜÖÄŠŽa-zõüöäšž\s\.\-]+\s:(\s<\/hi>)?\s\d+\s?\.\s<\/s>\s<s>((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_82_REPLACE = r'\1 <ignore>\3\5\8</ignore> \9'


# <p> <s> Teised kohtumised : Liverpool - Tottenham 4<+/>:<+/>0 ,
# <s> Tabeliseis : Iraan 12 <ignore> (8) </ignore> , Saudi Araabia 11 <ignore> (7) </ignore> </s> </p>
# </s> <s> Teisi tulemusi : Carlos Moya <ignore> ( Hispaania , 2 ) </ignore> - Fernando
PATT_83 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    ([A-ZÕÜÖÄŠŽa-zõüöäšž\s\.\-]+\s:\s[A-ZÕÜÖÄŠŽa-zõüöäšž]+\s(\-\s[A-ZÕÜÖÄŠŽa-zõüöäšž]+[^\s]+\s)?\d+(<\+\/>|\s<ignore>)
        ((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_83_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


PATT_84 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    ([A-ZÕÜÖÄŠŽa-zõüöäšž\s\.\-]+\s:\s[A-ZÕÜÖÄŠŽa-zõüöäšž]+\s([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s)?
        <ignore>((?!<\/ignore>).)+<\/ignore>\s-\s[A-ZÕÜÖÄŠŽa-zõüöäšž]+((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_84_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


# <p> <s> Zimbru Chisinau <ignore> ( Moldova ) 
# </ignore> – Dinamo Tbilisi <ignore> ( Gruusia ) </ignore> 2<+/>:<+/>0 <ignore>
PATT_85 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    (\s([A-ZÕÜÖÄŠŽa-zõüöäšž\-]+\s)+<ignore>((?!<\/ignore>).)+<\/ignore>\s[\-\–]
        \s?([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s)+(<ignore>((?!<\/ignore>).)+<\/ignore>\s\d+|\()
        ((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_85_REPLACE = r'\1 <ignore>\3\4\11</ignore> \12'


# <p> <s> 3 . ringi paarid : Chelsea London <ignore> ( Inglismaa )
# </ignore> – Skonto Riia <ignore> ( Läti ) </ignore> 
PATT_86 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    (\s\d+\s?\.\s?([a-zõüöäšž]+\s)+:\s([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s)+<ignore>((?!<\/ignore>).)+<\/ignore>\s[\-\–]
        \s([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s)+<ignore>((?!<\/ignore>).)+<\/ignore>
        ((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_86_REPLACE = r'\1 <ignore>\3\4\11</ignore> \12'


# <p rend="rasvane"> <s> Tšehhi - Kanada 1<+/>
PATT_87 = regex.compile(r'''
    (<p([^>]+)?>)(\s<s>)
    (\s([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s?){1,2}[\-\–]\s?([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s)+\d+<\+((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_87_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


# <s> [A-ZÕÜÖÄa-zõüöä]\+ [A-ZÕÜÖÄa-zõüöä]\+ : [A-ZÕÜÖÄa-zõüöä]\+ [A-ZÕÜÖÄa-zõüöä]\+ - [A-ZÕÜÖÄa-zõüöä]\+ [0-9] :
PATT_89 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    (\s([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s){1,2}:\s([A-ZÕÜÖÄŠŽa-zõüöäšž]+\s){1,2}-\s[A-ZÕÜÖÄŠŽa-zõüöäšž]+\s[0-9]((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_89_REPLACE = r'\1 <ignore>\3\4\8</ignore> \9'


# <ignore> ( SK Reval Sport spordihoone Aia t . </s> <s> <ignore> 20 ) </ignore> </ignore> ;
PATT_91 = regex.compile(r'''
    (<ignore>\s\(\s([A-ZÕÜÖÄa-zõüöä]+\s)+\.\s)<\/s>\s<s>\s<ignore>\s(\d+\s\)\s)<\/ignore>\s(<\/ignore>)
''', regex.X)
PATT_91_REPLACE = r'\1\3\4'

PATT_92 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    (\s(Mehed|Naised)\s:\s[0-9]+<\+\/>((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_92_REPLACE = r'\1 <ignore>\3\4\7</ignore> \8'

PATT_93 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    ((\s<hi\srend="rasvane">)?\s[A-ZÕÜÖÄŠŽ]-grupp\s:\s((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_93_REPLACE = r'\1 <ignore>\3\4\7</ignore> \8'

PATT_94 = regex.compile(r'''
    (<p([^>]+)?>|<\/s>)(\s<s>)
    ((\s<hi\srend="rasvane">)?\s[0-9]+\s\.\svoor\s:\s((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_94_REPLACE = r'\1 <ignore>\3\4\7</ignore> \8'


# SISEMISTE IGNOREIDE EEMALDUS
# <ignore> ( viimasel päeval võitis Goran Ivanisevic <ignore> ( Horvaatia ) </ignore> Thomas Musteri 6<+/>:<+/>7,7<+/>:<+/>5,6<+/>:<+/>7,6<+/>:<+/>2,7<+/>:<+/>5 ) </ignore> 
PATT_90 = regex.compile(r'''
    (<ignore>((?!<ignore>).)+)<ignore>\s(((?!<\/ignore>).)+)\s<\/ignore>(((?!<\/ignore>).)+<\/ignore>)
''', regex.X)
PATT_90_REPLACE = r'\1\3\5'


#SAATEKAVA
PATT_88 = regex.compile(r'''
    (<p>)(\s<s>(\s<hi\srend="rasvane">)?)
    (\s\d\d\s?\.\s?\d+(\s<\/hi>)?(\s|<\+\/>(-<\+\/>\d\d\s?\.\s?\d+)?)[0-9A-ZÕÜÖÄŠŽa-zõüöä\"\-]\s?[a-zõüöäšžA-ZÕÜÖÄŠŽ\.]+((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_88_REPLACE = r'\1 <ignore>\2\4\9</ignore> \10'


# <p> <s> <hi rend="rasvane"> 07 . 00 </hi> - <hi rend="rasvane"> 09 . 05 </hi> 
PATT_89 = regex.compile(r'''
    (<p>)(\s<s>\s<hi\srend="rasvane">)
    (\s\d\d\s?\.\s?\d+\s<\/hi>\s-\s<hi\srend="rasvane">\s\d\d((?!<\/s>\s<\/p>).)+)
    (<\/s>\s)(<\/p>)
''', regex.X)
PATT_89_REPLACE = r'\1 <ignore>\2\3\5</ignore> \6'


#----------------------------------------------------------------------------------------------------------


PATTERNS = [
  (PATT_75, PATT_75_REPLACE),
  (PATT_12, PATT_12_REPLACE),
  (PATT_2, PATT_2_REPLACE),
  (PATT_BRACS, PATT_BRACS_REPLACE),
  (PATT_REMOVE_NESTED_IGNORES, PATT_REMOVE_NESTED_IGNORES_SUB),
  (PATT_37, PATT_37_REPLACE),
  (PATT_22, PATT_22_REPLACE),
  (PATT_34, PATT_34_REPLACE),
  (PATT_1, PATT_1_REPLACE),
  (PATT_5, PATT_5_REPLACE),
  (PATT_3, PATT_3_REPLACE),
  (PATT_3_1, PATT_3_1_REPLACE),
  (PATT_4, PATT_4_REPLACE),
  (PATT_4_1, PATT_4_1_REPLACE),
  (PATT_4_2, PATT_4_2_REPLACE),
  (PATT_6, PATT_6_REPLACE),
  (PATT_6_1, PATT_6_1_REPLACE),
  (PATT_6_2, PATT_6_2_REPLACE),
  (PATT_6_3, PATT_6_3_REPLACE),
  (PATT_60, PATT_60_REPLACE),
  (PATT_61, PATT_61_REPLACE),
  (PATT_33, PATT_33_REPLACE),
  (PATT_36, PATT_36_REPLACE),
  (PATT_9, PATT_9_REPLACE),
  (PATT_11, PATT_11_REPLACE),
  (PATT_14, PATT_14_REPLACE),
  (PATT_15, PATT_15_REPLACE),
  (PATT_21, PATT_21_REPLACE),
  (PATT_4_3, PATT_4_3_REPLACE),
  (PATT_19, PATT_19_REPLACE),
  (PATT_23, PATT_23_REPLACE),
  (PATT_26, PATT_26_REPLACE),
  (PATT_26_1, PATT_26_1_REPLACE),
  (PATT_27, PATT_27_REPLACE),
  (PATT_20_1, PATT_20_1_REPLACE),
  (PATT_20_2, PATT_20_2_REPLACE),
  (PATT_45, PATT_45_REPLACE),
  (PATT_16, None),
  (PATT_64, PATT_64_REPLACE),
  (PATT_44, PATT_44_REPLACE),
  (PATT_46, PATT_46_REPLACE),
  (PATT_47, PATT_47_REPLACE),
  (PATT_48, PATT_48_REPLACE),
  (PATT_50, PATT_50_REPLACE),
  (PATT_51, PATT_51_REPLACE),
  (PATT_52, PATT_52_REPLACE),
  (PATT_37_1, PATT_37_1_REPLACE),
  (PATT_37_2, PATT_37_2_REPLACE),
  (PATT_49, PATT_49_REPLACE),
  (PATT_65, PATT_65_REPLACE),
  (PATT_65_1, PATT_65_1_REPLACE),
  (PATT_62, PATT_62_REPLACE),
  (PATT_57, PATT_57_REPLACE),
  (PATT_66_2, PATT_66_2_REPLACE),
  (PATT_66, PATT_66_REPLACE),
  (PATT_63, PATT_63_REPLACE),
  (PATT_63_2, PATT_63_2_REPLACE),
  (PATT_67, PATT_67_REPLACE),
  (PATT_68, PATT_68_REPLACE),
  (PATT_55, PATT_55_REPLACE),
  (PATT_69, PATT_69_REPLACE),
  (PATT_70, PATT_70_REPLACE),
  (PATT_71, PATT_71_REPLACE),
  (PATT_71_1, PATT_71_1_REPLACE),
  (PATT_72, PATT_72_REPLACE),
  (PATT_73, PATT_73_REPLACE),
  (PATT_74, PATT_74_REPLACE),
  (PATT_76, PATT_76_REPLACE),
  (PATT_4_4, PATT_4_4_REPLACE),
  (PATT_77, PATT_77_REPLACE),
  (PATT_78, PATT_78_REPLACE),
  (PATT_79, PATT_79_REPLACE),
  (PATT_80, PATT_80_REPLACE),
  (PATT_81, PATT_81_REPLACE),
  (PATT_82, PATT_82_REPLACE),
  (PATT_83, PATT_83_REPLACE),
  (PATT_84, PATT_84_REPLACE),
  (PATT_85, PATT_85_REPLACE),
  (PATT_86, PATT_86_REPLACE),
  (PATT_87, PATT_87_REPLACE),
  (PATT_88, PATT_88_REPLACE),
  (PATT_89, PATT_89_REPLACE),
  (PATT_3_2, PATT_3_2_REPLACE),
  (PATT_91, PATT_91_REPLACE),
  (PATT_92, PATT_92_REPLACE),
  (PATT_93, PATT_93_REPLACE),
  (PATT_94, PATT_94_REPLACE),
  (PATT_90, PATT_90_REPLACE),
  (PATT_tyhik, PATT_tyhik_REPLACE)
]


