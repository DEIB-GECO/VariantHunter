from tqdm import tqdm
from datetime import datetime

from .Parser import Parser
from ..utils.utils import start_date


class NextstrainParser(Parser):
    """
    Parser for Nextstrain metadata.tsv file
    """

    missing_info_mark = '?'

    def parse(self, selected_countries):
        print("*************** WARNING ********************************************* \n"+
              "NOT IMPLEMENTED: N-Content is required but not available. Default: n=0 for all the rows.")
        self.f.readline()

        for line in tqdm(self.f, desc='\t\t'):
            s = line.split("\t")

            country = s[7].strip()
            if len(selected_countries) != 0:
                if country.lower() not in selected_countries:
                    continue
            continent = s[6].strip()
            if s[8] == self.missing_info_mark:
                region = None
            else:
                region = s[8].strip()

            # TODO: add computation of N-Content
            n = 0.  # remove this lines once implemented
            # try:
            #     n = float(s[20])
            # except:
            #     n = 0.

            length = int(s[14])

            lin = s[19] if s[19] != self.missing_info_mark else 'None'

            try:
                date = (datetime.strptime(s[5], "%Y-%m-%d") - start_date).days
            except:
                continue

            if (29000 < length < 30000) and (n < 0.05):
                self.batch_timeloclin.append((date, continent, country, region, lin))
                for aa in s[47].split(","):
                    self.batch_muts.append((date, lin, aa.replace(':', '_'), continent, country, region))

            if len(self.batch_muts) > 50000:
                self.batch_to_muts()

            if len(self.batch_timeloclin) > 50000:
                self.batch_to_timeloclin()

            del line

        self.batch_to_muts()
        self.batch_to_timeloclin()
