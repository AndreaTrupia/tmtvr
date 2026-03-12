def query_view(db, design_doc_name, view_name, **kwargs):
    return db.view(f'{design_doc_name}/{view_name}', **kwargs)
