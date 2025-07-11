import requests
import io,sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GITHUB_TOKEN = 'token'
ORG_NAME = 'storehubnet'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

components = [
    "3p_webhook_adapter-infra-svc",
    "3pl_adapter-infra-svc",
    "3rd_party_food_delivery_adapter-svc",
    "app_push-infra-svc",
    "auth-api",
    "backend_nodejs-framework",
    "backoffice-v1-web",
    "backoffice-v2-bff",
    "beep-v1-web",
    "calculator-lib",
    "campaign-svc",
    "core-api",
    "crm-api",
    "customers-svc",
    "e-invoice_adapter-svc",
    "ecommerce-v1-api",
    "ecommerce-v1-consumer",
    "ecommerce-v1-web",
    "grpc_protocols-lib",
    "inventory-svc",
    "ist-v1-web",
    "logistics-app-svc",
    "merchant-domain-svc",
    "message_queue_topics-v1-lib",
    "messenger_apps-infra-svc",
    "online_purchase-svc",
    "online_store-domain-svc",
    "ost-v1-web",
    "otp-api",
    "payment-api",
    "payout-api",
    "promotion-api",
    "promotion-svc",
    "report-api",
    "shmanager-v1-bff",
    "sms-api",
    "subscription-app-svc",
    "subscription_adapter-infra-svc",
    "user_preference-api",
    "weather-svc",
    "webhook-svc"
]

def protect_branch(repo):
    url = f"https://api.github.com/repos/{ORG_NAME}/{repo}/branches/release/protection"
    payload = {
        "required_status_checks": None,  # 不强制状态检查
        "enforce_admins": True,          # 管理员也必须遵守规则
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1
        },
        "restrictions": None
    }
    resp = requests.put(url, headers=HEADERS, json=payload, verify=False)
    if resp.status_code in [200, 201]:
        print(f"{repo}: 保护设置成功")
    else:
        print(f"{repo}: 设置失败，状态码 {resp.status_code}，返回信息：{resp.text}")

def main():
    for repo in components:
        protect_branch(repo)

if __name__ == '__main__':
    main() 
