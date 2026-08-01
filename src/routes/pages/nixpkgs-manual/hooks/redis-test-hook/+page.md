# <a id="sec-redisTestHook"></a> `redisTestHook`

این قلاب یک سرور Redis را در طول `checkPhase` راه‌اندازی می‌کند. مثال:

```nix
{
  stdenv,
  redis,
  redisTestHook,
}:
stdenv.mkDerivation {

  # ...

  nativeCheckInputs = [ redisTestHook ];
}
```

اگر از یک `checkPhase` سفارشی استفاده می‌کنید، به یاد داشته باشید که فراخوانی‌های `runHook` را اضافه کنید:

```nix
{
  checkPhase = ''
    runHook preCheck

    # ... your tests

    runHook postCheck
  '';
}
```

## <a id="sec-redisTestHook-variables"></a> متغیرها

منطق hook متغیرهای زیر را می‌خواند و در صورت تنظیم‌نشدن یا خالی بودن، آن‌ها را روی یک مقدار پیش‌فرض قرار می‌دهد.

متغیرهای اکسپورت‌شده:

- `REDIS_SOCKET`: مسیر سوکت دامنه یونیکس

متغیرهای مخصوص Bash:

- `redisTestPort`: پورتی که توسط Redis استفاده می‌شود. به طور پیش‌فرض `6379` است.

مثال استفاده:

```nix
{
  stdenv,
  redis,
  redisTestHook,
}:
stdenv.mkDerivation {

  # ...

  nativeCheckInputs = [ redisTestHook ];

  preCheck = ''
    redisTestPort=6390;
  '';
}
```
