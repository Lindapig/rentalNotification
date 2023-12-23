import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


class Email:
    """
    Email Class for Sending Email Notifications

    This class handles email notification functionality, including sending email notifications
    with the provided content.

    Args:
        config (dict): A dictionary containing email setup details.

    Attributes:
        sender_address (str): The sender's email address.
        sender_password (str): The sender's email password.
        receiver_address (list): A list of recipient email addresses.
        receiver_address_str (str): A comma-separated string of recipient email addresses.

    Methods:
        send_email(content):
            Sends an email notification with the given content.

        create_html(data):
            Creates an HTML table from the provided data for use in the email.

    Usage:
        Initialize an Email object with the configuration and use the send_email method
        to send email notifications.
    """

    def __init__(self, config) -> None:
        # self.config = config
        self.sender_address = config["email_setup"]["sender_address"]
        self.sender_password = config["email_setup"]["sender_password"]
        self.receiver_address = config["email_setup"]["receiver_address_list"]
        self.receiver_address_str = ", ".join(
            config["email_setup"]["receiver_address_list"]
        )

    def send_email(self, content):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message = MIMEMultipart()
        message["From"] = self.sender_address
        message["To"] = self.receiver_address_str
        message["Subject"] = f"Bayonne Bay available at {current_date}"
        html_content = self.create_html(content)
        message.attach(MIMEText(html_content, "html"))
        session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with TLS
        session.starttls()  # enable security
        session.login(
            self.sender_address, self.sender_password
        )  # login with mail_id and password
        text = message.as_string()
        session.sendmail(self.sender_address, self.receiver_address, text)
        session.quit()

    @staticmethod
    def create_html(data):
        # Start the HTML string for the table
        html_table = "<table border='1'><thead><tr>"

        # Add table headers
        headers = data[0].keys()
        for header in headers:
            html_table += f"<th>{header}</th>"

        # Close header row and start body
        html_table += "</tr></thead><tbody>"

        # Add table rows
        for row in data:
            html_table += "<tr>"
            for cell in row.values():
                html_table += f"<td>{cell}</td>"
            html_table += "</tr>"

        # Close the table tag
        html_table += "</tbody></table>"
        html_content = f"""
        <html>
            <head></head>
            <body>
                <p>Here is the available list:</p>
                {html_table}
            </body>
        </html>
        """
        return html_content
