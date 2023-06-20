from pymongo.mongo_client import MongoClient

url = "mongodb://gvijaya5:fourthtask1@ac-au6j6wt-shard-00-00.nrbi45u.mongodb.net:27017,ac-au6j6wt-shard-00-01.nrbi45u.mongodb.net:27017,ac-au6j6wt-shard-00-02.nrbi45u.mongodb.net:27017/?ssl=true&replicaSet=atlas-ny6ie8-shard-0&authSource=admin&retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(url)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['sample_mflix']

# Access a specific collection within the database
collection = db['comments']

# Retrieve all documents from the collection
documents = list(collection.find())

print(documents[1])

# Create
def insert_data(data):
    if isinstance(data, dict):  # If data is a single document
        result = collection.insert_one(data)
        print('Inserted document ID:', result.inserted_id)
    elif isinstance(data, list):  # If data is a list of documents
        result = collection.insert_many(data)
        print('Inserted document IDs:', result.inserted_ids)
    else:
        print('Invalid data format. Expected dictionary or list of dictionaries.')

#Update
def update_document(document_id, updated_data):
    result = collection.update_one({'_id': document_id}, {'$set': updated_data})
    print('Modified document count:', result.modified_count)

#Delete
def delete_document(document_id):
    result = collection.delete_one({'_id': document_id})
    print('Deleted document count:', result.deleted_count)

new_document = {
    'name': 'John Doe',
    'email': 'johndoe@example.com',
    'message': 'Hello, MongoDB!'
}

# Specify the document ID to update
document_id = '64910c164f1a01c63866feda'

# Specify the updated data
updated_data = {
    'message': 'Updated message',
}

update_document(document_id, updated_data)

# Insert the document
insert_data(new_document)

# Close the connection
client.close()