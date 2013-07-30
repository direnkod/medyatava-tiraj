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

    results = open("results.tsv", "wb")
    header = "\t".join(names)
    header = u"Week\t%s\n" % header
    results.write(header.encode("utf-8"))
    for idx, week in enumerate(weeks):
        results.write(u"%s\t" % week.replace(".", ""))
        for name in names:
            results.write(u"%d\t" % overall[name][idx][1])
        results.write("\n")
    results.close()

