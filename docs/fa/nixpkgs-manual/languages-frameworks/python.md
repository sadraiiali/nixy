# پایتون {#python}

## مرجع {#reference}

### مفسرها {#interpreters}

@python-interpreter-table@

عبارت‌های Nix برای مفسرها را می‌توان در `pkgs/development/interpreters/python` یافت.

همه بسته‌هایی که به هر مفسر پایتون وابسته هستند، در صورت وجود چنین پوشه‌ای، `out/{python.sitePackages}` به `$PYTHONPATH` آن‌ها افزوده می‌شود.

#### نبود کتابخانه استاندارد ماژول `tkinter` {#missing-tkinter-module-standard-library}

برای کاهش اندازه بستار، ماژول `Tkinter`/`tkinter` به عنوان یک بسته جداگانه، یعنی `pythonPackages.tkinter` در دسترس است.

#### صفات در بسته‌های مفسرها {#attributes-on-interpreters-packages}

هر مفسر دارای صفات زیر است:

- `libPrefix`. نام پوشه در `${python}/lib/` برای مفسر مربوطه.
- `interpreter`. نام مستعار برای `${python}/bin/${executable}`.
- `buildEnv`. تابع برای ساخت محیط‌های مفسر پایتون به همراه بسته‌های اضافی همراه شده با هم. برای نحوه استفاده و مستندات به [](#python.buildenv-function) مراجعه کنید.
- `withPackages`. رابط ساده‌تر برای `buildEnv`. برای نحوه استفاده و مستندات به [](#python.withpackages-function) مراجعه کنید.
- `sitePackages`. نام مستعار برای `lib/${libPrefix}/site

```nix
{
  lib,
  buildPythonPackage,
  fetchPypi,

  # build-system
  setuptools,
  setuptools-scm,

  # dependencies
  attrs,
  pluggy,
  py,
  setuptools,
  six,

  # tests
  hypothesis,
}:

buildPythonPackage (finalAttrs: {
  pname = "pytest";
  version = "3.3.1";
  pyproject = true;

  src = fetchPypi {
    inherit (finalAttrs) pname version;

    hash = "sha256-z4Q23FnYaVNG/NOrKW3kZCXsqwDWQJbOvnn7Ueyy65M=";
  };

  postPatch = ''
    # don't test bash builtins
    rm testing/test_argcomplete.py
  '';

  build-system = [
    setuptools
    setuptools-scm
  ];

  dependencies = [
    attrs
    py
    setuptools
    six
    pluggy
  ];

  nativeCheckInputs = [ hypothesis ];

  meta = {
    changelog = "https://github.com/pytest-dev/pytest/releases/tag/${finalAttrs.version}";
    description = "Framework for writing tests";
    homepage = "https://github.com/pytest-dev/pytest";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [
      lovek323
      madjar
      lsix
    ];
  };
})
```

های محیطی
- `package` -> بسته
- `dependencies` -> وابستگی‌ها
- `dependency` -> وابستگی
- `build dependencies` -> وابستگی‌های ساخت (build dependency -> وابستگی ساخت)
- `attribute` -> صفت (attribute -> صفت (attribute))

Checking inline backticks:
`buildPythonPackage`
`buildPhase`
`${python.pythonOnBuildForHost.interpreter}

به منظور حفظ سازگاری، هنگامی که متغیر شل `makeWrapperArgs` به صورت یک رشته‌ی جداشده با فاصله (به جای یک آرایه‌ی Bash) در اسکریپت ساخت مشخص شود، محتوای رشته پیش از الحاق به دستور `wrapProgram` توسط Bash گسترش می‌یابد. با این

```nix
buildPythonPackage (finalAttrs: {
  pname = "pyspread";
  version = "2.4";
  src = fetchPypi {
    pname = "pyspread";
    inherit (finalAttrs) version;
    hash = "sha256-...";
  };
})
```

.mkDerivation`
- `buildPythonPackage` -> `buildPythonPackage`
- `buildPythonApplication` -> `buildPythonApplication`
- build inputs -> ورودی‌های ساخت
- dependencies -> وابستگی‌ها
- build-time -> زمان ساخت
- run-time -> زمان اجرا
- package set -> مجموعه بسته / مجموعه بسته

All look solid and consistent with standard Persian terminology in

```nix
with import <nixpkgs> { };

let
  pythonPackages = python3Packages.overrideScope (
    final: prev: {
      pandas = prev.pandas.overridePythonAttrs (old: rec {
        version = "0.19.1";
        src = fetchPypi {
          pname = "pandas";
          inherit version;
          hash = "sha256-JQn+rtpy/OA2deLszSKEuxyttqBzcAil50H+JDHUdCE=";
        };
      });
    }
  );
in
(pythonPackages.python.withPackages (ps: [ ps.blaze ])).env
```

مثال بعدی، یک بازنشانی غیربدیهی از پیاده‌سازی `blas` را برای استفاده در سراسر مجموعه بسته‌های Python نشان می‌دهد:

```nix
{
  python3PackagesWithBlas = python3Packages.overrideScope (
    final: prev: {
      # We need toPythonModule for the package set to evaluate this
      blas = final.toPythonModule (prev.blas.override { blasProvider = final.mkl; });
      lapack = final.toPythonModule (prev.lapack.override { lapackProvider = final.mkl; });
    }
  );
}
```
این کار یک مجموعه بسته جدید Python ایجاد می‌کند که پیاده‌سازی‌های blas و lapack در آن روی Intel MKL تنظیم شده‌اند.

این امر به‌ویژه برای کاربران numpy و scipy که می‌خواهند با پیاده‌سازی‌های دیگر blas به سرعت بیشتری دست یابند مفید است.
توجه داشته باشید که استفاده از `scipy = super.scipy.override { blas = super.pkgs.mkl; };` احتمالاً منجر به مشکلات کامپایل خواهد شد، زیرا وابستگی‌های scipy نیز باید از همان پیاده‌سازی blas استفاده کنند.

#### تابع `buildPythonApplication` {#buildpythonapplication-function}

تابع [`buildPythonApplication`](#buildpythonapplication-function) عملاً همانند [`buildPythonPackage`](#buildpythonpackage-function) است. هدف اصلی این تابع، ساخت یک بسته Python است که در آن کاربر فقط به فایل‌های اجرایی نیاز دارد و نه ماژول‌های قابل درون‌ریزی (importable). به همین دلیل، هنگام افزودن این بسته به یک [`python.buildEnv`](#python.buildenv-function)، ماژول‌ها در دسترس قرار نخواهند گرفت.

تفاوت دیگر این است که [`buildPythonPackage`](#buildpythonpackage-function) به‌طور پیش‌فرض نام بسته‌ها را با نسخه مفسر پیشوندگذاری می‌کند. از آنجا که این موضوع برای برنامه‌ها نامربوط است، این پیشوند حذف می‌شود.

هنگام بسته‌بندی یک برنامه Python با [`buildPythonApplication`](#buildpythonapplication-function)، باید با `callPackage` فراخوانی شود و `python3` یا `python3Packages` (احتمالاً با مشخص کردن نسخه مفسر) به آن داده شود، مانند این:

```nix
{
  lib,
  python3Packages,
  fetchPypi,
}:

python3Packages.buildPythonApplication (finalAttrs: {
  pname = "luigi";
  version = "2.7.9";
  pyproject = true;

  src = fetchPypi {
    inherit (finalAttrs) pname version;
    hash = "sha256-Pe229rT0aHwA98s+nTHQMEFKZPo/yw6sot8MivFDvAw=";
  };

  build-system = with python3Packages; [ setuptools ];

  dependencies = with python3Packages; [
    tornado
    python-daemon
  ];

  meta = {
    # ...
  };
})
```

سپس این مورد درست مانند هر برنامه دیگری به `pkgs/by-name` اضافه می‌شود.

از آنجا که بسته یک برنامه است، مصرف‌کننده نیازی ندارد نگران نسخه‌ها یا ماژول‌های Python باشد، و به همین دلیل آن‌ها در `python3Packages` قرار نمی‌گیرند.

#### تابع `toPythonApplication` {#topythonapplication-function}

بین برنامه‌ها و کتابخانه‌ها تفاوت قائل می‌شود، با این حال، گاهی اوقات یک بسته به عنوان هر دو استفاده می‌شود. در این حالت، بسته به عنوان یک کتابخانه به `python-packages.nix` و به عنوان یک برنامه به `pkgs/by-name` اضافه می‌شود. برای کاهش تکرار، می‌توان از `toPythonApplication` برای تبدیل یک کتابخانه به یک برنامه استفاده کرد.

عبارت نیکس (Nix expression) باید از [`buildPythonPackage`](#buildpythonpackage-function) استفاده کرده و از `python-packages.nix` فراخوانی شود. یک ارجاع باید از `pkgs/by-name` به صفت (attribute) موجود در `python-packages.nix` ایجاد شود، و `toPythonApplication` روی این ارجاع اعمال گردد:

```nix
{ python3Packages }:

python3Packages.toPythonApplication python3Packages.youtube-dl
```

#### تابع `toPythonModule` {#topythonmodule-function}

در برخی موارد، مانند اتصال‌ها (bindings)، یک بسته با استفاده از [`stdenv.mkDer

```nix
{
  opencv = toPythonModule (
    pkgs.opencv.override {
      enablePython = true;
      pythonPackages = self;
    }
  );
}
```

حتماً به ارسال نسخه صحیح Python توجه داشته باشید!

#### تابع `mkPythonMetaPackage` {#mkpythonmetapackage-function}

این تابع یک متا-بسته حاوی [فایل‌های

```nix
mkPythonMetaPackage {
  pname = "psycopg2-binary";
  inherit (psycopg2) optional-dependencies version;
  dependencies = [ psycopg2 ];
  meta = { inherit (psycopg2.meta) description homepage; };
}
```

#### تابع `mkPythonEditablePackage` {#mkpythoneditablepackage-function}

هنگام توسعه بسته‌های پایتون، معمول است که بسته‌ها در [حالت ویرایش‌پذیر](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) نصب شوند.
مانند `mkPythonMetaPackage` این تابع نیز برای ایجاد یک بسته ایجاد شده‌است که در غیر این صورت خالی خواهد بود، اما همچنین حاوی اشاره‌گری به یک مکان ناخالص در خارج از انبار نیکس (Nix store) است که می‌توان آن را بدون بازسازی تغییر داد.

ریشه ویرایش‌پذیر به صورت یک رشته پاس داده می‌شود. معمولاً فایل‌های `.pth` حاوی مسیرهای مطلق به مکان تغییرپذیر هستند. این موضوع همیشه با Nix راحت و کارآمد نیست، بنابراین متغیرهای محیطی در زمان اجرا گستر

```nix
{
  pkgs ? import <nixpkgs> { },
}:

let
  pyproject = pkgs.lib.importTOML ./pyproject.toml;

  myPython3Packages = pkgs.python3Packages.overrideScope (
    final: _: {
      # An editable package with a script that loads our mutable location
      my-editable = final.mkPythonEditablePackage {
        # Inherit project metadata from pyproject.toml
        pname = pyproject.project.name;
        inherit (pyproject.project) version;

        # The editable root passed as a string
        root = "$REPO_ROOT/src"; # Use environment variable expansion at runtime

        # Inject a script (other PEP-621 entrypoints are also accepted)
        inherit (pyproject.project) scripts;
      };
    }
  );

  pythonEnv = myPython3Packages.python.withPackages (ps: [ ps.my-editable ]);

in
pkgs.mkShell { packages = [ pythonEnv ]; }
```

#### تابع `python.buildEnv` {#python.buildenv-function}

محیط‌های پایتون را می‌توان با استفاده از تابع سطح پایین `pkgs.buildEnv` ایجاد کرد.
این مثال نحوه‌ی ایجاد محیطی را نشان می‌دهد که دارای چارچوب وب Pyramid است.
ذخیره‌ی موارد زیر به عنوان `default.nix`

```nix
with import <nixpkgs> { };

python3.buildEnv.override {
  extraLibs = [ python3Packages.pyramid ];
  ignoreCollisions = true;
}
```

و اجرای `nix-build` ایجاد خواهد کرد

```
/nix/store/cf1xhjwzmdki7fasgr4kz6di72ykicl5-python-2.7.8-env
```

با باینری‌های پوشش‌داده‌شده در `bin/`.

همچنین می‌توانید از صفت (attribute) `env` برای ایجاد محیط‌های محلی

```nix
with import <nixpkgs> { };

(python3.buildEnv.override {
  extraLibs = with python3Packages; [
    numpy
    requests
  ];
}).env
```

شما را وارد یک شل (Shell) می‌کند که در آن Python بسته‌های مشخص‌شده را در مسیر (path) خود خواهد داشت.

##### آرگومان‌های `python.buildEnv` {#python.buildenv-arguments}

* `extraLibs`: فهرستی از بسته‌های نصب‌شده درون محیط.

```nix
with import <nixpkgs> { };

python.withPackages (ps: [ ps.pyramid ])
```

[`withPackages`](#python.withpackages-function) مجموعه بسته‌های صحیح برای نسخه مفسر مشخص را به عنوان یک آرگومان به تابع پاس می‌دهد. در مثال بالا

```nix
with import <nixpkgs> { };

python3.withPackages (ps: [ ps.pyramid ])
```

اکنون `ps` روی `python3Packages` تنظیم شده‌است که با نسخه مفسر مطابقت دارد.

از آنجا که [`python.withPackages`](#python.

```nix
with import <nixpkgs> { };

(python3.withPackages (
  ps: with ps; [
    numpy
    requests
  ]
)).env
```

در مقایسه با [`python.buildEnv`](#python.buildenv-function)، تابع [`python.withPackages`](#python.withpackages-function) از گزینه‌های پیشرفته‌تری مانند `ignoreCollisions = true` یا `postBuild` پشتیبانی نمی‌کند. اگر به این گزینه‌ها نیاز دارید، باید از [`python.buildEnv`](#python.build

```nix
buildPythonPackage.override { stdenv = customStdenv; } {
  # package attrs...
}
```

زمان اجرا -> "وابستگی‌های زمان اجرای آنها"
- Python -> Python (kept Latin as per product names rule)
- Nix, NixOS, Nixpkgs -> Nix, NixOS, Nixpkgs
- user profile -> پروفایل کاربر
- interpreter -> مفسر

Formatting check:
Headings exact match:
## User Guide {#user-guide}
### Using Python {#using-python}
#### Overview {#overview}
#### Installing Python and

```sh
$ nix-shell -p 'python313.withPackages(ps: with ps; [ numpy toolz ])'
```

به‌طور پیش‌فرض `nix-shell` یک نشست `bash` را با این مفسر در `PATH` ما شروع می‌کند، بنابراین اگر در ادامه اجرا کنیم:

```Python console
[nix-shell:~/src/nixpkgs]$ python3
Python 3.13.3 (main, Apr  8 2025, 13:54:08) [GCC 14.2.1 20250322] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy; import toolz
```

توجه داشته باشید که هیچ ماژول دیگری در دسترس نیست، حتی اگر به صورت دستوری به عنوان وابستگی یک برنامه Python در محیط کاربر ما نصب شده باشد:

```Python console
>>> import requests
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'requests'
```

می‌توانیم هر تعداد ماژول اضافی که نیاز داریم به `nix-shell` اضافه کنیم و همچنان ۱ مفسر Python پوشش‌دار (wrapped) دریافت خواهیم کرد. می‌توانیم مفسر را مستقیماً به این صورت راه‌اندازی کنیم:

```sh
$ nix-shell -p "python313.withPackages (ps: with ps; [ numpy toolz requests ])" --run python3
Python 3.13.3 (main, Apr  8 2025, 13:54:08) [GCC 14.2.1 20250322] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>>
```

توجّه کنید که این بار یک محیط پایتون جدید ساخته شد که اکنون شامل `requests` است. ساخت یک محیط فقط اسکریپت‌های پوششی (wrapper) ایجاد می‌کند که وابستگی‌های انتخاب‌شده را در دسترس مفسر قرار می‌دهند و در عین حال

```python
#!/usr/bin/env python3
import numpy as np
a = np.array([1,2])
b = np.array([3,4])
print(f"The dot product of {a} and {b} is: {np.dot(a, b)}")
```

اجرای این اسکریپت نیازمند `python3` دارای `numpy` است. با استفاده از آنچه در بخش قبلی آموختیم، می‌توانیم یک شل (Shell) را راه‌اندازی کرده و آن را به‌صورت زیر اجرا کنیم:

```ShellSession
$ nix-shell -p 'python313.withPackages (ps: with ps; [ numpy ])' --run 'python3 foo.py'
The dot product of [1 2] and [3 4] is: 11
```

اما اگر خودمان اسکریپت را نگه‌داری کنیم و وابستگی‌های بیشتری وجود داشته باشد، ممکن است خوب باشد که آن وابستگی‌ها را در

```python
#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: [ ps.numpy ])"
import numpy as np
a = np.array([1,2])
b = np.array([3,4])
print(f"The dot product of {a} and {b} is: {np.dot(a, b)}")
```

سپس آن را اجرا می‌کنیم، بدون اینکه به هیچ‌گونه آماده‌سازی محیط نیاز باشد!

```sh
$ ./foo.py
The dot product of [1 2] and [3 4] is: 11
```

درون‌ریزی Nixpkgs را از کانال Nix ما دریافت می‌کند که این موضوع به دلیل هماهنگی کش با سایر ساخت‌های بسته خوب است، اما می‌توانیم با سنجاق کردن درون

```python
#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: [ ps.numpy ])"
#!nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/e51209796c4262bfb8908e3d6d72302fe4e96f5f.tar.gz
import numpy as np
a = np.array([1,2])
b = np.array([3,4])
print(f"The dot product of {a} and {b} is: {np.dot(a, b)}")
```

.org/manual/nix/stable/command-ref/nix-shell) راهنمای Nix توضیح داده شده‌است، `nix-shell` می‌تواند یک عبارت را از یک فایل `.nix` نیز بارگذاری کند.

```nix
with import <nixpkgs> { };
(python313.withPackages (
  ps: with ps; [
    numpy
    toolz
  ]
)).env
```

و سپس در خط فرمان، تنها با تایپ کردن `nix-shell` همان محیط قبلی تولید می‌شود. در یک پروژه معمولی، احتمالاً وابستگی‌های بسیار بیشتری خواهیم داشت؛ این موضوع می‌تواند روشی را برای توسعه‌دهندگان

```nix
with import <nixpkgs> { };
let
  pythonEnv = python313.withPackages (ps: [
    ps.numpy
    ps.toolz
  ]);
in
mkShell {
  packages = [
    pythonEnv

    black
    mypy

    libffi
    openssl
  ];
}
```

این یک محیط یکپارچه ایجاد می‌کند که نه تنها مفسر Python و وابستگی‌های پایتونی آن، بلکه ابزارهایی مانند `black` یا `mypy` و کتابخانه‌هایی مانند `libffi` و `openssl` را

```nix
# ~/.config/nixpkgs/overlays/myEnv.nix
self: super: {
  myEnv = super.buildEnv {
    name = "myEnv";
    paths = [
      # A Python 3 interpreter with some packages
      (self.python3.withPackages (
        ps: with ps; [
          pyflakes
          pytest
          black
        ]
      ))

      # Some other packages we'd like as part of this env
      self.mypy
      self.black
      self.ripgrep
      self.tmux
    ];
  };
}
```

سپس می‌توانید این را بسازید و در پروفایل خود نصب کنید با:

```sh
nix-env -iA myEnv
```

یکی از محدودیت‌های این روش این است که شما تنها می‌توانید ۱ محیط پایتون را به صورت سراسری نصب داشته باشید، زیرا آن‌ها در بارگیری `python` از `PATH` شما

```nix
{
  # ...

  environment.systemPackages = with pkgs; [
    (python314.withPackages (
      ps: with ps; [
        numpy
        toolz
      ]
    ))
  ];
}
```

### توسعه با Python {#developing-with-python}

در بالا، ما بیشتر روی موارد استفاده و اقدامات لازم برای شروع ایجاد محیط‌های کاری Python در Nix تمرکز کرده بودیم.

اکنون که اصول اولیه برای شروع به کار را می‌دانید، زمان آن رسیده‌است که یک گام به عقب برداریم و نگاه عمیق‌تری به نحوه بسته‌بندی بسته‌های Python در Nix بیندازیم.

#### بسته‌های کتابخانه‌ای Python در Nixpkgs {#python-library-packages-in-nixpkgs}

در Nix تمام بسته‌ها توسط توابع ساخته می‌شوند. تابع اصلی در Nix برای ساخت کتابخانه‌های Python، تابع [`buildPythonPackage`](#buildpythonpackage-function

```nix
{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
}:

buildPythonPackage (finalAttrs: {
  pname = "toolz";
  version = "0.10.0";
  pyproject = true;

  src = fetchPypi {
    inherit (finalAttrs) pname version;
    hash = "sha256-CP3V73yWSArRHBLUct4hrNMjWZlvaaUlkpm1QP66RWA=";
  };

  build-system = [ setuptools ];

  # has no tests
  doCheck = false;

  pythonImportsCheck = [
    "toolz.itertoolz"
    "toolz.functoolz"
    "toolz.dicttoolz"
  ];

  meta = {
    changelog = "https://github.com/pytoolz/toolz/releases/tag/${finalAttrs.version}";
    homepage = "https://github.com/pytoolz/toolz";
    description = "List processing tools and functional utilities";
    license = lib.licenses.bsd3;
  };
})
```

تنظیم این موضوع استفاده می‌شود که آیا هنگام ساخت بسته باید تست‌ها اجرا شوند یا خیر.

Since there are no tests, we rely on [`pythonImportsCheck`](#using-pythonimportscheck) to test whether the package can be imported.
از آنجا که هیچ تستی وجود ندارد،

```nix
with import <nixpkgs> { };

(
  let
    my_toolz = python313Packages.buildPythonPackage (finalAttrs: {
      pname = "toolz";
      version = "0.10.0";
      pyproject = true;

      src = fetchPypi {
        inherit (finalAttrs) pname version;
        hash = "sha256-CP3V73yWSArRHBLUct4hrNMjWZlvaaUlkpm1QP66RWA=";
      };

      build-system = [ python313Packages.setuptools ];

      # has no tests
      doCheck = false;

      meta = {
        homepage = "https://github.com/pytoolz/toolz/";
        description = "List processing tools and functional utilities";
        # [...]
      };
    });

  in
  python313Packages.python.withPackages (
    ps: with ps; [
      numpy
      my_toolz
    ]
  )
).env
```

اجرای `nix-shell` منجر به ایجاد محیطی می‌شود که در آن می‌توانید از Python 3.13 و بسته `toolz` استفاده کنید. همان‌طور که می‌بینید، ما مجبور بودیم صریحاً مشخص کنیم که می‌خواهیم بسته را برای کدام نسخه از Python بسازیم.

خب، ما در اینجا چه کار کردیم؟ در واقع، عبارت نیکس (Nix expression) که قبلاً برای ساخت یک محیط Python استفاده کرده بودیم را گرفتیم و اعلام کردیم که می‌خواهیم نسخه سفارشی خودمان از `toolz` به نام `my_toolz` را شامل شود. برای تعریف بسته خودمان در محدوده [`withPackages`](#python.withpackages-function) از یک عبارت `let` استفاده کردیم.

```nix
{
  lib,
  buildPythonPackage,
  fetchFromGitHub,
  pydantic,
  pytestCheckHook,
  requests,
  setuptools,
  websocket-client,
}:

buildPythonPackage (finalAttrs: {
  pname = "dirigera";
  version = "1.2.6";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "Leggin";
    repo = "dirigera";
    tag = "v${finalAttrs.version}";
    hash = "sha256-5pfzmaIkIEtxDtkhG1lOLSTjWahEDgQKLJKbAG5rBjE=";
  };

  build-system = [ setuptools ];

  dependencies = [
    pydantic
    requests
    websocket-client
  ];

  nativeCheckInputs = [ pytestCheckHook ];

  pythonImportsCheck = [ "dirigera" ];

  meta = {
    description = "Module for controlling the IKEA Dirigera Smart Home Hub";
    homepage = "https://github.com/Leggin/dirigera";
    changelog = "https://github.com/Leggin/dirigera/releases/tag/${finalAttrs.src.tag}";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [ fab ];
    mainProgram = "generate-token";
  };
})
```

می‌توانیم چندین وابستگی زمان اجرا شامل `pydantic`، `requests` و `websocket-client` را ببینیم. علاوه بر این، [`nativeCheckInputs`](#var-stden

```nix
{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  libxml2,
  libxslt,
}:

buildPythonPackage (finalAttrs: {
  pname = "lxml";
  version = "3.4.4";
  pyproject = true;

  src = fetchPypi {
    inherit (finalAttrs) pname version;
    hash = "sha256-s9NiusRxFydHzaNRMjjxFcvWxfi45jGb9ql6eJJyQJk=";
  };

  build-system = [ setuptools ];

  buildInputs = [
    libxml2
    libxslt
  ];

  # tests are meant to be ran "in-place" in the same directory as src
  doCheck = false;

  pythonImportsCheck = [
    "lxml"
    "lxml.etree"
  ];

  meta = {
    changelog = "https://github.com/lxml/lxml/releases/tag/lxml-${finalAttrs.version}";
    description = "Pythonic binding for the libxml2 and libxslt libraries";
    homepage = "https://lxml.de";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ sjourdois ];
  };
})
```

در این مثال، `lxml` و Nix می‌توانند دقیقاً تشخیص دهند که فایل‌های مربوط به وابستگی‌ها در کجا قرار دارند. همیشه این‌طور نیست.

مثال زیر بایندینگ‌های

```nix
{
  lib,
  buildPythonPackage,
  fetchPypi,

  # build dependencies
  setuptools,

  # dependencies
  fftw,
  fftwFloat,
  fftwLongDouble,
  numpy,
  scipy,
}:

buildPythonPackage (finalAttrs: {
  pname = "pyfftw";
  version = "0.9.2";
  pyproject = true;

  src = fetchPypi {
    inherit (finalAttrs) pname version;
    hash = "sha256-9ru2r6kwhUCaskiFoaPNuJCfCVoUL01J40byvRt4kHQ=";
  };

  build-system = [ setuptools ];

  buildInputs = [
    fftw
    fftwFloat
    fftwLongDouble
  ];

  dependencies = [
    numpy
    scipy
  ];

  preConfigure = ''
    export LDFLAGS="-L${fftw.dev}/lib -L${fftwFloat.out}/lib -L${fftwLongDouble.out}/lib"
    export CFLAGS="-I${fftw.dev}/include -I${fftwFloat.dev}/include -I${fftwLongDouble.dev}/include"
  '';

  # Tests cannot import pyfftw. pyfftw works fine though.
  doCheck = false;

  pythonImportsCheck = [ "pyfftw" ];

  meta = {
    changelog = "https://github.com/pyFFTW/pyFFTW/releases/tag/v${finalAttrs.version}";
    description = "Pythonic wrapper around FFTW, the FFT library, presenting a unified interface for all the supported transforms";
    homepage = "http://hgomersall.github.com/pyFFTW";
    license = with lib.licenses; [
      bsd2
      bsd3
    ];
  };
})
```

همچنین به خط [`doCheck = false;`](#var-stdenv-doCheck) توجه کنید، ما اجرای مجموعه تست را به‌طور صریح غیرفعال کرده‌ایم.

#### تست بسته‌های Python {#testing-python-packages}

توصیه شدید می‌شود که تست کردن بخشی از ساخت بسته باشد. این کار به جلوگیری از موقعیت‌هایی کمک می‌کند که در آن بسته قادر به ساخت و نصب بوده، اما در زمان اجرا قابل استفاده نیست.
بسته شما باید [`checkPhase`](#ssec-check

```nix
{
  nativeCheckInputs = [ pytest ];
  checkPhase = ''
    runHook preCheck

    pytest

    runHook postCheck
  '';
}
```

با این حال، مجموعه تست‌های بسیاری از مخازن به خوبی با محیط ایزوله ساخت Nix سازگار نیستند و معمولاً لازم است تست‌های زیادی غیرفعال شوند.

این امر با روش‌های زیر امکان‌پذیر است:
- شامل کردن مسیرها یا آیتم‌های تست (`path/to/file.py::MyClass` یا `path/to/file.py::MyClass::test_method`) با استفاده از آرگومان‌های موقعیتی.
- مستثنی کردن مسیرها با `--ignore` یا مسیرهای تطبیق‌یافته با الگو با `--ignore-glob`.
- مستثنی کردن آیتم‌های تست با استفاده از پرچم `--deselect

```nix
{ nativeCheckInputs = [ pytestCheckHook ]; }
```

`pytestCheckHook` صفات زیر را می‌شناسد:

`enabledTestPaths` و `disabledTestPaths`

: برای مشخص کردن الگوی مسیرها (فایل‌ها یا پوشه‌ها) یا موارد تست.

`enabledTests` و `disabledTests`

: برای مشخص کردن کلیدواژه‌ها جهت نام‌های کلاس یا نام‌های متد تست.

`enabledTestMarks` و `disabledTestMarks`

```nix
{
  nativeCheckInputs = [ pytestCheckHook ];

  # Allow running the following test paths and test objects.
  enabledTestPaths = [
    # Find tests under the tests directory.
    # The trailing slash is not necessary.
    "tests/"

    # Additionally run test_foo
    "other-tests/test_foo.py::Foo::test_foo"
  ];

  # Override the above-enabled test paths and test objects.
  disabledTestPaths = [
    # Tests under tests/integration requires additional data.
    "tests/integration"
  ];

  # Allow tests by keywords matching their class names or method names.
  enabledTests = [
    # pytest by default only runs test methods begin with "test_" or end with "_test".
    # This includes all functions whose name contains "test".
    "test"
  ];

  # Override the above-enabled tests by keywords matching their class names or method names.
  disabledTests = [
    # Tests touching networks.
    "upload"
    "download"
  ];

  # Additional pytest flags
  pytestFlags = [
    # Disable benchmarks and run benchmarking tests only once.
    "--benchmark-disable"
  ];
}
```

** `"bar"` -> که هم با `"Foo"` **و هم** با `"bar"` مطابقت دارند:

Draft 4:
به عنوان مثال، می‌توانید موارد تستی مانند `TestFoo::test_bar

```nix
{
  __structuredAttrs = true;

  disabledTests = [ "Foo and bar" ];
}
```

مزایای اصلی استفاده از `pytestCheckHook` برای ساخت دستورات `pytest`
ساختاریافتگی و دسترسی‌پذیری در زمان ارزیابی است.
این امر به‌ویژه برای انتخاب تست‌ها یا مشخص کردن پرچم‌ها به صورت شرطی مفید است:

```nix
{
  disabledTests = [
    # touches network
    "download"
    "update"
  ]
  ++ lib.optionals (pythonAtLeast "3.8") [
    # broken due to python3.8 async changes
    "async"
  ]
  ++ lib.optionals stdenv.buildPlatform.isDarwin [
    # can fail when building with other packages
    "socket"
  ];
}
```

#### استفاده از pythonImportsCheck {#using-pythonimportscheck}

اگرچه تست‌های واحد برای تأیید صحت یک بسته بسیار ترجیح داده می‌شوند، اما همه بسته‌ها مجموعه تست‌هایی ندارند که بتوان به راحتی اجرا کرد و برخی نیز اصلاً تستی ندارند. برای کمک به اطمینان از اینکه بسته همچنان کار می‌کند، [`pythonImportsCheck`](#using-pythonimportscheck) می‌تواند برای درون‌ریزی ماژول‌های فهرست‌شده تلاش کند.

```nix
{
  pythonImportsCheck = [
    "requests"
    "urllib"
  ];
}
```

تقریباً به این معناست:

```nix
{
  postCheck = ''
    PYTHONPATH=$out/${python.sitePackages}:$PYTHONPATH
    python -c "import requests; import urllib"
  '';
}
```

با این حال، این کار در فاز اختصاصی خودش انجام می‌شود و به اینکه [`doCheck = true;`](#var-stdenv-doCheck) باشد یا خیر وابسته نیست.

این امر همچنین می‌تواند برای حصول اطمینان از اینکه

```
pkg1<1.0
pkg2
pkg3>=1.0,<=2.0
```

می‌توانیم انجام دهیم:

```nix
{
  pythonRelaxDeps = [
    "pkg1"
    "pkg3"
  ];
  pythonRemoveDeps = [ "pkg2" ];
}
```

که منجر به فایل `requirements.txt` زیر می‌شود:

```
pkg1
pkg3
```

گزینه‌ی دیگر، پاس دادن `true` است که تمام وابستگی‌ها را تسهیل/حذف می‌کند؛ برای مثال:

```nix
{ pythonRelaxDeps = true; }
```

که به ایجاد فایل `requirements.txt` زیر منجر می‌شود:

```
pkg1
pkg2
pkg3
```

check-phase)
- `python -m unittest discover`

All inline code intact.
Heading level preserved: `#### Using unittestCheckHook {#using-unittestcheckhook}` -> `#### استفاده از unittestCheckHook {#using-unittestcheckhook}`

Check

```nix
{
  nativeCheckInputs = [ unittestCheckHook ];

  unittestFlags = [
    "-s"
    "tests"
    "-v"
  ];
}
```

`pytest` با `unittest` سازگار است، بنابراین در بیشتر موارد می‌توانید به جای آن از `pytestCheckHook` استفاده کنید.

#### استفاده از sphinxHook {#using-sphinxhook}

ابزار `sphinxHook` ابزاری مفید برای ساخت مستندات و صفحات راهنما (manpages) با استفاده از مولد محبوب مستندات Sphinx است.
این ابزار طوری تنظیم شده‌است که به‌طور خودکار مسیرهای رایج کد منبع مستندات را پیدا کرده و آن‌ها را با استفاده از سبک پیش‌فرض `html` رندر کند.

```nix
{
  outputs = [
    "out"
    "doc"
  ];

  nativeBuildInputs = [ sphinxHook ];
}
```

این قلاب، در صورت وجود خروجی `doc`، فرآورده‌ی ساخت را به‌طور خودکار ساخته و در آن نصب می‌کند. همچنین یک تغییر مسیر خودکار برای فرآورده‌های ساختِ سازنده (Builder) `man` به سمت هدف `man` فراهم می‌کند.

```nix
{
  outputs = [
    "out"
    "doc"
    "man"
  ];

  # Use multiple builders
  sphinxBuilders = [
    "singlehtml"
    "man"
  ];
}
```

وقتی قلاب قادر به یافتن ریشه سورس مستندات شما نیست، `sphinxRoot` را بازنویسی کنید.

```nix
{
  # Configure sphinxRoot for uncommon paths
  sphinxRoot = "weird/docs/path";
}
```

این قلاب همچنین برای بسته‌های خارج از بوم‌سازگان پایتون با ارجاع به آن از طریق `sphinxHook` در سطح بالا در دسترس است.

### سازمان‌دهی بسته‌های خود {#organising-your-

```nix
{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
}:

buildPythonPackage (finalAttrs: {
  pname = "toolz";
  version = "0.10.0";
  pyproject = true;

  src = fetchPypi {
    inherit (finalAttrs) pname version;
    hash = "sha256-CP3V73yWSArRHBLUct4hrNMjWZlvaaUlkpm1QP66RWA=";
  };

  build-system = [ setuptools ];

  meta = {
    changelog = "https://github.com/pytoolz/toolz/releases/tag/${version}";
    homepage = "https://github.com/pytoolz/toolz/";
    description = "List processing tools and functional utilities";
    license = lib.licenses.bsd3;
  };
})
```

این یک آرگومان [`buildPythonPackage`](#buildpythonpackage-function) می‌گیرد. ما اکنون این تابع را با استفاده از `callPackage` در تعریف محیط خود فراخوانی می‌کنیم.

```nix
with import <nixpkgs> { };

(
  let
    toolz = callPackage /path/to/toolz/release.nix {
      buildPythonPackage = python3Packages.buildPythonPackage;
    };
  in
  python3.withPackages (ps: [
    ps.numpy
    toolz
  ])
).env
```

نکته مهمی که باید به خاطر داشت این است که نسخه Python که بسته برای آن ساخته می‌شود، به derivation `python` که به [`buildPythonPackage`](#buildpythonpackage-function) پاس داده شده بستگی دارد. Nix تلاش می‌کند در صورت امکان آرگومان‌ها را به طور خودکار پاس دهد، به همین دلیل معمولاً نیازی نیست صریحاً مشخص کنید که کدام derivation `python` باید استفاده شود. در مثال بالا ما از [`buildPythonPackage`](#buildpythonpackage-function) استفاده می‌کنیم که بخشی از مجموعه `python3Packages` است و در این حالت، مفسر `python3` به طور خودکار استفاده می‌شود.

## FAQ {#faq}

### How to solve circular dependencies? {#how-to-solve-circular-dependencies}

بسته‌های `A` و `B` را در نظر بگیرید که به یکدیگر وابسته هستند. هنگام بسته‌بندی `B`، یک راه حل این است که بسته `A` را بازنشانی کنید تا به عنوان ورودی به `B` وابسته نباشد. همین کار باید هنگام بسته‌بندی `A` نیز انجام شود.

### How to override a Python package? {#how-to-

```nix
with import <nixpkgs> { };

let
  pythonPackages = python3Packages.overrideScope (
    final: prev: {
      pandas = prev.pandas.overridePythonAttrs {
        name = "foo";
      };
    }
  );
in
(pythonPackages.python.withPackages (ps: [ ps.pandas ])).env
```

-> preserved inline code `pandas`
- `foo` -> preserved inline code `foo`
- `django` -> preserved inline code `django`
- `scipy` -> preserved inline code `sc

```nix
with import <nixpkgs> { };

let
  pythonPackages = python313Packages.overrideScope (_: prev: { scipy = prev.scipy_0_17; });
in
(pythonPackages.python.withPackages (ps: [ ps.blaze ])).env
```

بسته‌ی درخواست‌شده `blaze` به `pandas` وابسته است که خود به `scipy` وابسته است.

اگر می‌خواهید تمام Nixpkgs از تغییرات شما استفاده کند، همان‌طور که در این راهنما توضیح داده شده‌است، می‌توانید از `overlays` استفاده کنید. در مثال زیر، یک `inkscape` را با استفاده از نسخه‌ی متفاوتی از `numpy` می‌سازیم.

```nix
let
  pkgs = import <nixpkgs> { };
  newpkgs = import pkgs.path {
    overlays = [
      (_: prev: {
        python313 =
          let
            pythonPackages = prev.python313Packages.overrideScope (
              _: prev: {
                numpy = prev.numpy_1_18;
              }
            );
          in
          pythonPackages.python3;
      })
    ];
  };
in
newpkgs.inkscape
```

### دستور `python setup.py bdist_wheel` نمی‌تواند .whl را ایجاد کند {#python-setup.py-bdist_wheel-cannot-create-.whl}

اجرای `python setup.py bdist_wheel` در یک `nix-shell` با این خطا مواجه می‌شود:

```
ValueError: ZIP does not support timestamps before 1980
```

این به این دلیل است که فایل‌های انبار نیکس (Nix store) (که دارای مهر زمانی مبدأ یونیکس ۱ ژانویه ۱۹۷۰ هستند) در فایل ZIP. گنجان

```shell
nix-shell --run "SOURCE_DATE_EPOCH=315532800 python3 setup.py bdist_wheel"
```

یا زمان فعلی:

```shell
nix-shell --run "SOURCE_DATE_EPOCH=$(date +%s) python3 setup.py bdist_wheel"
```

یا `SOURCE_DATE_EPOCH` را از حالت تنظیم خارج کنید:

```shell
nix-shell --run "unset SOURCE_DATE_EPOCH; python3 setup.py bdist_wheel"
```

### مشکلات `install_data` / `data_files` {#install_data-data_files-problems}

اگر با خطای زیر مواجه شدید:

```
could not create '/nix/store/6l1bvljpy8gazlsw2aw9skwwp4pmvyxw-python-2.7.8/etc':
Permission denied
```

این یک [اشکال شناخته‌شده](https://github.com/pypa/setuptools/issues/130) در `setuptools` است. `install_data` در Setuptools از `--prefix` پیروی نمی‌کند. نمونه‌ای از چنین بسته‌ای که از این ویژگی استفاده می‌کند `pkgs/tools/X11/xpra/default.nix` است.

به عنوان راهکار موقت، آن را به عنوان یک گام اضافی `preInstall` نصب کنید:

```shell
${python.pythonOnBuildForHost.interpreter} setup.py install_data --install-dir=$out --root=$out
sed -i '/ = data\_files/d' setup.py
```

### دلیل عدم وجود site-packages سراسری {#rationale-of-non-existent-global-site-packages}

در بیشتر سیستم‌عامل‌ها یک `site-packages` سراسری نگه‌داری می‌شود. با این حال، اگر بخواهید چندین نسخه‌ی پایتون را اجرا کنید یا نسخه‌های متعددی از کتابخانه‌های خاصی را برای پروژه‌های خود داشته باشید، این امر مشکل‌ساز می‌شود. به‌طور کلی، شما چنین مشکلاتی را با ایجاد محیط‌های مجازی با استفاده از `virtualenv` حل می‌کنید.

در Nix، هر بسته دارای یک درخت وابستگی ایزوله‌شده‌است که در مورد پایتون، در دسترس بودن نسخه‌های درست مفسر و کتابخانه‌ها یا بسته‌ها را تضمین می‌کند. بنابراین نیازی به نگه‌داری یک `site-packages` سراسری وجود ندارد.

اگر می‌خواهید یک محیط پایتون برای توسعه ایجاد کنید، روش توصیه‌شده استفاده از `nix-shell` است، چه با تابع [`python.buildEnv`](#python.buildenv-function) و چه بدون آن.

### چگونه می‌توان از ماژول‌های پایتون با استفاده از pip در یک محیط مجازی استفاده کرد، مشابه آنچه در سایر سیستم‌عامل‌ها به آن عادت دارم؟ {#how-

```nix
with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in
pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.venv";
  buildInputs = [
    # A Python interpreter including the 'venv' module is required to bootstrap
    # the environment.
    pythonPackages.python

    # This executes some shell code to initialize a venv in $venvDir before
    # dropping into the shell
    pythonPackages.venvShellHook

    # Those are dependencies that we would like to use from nixpkgs, which will
    # add them to PYTHONPATH and thus make them accessible from within the venv.
    pythonPackages.numpy
    pythonPackages.requests

    # In this particular example, to compile any binary extensions they may
    # require, the Python modules listed in the hypothetical requirements.txt need
    # the following packages to be installed locally:
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib
  ];

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -r requirements.txt
  '';

  # Now we can execute any commands within the virtual environment.
  # This is optional and can be left out to run pip manually.
  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
  '';

}
```

در صورتی که `venvShellHook` ارائه‌شده کافی نباشد، می‌توانید قلاب شل سفارشی خود را تعریف کرده و مانند مثال زیر آن را متناسب با نیازهایتان تغییر دهید:

```nix
with import <nixpkgs> { };

let
  venvDir = "./.venv";
  pythonPackages = python3Packages;
in
pkgs.mkShell rec {
  name = "impurePythonEnv";
  buildInputs = [
    pythonPackages.python
    # ...
  ];

  # This is very close to how venvShellHook is implemented, but
  # adapted to use 'virtualenv'
  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s)

    if [ -d "${venvDir}" ]; then
      echo "Skipping venv creation, '${venvDir}' already exists"
    else
      echo "Creating new venv environment in path: '${venvDir}'"
      ${pythonPackages.python.interpreter} -m venv "${venvDir}"
    fi

    # Under some circumstances it might be necessary to add your virtual
    # environment to PYTHONPATH, which you can do here too;
    # PYTHONPATH=$PWD/${venvDir}/${pythonPackages.python.sitePackages}/:$PYTHONPATH

    source "${venvDir}/bin/activate"

    # As in the previous example, this is optional.
    pip install -r requirements.txt
  '';
}
```

پنهان

So:
با این حال، این بسته‌ها به‌صورت محلی در پوشه `virtualenv` ذخیره‌شده در حافظه‌ی پنهان خواهند ماند و

```nix
{
  nixpkgs.config.packageOverrides = final: _: {
    python3Packages = super.python3Packages.overrideScope (pySuper: {
      twisted = pySuper.twisted.overridePythonAttrs {
        src = final.fetchPypi {
          pname = "Twisted";
          version = "19.10.0";
          hash = "sha256-c5S6fycq5yKnTz2Wnc9Zm8TvCTvDkgOHSKSQ8XJKUV0=";
          extension = "tar.bz2";
        };
      };
    });
  };
}
```

`python3Packages.twisted` اکنون به‌صورت سراسری بازنشانی شده‌است.
همه بسته‌ها و همچنین تمام سرویس‌های NixOS که به `twisted` ارجاع می‌دهند (مانند `services.buildbot-worker`) اکنون از تعریف جدید استفاده می‌کنند.
توجه داشته باشید که `python-super` به مجموعه بسته‌های قدیمی و `python-self` به نسخه جدیدِ بازنشانی‌شده اشاره دارد.

برای تغییر دادن تنها یک مجموعه بسته‌های Python به جای کل derivation پایتون، از این قطعه‌کد استفاده کنید:

```nix
{
  myPythonPackages = python3Packages.overrideScope (final: super: { twisted = <...>; });
}
```

### چگونه یک بسته پایتون را با استفاده از اورلی‌ها بازنشانی کنیم؟ {#how-to-override-a-python-package-using-overlays}

از قالب اورلی زیر استفاده کنید:

```nix
self: _: {
  python3Packages = super.python3Packages.overrideScope (pySuper: {
    twisted = pySuper.twisted.overrideAttrs {
      src = final.fetchPypi {
        pname = "Twisted";
        version = "19.10.0";
        hash = "sha256-c5S6fycq5yKnTz2Wnc9Zm8TvCTvDkgOHSKSQ8XJKUV0=";
        extension = "tar.bz2";
      };
    };
  });
}
```

### چگونه یک بسته Python را برای تمام نسخه‌های Python با استفاده از افزونه‌ها بازنشانی کنیم؟ {#how-to-override-a-python-package-for-all-python-versions-using-extensions}

اورلی زیر،

```nix
final: prev: {
  pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
    (python-final: python-prev: {
      foo = python-prev.foo.overridePythonAttrs (oldAttrs: {
        # ...
      });
    })
  ];
}
```

### چگونه از MKL اینتل همراه با numpy و scipy استفاده کنیم؟ {#how-to-use-intels-mkl-with-numpy-and-scipy}

می‌توان MKL را با استفاده از یک overlay پیکرب

```nix
let
  pkgs = import ./. { };
  mypython = pkgs.python3.override {
    enableOptimizations = true;
    reproducibleBuild = false;
    self = mypython;
  };
in
mypython
```

### چگونه وابستگی‌های اختیاری را اضافه کنیم؟ {#python-optional-dependencies}

برخی بسته‌ها برای قابلیت‌های اضافی، وابستگی‌های اختیاری تعریف می‌کنند. در
`setuptools` به این بخش `extras_require` و در `flit` به آن
`extras-require` گفته می‌شود، در حالی که PEP 621 این‌ها را `optional-dependencies` می‌نامد.

```nix
{
  optional-dependencies = {
    complete = [ distributed ];
  };
}
```

و اجازه دادن به بسته‌ای که نیازمند ویژگی اضافی (extra) است تا این فهرست را به وابستگی‌های خود اضافه کند

```nix
{
  dependencies = [
    # ...
  ]
  ++ dask.optional-dependencies.complete;
}
```

این روش از `passthru` استفاده می‌کند، به این معنی که تغییر `optional-dependencies` یک بسته باعث ساخت مجدد آن نمی‌شود.

توجه داشته باشید که این روش بر افزودن پارامترها به سازنده‌ها ترجیح داده می‌شود، زیرا آن کار می‌تواند منجر به وابستگی بسته‌ها به گونه‌های مختلف شده و در نتیجه باعث ایجاد تداخل شود.

::: {.note}
صفت `optional-dependencies` فقط باید برای گروه‌های وابستگی به همان صورتی که

* کتابخانه‌های Python از `python-packages.nix` فراخوانی می‌شوند و با [`buildPythonPackage`](#buildpythonpackage-function) بسته‌بندی می‌گردند. عبارت یک کتابخانه باید در `pkgs/development/python-modules/<name>/default.nix` قرار داشته باشد.
* برنامه‌های Python خارج از `python-packages.nix` قرار می‌گیرند و با [`buildPythonApplication`](#buildpythonapplication-function

کل مجموعه بسته‌های Python دارای بسته‌های زیادی است که به‌طور منظم به‌روزرسانی نمی‌شوند، زیرا یا یک کامپوننت بسیار شکننده در بوم‌سازگان Python هستند، مانند بسته `hypothesis`، یا بسته‌هایی هستند که نگه‌دارنده‌ای

```ShellSession
$ maintainers/scripts/update-python-libraries --target minor --commit --use-pkgs-prefix pkgs/development/python-modules/**/default.nix
```

## زمان‌بندی به‌روزرسانی CPython {#python-cpython-update-schedule}

با [PEP 602](https://www.python.org/dev/peps/pep-0602/)، CPython اکنون از یک چرخه انتشار سالانه پیروی می‌کند. در Nixpkgs، تمامی مفسرهای پشتیبانی‌شده در دسترس قرار می‌گیرند، اما تنها مجموعه‌بسته‌های مربوط به دو مفسر اخیر ساخته می‌شوند؛ این امر راهکاری میانه بین استفاده از جدیدترین مفسر و میزان پشتیبانی اکثریت بسته‌های Python است.

مفسرهای جدید CPython در ماه اکتبر منتشر می‌شوند. به‌طور کلی، مدتی طول می‌کشد تا اکثریت پروژه‌های فعال Python از آخرین مفسر پایدار پشتیبانی کنند. برای کمک به تسهیل مهاجرت کاربران Nixpkgs بین مفسرهای Python، زمان‌بندی زیر استفاده خواهد شد:

| زمان
