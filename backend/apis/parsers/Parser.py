class Parser:
    """
    Abstract parser for the metadata.tsv file
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

        self.sequences_count = 0
        self.lineages_count = 0
        self.locations_count = 0
        self.proteins_count = 0

        self.lineages_dict = {}
        self.regions_dict = {}
        self.countries_dict = {}
        self.continents_dict = {}
        self.region_country_dict = {}
        self.country_continent_dict = {}
        self.proteins_dict = {}

        self.batch_subs = []
        self.batch_seqs = []

    def batch_to_subs(self):
        """
        Inserts data from batch_subs into the substitutions table
        """
        query = ''' INSERT INTO substitutions(sequence_id, protein_id, mut) 
                    VALUES (?,?,?)'''
        self.con.executemany(query, self.batch_subs)
        del self.batch_subs
        self.batch_subs = []

    def batch_to_seqs(self):
        """
        Inserts data from batch_seqs into the sequences table
        """
        query = ''' INSERT INTO sequences(sequence_id, date, lineage_id, continent_id, country_id, region_id) 
                    VALUES (?,?,?,?,?,?)'''
        self.con.executemany(query, self.batch_seqs)
        self.con.commit()
        del self.batch_seqs
        self.batch_seqs = []

    def dict_to_tables(self):
        """
        Inserts data from dictionaries into the tables
        """

        query = ''' INSERT INTO proteins (protein, protein_id)
                    VALUES (?,?)'''
        self.con.executemany(query, self.proteins_dict.items())

        query = ''' INSERT INTO continents (continent_id) 
                    VALUES (?)'''
        self.con.executemany(query, [(x,) for x in self.continents_dict.values()])

        query = ''' INSERT INTO countries (country_id, continent_id) 
                    VALUES (?,?)'''
        self.con.executemany(query, self.country_continent_dict.items())

        query = ''' INSERT INTO regions (region_id, country_id)
                            VALUES (?,?)'''
        self.con.executemany(query, self.region_country_dict.items())

        query = ''' INSERT INTO locations (location, location_id)
                    VALUES (?,?)'''
        self.con.executemany(
            query, [*self.regions_dict.items(), *self.countries_dict.items(), *self.continents_dict.items()]
        )

        query = ''' INSERT INTO lineages (lineage, lineage_id)
                            VALUES (?,?)'''
        self.con.executemany(query, self.lineages_dict.items())

        cur = self.con.cursor()
        cur.execute('''   CREATE VIEW temp.lin_mut_counts AS
                            SELECT lineage_id, protein_id, mut, count(*) AS count
                            FROM substitutions NATURAL JOIN sequences
                            GROUP BY lineage_id, protein_id, mut;''')

        cur.execute('''   CREATE VIEW temp.lin_counts AS
                            SELECT lineage_id, count(*) as count
                            FROM sequences
                            GROUP BY lineage_id;''')

        cur.execute('''   INSERT INTO lineages_characterization
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
            selected_countries: Set containing the string of the countries to be loaded
        """
        pass

    def get_sequence_id(self):
        """
        Gets the sequence id
        Returns: The id of the sequence

        """
        sequence_id = self.sequences_count
        self.sequences_count += 1
        return sequence_id

    def get_location_ids(self, continent_name, country_name, region_name):
        """
        Gets the ids of the locations and update the dictionaries
        Args:
            continent_name: The name of the continent to be considered
            country_name:   The name of the country to be considered
            region_name:    The name of the region to be considered

        Returns: Ids of continent, country and region

        """
        region_id = self.get_region_id(region_name)
        country_id = self.get_country_id(country_name)
        continent_id = self.get_continent_id(continent_name)

        if self.region_country_dict.get(region_id) is None:
            self.region_country_dict[region_id] = country_id
            if self.country_continent_dict.get(country_id) is None:
                self.country_continent_dict[country_id] = continent_id

        return continent_id, country_id, region_id

    def get_region_id(self, region_name):
        """
        Gets the region id from the region name  by updating the dictionary
        Args:
            region_name: The name of the region to be considered

        Returns: The id of the region

        """
        region_id = self.regions_dict.get(region_name)
        if region_id is None:
            region_id = self.locations_count
            self.locations_count += 1
            self.regions_dict[region_name] = region_id
        return region_id

    def get_country_id(self, country_name):
        """
        Gets the country id from the country name  by updating the dictionary
        Args:
            country_name: The name of the country to be considered

        Returns: The id of the country

        """
        country_id = self.countries_dict.get(country_name)
        if country_id is None:
            country_id = self.locations_count
            self.locations_count += 1
            self.countries_dict[country_name] = country_id
        return country_id

    def get_continent_id(self, continent_name):
        """
        Gets the continent id from the continent name  by updating the dictionary
        Args:
            continent_name: The name of the continent to be considered

        Returns: The id of the continent

        """
        continent_id = self.continents_dict.get(continent_name)
        if continent_id is None:
            continent_id = self.locations_count
            self.locations_count += 1
            self.continents_dict[continent_name] = continent_id
        return continent_id

    def get_lineage_id(self, lineage_name):
        """
        Gets the lineage id from the lineage name  by updating the dictionary
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
