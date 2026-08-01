# <a id="friction-graphics"></a> Friction

[Friction](https://friction.graphics/) یک برنامه متن‌باز گرافیک متحرک برداری برای ایجاد پویانمایی جهت پلتفرم‌های وب و ویدیو است.

## <a id="friction-graphics-wayland"></a> پشتیبانی از Wayland

پروژه بالادستی به دلیل پشتیبانی ناقص از Wayland (عدم کارکرد حالت تمام‌صفحه، از کار افتادن برخی تعاملات ماوس)، به طور صریح استفاده از X11 (XCB) را در Linux اجباری کرده است.
این موضوع بدان معناست که برنامه به طور پیش‌فرض تحت XWayland اجرا می‌شود و از مقیاس‌بندی HiDPI در سطح کامپوزیتور پیروی نمی‌کند.

برای فعال‌سازی پشتیبانی نیتیو (بومی) از Wayland و حذف بازنشانی اجباری X11:

```nix
friction-graphics.override { enableWayland = true; }
```
