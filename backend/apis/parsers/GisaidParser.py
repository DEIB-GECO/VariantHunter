from datetime import datetime

from tqdm import tqdm

from .Parser import Parser
from ..utils.utils import start_date


class GisaidParser(Parser):
    """
    Parser for Gisaid metadata.tsv file
    """

    # ############    Parser static configuration     ############ #
    missing_info_mark = ''  # marker used when data is missing
    location_col = 'Location'  # name for location column
    location_separator = '/'  # marker used to separate continent,country and region names in location col
    date_col = 'Collection date'  # name for collection date column
    lineage_col = 'Pango lineage'  # name for pango lineage name column
    length_col = 'Sequence length'  # name for length column
    n_content_col = 'N-Content'  # name for missing data column
    aa_subs_col = 'AA Substitutions'  # name for aa substitutions column

    # ############################################################ #

    def parse(self, selected_countries):
        # Read first line and extract cols positions
        self.auto_extract_cols(expected_cols=[self.location_col, self.date_col, self.lineage_col,
                                              self.length_col, self.n_content_col, self.aa_subs_col])

        for line in tqdm(self.f, desc='\t\t'):
            s = line.split("\t")

            # Parse and filtering of location data
            locs = s[self.cols[self.location_col]].split('/')
            country_name = locs[1].strip()
            if len(selected_countries) != 0:
                if country_name.lower() not in selected_countries:
                    continue
            continent_name = locs[0].strip()
            if continent_name == country_name:
                country_name = None

            if len(locs) < 3:
                region_name = None
            else:
                region_name = locs[2].strip()
                if region_name == country_name:
                    region_name = None

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
                n = float(s[self.cols[self.n_content_col]])
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
                for aa in s[self.cols[self.aa_subs_col]][1:-1].split(","):
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
