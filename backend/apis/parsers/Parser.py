from datetime import datetime

from apis.utils.utils import start_date


class Parser:
    """
    Generic parser for the metadata.tsv file
    In its implementations, this class allows the extraction of sequence data from the metadata tsv file
    """

    def __init__(self, con, f):
        """
        Initializes the parser object
        Args:
            con:    The connection to the db
            f:      The file stream to be parsed
        """
        self.con = con
        self.f = f
        self.cols = {}
        self.filter_by_data_flag = False
        self.beginning_date_flag = False
        self.end_data_flag = False
        self.beginning_date = None
        self.end_date = None

        self.sequences_count = 0
        self.lineages_count = 0
        self.locations_count = 0
        self.proteins_count = 0

        self.lineages_dict = {}
        self.proteins_dict = {}
        self.locations_dict = {}

        self.batch_subs = []
        self.batch_seqs = []

    def set_date_range(self, beginning_date, end_date):
        """
        Sets the date range for the parsing. Only the rows that refers to this period will be considered.
        Args:
            beginning_date: String representing the start date or "beginning" value (YYYY-mm-dd)
            end_date:       String representing the end date or "end" value (YYYY-mm-dd)
        """
        self.beginning_date_flag = (beginning_date != 'beginning')
        self.end_data_flag = (end_date != 'end')
        self.filter_by_data_flag = (self.beginning_date_flag or self.end_data_flag)

        if self.beginning_date_flag:
            self.beginning_date = (datetime.strptime(beginning_date, "%Y-%m-%d") - start_date).days
        if self.end_data_flag:
            self.end_date = (datetime.strptime(end_date, "%Y-%m-%d") - start_date).days

    def auto_extract_cols(self, expected_cols):
        """
        Automatically extract columns positions based on the names of the columns
        and populate cols attribute with this information
        Args:
            expected_cols: List of string representing the names of the expected columns
        """
        line = self.f.readline()
        s = line.split("\t")
        # Generate a dictionary of the form {col_name: position_idx , ...}
        self.cols = {name: idx for idx, name in enumerate(s)}

        # Verify compatibility: if keys in expected_cols are missing, exit.
        found_keys = list(self.cols.keys())
        has_failed = any(col not in found_keys for col in expected_cols)
        if has_failed:
            print(
                "\n\033[91m* FATAL ERROR: \tThe metadata file is malformed or its structure has changed and " +
                "is not compatible with this version of Variant Hunter.\n*\n*\t\t" +
                "Make sure the file type parameter is correct and try again. \n*\t\t"
                "If the problem persists, please report this error by opening an issue at " +
                "github.com/DEIB-GECO/VariantHunter/issues \033[0m")
            exit(-1)

    def is_out_of_range(self, date):
        """
        Checks whether a date is in the date range of interest or not
        Args:
            date: The date to be checked

        Returns: True iff the date is out of the filtered range of interest

        """
        return ((self.beginning_date_flag and date < self.beginning_date) or
                (self.end_data_flag and date > self.end_date))

    def batch_to_subs(self):
        """
        Inserts data from batch_subs into the aa_substitutions table
        """
        query = ''' INSERT INTO temp_table2.aa_substitutions(sequence_id, protein_id, mut) 
                    VALUES (?,?,?)'''
        self.con.executemany(query, self.batch_subs)
        self.con.commit()
        del self.batch_subs
        self.batch_subs = []

    def batch_to_seqs(self):
        """
        Inserts data from batch_seqs into the sequences table
        """
        query = ''' INSERT INTO temp_table1.sequences(sequence_id, date, lineage_id, continent_id, country_id, region_id) 
                    VALUES (?,?,?,?,?,?)'''
        self.con.executemany(query, self.batch_seqs)
        self.con.commit()
        del self.batch_seqs
        self.batch_seqs = []

    def dict_to_tables(self):
        """
        Inserts data from dictionaries into the tables
        """
        print(f"\t\t Loading proteins info ... ")

        query = ''' INSERT INTO proteins (protein, protein_id) VALUES (?,?)'''
        self.con.executemany(query, self.proteins_dict.items())
        self.con.commit()

        print(f"\t\t Loading locations info ... ")

        query = ''' INSERT INTO continents (continent_id) VALUES (?)'''
        data = self.locations_dict.items()
        continents = [(cont_name, cont_data['id']) for (cont_name, cont_data) in data]
        self.con.executemany(query, [(cont_data['id'],) for (cont_name, cont_data) in data])

        query = ''' INSERT INTO countries (country_id, continent_id) VALUES (?,?)'''
        data = [(cont_data['id'], cou_name, cou_data) for (cont_name, cont_data) in data
                for cou_name, cou_data in cont_data['countries'].items()]
        countries = [(cou_name, cou_data['id']) for (cont_id, cou_name, cou_data) in data]
        self.con.executemany(query, [(cou_data['id'], cont_id) for (cont_id, cou_name, cou_data) in data])

        query = ''' INSERT INTO regions (region_id, country_id) VALUES (?,?)'''
        data = [(cou_data['id'], reg_name, reg_data) for (cont_id, cou_name, cou_data) in data
                for reg_name, reg_data in cou_data['regions'].items()]
        regions = [(reg_name, reg_data['id']) for (cou_id, reg_name, reg_data) in data]
        self.con.executemany(query, [(reg_data['id'], cou_id) for (cou_id, reg_name, reg_data) in data])

        query = ''' INSERT INTO locations (location, location_id) VALUES (?,?)'''
        self.con.executemany(query, regions + countries + continents)
        self.con.commit()

        print(f"\t\t Loading lineages info ...")

        query = ''' INSERT INTO lineages (lineage, lineage_id)
                            VALUES (?,?)'''
        self.con.executemany(query, self.lineages_dict.items())
        self.con.commit()

        print(f"\t\t Analyzing lineages info ... ")

        cur = self.con.cursor()
        # Compute the number of lineages sequences affected by a given mutation
        cur.execute('''   CREATE VIEW temp.lin_mut_counts AS
                            SELECT lineage_id, protein_id, mut, count(*) AS count
                            FROM aa_substitutions NATURAL JOIN sequences
                            GROUP BY lineage_id, protein_id, mut;''')

        # Compute the total number of lineages sequences
        cur.execute('''   CREATE VIEW temp.lin_counts AS
                            SELECT lineage_id, count(*) as count
                            FROM sequences
                            GROUP BY lineage_id;''')

        # Compute lineages characteristics as the mutations affecting at least 50% of lineage's sequences
        cur.execute('''   INSERT INTO lineages_characteristics
                            SELECT lineage_id, protein_id, mut
                            FROM lin_mut_counts AS LM
                            WHERE LM.count >= (
                                SELECT count*0.5
                                FROM lin_counts
                                WHERE lineage_id=LM.lineage_id
                                );''')
        self.con.commit()

    def parse(self, selected_countries):
        """
        Performs the parsing of the file, loading the data into the database.
        Args:
            selected_countries: List of strings representing the names of the countries to be loaded
        """
        pass

    def get_sequence_id(self):
        """
        Gets the sequence id
        Returns: The id to be assigned to the sequence

        """
        sequence_id = self.sequences_count
        self.sequences_count += 1
        return sequence_id

    def get_location_ids(self, continent_name, country_name, region_name):
        """
        Gets the ids of the locations and update the dictionaries.
        Args:
            continent_name: The name of the continent to be considered
            country_name:   The name of the country to be considered. Possibly None if unknown
            region_name:    The name of the region to be considered. Possibly None if unknown

        Returns: Ids of continent, country and region

        """
        continent_data = self.locations_dict.get(continent_name)
        if continent_data is None:
            # New continent: add it
            continent_id = self.locations_count
            self.locations_count += 1
            self.locations_dict[continent_name] = {'id': continent_id, 'countries': {}}
            continent_data = self.locations_dict.get(continent_name)
        else:
            # Already seen continent
            continent_id = continent_data['id']

        if country_name is not None:
            country_data = continent_data['countries'].get(country_name)
            if country_data is None:
                # New country: add it
                country_id = self.locations_count
                self.locations_count += 1
                continent_data['countries'][country_name] = {'id': country_id, 'regions': {}}
                country_data = continent_data['countries'].get(country_name)
            else:
                # Already seen country
                country_id = country_data['id']

            if region_name is not None:
                region_data = country_data['regions'].get(region_name)
                if region_data is None:
                    # New country: add it
                    region_id = self.locations_count
                    self.locations_count += 1
                    country_data['regions'][region_name] = {'id': region_id}
                else:
                    # Already seen country
                    region_id = region_data['id']
            else:
                region_id = None
        else:
            country_id = None
            region_id = None

        return continent_id, country_id, region_id

    def get_lineage_id(self, lineage_name):
        """
        Gets lineage id by lineage name and updates the dictionary if necessary
        Args:
            lineage_name: The name of the lineage to be considered

        Returns: The id of the lineage

        """
        lineage_id = self.lineages_dict.get(lineage_name)
        if lineage_id is None:
            lineage_id = self.lineages_count
            self.lineages_count += 1
            self.lineages_dict[lineage_name] = lineage_id
        return lineage_id

    def get_protein_id(self, protein_name):
        """
        Gets the protein id from the protein name  by updating the dictionary
        Args:
            protein_name: The name of the protein to be considered

        Returns: The id of the protein

        """
        protein_id = self.proteins_dict.get(protein_name)
        if protein_id is None:
            protein_id = self.proteins_count
            self.proteins_count += 1
            self.proteins_dict[protein_name] = protein_id
        return protein_id
