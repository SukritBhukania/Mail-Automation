# Mail-Automation
This project helps with the logic of automating reports through mail

# Fresh Produce Daily Analysis and Email Notification

This Python script fetches data from an SQLite database, performs basic analysis (calculating the average price of fresh produce), and sends an email with the results to predefined recipients. It is designed to run daily, sending a report with the analysis of the previous day's data.

## Requirements

Before running the script, ensure you have the following Python packages installed:

- `pandas`: For data manipulation and analysis
- `smtplib`: For sending emails
- `sqlite3`: For interacting with the SQLite database
- `email.mime`: For creating and sending email messages

You can install the required packages using `pip`:

```bash
pip install pandas
```
The script queries an SQLite database to fetch the fresh produce data for the previous day.
```
def fetch_data(query):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```
The script calculates the average price of fresh produce based on the fetched data. The analysis can be customized for other metrics as needed.
```
def analyze_data(df):
    average_price = df['price'].mean()
    return average_price
```
Once the analysis is complete, an email is sent to the designated recipients with the results of the analysis.
```
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
```
The main part of the script combines all functions to fetch data, analyze it, and send the email.

```
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
```
How to Use
- Update the SQL Query: Customize the SQL query in the script to match your database structure and requirements.
- Configure Email Settings: Set up the email sender credentials (sender_email and sender_password), and specify the SMTP server and port. You may need to enable "less secure apps" on your email provider or use OAuth2 for more secure authentication.
- Set Recipients: Add the email addresses of the recipients who will receive the daily report in the email_recipients list.
- Schedule the Script: Use a task scheduler (like cron on Linux or Task Scheduler on Windows) to run the script daily.
