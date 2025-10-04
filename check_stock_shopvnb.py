import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

PRODUCT_URL = "https://shopvnb.com/vot-cau-long-yonex-astrox-100zz-va.html"
CHECK_TEXT = "Tạm hết hàng"

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

def check_stock():
    try:
        response = requests.get(PRODUCT_URL, timeout=15)
        response.raise_for_status()
        html = response.text

        if CHECK_TEXT.lower() in html.lower():
            print(f"[{datetime.now()}] Hết hàng.")
            return False
        else:
            print(f"[{datetime.now()}] CÓ HÀNG!")
            return True
    except Exception as e:
        print(f"Lỗi khi kiểm tra: {e}")
        return False

def send_email():
    subject = "CHAT-GPT thông báo sản phẩm có hàng"
    body = f"""\
CHAT-GPT thông báo:
Sản phẩm Yonex Astrox 100ZZ VA đã có hàng!
Thời điểm: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
Link: {PRODUCT_URL}
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("✅ Đã gửi email thông báo thành công.")
    except Exception as e:
        print(f"❌ Lỗi khi gửi email: {e}")

if __name__ == "__main__":
    if check_stock():
        send_email()
