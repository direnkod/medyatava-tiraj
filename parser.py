#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Medyatava-tiraj
# Copyright (C) 2013 Ozan Caglayan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# This script parses medyatava.com/tiraj web page to fetch press runs
# for daily Turkish newspapers. It generates a TSV (tab separated values)
# file called results.tsv that you can use for visualization purposes.

import re
import datetime

from HTMLParser import HTMLParser
import urllib2

BASE_URL = "http://www.medyatava.com/tiraj"

# Set this to the oldest week (monday) that you want to include
OLDEST = "27.05.2013"

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dates = []
        self.current = None
        self.tirage = {}
        self.in_table = False
        self.tag = None

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        if self.in_table:
            if self.tag == "img" and len(attrs) == 3:
                # newspaper name
                self.current = attrs[1][1]

    def handle_endtag(self, tag):
        if tag == "thead":
            # Table starts
            self.in_table = True
        if tag == "table":
            self.in_table = False

    def handle_data(self, data):
        if self.tag == "option" and \
                        re.match("[0-9]{2}\.[0-9]{2}\.[0-9]{4}", data):
            self.dates.append(data)
        if self.in_table:
            if self.tag == "td":
                if not self.tirage.has_key(self.current):
                    try:
                        self.tirage[self.current] = int(data.strip().replace(".", ""))
                    except:
                        print "Problem parsing '%s', skipping.." % self.current

if __name__ == "__main__":
    parser = MyHTMLParser()
    parser.feed(urllib2.urlopen(BASE_URL).read().decode("utf-8"))

    overall = {u"ZAMAN"      : [],
               u"HÜRRİYET"   : [],
               u"BİRGÜN"     : [],
               u"POSTA"      : [],
               u"MİLLİYET"   : [],
               u"AKŞAM"      : [],
               u"SÖZCÜ"      : [],
               u"TARAF"      : [],
               u"SABAH"      : [],
               u"HABERTÜRK"  : [],
               u"TÜRKİYE"    : [],
               u"STAR"       : [],
               u"VATAN"      : [],
               u"YENİ ŞAFAK" : [],
               u"TAKVİM"     : [],
               u"BUGÜN"      : [],
               u"AYDINLIK"   : [],
               u"YURT"       : [],
               u"YENİ AKİT"  : [],
               u"CUMHURİYET" : [],
               u"RADİKAL"    : [],
               u"SOL GAZETESİ":[],
               u"EVRENSEL"   : [],
               }

    mainstream = [u"HÜRRİYET",
                  u"MİLLİYET",
                  u"AKŞAM",
                  u"SABAH",
                  u"HABERTÜRK",
                  u"TÜRKİYE",
                  u"STAR",
                  u"VATAN",
                  u"YENİ ŞAFAK",
                  u"TAKVİM",
                  u"BUGÜN"]

    opposite = [u"BİRGÜN",
                u"SÖZCÜ",
                u"TARAF",
                u"AYDINLIK",
                u"YURT",
                u"CUMHURİYET",
                u"SOL GAZETESİ",
                u"EVRENSEL"]

    # Weeks to analyze
    weeks = parser.dates[:parser.dates.index(OLDEST) + 1]

    for week in weeks:
        del parser
        parser = MyHTMLParser()
        parser.feed(urllib2.urlopen("%s/%s" % (BASE_URL,
            week)).read().decode("utf-8"))
        for key in overall:
            overall[key].append((week, parser.tirage[key]))

    for key in overall:
        overall[key].sort(key=lambda x:
                datetime.datetime.strptime(x[0], "%d.%m.%Y"))

    names = sorted(overall.keys())
    results = open("results.tsv", "wb")
    header = "\t".join(names)
    header = u"Week\t%s\n" % header
    results.write(header.encode("utf-8"))
    for idx, week in enumerate(weeks):
        results.write(u"%s\t" % week.replace(".", ""))
        for name in names:
            results.write(u"%d\t" % overall[name][idx][1])
        results.write("\n")

    for name in names:
        print "%s\n" % name.encode("utf-8")
        print "\n".join([u"  %s: %s" % (w,t) for w,t in overall[name]])
        print "%12s: %d" % ("Toplam", sum([t for w,t in overall[name]]))
        print "%12s: %d" % ("Fark", overall[name][-1][1]-overall[name][0][1])
        print

    mainstream_sum_begin = sum([overall[k][0][1] for k in mainstream])
    mainstream_sum_now = sum([overall[k][-1][1] for k in mainstream])
    opposite_sum_begin = sum([overall[k][0][1] for k in opposite])
    opposite_sum_now = sum([overall[k][-1][1] for k in opposite])

    print "Ana Akim Toplam (%s): %d" % (OLDEST, mainstream_sum_begin)
    print "Ana Akim Toplam (%s): %d" % (weeks[0], mainstream_sum_now)
    print "    Fark: %d" % (mainstream_sum_now - mainstream_sum_begin)
    print "Muhalif Toplam  (%s): %d" % (OLDEST, opposite_sum_begin)
    print "Muhalif Toplam  (%s): %d" % (weeks[0], opposite_sum_now)
    print "    Fark: %d" % (opposite_sum_now - opposite_sum_begin)

    results.close()
