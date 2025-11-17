#!/usr/bin/env python3
# Smart Google-Dork Generator v2.1 (Refined)
import argparse, json, csv, random, urllib.parse, webbrowser, sys, os
from typing import List, Tuple

class Colors:
    HEADER = '\033[95m'; BLUE = '\033[94m'; GREEN = '\033[92m'
    WARNING = '\033[93m'; FAIL = '\033[91m'; ENDC = '\033[0m'; BOLD = '\033[1m'

# تحسين القاموس ليشمل أنواع البحث المختلفة
LANG = {
    'ar': {
        'gen': '[+] بحث عام دقيق:',
        'files': '[+] استهداف الملفات والمستندات:',
        'url': '[+] استهداف العناوين والروابط:',
        'admin': '[+] لوحات التحكم والأنظمة:',
        'sensitive': '[+] ملفات سرية ومعلومات حساسة:',
        'link': '🔗 الرابط:',
        'saved': '✅ تم الحفظ بنجاح في:',
        'opening': '🚀 جاري فتح الروابط في المتصفح...',
        'random_pick': '🔀 تم اختيار ({}) نتائج عشوائية.'
    },
    'en': {
        'gen': '[+] General Precision:',
        'files': '[+] Document Hunter:',
        'url': '[+] Title & URL Focus:',
        'admin': '[+] Admin & Login Pages:',
        'sensitive': '[+] Sensitive Info Hunter:',
        'link': '🔗 Link:',
        'saved': '✅ Saved successfully to:',
        'opening': '🚀 Opening links in browser...',
        'random_pick': '🔀 Randomly selected ({}) queries.'
    }
}

def build_google_link(q: str) -> str:
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)

def generate_queries(keyword: str, domain=None, filetype=None,
                     exclude=None, strict=False, lang='ar') -> List[Tuple[str, str]]:
    queries = []
    term = f'"{keyword}"' if strict else keyword
    exclusion = f" -{exclude}" if exclude else ""
    
    # دالة مساعدة لإضافة الاستعلام مع نوعه الصحيح
    def add(type_key: str, q: str):
        # جلب الوصف الصحيح بناءً على اللغة ونوع البحث
        queries.append((LANG[lang][type_key], q))

    # 1. General
    add('gen', f'{term} {exclusion}' + (f' site:{domain}' if domain else ''))

    # 2. Files
    docs = f'filetype:{filetype}' if filetype else '(filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:ppt)'
    add('files', f'{term} {docs} {exclusion}' + (f' site:{domain}' if domain else ''))

    # 3. Structure (Title/URL)
    add('url', f'(intitle:"{keyword}" OR inurl:"{keyword}") {exclusion}' + (f' site:{domain}' if domain else ''))

    # 4. Admin & Login
    add('admin', f'{term} (intitle:"index of" OR intitle:"login" OR intitle:"admin" OR inurl:login) {exclusion}' + (f' site:{domain}' if domain else ''))

    # 5. Sensitive
    sensitive = f'{term} (intext:"confidential" OR intext:"internal use only" OR intext:"password") {exclusion}'
    if filetype: sensitive += f' filetype:{filetype}'
    if domain: sensitive += f' site:{domain}'
    add('sensitive', sensitive)

    return queries

def save_results(results: List[Tuple[str, str]], fmt: str, lang: str = 'ar'):
    # تجهيز البيانات للحفظ
    data = [{'type': t.strip('[:] '), 'dork': d, 'link': build_google_link(d)} for t, d in results]
    fname = f'dorks_results.{fmt}'
    
    try:
        if fmt == 'json':
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        elif fmt == 'csv':
            with open(fname, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Type', 'Dork', 'Link'])
                writer.writerows([(row['type'], row['dork'], row['link']) for row in data])
        else:  # txt
            with open(fname, 'w', encoding='utf-8') as f:
                for row in data:
                    f.write(f"{row['type']}\n{row['dork']}\n{row['link']}\n" + "-"*40 + "\n")
        
        print(f"{Colors.GREEN}{LANG[lang]['saved']} {Colors.BOLD}{fname}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error saving file: {e}{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description="Smart Google-Dork Generator v2.1", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("keyword", help="الكلمة المفتاحية (Target)")
    parser.add_argument("-d", "--domain", help="نطاق الموقع (ex: sa, gov.ae)")
    parser.add_argument("-f", "--filetype", help="نوع الملف (ex: pdf)")
    parser.add_argument("-x", "--exclude", help="استبعاد كلمات")
    parser.add_argument("-e", "--exact", action="store_true", help="بحث حرفي دقيق")
    parser.add_argument("-r", "--random", type=int, help="عدد عشوائي للنتائج")
    parser.add_argument("-o", "--open", action="store_true", help="فتح في المتصفح")
    parser.add_argument("--save", choices=['json', 'csv', 'txt'], help="حفظ النتائج")
    parser.add_argument("--lang", choices=['ar', 'en'], default='ar', help="اللغة (ar/en)")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # توليد النتائج
    results = generate_queries(args.keyword, args.domain, args.filetype, args.exclude, args.exact, args.lang)

    # المعالجة العشوائية
    if args.random:
        if args.random > len(results): args.random = len(results)
        results = random.sample(results, args.random)
        print(Colors.WARNING + LANG[args.lang]['random_pick'].format(len(results)) + Colors.ENDC)

    # حفظ النتائج
    if args.save:
        save_results(results, args.save, args.lang)

    # فتح الروابط (بدون إيقاف الطباعة)
    if args.open:
        print(Colors.BLUE + LANG[args.lang]['opening'] + Colors.ENDC)
        for _, dork in results:
            webbrowser.open_new_tab(build_google_link(dork))

    # طباعة النتائج على الشاشة
    print("\n" + "="*60)
    for title, dork in results:
        print(f"{Colors.GREEN}{title}{Colors.ENDC}")
        print(f"{Colors.BOLD}{dork}{Colors.ENDC}")
        print(f"{LANG[args.lang]['link']} {Colors.BLUE}{build_google_link(dork)}{Colors.ENDC}")
        print("-" * 60)

if __name__ == "__main__":
    main()
