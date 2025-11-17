#!/usr/bin/env python3
# dork_generator.py – الإصدار 3 (مع دعم التصنيف والمتغيرات)
import argparse, random, urllib.parse, webbrowser, csv, sys, os

# عوامل تشغيل Google Dorks المدعومة
OPS = ('site','inurl','intitle','intext','filetype','allintext','allintitle','allinurl', 'cache', 'related', 'info', 'link')
QUOTE = lambda x: f'"{x}"' if ' ' in x and not (x.startswith('"') and x.endswith('"')) else x

def iter_dorks(path):
    """
    قراءة ملف الـ Dorks، وتحديد الفئات، وتصفية الـ Dorks الصالحة.
    """
    current_category = "Uncategorized"
    dorks_list = []
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # التعامل مع خطوط التصنيف
                if line.startswith('# CATEGORY:'):
                    current_category = line.split(':', 1)[1].strip()
                    continue
                
                # تصفية الـ Dorks الصالحة
                if not line.startswith('#') and any(line.startswith(op + ':') for op in OPS):
                    dorks_list.append({
                        'dork': line,
                        'category': current_category
                    })
    except FileNotFoundError:
        sys.exit(f'Error: Dorks file not found at {path}')
    except Exception as e:
        sys.exit(f'Error reading dorks file: {e}')
        
    return dorks_list

def build_url(dork): 
    """بناء رابط البحث مع ترميز URL."""
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(dork)

def main():
    p = argparse.ArgumentParser(
        description="Google-Dorks runner (v3) - Supports categories and variable substitution.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    p.add_argument('-f','--file', default='dorks.txt', help='Path to the dorks file. Default is dorks.txt')
    p.add_argument('-l','--list', action='store_true', help='List only (use with -c to list categories)')
    p.add_argument('-o','--open', action='store_true', help='Open in browser')
    p.add_argument('-s','--search', help='Keyword filter')
    p.add_argument('-e','--exact', action='store_true', help='Quote keyword filter')
    p.add_argument('-r','--random', type=int, help='Pick N random dorks')
    p.add_argument('-c','--category', help='Filter by category name')
    p.add_argument('-t','--target', help='Target domain or keyword for variable substitution (e.g., {target_domain})')
    p.add_argument('--csv', help='Export results to csv file')
    args = p.parse_args()

    dorks_data = iter_dorks(args.file)
    if not dorks_data: sys.exit('No valid dorks found.')

    # 1. تصفية حسب الفئة
    if args.category:
        dorks_data = [d for d in dorks_data if args.category.lower() in d['category'].lower()]
        if not dorks_data: sys.exit(f'No dorks found in category "{args.category}".')

    # 2. استبدال المتغيرات
    if args.target:
        for d in dorks_data:
            d['dork'] = d['dork'].replace('{target_domain}', args.target).replace('{keyword}', args.target)
    
    # 3. تصفية حسب الكلمة المفتاحية
    if args.search:
        search_term = QUOTE(args.search) if args.exact else args.search
        dorks_data = [d for d in dorks_data if search_term.lower() in d['dork'].lower()]
        if not dorks_data: sys.exit(f'No dorks found matching "{args.search}".')

    # 4. اختيار عشوائي
    if args.random:
        dorks_data = random.sample(dorks_data, min(args.random, len(dorks_data)))

    # 5. وضع القائمة
    if args.list:
        if not args.category:
            print("Available Categories:")
            categories = sorted(list(set(d['category'] for d in dorks_data)))
            for cat in categories:
                print(f"- {cat}")
            print("\nUse -c <category_name> to list dorks in that category.")
        else:
            print(f"Dorks in Category: {args.category}")
            for d in dorks_data: print(d['dork'])
        return

    # 6. بناء الروابط
    dorks = [d['dork'] for d in dorks_data]
    urls = [build_url(d) for d in dorks]

    # 7. تصدير CSV
    if args.csv:
        with open(args.csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Dork', 'URL'])
            writer.writerows(zip(dorks, urls))
        print(f'Saved {len(urls)} rows to {args.csv}')

    # 8. الفتح أو الطباعة
    if args.open:
        print(f"Opening {len(urls)} dorks in browser...")
        for u in urls: webbrowser.open_new_tab(u)
    else:
        for u in urls: print(u)

if __name__ == '__main__': main()
