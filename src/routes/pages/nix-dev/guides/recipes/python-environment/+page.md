# <a id="python-dev-environment"></a> راه‌اندازی محیط توسعه پایتون

در این مثال، شما به عنوان یک تمرین، یک برنامه وب پایتون با استفاده از چارچوب وب [Flask](https://flask.palletsprojects.com) خواهید ساخت.
برای استفاده‌ی بهینه از این بخش، باید با [محیط‌های اعلامی و قابل بازتولید](/pages/nix-dev/tutorials/first-steps/declarative-shell) آشنا باشید.

یک فایل جدید به نام `myapp.py` ایجاد کرده و کد زیر را به آن اضافه کنید:

```python
#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {
        "message": "Hello, Nix!"
    }

def run():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run()
```

این یک برنامه ساده Flask است که یک سند JSON با پیام `"Hello, Nix!"` را ارائه می‌دهد.

یک فایل جدید `shell.nix` برای اعلام محیط توسعه ایجاد کنید:

```nix
{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11") {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python3.withPackages (ps: [ ps.flask ]))
    curl
    jq
  ];
}
```

این سند یک محیط شل را با یک نمونه از `python3` توصیف می‌کند که شامل بسته `flask` با استفاده از [`python3.withPackages`](https://nixos.org/manual/nixpkgs/stable/#python.withpackages-function) است.
همچنین شامل [`curl`] (ابزاری برای انجام درخواست‌های وب) و [`jq`] (ابزاری برای تجزیه و قالب‌بندی اسناد JSON) می‌شود.

[`curl`]: https://search.nixos.org/packages?show=curl
[`jq`]: https://search.nixos.org/packages?show=jq

هیچ‌کدام از این دو مورد، بسته پایتون نیستند.
اگر از [virtualenv](https://virtualenv.pypa.io/en/latest/) پایتون استفاده می‌کردید، افزودن این ابزارها به محیط توسعه بدون انجام مراحل دستی اضافی امکان‌پذیر نبود.

برای ورود به محیطی که تازه اعلام کرده‌اید، دستور `nix-shell` را اجرا کنید:

```shell
$ nix-shell
these 2 derivations will be built:
  /nix/store/5yvz7zf8yzck6r9z4f1br9sh71vqkimk-builder.pl.drv
  /nix/store/aihgjkf856dbpjjqalgrdmxyyd8a5j2m-python3-3.9.13-env.drv
these 93 paths will be fetched (109.50 MiB download, 468.52 MiB unpacked):
  /nix/store/0xxjx37fcy2nl3yz6igmv4mag2a7giq6-glibc-2.33-123
  /nix/store/138azk9hs5a2yp3zzx6iy1vdwi9q26wv-hook
...

[nix-shell:~]$
```

برنامه وب را در این محیط شل راه‌اندازی کنید:

```shell
[nix-shell:~]$ python ./myapp.py
 * Serving Flask app 'myapp'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000
Press CTRL+C to quit
```

اکنون یک وب‌اپلیکیشن پایتون در حال اجرا دارید.
آن را امتحان کنید.

یک ترمینال جدید باز کنید تا جلسه دیگری از محیط شل را شروع کرده و دستورات زیر را دنبال کنید:

```shell
$ nix-shell

[nix-shell:~]$ curl 127.0.0.1:5000
{"message":"Hello, Nix!"}

[nix-shell:~]$ curl 127.0.0.1:5000 | jq '.message'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    26  100    26    0     0  13785      0 --:--:-- --:--:-- --:--:-- 26000
"Hello, Nix!"
```

همان‌طور که نشان داده شد، می‌توانید برای تست کردن وب‌اپلیکیشن در حال اجرا، بدون هیچ‌گونه نصب دستی، هم از `curl` و هم از `jq` استفاده کنید.

می‌توانید فایل‌هایی را که ایجاد کرده‌ایم به کنترل نسخه کامیت کرده و آن‌ها را با دیگران به اشتراک بگذارید.
سایر افراد نیز می‌توانند تا زمانی که [Nix را نصب کرده باشند](/pages/nix-dev/install-nix)، از همان محیط شل استفاده کنند.

## گام‌های بعدی

- [packaging-tutorial](/pages/nix-dev/tutorials/packaging-existing-software)
- [file-sets-tutorial](/pages/nix-dev/tutorials/working-with-local-files)
- [automatic-direnv](/pages/nix-dev/guides/recipes/direnv)
- [dependency-management](/pages/nix-dev/guides/recipes/dependency-management)
