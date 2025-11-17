# Google Dorks Generator

أداة بسيطة مكتوبة بلغة Python لتوليد استفسارات بحث متقدمة على جوجل (Google Dorks) من قائمة محددة.

## الميزات

*   تحميل قائمة الـ Dorks من ملف نصي (`dorks.txt`).
*   عرض قائمة الـ Dorks.
*   البحث عن Dork معين وفتحه مباشرة في المتصفح.
*   إمكانية فتح جميع الـ Dorks في المتصفح (للاستخدام الحذر).

## المتطلبات

*   Python 3.x

## طريقة الاستخدام

1.  **الاستنساخ (Clone) للمستودع:**
    ```bash
    git clone [سيتم وضع رابط المستودع هنا]
    cd google-dorks-generator
    ```

2.  **التشغيل:**

    *   **لعرض قائمة الـ Dorks فقط:**
        ```bash
        python3 dork_generator.py -l
        ```

    *   **للبحث عن Dork معين وفتحه (مثلاً للبحث عن Dorks متعلقة بـ "Jira"):**
        ```bash
        python3 dork_generator.py -s Jira --open
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
*   `dorks.txt`: ملف يحتوي على قائمة الـ Google Dorks (واحد في كل سطر).
*   `README.md`: هذا الملف.
