import requests
from requests.adapters import HTTPAdapter

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,pt;q=0.7',
    'Cache-Control': 'no-store',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Expires': '0',
    'Origin': 'https://meu.inss.gov.br',
    'Pragma': 'no-cache',
    'Referer': 'https://meu.inss.gov.br/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

def need_update(cpf: str, session=None):
    cpf = cpf.replace('.','').replace('-','')

    json_data = {
        'cpf': cpf,
    }
    
    if session:
        response = session.post('https://vip-pmeuinss-api.inss.gov.br/apis/revisaoBPC/consultar', HTTPAdapter(max_retries=2), headers=headers, json=json_data)
    else:
        response = requests.post('https://vip-pmeuinss-api.inss.gov.br/apis/revisaoBPC/consultar', HTTPAdapter(max_retries=2), headers=headers, json=json_data)
    
    if response.status_code == 504:
        return False
    
    if response.status_code == 406:
        print(response.url)
        return False
    
    response.raise_for_status()
    
    if response.status_code == 200:
        return True
        
    return False


def has_cadunico(cpf: str, session=None):
    return not need_update(cpf, session)

