from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError

def create_paper(uri, user, password, title, authors, abstract, pdf_url, published, updated):
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        with driver.session() as session:
            try:
                result = session.write_transaction(_create_and_return_paper, title, authors, abstract, pdf_url, published, updated)
            except ConstraintError as e:
                print(f"Constraint error: {e}")
                result = session.write_transaction(_update_paper, title, authors, abstract, pdf_url, published, updated)
            return result

def _create_and_return_paper(tx, title, authors, abstract, pdf_url, published, updated):
    query = (
        "CREATE (p:Paper {title: $title, authors: $authors, abstract: $abstract, "
        "pdf_url: $pdf_url, published: $published, updated: $updated}) "
        "RETURN p"
    )
    result = tx.run(query, title=title, authors=authors, abstract=abstract, 
                    pdf_url=pdf_url, published=published, updated=updated)
    return result.single()[0]

def _update_paper(tx, title, authors, abstract, pdf_url, published, updated):
    query = (
        "MATCH (p:Paper {title: $title}) "
        "SET p.authors = $authors, p.abstract = $abstract, p.pdf_url = $pdf_url, "
        "p.published = $published, p.updated = $updated "
        "RETURN p"
    )
    result = tx.run(query, title=title, authors=authors, abstract=abstract, 
                    pdf_url=pdf_url, published=published, updated=updated)
    return result.single()[0]
