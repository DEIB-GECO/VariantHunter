from datetime import datetime

from tqdm import tqdm

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
            country_name = locs[1].strip()
            if len(selected_countries) != 0:
                if country_name.lower() not in selected_countries:
                    continue
            continent_name = locs[0].strip()
            if len(locs) < 3:
                region_name = None
            else:
                region_name = locs[2].strip()

            try:
                n = float(s[20])
            except:
                n = 0.

            length = int(s[6])
            lineage_name = s[11] if s[11] != self.missing_info_mark else 'None'

            try:
                date = (datetime.strptime(s[3], "%Y-%m-%d") - start_date).days
            except:
                continue

            if (29000 < length < 30000) and (n < 0.05):
                continent_id, country_id, region_id = self.get_location_ids(continent_name, country_name, region_name)
                lineage_id = self.get_lineage_id(lineage_name)
                sequence_id = self.get_sequence_id()

                self.batch_seqs.append((sequence_id, date, lineage_id, continent_id, country_id, region_id))
                for aa in s[14][1:-1].split(","):
                    if aa != '':
                        protein_name, mutation_name = aa.split("_")
                        protein_id = self.get_protein_id(protein_name)
                        self.batch_subs.append((sequence_id, protein_id, mutation_name))

            if len(self.batch_subs) > 50000:
                self.batch_to_subs()

            if len(self.batch_seqs) > 50000:
                self.batch_to_seqs()

            del line

        self.batch_to_subs()
        self.batch_to_seqs()
        self.dict_to_tables()
