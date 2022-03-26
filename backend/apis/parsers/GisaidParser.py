from tqdm import tqdm
from datetime import datetime

from .Parser import Parser
from ..utils.utils import start_date


class GisaidParser(Parser):
    """
    Parser for Gisaid metadata.tsv file
    """

    missing_info_mark = ''

    def parse(self, selected_countries):
        self.f.readline()

        for line in tqdm(self.f, desc='\t\t'):
            s = line.split("\t")

            locs = s[4].split('/')
            country = locs[1].strip()
            if len(selected_countries) != 0:
                if country.lower() not in selected_countries:
                    continue
            continent = locs[0].strip()
            if len(locs) < 3:
                region = None
            else:
                region = locs[2].strip()

            try:
                n = float(s[20])
            except:
                n = 0.

            length = int(s[6])

            lin = s[11] if s[11] != self.missing_info_mark else 'None'

            try:
                date = (datetime.strptime(s[3], "%Y-%m-%d") - start_date).days
            except:
                continue

            if (29000 < length < 30000) and (n < 0.05):
                self.batch_timeloclin.append((date, continent, country, region, lin))
                for aa in s[14][1:-1].split(","):
                    self.batch_muts.append((date, lin, aa, continent, country, region))

            if len(self.batch_muts) > 50000:
                self.batch_to_muts()

            if len(self.batch_timeloclin) > 50000:
                self.batch_to_timeloclin()

            del line

        self.batch_to_muts()
        self.batch_to_timeloclin()