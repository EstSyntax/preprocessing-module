#!/usr/bin/python3
# coding: utf8

"""
Programmi käivitamiseks:

Ühe kindla faili töötlemiseks (koos lausete loendamisega):
python3 eeltootlus.py --file tea_drt66d/tea_dr8055.tasak.xml --output-dir dr_eeltoodeldud --count-sentences 

Ühe kindla faili töötlemiseks (ilma lausete loendamiseta):
python3 eeltootlus.py --file tea_drt66d/tea_dr8055.tasak.xml --output-dir dr_eeltoodeldud

Terve kausta xml-ide töötlemine (koos lausete loendamisega):
python3 eeltootlus.py --directory tea_drt66d --output-dir dr_eeltoodeldud --count-sentences

Terve kausta xml-ide töötlemine (ilma lausete loendamiseta):
python3 eeltootlus.py --directory tea_drt66d --output-dir dr_eeltoodeldud

Skriptis kasutamiseks (lausete loendamisega):
cat tea_drt66d/tea_dr8055.tasak.xml | ./eeltootlus.py --count-sentences > toodeldud.xml

Skriptis kasutamiseks (ilma loendamiseta):
cat tea_drt66d/tea_dr8055.tasak.xml | ./eeltootlus.py > toodeldud.xml
"""

from __future__ import print_function


import argparse
import os
from multiprocessing.dummy import Pool
import re
import sys
import time

import tea_patterns


RESULTS_DIR = 'dr_eeltoodeldud'
DATA_DIR = 'tea_drt66d'


class Processor(object):

    def __init__(self, count_sentences):
        """
        Protsessori konstruktor
        count_sentences määrab, kas lauseid protsessimise ajal failis
        loendatakse või mitte
        """
        self.count_sentences = count_sentences
        self._sentence_count = 0
        self._sentence_patt = re.compile(r'<s>(?! <id="\d+">)')

    def _count_sentences(self, line):
        """
        lisab etteantud reas lause alguse sümboli järele selle lause
        järjekorranumbri failis ja tagastab muudetud rea
        """
        if not self.count_sentences:
            return line
        # lisame ükshaaval lausete alguste juurde järjekorranumbri, kuni
        # pole enam ühtegi järjekorranumbrita lause algust
        while self._sentence_patt.search(line):
            self._sentence_count += 1
            line = self._sentence_patt.sub(
                r'<s> <id="%d">' % self._sentence_count, line, count=1
            )
        return line

    def process_line(self, line):
        """ teostab rea töötlemise """
        # asendame kõik etteantud mustri vasted, kui mustrile üldse vaste leidub
        for regexp, replace in tea_patterns.PATTERNS:
            if callable(regexp):
                line = regexp(line)
            elif regexp.search(line):
                line = regexp.sub(replace, line)
        # viimaks sooritame lausete loenduse
        return self._count_sentences(line)

    def process(self, fid=None, fod=None):
        """ faili töötlemine, sisendiks faili tüüpi objektid """
        # kui sisendit või väljundit ette ei anta kasutame
        # vastavalt standardsisendit või standardväljundit
        if fid is None:
            fid = sys.stdin
        if fod is None:
            fod = sys.stdout
        fod.writelines(map(self.process_line, fid))

    def process_file(self, file_path, output_dir_path):
        """ faili töötlemine, sisendiks failiteed """
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir_path, filename)
        output_path = "%s_eel%s" % os.path.splitext(output_path)
        if file_path == output_path:
            print("Skipping file %s, it would be overwritten" % file_path)
            return
        else:
            print("Processing file %s to %s" % (file_path, output_path))
        with open(file_path) as fid, open(output_path, 'w') as fod:
            self.process(fid, fod)

    @staticmethod
    def process_directory(input_dir, output_dir, count_sentences):
        """
        Kaustas olevate xml failide töötlemine
        Funktsiooni argumentideks on sisend- ja väljundkausta teed
        """
        def process(filepath):
            Processor(count_sentences).process_file(filepath, output_dir)

        # kui väljundkausta ei eksisteeri, siis tee see
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # otsime sisendkaustast üles kõik xml-laiendiga failid
        xmls = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.xml')]
        Pool().map(process, xmls) # funktsiooni process rakendatakse kõikidele failidele eraldi lõimedena


def main():
    # käsurea parameetrite paikapanemine
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file', type=str, metavar='filepath',
        help='file to be parsed')
    parser.add_argument(
        '--directory', type=str,  metavar='dirpath', # default=DATA_DIR,
        help='parse all files from the directory')
    parser.add_argument(
        '--output-dir', type=str, metavar='outputpath', # default=RESULTS_DIR,
        help='directory where parsed files are saved')
    parser.add_argument(
        '--count-sentences', dest='count_sentences', action='store_true',
        help='boolean, whether to count sentence tags in xml or not')
    parser.set_defaults(count_sentences=False)
    args = parser.parse_args()

    error = ""
    if args.file and args.directory:
        error = "Provide file or directory, not both"
    elif args.file and not os.path.exists(args.file):
        error = "File %r does not exists" % args.file
    elif args.directory and not os.path.exists(args.directory):
        error = "Directory %r does not exists" % args.directory
    elif args.file and not args.output_dir:
        error = "Missing output directory for file parsing"
    elif args.directory and not args.output_dir:
        error = "Missing output directory for parsing directory"
    if error:
        sys.stderr.write("%s\n" % error)
        sys.exit(1)

    try:
        import regex
    except ImportError:
        print('Mooduli "regex" importimine ebaõnnestus.')
        print('Mooduli "regex" saad paigaldada käsuga `(sudo) pip install regex`')
        print('Mooduli dokumentatsioon on leitav siit: https://pypi.python.org/pypi/regex')
        sys.exit(1)

    if args.file: # kui käsurea parameetriks on fail, siis töötle seda faili
        Processor(args.count_sentences).process_file(
            args.file, args.output_dir)
    elif args.directory: # kui sisendiks on kaust, siis töötle seal kaustas olevaid xmle
        Processor.process_directory(
            args.directory, args.output_dir, args.count_sentences)
    else:
        # kui faili/kausta parameetrit ei anta, siis loe sisend standardsisendist
        # ja kirjuta väljund standardväljundisse (nt skriptis kasutamiseks)
        Processor(args.count_sentences).process()


if __name__ == '__main__':
    main()
