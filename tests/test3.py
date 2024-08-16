
import re


def extract_link(banner):
    # الگوی regex برای پیدا کردن لینک
    # این الگو به دنبال رشته‌هایی می‌گردد که با http:// یا https:// شروع شده و پس از آن کاراکترهای معتبر URL قرار دارند
    pattern = r'https?://[^\s]+'
    
    # جستجوی الگو در متن
    match = re.search(pattern, banner)
    
    # اگر لینک پیدا شد، آن را برگردان
    if match:
        return match.group(0)
    else:
        return None

link="""Super GP

naмe : 【﻿𝐒𝐓𝐈𝐂𝐊】

мeмвer: کیفیت مهم تر از کمیته

lιnĸ : https://t.me/+rQWBKLM4_Lw4NjU0"""

result =extract_link(link)
print (result)