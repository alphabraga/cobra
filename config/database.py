from montydb import MontyClient, set_storage

def connection():

    set_storage(
        repository="database",  
        storage="flatfile",     
        mongo_version="4.0",    
        use_bson=False,         
        cache_modified=10
    )

    database = 'pessoas'
    client =  MontyClient()
    db = client.get_database(database)
    return db