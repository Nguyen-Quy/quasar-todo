import hug
from hug.middleware import CORSMiddleware
from models import Todo, session
from datetime import datetime

origins = [
    "http://localhost:9000",
    "http://localhost:9200",
]
api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=origins))


@hug.get("/todos")
def get_todos(pageNum: hug.types.number = 1, pageSize: hug.types.number = 10):
    todos = session.query(Todo)
    # paginate by pageNum & pageSize
    offset = (pageNum - 1) * pageSize
    paginated_lst = todos.offset(offset).limit(pageSize).all()

    result_lst = [
        {
            "id": todo.id,
            "title": todo.title,
            "createdAt": todo.created_at,
            "updatedAt": todo.updated_at,
            "done": todo.done,
        }
        for todo in paginated_lst
    ]

    return {
        "todoList": result_lst,
        "total": todos.count(),
        "message": "Successfully get todoList",
    }


@hug.post("/todos")
def create_todo(
    title: hug.types.text,
    done: hug.types.boolean = False,
):
    new_todo = Todo(title=title, done=done)
    new_todo.created_at = datetime.now()
    session.add(new_todo)
    session.commit()

    return {
        "message": "Todo created successfully",
        "id": new_todo.id,
        "title": new_todo.title,
        "done": new_todo.done,
        "createdAt": new_todo.created_at,
    }


@hug.put("/todos/{todo_id}")
def update_todo(
    todo_id: hug.types.number,
    title: hug.types.text = None,
    done: hug.types.boolean = False,
):
    new_todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if not new_todo:
        return {"message": "Todo not found"}
    new_todo.title = title
    new_todo.done = done
    new_todo.updated_at = datetime.now()
    session.commit()

    return {
        "message": "Todo updated successfully",
        "id": new_todo.id,
        "title": new_todo.title,
        "done": new_todo.done,
        "updatedAt": new_todo.updated_at,
    }


@hug.get("/todos/{todo_id}")
def get_todo(todo_id: hug.types.number):
    todo = session.query(Todo).filter(Todo.id == todo_id).first()

    return (
        {
            "id": todo.id,
            "title": todo.title,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at,
            "done": todo.done,
        }
        if todo
        else {"message": "Todo not found"}
    )


@hug.delete("/todos/{todo_id}")
def delete_todo(todo_id: hug.types.number):
    del_todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if not del_todo:
        return {"message": "Todo not found"}
    session.delete(del_todo)
    session.commit()

    return {"message": "Todo deleted successfully"}


if __name__ == "__main__":
    api.http.serve(port=8888)
