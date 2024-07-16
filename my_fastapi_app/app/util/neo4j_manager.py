from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError

def create_paper(uri, user, password, title, authors, abstract, pdf_url, published, updated, keywords=None, institution=None):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        try:
            result = session.write_transaction(
                _create_and_return_paper, title, authors, abstract, pdf_url, published, updated, keywords, institution)
            if not result:
                print(f"No result returned from the creation query for paper: {title}")
            else:
                print(f"Successfully created/updated paper: {title}")
        except ConstraintError as e:
            print(f"Constraint error: {e}")
            result = session.write_transaction(
                _update_paper, title, authors, abstract, pdf_url, published, updated, keywords, institution)
            if not result:
                print(f"No result returned from the update query for paper: {title}")
            else:
                print(f"Successfully updated paper: {title}")
    driver.close()
    return result

def _create_and_return_paper(tx, title, authors, abstract, pdf_url, published, updated, keywords, institution):
    query = """
    MERGE (p:Paper {title: $title})
    ON CREATE SET p.abstract = $abstract, p.pdf_url = $pdf_url, p.published = $published, p.updated = $updated
    ON MATCH SET p.abstract = $abstract, p.pdf_url = $pdf_url, p.published = $published, p.updated = $updated
    WITH p
    UNWIND split($authors, ', ') AS author_name
    MERGE (a:Author {name: author_name})
    MERGE (a)-[:WROTE]->(p)
    WITH p, a
    FOREACH (keyword IN split($keywords, ', ') |
        MERGE (k:Keyword {name: keyword})
        MERGE (p)-[:HAS_KEYWORD]->(k)
    )
    FOREACH (inst IN split($institution, ', ') |
        MERGE (i:Institution {name: inst})
        MERGE (p)-[:BELONGS_TO]->(i)
    )
    RETURN p
    """
    result = tx.run(query, title=title, authors=authors, abstract=abstract, pdf_url=pdf_url, published=published, updated=updated, keywords=keywords or "", institution=institution or "")
    return result.single()

def _update_paper(tx, title, authors, abstract, pdf_url, published, updated, keywords, institution):
    query = """
    MATCH (p:Paper {title: $title})
    SET p.abstract = $abstract, p.pdf_url = $pdf_url, p.published = $published, p.updated = $updated
    WITH p
    UNWIND split($authors, ', ') AS author_name
    MERGE (a:Author {name: author_name})
    MERGE (a)-[:WROTE]->(p)
    WITH p, a
    FOREACH (keyword IN split($keywords, ', ') |
        MERGE (k:Keyword {name: keyword})
        MERGE (p)-[:HAS_KEYWORD]->(k)
    )
    FOREACH (inst IN split($institution, ', ') |
        MERGE (i:Institution {name: inst})
        MERGE (p)-[:BELONGS_TO]->(i)
    )
    RETURN p
    """
    result = tx.run(query, title=title, authors=authors, abstract=abstract, pdf_url=pdf_url, published=published, updated=updated, keywords=keywords or "", institution=institution or "")
    return result.single()
