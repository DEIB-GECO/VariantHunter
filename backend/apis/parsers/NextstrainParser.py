from datetime import datetime

from tqdm import tqdm

from .Parser import Parser
from ..utils.utils import start_date


class NextstrainParser(Parser):
    """
    Parser for Nextstrain metadata.tsv file
    """

    # ############    Parser static configuration     ############ #
    missing_info_mark = '?'  # marker used when data is missing
    continent_col = 'region'  # name for continent column
    country_col = 'country'  # name for country column
    region_col = 'division'  # name for region column
    date_col = 'date'  # name for collection date column
    lineage_col = 'pango_lineage'  # name for pango lineage name column
    length_col = 'length'  # name for length column
    missing_data_col = 'missing_data'  # name for missing data column
    aa_subs_col = 'aaSubstitutions'  # name for aa substitutions column

    def parse(self, selected_countries):
        # Read first line and extract cols positions
        self.auto_extract_cols(
            expected_cols=[self.continent_col, self.country_col, self.region_col, self.date_col, self.lineage_col,
                           self.length_col, self.missing_data_col, self.aa_subs_col])

        for line in tqdm(self.f, desc='\t\t'):
            s = line.split("\t")

            # Parse and filtering of location data
            country_name = s[self.cols[self.country_col]].strip()
            if len(selected_countries) != 0:
                if country_name.lower() not in selected_countries:
                    continue
            continent_name = s[self.cols[self.continent_col]].strip()
            region_name = s[self.cols[self.region_col]]
            if region_name == self.missing_info_mark:
                region_name = None
            else:
                region_name = region_name.strip()

            # Parse and filtering of date data
            try:
                date = (datetime.strptime(s[self.cols[self.date_col]], "%Y-%m-%d") - start_date).days
            except:
                continue
            if self.filter_by_data_flag and self.is_out_of_range(date):
                continue

            # Parse lineage data
            lineage_name = s[self.cols[self.lineage_col]]
            lineage_name = lineage_name if lineage_name != self.missing_info_mark else 'None'

            # Parse quality data
            length = int(s[self.cols[self.length_col]])
            try:
                n = float(s[self.cols[self.missing_data_col]]) / length
            except:
                n = 0.

            # Filtering based on quality data
            if (29000 < length < 30000) and (n < 0.05):
                # Identifier assignment (handled manually for performance reasons)
                continent_id, country_id, region_id = self.get_location_ids(continent_name, country_name, region_name)
                lineage_id = self.get_lineage_id(lineage_name)
                sequence_id = self.get_sequence_id()

                self.batch_seqs.append((sequence_id, date, lineage_id, continent_id, country_id, region_id))

                # Parse aa substitutions
                for aa in s[self.cols[self.aa_subs_col]].split(","):
                    if aa != '':
                        protein_name, mutation_name = aa.split(":")
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
