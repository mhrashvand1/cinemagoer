# Copyright 2004-2022 Davide Alberani <da@erlug.linux.it>
#           2008-2018 H. Turgut Uyar <uyar@tekir.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
This module provides the classes (and the instances) that are used to parse
the results of a search for a given person.

For example, when searching for the name "Mel Gibson", the parsed page
would be:

http://www.imdb.com/find?q=Mel+Gibson&s=nm
"""

from imdb.utils import analyze_name

from .piculet import Path, Rule, Rules, reducers
from .searchMovieParser import DOMHTMLSearchMovieParser
from .utils import analyze_imdbid


class DOMHTMLSearchPersonParser(DOMHTMLSearchMovieParser):
    """A parser for the name search page."""

    rules = [
        Rule(
            key='data',
            extractor=Rules(
                foreach='//li[contains(@class, "find-name-result")]',
                rules=[
                    Rule(
                        key='link',
                        extractor=Path('.//a[@class="ipc-metadata-list-summary-item__t"]/@href', reduce=reducers.first)
                    ),
                    Rule(
                        key='name',
                        extractor=Path('.//a[@class="ipc-metadata-list-summary-item__t"]/text()')
                    ),
                    Rule(
                        key='headshot',
                        extractor=Path('.//img[@class="ipc-image"]/@src')
                    )
                ],
                transform=lambda x: (
                    analyze_imdbid(x.get('link')),
                    analyze_name(x.get('name', '') + x.get('index', ''), canonical=1),
                    x.get('akas'),
                    x.get('headshot')
                )
            )
        )
    ]

    def _init(self):
        super()._init()
        self.img_type = 'headshot'


_OBJECTS = {
    'search_person_parser': ((DOMHTMLSearchPersonParser,), {'kind': 'person'})
}
