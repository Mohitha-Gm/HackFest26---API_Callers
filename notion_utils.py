from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

NOTION_SECRET = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("DATABASE_ID")
COMPANY_CONTACTS_DB_ID = os.getenv("COMPANY_CONTACTS_DB_ID")

notion = Client(auth=NOTION_SECRET)


def fetch_jobs():
    response = notion.databases.query(database_id=DATABASE_ID)
    jobs = []

    for page in response["results"]:
        props = page["properties"]

        job = {
            "company": props["Company"]["title"][0]["text"]["content"]
            if props["Company"]["title"] else "",

            "role": props["Role"]["rich_text"][0]["text"]["content"]
            if props["Role"]["rich_text"] else "",

            "resume_version": props["Resume Version"]["select"]["name"]
            if props["Resume Version"]["select"] else "",

            "status": props["Status"]["select"]["name"]
            if props["Status"]["select"] else "",

            "application_date": props["Application Date"]["date"]["start"]
            if props["Application Date"]["date"] else "",

            "follow_up_sent": props["Follow-up Sent"]["checkbox"],

            "page_id": page["id"],

            "cold_email_sent": props["Cold Email Sent"]["checkbox"]
            if props.get("Cold Email Sent") else False
        }

        jobs.append(job)

    return jobs


def mark_followup_sent(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "Follow-up Sent": {
                "checkbox": True
            }
        }
    )

def store_insights(insights, total_jobs, followups_count):
    from dotenv import load_dotenv
    load_dotenv()
    insights_db_id = os.getenv("INSIGHTS_DB_ID")

    notion.pages.create(
        parent={"database_id": insights_db_id},
        properties={
            "Run Summary": {
                "title": [{"text": {"content": "Autonomous Agent Run"}}]
            },
            "Date": {
                "date": {"start": datetime.now().isoformat()}
            },
            "Insights": {
                "rich_text": [{"text": {"content": insights[:2000]}}]
            },
            "Total Jobs": {
                "number": total_jobs
            },
            "Followups Triggered": {
                "number": followups_count
            }
        }
    )

def store_insights(insights, total_jobs, followups_count, timestamp):

    insights_db_id = os.getenv("INSIGHTS_DB_ID")

    notion.pages.create(
        parent={"database_id": insights_db_id},
        properties={
            "Run Summary": {
                "title": [{"text": {"content": f"Agent Run - {timestamp}"}}]
            },
            "Date": {
                "date": {"start": datetime.now().isoformat()}
            },
            "Insights": {
                "rich_text": [{"text": {"content": insights[:2000]}}]
            },
            "Total Jobs": {
                "number": total_jobs
            },
            "Followups Triggered": {
                "number": followups_count
            }
        }
    )


def fetch_company_contact(company_name):
    response = notion.databases.query(
        database_id=COMPANY_CONTACTS_DB_ID,
        filter={
            "property": "Company",
            "title": {
                "equals": company_name
            }
        }
    )

    results = response.get("results", [])

    if not results:
        return None

    props = results[0]["properties"]

    return {
        "email": props["Hiring Email"]["email"],
        "hr_name": props["HR Name"]["rich_text"][0]["text"]["content"]
        if props["HR Name"]["rich_text"] else "Hiring Team"
    }


def mark_cold_email_sent(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "Cold Email Sent": {
                "checkbox": True
            }
        }
    )