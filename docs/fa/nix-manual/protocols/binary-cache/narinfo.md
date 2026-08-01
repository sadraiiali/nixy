# قالب `.narinfo`

یک فایل `.narinfo` شامل [متاداده‌ی شیء انبار](@docroot@/store/store-object.md#metadata) در قالب [کش باینری](@docroot@/protocols/binary-cache/index.md) است.
این یک قالب ساده‌ی خط‌گرا است که در آن هر خط یک جفت `Key: Value` است.
برخی کلیدها (مانند `Sig`) ممکن است چندین بار ظاهر شوند.

نام این فایل `<hash>.narinfo` است که در آن `<hash>` بخش [هش](@docroot@/store/store-path.md#digest) مربوط به [مسیر انبار](@docroot@/store/store-path.md) شیء انبار است.

فیلدها با موارد مستندشده در قالب JSON [اطلاعات شیء انبار](@docroot@/protocols/json/store-object-info.md) مطابقت دارند:

| فیلد `.narinfo` | فیلد JSON | تفاوت‌ها |
|---|---|---|
| `StorePath` | [`path`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_path) | [مسیر انبار](@docroot@/store/store-path.md) کامل به جای [نام پایه مسیر انبار](@docroot@/store/store-path.md#base-name) |
| `URL` | [`url`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_url) | |
| `Compression` | [`compression`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_compression) | در صورت حذف، به‌طور پیش‌فرض `bzip2` در نظر گرفته می‌شود |
| `FileHash` | [`downloadHash`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_downloadHash) | هش کدگذاری‌شده با رشته به جای ساختاریافته |
| `FileSize` | [`downloadSize`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_downloadSize) | |
| `NarHash` | [`narHash`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_narHash) | هش کدگذاری‌شده با رشته به جای ساختاریافته |
| `NarSize` | [`narSize`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_narSize) | |
| `References` | [`references`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_references) | [نام‌های پایه مسیر انبار](@docroot@/store/store-path.md#base-name) جداشده با فاصله به جای آرایه JSON |
| `Deriver` | [`deriver`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_deriver) | [نام پایه مسیر انبار](@docroot@/store/store-path.md#base-name)؛ مقدار `unknown-deriver` به جای `null` |
| `Sig` | [`signatures`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_signatures) | ممکن است به جای استفاده از آرایه، چندین بار ظاهر شود |
| `CA` | [`ca`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_ca) | [آدرس محتوا](@docroot@/store/store-object/content-address.md) کدگذاری‌شده با رشته به جای ساختاریافته |

## مثال

<!-- TODO make this include a test file instead of being manually written once we have one -->

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
