# <a id="sec-memcachedTestHook"></a> `memcachedTestHook`

این قلاب یک سرور Memcached را در طول `checkPhase` راه‌اندازی می‌کند. مثال:

```nix
{ stdenv, memcachedTestHook }:
stdenv.mkDerivation {

  # ...

  nativeCheckInputs = [ memcachedTestHook ];
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

## <a id="sec-memcachedTestHook-variables"></a> متغیرها

متغیرهای مخصوص Bash:

 - `memcachedTestPort`: پورت مورد استفاده توسط Memcached. مقدار پیش‌فرض `11211` است

نمونه استفاده:

```nix
{ stdenv, memcachedTestHook }:
stdenv.mkDerivation {

  # ...

  nativeCheckInputs = [ memcachedTestHook ];

  preCheck = ''
    memcachedTestPort=1234;
  '';
}
```
