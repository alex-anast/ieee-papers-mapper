import logging
import duckdb
import pandas as pd
from ieee_papers_mapper.models import ProcessedPaper, ClassifiedPaper, Author

logger = logging.getLogger("ieee_logger")


class PaperRepository:
    def __init__(self, connection: duckdb.DuckDBPyConnection):
        self.connection = connection
        self.cursor = connection.cursor()

    def paper_exists(self, is_number: str) -> bool:
        query = "SELECT 1 FROM papers WHERE is_number = ?"
        self.cursor.execute(query, (is_number,))
        return self.cursor.fetchone() is not None

    def insert_paper(self, paper: ProcessedPaper) -> int:
        query = """
        INSERT INTO papers (is_number, insert_date, publication_year, download_count,
                            citing_patent_count, title, abstract)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING paper_id
        """
        result = self.cursor.execute(
            query,
            (
                paper.is_number,
                paper.insert_date,
                paper.publication_year,
                paper.download_count,
                paper.citing_patent_count,
                paper.title,
                paper.abstract,
            ),
        )
        self.connection.commit()
        return result.fetchone()[0]

    def insert_authors(self, paper_id: int, authors: list[Author]) -> None:
        query = "INSERT INTO authors (paper_id, name, affiliation) VALUES (?, ?, ?)"
        for author in authors:
            self.cursor.execute(query, (paper_id, author.full_name, author.affiliation))
        self.connection.commit()

    def insert_index_terms(
        self, paper_id: int, term_type: str, terms: list[str]
    ) -> None:
        query = "INSERT INTO index_terms (paper_id, term_type, term) VALUES (?, ?, ?)"
        for term in terms:
            self.cursor.execute(query, (paper_id, term_type, term))
        self.connection.commit()

    def insert_prompt(self, paper_id: int, prompt: str) -> None:
        query = "INSERT INTO prompts (paper_id, prompt_text) VALUES (?, ?)"
        self.cursor.execute(query, (paper_id, prompt))
        self.connection.commit()

    def insert_full_paper(self, paper: ProcessedPaper) -> None:
        if self.paper_exists(paper.is_number):
            return
        paper_id = self.insert_paper(paper)
        self.insert_authors(paper_id, paper.authors)
        for term_type, terms in [
            ("ieee", paper.index_terms_ieee),
            ("dynamic", paper.index_terms_dynamic),
        ]:
            self.insert_index_terms(paper_id, term_type, terms)
        self.insert_prompt(paper_id, paper.prompt)

    def get_unclassified_papers(self) -> pd.DataFrame:
        return pd.read_sql_query(
            sql="""
                SELECT p.paper_id, pr.prompt_text
                FROM papers p
                JOIN prompts pr ON p.paper_id = pr.paper_id
                WHERE NOT EXISTS (
                    SELECT 1 FROM classification c WHERE c.paper_id = p.paper_id
                )
            """,
            con=self.connection,
        )

    def insert_classifications(self, classifications: list[ClassifiedPaper]) -> None:
        df = pd.DataFrame([c.model_dump() for c in classifications])
        self.connection.register("df_classified_view", df)
        self.connection.execute(
            "INSERT INTO classification (paper_id, category, confidence) "
            "SELECT paper_id, category, confidence FROM df_classified_view"
        )
        self.connection.unregister("df_classified_view")
        self.connection.commit()
