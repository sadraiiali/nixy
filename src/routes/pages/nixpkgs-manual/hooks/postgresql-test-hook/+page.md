# <a id="sec-postgresqlTestHook"></a> `postgresqlTestHook`

این قلاب یک سرور PostgreSQL را در طول `checkPhase` راه‌اندازی می‌کند. مثال:

```nix
{
  stdenv,
  postgresql,
  postgresqlTestHook,
}:
stdenv.mkDerivation {

  # ...

  nativeCheckInputs = [
    postgresql
    postgresqlTestHook
  ];
}
```

اگر از `checkPhase` سفارشی استفاده می‌کنید، به یاد داشته باشید که فراخوانی‌های `runHook` را اضافه کنید:

```nix
checkPhase ''
  runHook preCheck

  # ... your tests

  runHook postCheck
''
```

## <a id="sec-postgresqlTestHook-variables"></a> متغیرها

منطق قلاب تعداد مشخصی متغیر را می‌خواند و در صورت تنظیم‌نشدن یا خالی بودن، آن‌ها را به یک مقدار پیش‌فرض مقداردهی می‌کند.

متغیرهای صادرشده:

 - `PGDATA`: مکان فایل‌های سرور.
 - `PGHOST`: مکان پوشهٔ سوکت دامنه‌ی یونیکس؛ `host` پیش‌فرض در یک رشته‌ی اتصال (connection string).
 - `PGUSER`: کاربر برای ساخت / ورود با آن، پیش‌فرض: `test_user`.
 - `PGDATABASE`: نام پایگاه‌داده، پیش‌فرض: `test_db`.

متغیرهای مخصوص Bash:

 - `postgresqlTestUserOptions`: گزینه‌های SQL مورد استفاده هنگام ساخت نقش `$PGUSER`، پیش‌فرض: `"LOGIN"`. مثال: `"LOGIN SUPERUSER"`
 - `postgresqlTestSetupSQL`: دستورات SQL برای اجرا به عنوان مدیر پایگاه‌داده پس از راه‌اندازی، پیش‌فرض: دستوراتی که `$PGUSER` و `$PGDATABASE` را می‌سازند.
 - `postgresqlTestSetupCommands`: دستورات bash برای اجرا پس از شروع پایگاه‌داده، پیش‌فرض آن اجرای `$postgresqlTestSetupSQL` به عنوان مدیر پایگاه‌داده است.
 - `postgresqlEnableTCP`: برای فعال‌سازی شنود TCP روی `1` تنظیم شود. غیرقابل‌اعتماد (Flaky)؛ توصیه نمی‌شود.
 - `postgresqlStartCommands`: به‌طور پیش‌فرض `pg_ctl start`.
 - `postgresqlExtraSettings`: پیکربندی اضافی برای افزودن به `postgresql.conf`

## <a id="sec-postgresqlTestHook-hooks"></a> قلاب‌ها

تعدادی قلاب اضافی در postgresqlTestHook اجرا می‌شوند:

 - `postgresqlTestSetupPost`: پس از آماده‌سازی و پیکربندی postgresql اجرا می‌شود.

## <a id="sec-postgresqlTestHook-tcp"></a> TCP و ایزوله‌سازی Nix

`postgresqlEnableTCP` به ایزوله‌سازی شبکه متکی است که در macOS و برخی نصب‌های سفارشی Nix در دسترس نیست و منجر به تست‌های غیرقابل‌اعتماد می‌شود.
به همین دلیل، این گزینه به‌طور پیش‌فرض غیرفعال است.

راهکار ترجیحی این است که مجموعه تست را مجبور کنید از اتصال سوکت دامنه‌ی یونیکس استفاده کند. این رفتار پیش‌فرض در زمانی است که هیچ پارامتر اتصال `host` ارائه نشده باشد.
با این حال، برخی مجموعه‌های تست مقداری را برای `host` به صورت هاردکد در خود دارند، بنابراین ممکن است به یک پچ نیاز باشد. اگر می‌توانید پچ را به آپ‌استریم ارسال کنید، می‌توانید کاری کنید که در صورت تنظیم بودن متغیر محیطی `PGHOST`، مقدار `host` به‌طور پیش‌فرض به آن اشاره کند. در غیر این صورت، می‌توانید آن را به صورت محلی پچ کنید تا پارامتر `host` در رشته اتصال به طور کامل حذف شود.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> خطای `libpq: failed (could not receive data from server: Connection refused` عموماً نشان‌دهندهٔ این است که مجموعه تست در حال تلاش برای برقراری اتصال از طریق TCP است.
