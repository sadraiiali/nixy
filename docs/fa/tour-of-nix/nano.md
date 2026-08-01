# اشکال‌زدایی بسته‌بندی nano

> درس **26** از 35 · مسیر `nano`

این فایل `default.nix` مربوط به ویرایشگر متن nano در Nixpkgs است.

* تمام خطاها را پیدا کرده و برطرف کنید تا یک `مجموعه ویژگی` معتبر ارزیابی شود.

**نکته:** مجبور شدیم برخی توابع ساختگی (دامی) را اضافه کنیم، وگرنه در محیط ساده‌شدهٔ جاوا اسکریپت ما کار نمی‌کرد.

## کد شروع

```nix
let
  #dummyfunctions
  fetchurl = x: x;
  ncurses = "ncurses";
  gettext = "gettext";
in
rec {
  pname = "nano"
  version = 2.3.6";

  name = "${pname}-${version}";

  src = fetchurl {
    url = "mirror://gnu/nano/{name}.tar.gz";
    sha256 = "a74bf3f18b12c1c777ae737c0e463152439e381aba8720b4bc67449f36a09534";
  };

  buildInputs = [ ncurses gettext ];

  configureFlags = "sysconfdir=/etc";

  meta = {
    homepage = http://www.nano-editor.org/;
    description  "A small, user-friendly console text editor";
  };
}
```

## راه‌حل

```nix
let
  #dummyfunctions
  fetchurl = x: x;
  ncurses = "ncurses";
  gettext = "gettext";
in
rec {
  pname = "nano";
  version = "2.3.6";

  name = "${pname}-${version}";

  src = fetchurl {
    url = "mirror://gnu/nano/${name}.tar.gz";
    sha256 = "a74bf3f18b12c1c777ae737c0e463152439e381aba8720b4bc67449f36a09534";
  };

  buildInputs = [ ncurses gettext ];

  configureFlags = "sysconfdir=/etc";

  meta = {
    homepage = http://www.nano-editor.org/;
    description = "A small, user-friendly console text editor";
  };
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=9EcFI_hFlHs&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=nano) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
