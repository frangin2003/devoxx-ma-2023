import sqlite3
from ariadne import QueryType, MutationType, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
import uvicorn

# Load the GraphQL schema from a file
type_defs = load_schema_from_path("ghosts_schema.graphql")

# Define the resolvers
query = QueryType()
mutation = MutationType()

@query.field("ghosts")
def resolve_ghosts(obj, info, name=None):
    conn = sqlite3.connect('ghosts.db')
    c = conn.cursor()
    if name is not None:
        c.execute('SELECT * FROM ghosts WHERE name = ?', (name,))
    else:
        c.execute('SELECT * FROM ghosts')
    ghosts = []
    for row in c.fetchall():
        ghosts.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "age": row[3],
            "haunting_hours": row[4],
            "location": row[5]
        })
    conn.close()
    return ghosts

@mutation.field("createGhost")
def resolve_create_ghost(obj, info, name, description, age, haunting_hours, location):
    conn = sqlite3.connect('ghosts.db')
    c = conn.cursor()
    c.execute('INSERT INTO ghosts (name, description, age, haunting_hours, location) VALUES (?, ?, ?, ?, ?)', (name, description, age, haunting_hours, location))
    ghost_id = c.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": ghost_id,
        "name": name,
        "description": description,
        "age": age,
        "haunting_hours": haunting_hours,
        "location": location
    }

@mutation.field("updateGhost")
def resolve_update_ghost(obj, info, id, name=None, description=None, age=None, haunting_hours=None, location=None):
    conn = sqlite3.connect('ghosts.db')
    c = conn.cursor()
    update_values = {}
    if name is not None:
        update_values["name"] = name
    if description is not None:
        update_values["description"] = description
    if age is not None:
        update_values["age"] = age
    if haunting_hours is not None:
        update_values["haunting_hours"] = haunting_hours
    if location is not None:
        update_values["location"] = location
    update_query = "UPDATE ghosts SET " + ", ".join([f"{key} = ?" for key in update_values.keys()]) + " WHERE id = ?"
    update_params = list(update_values.values()) + [id]
    c.execute(update_query, update_params)
    conn.commit()
    c.execute('SELECT * FROM ghosts WHERE id = ?', (id,))
    row = c.fetchone()
    conn.close()
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "age": row[3],
        "haunting_hours": row[4],
        "location": row[5]
    }

@mutation.field("deleteGhost")
def resolve_delete_ghost(obj, info, id):
    conn = sqlite3.connect('ghosts.db')
    c = conn.cursor()
    c.execute('DELETE FROM ghosts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return True

# Create the executable schema
schema = make_executable_schema(type_defs, query, mutation)

# Create the GraphQL app
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
