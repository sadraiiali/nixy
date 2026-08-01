# رشته چندخطی

> درس **5** / 35 · مسیر `strings/multiline`

در Nix، شما اغلب از `رشته‌`های چندخطی برای ایجاد فایل‌های متنی با استفاده از دو نقل‌قول جفت، یعنی `''xxx''` در ترکیب با صفات استفاده می‌کنید:

    foo = ''
      foo: ${fooValue}
      bar: ${barValue}
    '';

درباره‌ی مدیریت رشته در Nix حتماً <https://nixos.org/manual/nix/stable/language/values> را مطالعه کنید!

بنابراین حالا:

 * قالب ex0 را مطابق آنچه بررسی‌کننده‌ی راه‌حل درخواست می‌کند، تنظیم کنید!

**نکته:** کمی با عمق توررفتگی فاصله (space) بازی کنید و ببینید چه تغییری روی رشته‌ی تولیدشده اعمال می‌کند.

**نکته:** اگر `vip` برابر با `false` باشد، یک خط جدید خالی همراه با توررفتگی دریافت می‌کنیم! همچنین می‌توانیم vipString را با استفاده از `ex0 = ''...'' + vipString` به ex0 الحاق کنیم و vipString را به جای `''` با `"` بازنویسی کنیم تا این مشکل برطرف شود، زیرا `"` فضاهای خالی ابتدایی ما را حذف نخواهد کرد.

## کد شروع

```nix
let 
  user = "mrNix";
  pass = "99supersecret";
  vip = true;
  vipString = if vip == true then ''vip: XXX '' else XXX
in
{
  ex0 = ''
  ${user}
    password: XXX
    ${vipString}
  '';
}
```

## راه‌حل

```nix
let 
  user = "mrNix";
  pass = "99supersecret";
  vip = true;
  vipString = if vip == true then ''vip: "true" '' else "";
in
{
  ex0 = ''
  ${user}
    password: ${pass}
    ${vipString}
  '';
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=DiuMuzxOqtM&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=strings/multiline) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
