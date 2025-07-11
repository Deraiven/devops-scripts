import requests
import csv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def get_branch_protection(repo_full_name, branch):
    url = f'https://api.github.com/repos/{repo_full_name}/branches/{branch}/protection'
    resp = requests.get(url, headers=HEADERS, verify=False)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None

def get_status_checks_info(protection):
    if not protection or not protection.get('required_status_checks'):
        return '否', '否', ''
    
    checks = protection['required_status_checks']
    is_strict = checks.get('strict', False)
    contexts = checks.get('contexts', [])
    
    return ('是', 
            '是' if is_strict else '否', 
            ', '.join(contexts) if contexts else '无具体检查项')

def main():
    with open('branch_protection_report.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            '仓库',
            'master分支是否保护',
            '需要状态检查',
            '状态检查-严格模式',
            '状态检查项目',
            '管理员也必须遵守规则',
            '需要PR审核',
            '有推送限制'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in components:
            repo_name = f'{ORG_NAME}/{repo}'
            protection = get_branch_protection(repo_name, 'master')
            has_checks, is_strict, check_contexts = get_status_checks_info(protection)
            row = {
                '仓库': repo_name,
                'master分支是否保护': '是' if protection else '否',
                '需要状态检查': has_checks,
                '状态检查-严格模式': is_strict,
                '状态检查项目': check_contexts,
                '管理员也必须遵守规则': '是' if protection and protection.get('enforce_admins', {}).get('enabled') else '否',
                '需要PR审核': '是' if protection and protection.get('required_pull_request_reviews') else '否',
                '有推送限制': '是' if protection and protection.get('restrictions') else '否'
            }
            writer.writerow(row)

if __name__ == '__main__':
    main()
