# Google Dorks Generator (v3)

أداة بسيطة مكتوبة بلغة Python لتوليد استفسارات بحث متقدمة على جوجل (Google Dorks) من قائمة محددة.

## الميزات الجديدة في الإصدار 3

*   **التصنيف (Categories):** تجميع الـ Dorks في فئات لتسهيل التصفية.
*   **استبدال المتغيرات:** دعم استبدال المتغيرات مثل `{target_domain}` و `{keyword}` بقيمة محددة من سطر الأوامر.
*   **عوامل تشغيل إضافية:** دعم عوامل تشغيل بحث Google إضافية مثل `cache:` و `related:`.

## المتطلبات

*   Python 3.x

## طريقة الاستخدام

1.  **الاستنساخ (Clone) للمستودع:**
    ```bash
    git clone https://github.com/prof8080/google-dorks-generator
    cd google-dorks-generator
    ```

2.  **التشغيل:**

    *   **لعرض قائمة التصنيفات المتاحة:**
        ```bash
        python3 dork_generator.py -l
        ```

    *   **لعرض الـ Dorks في تصنيف معين (مثلاً "Login Pages and Admin Panels"):**
        ```bash
        python3 dork_generator.py -l -c "Login Pages and Admin Panels"
        ```

    *   **للبحث عن Dork معين وفتحه (مثلاً للبحث عن Dorks متعلقة بـ "Jira"):**
        ```bash
        python3 dork_generator.py -s Jira --open
        ```

    *   **لاستبدال متغير `{target_domain}` في الـ Dorks والبحث عن كلمة مفتاحية (مثلاً "admin") وفتح النتائج:**
        ```bash
        python3 dork_generator.py -t example.com -s admin --open
        ```

    *   **لتصدير النتائج إلى ملف CSV:**
        ```bash
        python3 dork_generator.py -t example.com --csv results.csv
        ```

    *   **لفتح جميع الـ Dorks (استخدم بحذر):**
        ```bash
        python3 dork_generator.py -o
        ```

    *   **لإنشاء روابط البحث دون فتحها:**
        ```bash
        python3 dork_generator.py
        ```

## الملفات

*   `dork_generator.py`: ملف الكود الرئيسي للأداة.
*   `dorks.txt`: ملف يحتوي على قائمة الـ Google Dorks المصنفة (واحد في كل سطر).
*   `README.md`: هذا الملف.
