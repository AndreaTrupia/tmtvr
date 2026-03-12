def create_view(db, design_doc_name, view_name, map_fun, reduce_fun=None):
    design_doc = db.get(f'_design/{design_doc_name}')
    if not design_doc:
        design_doc = {'_id': f'_design/{design_doc_name}', 'views': {}}
    
    design_doc['views'][view_name] = {
        'map': map_fun,
        'reduce': reduce_fun
    }
    db.save(design_doc)
