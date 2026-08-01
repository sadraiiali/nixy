# 10.4.2. قالب .narinfo

یک فایل `.narinfo` شامل [متاداده‌ی شیء انبار](/pages/nix-manual/store/store-object#metadata) در قالب [کش باینری](/pages/nix-manual/protocols/binary-cache) است.
این یک قالب ساده‌ی خط‌گرا است که در آن هر خط یک جفت `Key: Value` است.
برخی کلیدها (مانند `Sig`) ممکن است چندین بار ظاهر شوند.

نام این فایل `&lt;hash&gt;.narinfo` است که در آن `&lt;hash&gt;` بخش [هش](/pages/nix-manual/store/store-path#digest) مربوط به [مسیر انبار](/pages/nix-manual/store/store-path) شیء انبار است.

فیلدها با موارد مستندشده در قالب JSON [اطلاعات شیء انبار](/pages/nix-manual/protocols/json/store-object-info) مطابقت دارند:

| فیلد `.narinfo` | فیلد JSON | تفاوت‌ها |
|---|---|---|
| `StorePath` | [`path`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_path) | [مسیر انبار](/pages/nix-manual/store/store-path) کامل به جای [نام پایه مسیر انبار](/pages/nix-manual/store/store-path#base-name) |
| `URL` | [`url`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_url) | |
| `Compression` | [`compression`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_compression) | در صورت حذف، به‌طور پیش‌فرض `bzip2` در نظر گرفته می‌شود |
| `FileHash` | [`downloadHash`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_downloadHash) | هش کدگذاری‌شده با رشته به جای ساختاریافته |
| `FileSize` | [`downloadSize`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_downloadSize) | |
| `NarHash` | [`narHash`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_narHash) | هش کدگذاری‌شده با رشته به جای ساختاریافته |
| `NarSize` | [`narSize`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_narSize) | |
| `References` | [`references`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_references) | [نام‌های پایه مسیر انبار](/pages/nix-manual/store/store-path#base-name) جداشده با فاصله به جای آرایه JSON |
| `Deriver` | [`deriver`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_deriver) | [نام پایه مسیر انبار](/pages/nix-manual/store/store-path#base-name)؛ مقدار `unknown-deriver` به جای `null` |
| `Sig` | [`signatures`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_signatures) | ممکن است به جای استفاده از آرایه، چندین بار ظاهر شود |
| `CA` | [`ca`](/pages/nix-manual/protocols/json/store-object-info#oneOf_i2_ca) | [آدرس محتوا](/pages/nix-manual/store/store-object/content-address) کدگذاری‌شده با رشته به جای ساختاریافته |

## مثال

```
StorePath: /nix/store/n5wkd9frr45pa74if5gpz9j7mifg27fh-foo
URL: nar/1w1fff338fvdw53sqgamddn1b2xgds473pv6y13gizdbqjv4i5p3.nar.xz?sha256=1w1fff338fvdw53sqgamddn1b2xgds473pv6y13gizdbqjv4i5p3
Compression: xz
FileHash: sha256:09ymwqf5i9q7d4dm7x4pjjcqqj0qrcp5lnznbh42gfsci5hcbqqm
FileSize: 4029176
NarHash: sha256:09ymwqf5i9q7d4dm7x4pjjcqqj0qrcp5lnznbh42gfsci5hcbqqm
NarSize: 34878
References: g1w7hy3qg1w7hy3qg1w7hy3qg1w7hy3q-bar n5wkd9frr45pa74if5gpz9j7mifg27fh-foo
Deriver: g1w7hy3qg1w7hy3qg1w7hy3qg1w7hy3q-bar.drv
Sig: asdf:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
Sig: qwer:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
CA: fixed:r:sha256:1lr187v6dck1rjh2j6svpikcfz53wyl3qrlcbb405zlh13x0khhh
```
