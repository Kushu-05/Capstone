import logging

from io_utils import load_subscribers, load_cdrs
from models import Subscriber, CDR
from rating import compute_cost
from reporting import generate_report, save_report, print_summary

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

subscriber_data = load_subscribers("data/subscribers.json")

subscribers = {}

for item in subscriber_data.values():

    subscribers[item["msisdn"]] = Subscriber(
        item["msisdn"],
        item["plan_type"]
    )

cdr_data = load_cdrs("data/cdrs.csv")

for row in cdr_data:

    cdr = CDR(
        row["msisdn"],
        row["call_type"],
        row["duration_sec"]
    )

    cdr.cost = compute_cost(
        cdr.call_type,
        cdr.duration_sec
    )

    if cdr.msisdn in subscribers:

        subscribers[cdr.msisdn].add_call(cdr)

        logging.info(
            f"{cdr.msisdn} {cdr.call_type} {cdr.duration_sec}s ₹{cdr.cost}"
        )

report = generate_report(subscribers)

save_report(report, "output/report.json")

print_summary(report)

print("\nReport Generated Successfully!")
