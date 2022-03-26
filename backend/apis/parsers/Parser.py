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
        self.batch_muts = []
        self.batch_timeloclin = []

    def batch_to_muts(self):
        """
        Inserts data from batch_muts to the muts table
        """
        query = "INSERT INTO muts(date, lineage, mut, continent, country, region) VALUES (?,?,?,?,?,?)"
        self.con.executemany(query, self.batch_muts)
        self.con.commit()
        del self.batch_muts
        self.batch_muts = []

    def batch_to_timeloclin(self):
        """
        Inserts data from batch_timeloclin to the timeloclin table
        """
        query = "INSERT INTO timeloclin(date, continent, country, region, lineage) VALUES (?,?,?,?,?)"
        self.con.executemany(query, self.batch_timeloclin)
        self.con.commit()
        del self.batch_timeloclin
        self.batch_timeloclin = []

    def parse(self, selected_countries):
        """
        Performs the parsing of the file, loading the data into the database.
        Args:
            selected_countries: Set containing the string of the countries to be loaded
        """
        pass
