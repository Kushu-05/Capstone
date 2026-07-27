import csv
import json
import argparse
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ----------------------------------------------------
# Logging Configuration
# ----------------------------------------------------
logging.basicConfig(
    filename="ticket.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------
app = FastAPI(
    title="NimbusTech Ticket API",
    version="1.0"
)

# ----------------------------------------------------
# Constants
# ----------------------------------------------------
PRIORITY_SCORE = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

# ----------------------------------------------------
# Pydantic Model
# ----------------------------------------------------
class Ticket(BaseModel):
    ticketId: str
    customerName: str
    category: str
    priority: str
    createdAt: str
    slaHours: int
    status: str

# ----------------------------------------------------
# Global Storage
# ----------------------------------------------------
tickets = []

# ----------------------------------------------------
# Validation Function
# ----------------------------------------------------
def validate_ticket(row):

    required = [
        "ticketId",
        "customerName",
        "category",
        "priority",
        "createdAt",
        "slaHours",
        "status"
    ]

    for field in required:
        if field not in row or row[field] == "":
            return False

    if row["priority"] not in PRIORITY_SCORE:
        return False

    try:
        int(row["slaHours"])
    except:
        return False

    try:
        datetime.strptime(
            row["createdAt"],
            "%Y-%m-%d %H:%M:%S"
        )
    except:
        return False

    return True


# ----------------------------------------------------
# SLA Calculation
# ----------------------------------------------------
def calculate_sla(ticket):

    created = datetime.strptime(
        ticket["createdAt"],
        "%Y-%m-%d %H:%M:%S"
    )

    now = datetime.now()

    hours = (now - created).total_seconds() / 3600

    return hours > int(ticket["slaHours"])


# ----------------------------------------------------
# CSV Processing
# ----------------------------------------------------
def process_csv(input_file, output_file):

    valid = []

    invalid = []

    total = 0

    with open(input_file, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            total += 1

            if validate_ticket(row):

                row["priorityScore"] = PRIORITY_SCORE[row["priority"]]

                row["slaBreached"] = calculate_sla(row)

                valid.append(row)

            else:

                invalid.append(row)

    if total > 0:

        invalid_percentage = len(invalid) / total

        if invalid_percentage > 0.10:

            logging.error("More than 10 percent invalid rows")

            raise Exception("Invalid rows exceed 10%")

    report = {

        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "totalRecords": total,

        "validRecords": len(valid),

        "invalidRecords": len(invalid),

        "tickets": valid

    }

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(report, file, indent=4)

    logging.info("JSON Report Generated")

    return report


# ----------------------------------------------------
# Load JSON
# ----------------------------------------------------
def load_json(filename):

    global tickets

    with open(filename, "r", encoding="utf-8") as file:

        data = json.load(file)

        tickets = data["tickets"]

    logging.info("Tickets Loaded")
  # ----------------------------------------------------
# HOME API
# ----------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "NimbusTech Ticket API Running"
    }


# ----------------------------------------------------
# GET ALL TICKETS
# ----------------------------------------------------
@app.get("/tickets")
def get_tickets():

    return {
        "count": len(tickets),
        "tickets": tickets
    }


# ----------------------------------------------------
# GET TICKET BY ID
# ----------------------------------------------------
@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):

    for ticket in tickets:

        if ticket["ticketId"] == ticket_id:
            return ticket

    raise HTTPException(
        status_code=404,
        detail="Ticket Not Found"
    )


# ----------------------------------------------------
# GET SLA BREACHED TICKETS
# ----------------------------------------------------
@app.get("/tickets/breached")
def breached():

    result = []

    for ticket in tickets:

        if ticket["slaBreached"]:

            result.append(ticket)

    return {
        "count": len(result),
        "tickets": result
    }


# ----------------------------------------------------
# CREATE TICKET
# ----------------------------------------------------
@app.post("/tickets")
def create_ticket(ticket: Ticket):

    for t in tickets:

        if t["ticketId"] == ticket.ticketId:

            raise HTTPException(
                status_code=400,
                detail="Ticket ID Already Exists"
            )

    data = ticket.dict()

    data["priorityScore"] = PRIORITY_SCORE[data["priority"]]

    data["slaBreached"] = calculate_sla(data)

    tickets.append(data)

    logging.info(
        f"Ticket Created : {ticket.ticketId}"
    )

    return {
        "message": "Ticket Added Successfully",
        "ticket": data
    }


# ----------------------------------------------------
# UPDATE TICKET
# ----------------------------------------------------
@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, ticket: Ticket):

    for index in range(len(tickets)):

        if tickets[index]["ticketId"] == ticket_id:

            data = ticket.dict()

            data["priorityScore"] = PRIORITY_SCORE[data["priority"]]

            data["slaBreached"] = calculate_sla(data)

            tickets[index] = data

            logging.info(
                f"Ticket Updated : {ticket_id}"
            )

            return {
                "message": "Ticket Updated",
                "ticket": data
            }

    raise HTTPException(
        status_code=404,
        detail="Ticket Not Found"
    )


# ----------------------------------------------------
# DELETE TICKET
# ----------------------------------------------------
@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str):

    for ticket in tickets:

        if ticket["ticketId"] == ticket_id:

            tickets.remove(ticket)

            logging.info(
                f"Ticket Deleted : {ticket_id}"
            )

            return {
                "message": "Ticket Deleted Successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Ticket Not Found"
      
    )# ----------------------------------------------------
# SAVE JSON
# ----------------------------------------------------
def save_json(filename):

    report = {

        "generatedAt": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "totalRecords": len(tickets),

        "validRecords": len(tickets),

        "invalidRecords": 0,

        "tickets": tickets

    }

    with open(filename, "w", encoding="utf-8") as file:

        json.dump(report, file, indent=4)

    logging.info("JSON Saved Successfully")


# ----------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------
def main():

    parser = argparse.ArgumentParser(
        description="NimbusTech Ticket Processing"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input CSV File"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON File"
    )

    args = parser.parse_args()

    try:

        process_csv(
            args.input,
            args.output
        )

        load_json(
            args.output
        )

        logging.info(
            "Processing Completed Successfully"
        )

        print("-----------------------------------")
        print("Ticket Processing Completed")
        print("-----------------------------------")
        print("Valid Tickets :", len(tickets))
        print("JSON File :", args.output)
        print("-----------------------------------")

    except Exception as e:

        logging.error(str(e))

        print("ERROR :", e)


# ----------------------------------------------------
# PROGRAM ENTRY
# ----------------------------------------------------
if __name__ == "__main__":

    main()
  
