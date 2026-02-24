from datetime import datetime
from notion_utils import (
    fetch_jobs,
    store_insights,
    fetch_company_contact,
    mark_cold_email_sent,
)
from analysis_agent import (
    analyze_patterns,
    generate_followup_email,
    generate_cold_outreach,
    get_resume_summary,
)
from gmail_auth import authenticate_gmail
from email.mime.text import MIMEText
from dotenv import load_dotenv
import base64
import os

load_dotenv()

YOUR_EMAIL = os.getenv("YOUR_EMAIL")


# -----------------------------
# Email Sender
# -----------------------------
def send_email(service, to, subject, body):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()


# -----------------------------
# Detect 7-Day Followups
# -----------------------------
def get_followups(jobs):
    followups = []

    for job in jobs:
        if job["status"] == "Applied" and not job["follow_up_sent"]:
            applied_date = datetime.fromisoformat(job["application_date"])
            days = (datetime.now() - applied_date).days

            if days >= 7:
                followups.append(job)

    return followups


# -----------------------------
# Core Agent Logic (Single Run)
# -----------------------------
def run_agent():
    print("🚀 Autonomous Job Agent Running...")

    jobs = fetch_jobs()
    total_jobs = len(jobs)

    service = authenticate_gmail()
    resume_summary = get_resume_summary()

    # 1️⃣ Strategic Analysis
    insights = analyze_patterns(jobs)

    # 2️⃣ Reminder Followups (to YOU)
    followups = get_followups(jobs)

    for job in followups:
        email_body = generate_followup_email(job)

        send_email(
            service,
            YOUR_EMAIL,
            f"Reminder: Follow-up for {job['company']} - {job['role']}",
            email_body
        )

    # 3️⃣ Autonomous Cold Outreach (to COMPANY)
    cold_emails_sent = 0

    for job in jobs:
        if job["status"] == "Applied" and not job["cold_email_sent"]:
            applied_date = datetime.fromisoformat(job["application_date"])
            days = (datetime.now() - applied_date).days

            if days >= 7:

                contact = fetch_company_contact(job["company"])

                if contact and contact["email"]:

                    email_body = generate_cold_outreach(
                        job,
                        resume_summary,
                        contact["hr_name"]
                    )

                    send_email(
                        service,
                        contact["email"],
                        f"Application Follow-Up – {job['role']}",
                        email_body
                    )

                    mark_cold_email_sent(job["page_id"])
                    cold_emails_sent += 1

    # 4️⃣ Send Strategic Summary to YOU
    send_email(
        service,
        YOUR_EMAIL,
        "🤖 Job Agent Strategic Update",
        insights
    )

    # 5️⃣ Store Insights in Notion
    store_insights(
        insights,
        total_jobs,
        len(followups),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    print(f"✅ Run Completed. Cold emails sent: {cold_emails_sent}")


# -----------------------------
# ENTRY POINT (Cloud Run Ready)
# -----------------------------
if __name__ == "__main__":
    run_agent()