from neo4j import GraphDatabase

def create_paper(uri, user, password, title, authors, abstract, pdf_url, published, updated):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.write_transaction(_create_and_return_paper, title, authors, abstract, pdf_url, published, updated)
    driver.close()
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

def find_paper_by_title(uri, user, password, title):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.read_transaction(_find_and_return_paper, title)
    driver.close()
    return result

def _find_and_return_paper(tx, title):
    query = (
        "MATCH (p:Paper {title: $title}) "
        "RETURN p.title, p.authors, p.abstract, p.pdf_url, p.published, p.updated"
    )
    result = tx.run(query, title=title)
    return [record["p"] for record in result]


