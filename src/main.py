import json
from xml.dom import minidom

from fastapi import Depends, FastAPI, Request, Response
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/new_user/", operation_id="get_new_user")
async def create_user(request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Gets a new user created in the database.

    We don't need strong types here, we can just use the request object to get the body of the request
    and it is the responsibility of the user to send the correct data.

    If wrong data is sent, an error is returned as a status message.
    """
    # get the body of the request
    body = await request.json()

    try:
        # Create the User ID object
        email = body["email"]
        user_id = models.User(email=email)

        # Add the user to the database
        db.add(user_id)
        db.commit()

        # Refresh the user_id object to get the id
        db.refresh(user_id)

        # Now create the user details object
        user_name = body["user_name"]
        department = body["department"]
        salary = body["salary"]
        user = models.UserDetails(
            user_id=user_id.id,
            user_name=user_name,
            department=department,
            salary=salary,
        )

        # Add the user to the database
        db.add(user)
        db.commit()
    except Exception as e:
        # if there is an error, return 200 with the error as a status message
        response = {"status": f"Error: {e}", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)

    return Response(content=f"User created with id {user_id.id}", status_code=200)


@app.get("/user/{user_id}", operation_id="get_user_by_id")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> Response:
    """
    Gets a user from the database by their ID.
    """
    try:
        user_id_model = db.query(models.User).filter(models.User.id == user_id).first()
        if user_id_model is None:
            response = {
                "status": f"Error: User with id {user_id} not found",
                "status_code": 404,
            }
            return Response(content=json.dumps(response), status_code=200)

        user = (
            db.query(models.UserDetails)
            .filter(models.UserDetails.user_id == user_id)
            .first()
        )
        if user is None:
            response = {
                "status": f"Error: User with id {user_id} not found",
                "status_code": 404,
            }
            return Response(content=json.dumps(response), status_code=200)

        root = minidom.Document()
        xml = root.createElement("root")
        root.appendChild(xml)
        userChild = root.createElement("user")
        userChild.setAttribute("user_id", str(user.user_id))
        userChild.setAttribute("email", user_id_model.email)
        userChild.setAttribute("user_name", user.user_name)
        userChild.setAttribute("department", user.department)
        userChild.setAttribute("salary", user.salary)
        xml.appendChild(userChild)
        xml_str = root.toprettyxml(indent="\t")

        return Response(content=xml_str, status_code=200)
    except Exception as e:
        # if there is an error, return 200 with the error as a status message
        response = {"status": f"Error: {e}", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)


@app.get("/add_ticket/", operation_id="add_new_ticket")
async def create_new_ticket(
    request: Request, db: Session = Depends(get_db)
) -> Response:
    """
    Gets a new ticket created in the database.

    We don't need strong types here, we can just use the request object to get the body of the request
    and it is the responsibility of the user to send the correct data.

    If wrong data is sent, an error is returned as a status message.
    """
    # get the body of the request
    body = await request.json()

    try:
        # Create the Ticket object
        user_id = body["user_id"]
        title = body["title"]
        ticket_body = body["body"]
        status = body["status"]
        ticket = models.Ticket(
            user_id=user_id, title=title, body=ticket_body, status=status
        )

        # Add the ticket to the database
        db.add(ticket)
        db.commit()
    except Exception as e:
        # if there is an error, return 200 with the error as a status message
        response = {"status": f"Error: {e}", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)

    return Response(content="Ticket created", status_code=200)


@app.get("/all_tickets/", operation_id="get_tickets")
def get_tickets(db: Session = Depends(get_db)) -> Response:
    """
    Gets all the tickets in the database.
    """
    try:
        tickets = db.query(models.Ticket).all()
        ids = list(map(lambda x: str(x.id), tickets))
        # Convert the list of ids to a string
        ids = ", ".join(ids)

        return Response(content=f"Tickets: {ids}", status_code=200)
    except Exception as e:
        # if there is an error, return 200 with the error as a status message
        response = {"status": f"Error: {e}", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)


@app.get("/tikcet/", operation_id="get_ticket")
async def get_ticket(request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Gets a ticket from the database.

    The ticket ID is passed in in the body of the request.
    """
    try:
        # get the body of the request
        body = await request.json()
        ticket_id = body["ticket_id"]

        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if ticket is None:
            response = {"status": "Ticket not found", "status_code": 404}
            return Response(content=json.dumps(response), status_code=200)

        return Response(content=json.dumps(ticket.to_dict()), status_code=200)
    except Exception as e:
        # if there is an error, return 200 with the error as a status message
        response = {"status": f"Error: {e}", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)


@app.get("/update_ticket/", operation_id="update_ticket")
async def update_ticket(request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Updates a ticket in the database.

    The ticket ID is passed in in the body of the request.
    """
    try:
        # get the body of the request
        body = await request.json()
        ticket_id = body["ticket_id"]

        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if ticket is None:
            response = {"status": "Ticket not found", "status_code": 404}
            return Response(content=json.dumps(response), status_code=200)

        # Update the ticket status
        ticket.user_id = body["user_id"]
        ticket.title = body["title"]
        ticket.body = body["body"]
        ticket.status = body["status"]
        db.commit()

        return Response(content=json.dumps(ticket.to_dict()), status_code=200)
    except Exception as e:
        # if there is an error, return 200 with the error as a status message
        response = {"status": f"Error: {e}", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)


@app.get("/search_tickets/", operation_id="search_tickets")
async def search_tickets(request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Searches for tickets in the database.

    The search term is passed in in the body of the request.
    """
    try:
        # get the body of the request
        body = await request.json()

        # Check if we have status in the body, if so, search for it
        if "status" in body:
            status = body["status"]
            tickets = (
                db.query(models.Ticket).filter(models.Ticket.status == status).all()
            )
            if tickets is None:
                response = {"status": "Ticket not found", "status_code": 404}
                return Response(content=json.dumps(response), status_code=200)

            return Response(
                content=json.dumps([ticket.to_dict() for ticket in tickets]),
                status_code=200,
            )

        # If we have user_id in the body, search for it
        if "user_id" in body:
            user_id = body["user_id"]
            tickets = (
                db.query(models.Ticket).filter(models.Ticket.user_id == user_id).all()
            )
            if tickets is None:
                response = {"status": "Ticket not found", "status_code": 404}
                return Response(content=json.dumps(response), status_code=200)

            return Response(
                content=json.dumps([ticket.to_dict() for ticket in tickets]),
                status_code=200,
            )

        # If we have title in the body, search for it
        if "title" in body:
            title = body["title"]
            tickets = db.query(models.Ticket).filter(models.Ticket.title == title).all()
            if tickets is None:
                response = {"status": "Ticket not found", "status_code": 404}
                return Response(content=json.dumps(response), status_code=200)

            return Response(
                content=json.dumps([ticket.to_dict() for ticket in tickets]),
                status_code=200,
            )

        # If we have body in the body, search for it
        if "description" in body:
            ticket_body = body["description"]
            tickets = (
                db.query(models.Ticket).filter(models.Ticket.body == ticket_body).all()
            )
            if tickets is None:
                response = {"status": "Ticket not found", "status_code": 404}
                return Response(content=json.dumps(response), status_code=200)

            return Response(
                content=json.dumps([ticket.to_dict() for ticket in tickets]),
                status_code=200,
            )

        response = {"status": "No search term", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)
    except Exception as e:
        # if there is an error, return 200 with the error as a status message
        response = {"status": f"Error: {e}", "status_code": 400}
        return Response(content=json.dumps(response), status_code=200)
