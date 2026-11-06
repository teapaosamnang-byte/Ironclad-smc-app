import os
from dotenv import load_dotenv

# ហៅទាញយកទិន្នន័យពីឯកសារ .env មកប្រើប្រាស់
load_dotenv()

def get_broker_credentials():
    """ទាញយកព័ត៌មានគណនី MT5 យ៉ាងមានសុវត្ថិភាព (មិនបារម្ភរឿងបែកធ្លាយកូដ)"""
    login_id = os.getenv("MT5_LOGIN")
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    
    # ផ្ទៀងផ្ទាត់ការទាញយក
    if not login_id or not password or not server:
        raise ValueError("⚠️ រកមិនឃើញព័ត៌មាន Login របស់ MT5 នៅក្នុង Environment Variables ទេ សូមពិនិត្យមើលឯកសារ .env ឡើងវិញ!")
        
    return {
        "login": int(login_id),
        "password": password,
        "server": server
    }

# សម្រាប់យកទៅហៅប្រើប្រាស់ក្នុងកូដផ្សេងៗ
MT5_CONFIG = get_broker_credentials()