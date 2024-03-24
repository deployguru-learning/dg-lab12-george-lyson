import json
import requests

def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def verify_authorization(email, product, config):
    authorized_users_george = config.get('george', {})
    authorized_users_ellie = config.get('ellie', {})
    
    if email in authorized_users_george and product in authorized_users_george[email]:
        return True
    elif email in authorized_users_ellie and product in authorized_users_ellie[email]:
        return True
    else:
        return False


def notify_slack(message, slack_webhook_url):
    payload = {'text': message}
    try:
        response = requests.post(slack_webhook_url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send notification to Slack: {e}")

def main():
    config = load_config('config.json')
    email = input("Enter email: ")
    product = input("Enter product: ")

    if verify_authorization(email, product, config):
        print("Authorization successful. Launching product...")
        # Add your product launch logic here
    else:
        print("Authorization failed. You are not authorized to launch this product.")
        slack_webhook_url = "https://hooks.slack.com/services/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"
        notify_slack(f"Unauthorized product launch attempt by {email} for product {product}.", slack_webhook_url)

if __name__ == "__main__":
    main()
