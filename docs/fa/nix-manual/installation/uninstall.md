# حذف نصب Nix

## چندکاربره

حذف یک [نصب چندکاربره](./installing-binary.md#multi-user-installation) به سیستم‌عامل بستگی دارد.

### لینوکس

اگر روی لینوکس با systemd هستید:

1. سرویس daemon مربوط به Nix را حذف کنید:

```console
sudo systemctl stop nix-daemon.service
sudo systemctl disable nix-daemon.socket nix-daemon.service
sudo systemctl daemon-reload
```

2. حذف فایل‌های ایجادشده توسط Nix:

```console
sudo rm -rf /etc/nix /etc/profile.d/nix.sh /etc/tmpfiles.d/nix-daemon.conf /nix ~/.local/share/nix ~/.local/state/nix ~/.cache/nix ~/.nix-defexpr ~/.nix-profile ~/.nix-channels ~root/.nix-channels ~root/.nix-defexpr ~root/.nix-profile ~root/.cache/nix
```

۳. حذف کاربران ساخت (builders) و گروه آن‌ها:

```console
for i in $(seq 1 32); do
  sudo userdel nixbld$i
done
sudo groupdel nixbld
```

4. همچنین ممکن است ارجاعاتی به Nix در فایل‌های زیر وجود داشته باشد:
   - `/etc/bash.bashrc`
   - `/etc/bashrc`
   - `/etc/profile`
   - `/etc/zsh/zshrc`
   - `/etc/zshrc`

   که می‌توانید آن‌ها را حذف کنید.

### FreeBSD

1. سرویس daemon مربوط به Nix را متوقف کرده و حذف کنید:

```console
sudo service nix-daemon stop
sudo rm -f /usr/local/etc/rc.d/nix-daemon
sudo sysrc -x nix_daemon_enable
```

2. حذف فایل‌های ایجادشده توسط Nix:

```console
sudo rm -rf /etc/nix /usr/local/etc/profile.d/nix.sh /nix ~/.local/share/nix ~/.local/state/nix ~/.cache/nix ~/.nix-defexpr ~/.nix-profile ~/.nix-channels ~root/.nix-channels ~root/.nix-defexpr ~root/.nix-profile ~root/.cache/nix
```

۳. کاربران ساخت و گروه آن‌ها را حذف کنید:

```console
for i in $(seq 1 32); do
  sudo pw userdel nixbld$i
done
sudo pw groupdel nixbld
```

۴. همچنین ممکن است ارجاعاتی به Nix در موارد زیر وجود داشته باشد:
   - `/usr/local/etc/bashrc`
   - `/usr/local/etc/zshrc`
   - فایل‌های پیکربندی شل در پوشه‌های خانه‌ی کاربران

   که می‌توانید آن‌ها را حذف کنید.

### macOS

> **به‌روزرسانی به macOS 15 Sequoia**
>
> اگر اخیراً به macOS 15 Sequoia به‌روزرسانی کرده‌اید و دچار مشکلات زیر شده‌اید
>
> ```console
> error: the user '_nixbld1' in the group 'nixbld' does not exist
> ```
>
> هنگام اجرای دستورات Nix، برای اطلاع از دستورالعمل‌های رفع مشکل نصب بدون نیاز به نصب مجدد، به مسأله‌ی گیت‌هاب [NixOS/nix#10892](https://github.com/NixOS/nix/issues/10892) مراجعه کنید.

1. اگر فایل‌های راه‌اندازی شل سرتاسر سیستم از زمان نصب Nix تغییری نکرده‌اند، از نسخه‌های پشتیبان تهیه‌شده توسط نصب‌کننده استفاده کنید:

```console
sudo mv /etc/zshrc.backup-before-nix /etc/zshrc
sudo mv /etc/bashrc.backup-before-nix /etc/bashrc
sudo mv /etc/bash.bashrc.backup-before-nix /etc/bash.bashrc
```

در غیر این صورت، برای حذف خطوطی که `nix-daemon.sh` را منبع‌دهی (source) می‌کنند، `/etc/zshrc`، `/etc/bashrc` و `/etc/bash.bashrc` را ویرایش کنید. این خطوط باید به شکل زیر باشند:

```bash
# Nix
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
# End Nix
```

۲. متوقف کردن و حذف سرویس‌های دیمن Nix:

```console
sudo launchctl unload /Library/LaunchDaemons/org.nixos.nix-daemon.plist
sudo rm /Library/LaunchDaemons/org.nixos.nix-daemon.plist
sudo launchctl unload /Library/LaunchDaemons/org.nixos.darwin-store.plist
sudo rm /Library/LaunchDaemons/org.nixos.darwin-store.plist
```

این کار خدمت پس‌زمینه Nix را متوقف کرده و مانع از راه‌اندازی مجدد آن در بوت بعدی سیستم می‌شود.

3. گروه `nixbld` و کاربران `_nixbuildN` را حذف کنید:

```console
sudo dscl . -delete /Groups/nixbld
for u in $(sudo dscl . -list /Users | grep _nixbld); do sudo dscl . -delete /Users/$u; done
```

این کار تمام کاربران ساختی را که دیگر کاربردی ندارند حذف خواهد کرد.

4. فایل fstab را با استفاده از `sudo vifs` ویرایش کنید تا خط مربوط به متصل کردن (mount) حجم انبار Nix روی `/nix` که به شکل زیر است، حذف شود

```
UUID=<uuid> /nix apfs rw,noauto,nobrowse,suid,owners
```

یا

```
LABEL=Nix\040Store /nix apfs rw,nobrowse
```

با قرار دادن مکان‌نما روی خط مربوطه با استفاده از کلیدهای جهت‌نما، فشردن `dd` و سپس تایپ `:wq` برای ذخیره فایل.

این کار مانع از اتصال خودکار حجم انبار Nix خواهد شد.

5. فایل `/etc/synthetic.conf` را ویرایش کنید تا خط `nix` حذف شود.
   اگر این تنها خط موجود در فایل است، می‌توانید آن را به طور کامل حذف کنید:

```bash
if [ -f /etc/synthetic.conf ]; then
  if [ "$(cat /etc/synthetic.conf)" = "nix" ]; then
    sudo rm /etc/synthetic.conf
  else
    sudo vi /etc/synthetic.conf
  fi
fi
```

این کار مانع از ایجاد پوشه خالی `/nix` خواهد شد.

6. فایل‌هایی را که نیکس به سیستم شما اضافه کرده‌است، به جز انبار، حذف کنید:

```console
sudo rm -rf /etc/nix /var/root/.nix-profile /var/root/.nix-defexpr /var/root/.nix-channels ~/.nix-profile ~/.nix-defexpr ~/.nix-channels ~/.local/share/nix ~/.local/state/nix ~/.cache/nix
```

۷. حذف حجم (Volume) انبار Nix:

```console
sudo diskutil apfs deleteVolume /nix
```

این کار حجم انبار Nix و هر چیزی را که به انبار اضافه شده بود، حذف خواهد کرد.

اگر خروجی نشان دهد که فرمان نتوانسته حجم را حذف کند، باید مطمئن شوید که حجم انبار Nix _بدون اتصال_ (unmounted) ندارید.
به دنبال حجمی با نام "Nix Store" در خروجی فرمان زیر بگردید:

```console
diskutil list
```

اگر حجم «انبار نیکس» (Nix Store) را پیدا کردید، آن را با اجرای دستور `diskutil apfs deleteVolume` و شناسه `diskXsY` حجم انبار حذف کنید.

اگر خطایی مبنی بر اینکه حجم توسط هسته (kernel) در حال استفاده است دریافت کردید، سیستم را راه‌اندازی مجدد (Reboot) کرده و بلافاصله پیش از شروع هر فرآیند دیگری، حجم را حذف کنید.

> **نکته**
>
> پس از اتمام مراحل ذکر شده در اینجا، همچنان یک پوشه `/nix` خالی خواهید داشت.
> این نشانه‌ی انتظاری از یک حذف نصب موفق است.
> پوشه `/nix` خالی در راه‌اندازی مجدد (reboot) بعدی ناپدید خواهد شد.
>
> برای اتمام حذف نصب Nix نیازی به راه‌اندازی مجدد (reboot) ندارید.
> حذف نصب کامل شده‌است.
> سیستم‌عامل macOS (نسخه Catalina به بعد) مستقیماً پوشه‌های ریشه را کنترل می‌کند و ریشه‌ی فقط‌خواندنی آن مانع از حذف دستی نقطه اتصال `/nix` خالی می‌شود.

## تک‌کاربره

برای حذف یک [نصب تک‌کاربره](./installing-binary.md#single-user-installation) از Nix، دستور زیر را اجرا کنید:

```console
rm -rf /nix ~/.nix-channels ~/.nix-defexpr ~/.nix-profile ~/.local/share/nix ~/.local/state/nix ~/.cache/nix
```

ممکن است بخواهید ارجاعات به Nix را نیز به‌صورت دستی از فایل `~/.profile` خود حذف کنید.
