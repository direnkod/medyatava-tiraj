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

import json

if __name__ == "__main__":

    overall = json.loads(open("tiraj.json", "rb").read())

    names = sorted(overall.keys())
    weeks = [s[0] for s in overall.values()[0]]

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

    for name in sorted(overall.keys()):
        print "%s\n" % name.encode("utf-8")
        print "\n".join([u"  %s: %s" % (w,t) for w,t in overall[name]])
        print "%12s: %d" % ("Toplam", sum([t for w,t in overall[name]]))
        print "%12s: %d" % ("Fark", overall[name][-1][1]-overall[name][0][1])
        print

    mainstream_sum_begin = sum([overall[k][0][1] for k in mainstream])
    mainstream_sum_now = sum([overall[k][-1][1] for k in mainstream])
    opposite_sum_begin = sum([overall[k][0][1] for k in opposite])
    opposite_sum_now = sum([overall[k][-1][1] for k in opposite])

    print "Ana Akim Toplam (%s): %d" % (weeks[0], mainstream_sum_begin)
    print "Ana Akim Toplam (%s): %d" % (weeks[-1], mainstream_sum_now)
    print "    Fark: %d" % (mainstream_sum_now - mainstream_sum_begin)
    print "Muhalif Toplam  (%s): %d" % (weeks[0], opposite_sum_begin)
    print "Muhalif Toplam  (%s): %d" % (weeks[-1], opposite_sum_now)
    print "    Fark: %d" % (opposite_sum_now - opposite_sum_begin)

