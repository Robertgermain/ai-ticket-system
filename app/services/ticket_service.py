# Service layer for ticket business logic

# In-memory storage (temporary until database is added)
tickets = []

# Simple ID counter (ensures unique IDs)
ticket_id_counter = 1


def get_all_tickets():
    return tickets


def get_ticket_by_id(ticket_id: int):
    return next((t for t in tickets if t["id"] == ticket_id), None)


def create_ticket(title: str, description: str):
    global ticket_id_counter

    new_ticket = {
        "id": ticket_id_counter,
        "title": title,
        "description": description,
        "status": "open",
    }

    tickets.append(new_ticket)
    ticket_id_counter += 1

    return new_ticket


def update_ticket(ticket_id: int, title: str, description: str):
    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        return None

    ticket["title"] = title
    ticket["description"] = description

    return ticket


def delete_ticket(ticket_id: int):
    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        return None

    tickets.remove(ticket)
    return ticket
