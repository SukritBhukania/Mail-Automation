import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
from datetime import datetime

# Function to fetch data from SQL database
def fetch_data(query):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to perform analysis on data
def analyze_data(df):
    # Example analysis: Calculate the average price
    average_price = df['price'].mean()
    return average_price

# Function to send email
def send_email(subject, body, recipients):
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipients, text)
    server.quit()

if __name__ == "__main__":
    # Define SQL query
    sql_query = """
    SELECT * FROM fresh_produce
    WHERE date = DATE('now', '-1 day')
    """

    # Fetch data
    data = fetch_data(sql_query)
    
    # Perform analysis
    analysis_result = analyze_data(data)
    
    # Prepare email content
    email_subject = f"Daily Fresh Produce Analysis - {datetime.now().strftime('%Y-%m-%d')}"
    email_body = f"The average price of fresh produce yesterday was ${analysis_result:.2f}."
    email_recipients = ["recipient1@example.com", "recipient2@example.com"]

    # Send email
    send_email(email_subject, email_body, email_recipients)

    print("Email sent successfully.")