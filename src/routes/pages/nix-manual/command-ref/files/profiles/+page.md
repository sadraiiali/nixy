# 8.6.2. پروفایل‌ها

## پروفایل‌ها

پوشه‌ای که حاوی پیوندهایی به پروفایل‌های مدیریت‌شده توسط [`nix-env`] و [`nix profile`] است:

- مسیر `$XDG_STATE_HOME/nix/profiles` برای کاربران عادی
- مسیر `$NIX_STATE_DIR/profiles/per-user/root` اگر کاربر `root` باشد

یک پروفایل، پوشه‌ای از پیوندهای نمادین (symlinks) به فایل‌ها در انبار Nix است.

### ساختار سیستم‌فایل

نسخه‌بندی پروفایل‌ها به شکل زیر است. هنگام استفاده از یک پروفایل به نام *path*، متغیر *path* یک پیوند نمادین به *path*`-`*N*`-link` است که در آن *N* نسخهٔ پروفایل محسوب می‌شود.
به نوبه خود، *path*`-`*N*`-link` نیز یک پیوند نمادین به مسیری در انبار Nix است.
برای نمونه:

```shell
$ ls -l ~alice/.local/state/nix/profiles/profile*
lrwxrwxrwx 1 alice users 14 Nov 25 14:35 /home/alice/.local/state/nix/profiles/profile -> profile-7-link
lrwxrwxrwx 1 alice users 51 Oct 28 16:18 /home/alice/.local/state/nix/profiles/profile-5-link -> /nix/store/q69xad13ghpf7ir87h0b2gd28lafjj1j-profile
lrwxrwxrwx 1 alice users 51 Oct 29 13:20 /home/alice/.local/state/nix/profiles/profile-6-link -> /nix/store/6bvhpysd7vwz7k3b0pndn7ifi5xr32dg-profile
lrwxrwxrwx 1 alice users 51 Nov 25 14:35 /home/alice/.local/state/nix/profiles/profile-7-link -> /nix/store/mp0x6xnsg0b8qhswy6riqvimai4gm677-profile
```

هر یک از این پیوندهای نمادین (symlinks) ریشه‌ای برای جمع‌کننده‌ی زباله (garbage collector) نیکس است.

محتویات مسیر انبار متناظر با هر نسخه از پروفایل، درختی از پیوندهای نمادین به فایل‌های بسته‌های نصب‌شده است، به عنوان مثال

```shell
$ ll -R ~eelco/.local/state/nix/profiles/profile-7-link/
/home/eelco/.local/state/nix/profiles/profile-7-link/:
total 20
dr-xr-xr-x 2 root root 4096 Jan  1  1970 bin
-r--r--r-- 2 root root 1402 Jan  1  1970 manifest.nix
dr-xr-xr-x 4 root root 4096 Jan  1  1970 share

/home/eelco/.local/state/nix/profiles/profile-7-link/bin:
total 20
lrwxrwxrwx 5 root root 79 Jan  1  1970 chromium -> /nix/store/cyxny9d1zjb9l9103fr6j6kavp3bqjxf-chromium-86.0.4240.111/bin/chromium
lrwxrwxrwx 7 root root 87 Jan  1  1970 spotify -> /nix/store/w9182874m1bl56smps3m5zjj36jhp3rn-spotify-1.1.26.501.gbe11e53b-15/bin/spotify
lrwxrwxrwx 3 root root 79 Jan  1  1970 zoom-us -> /nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927/bin/zoom-us

/home/eelco/.local/state/nix/profiles/profile-7-link/share/applications:
total 12
lrwxrwxrwx 4 root root 120 Jan  1  1970 chromium-browser.desktop -> /nix/store/sqzyx2l85i6j2a77pnyvglh3bvzwmjjp-chromium-unwrapped-86.0.4240.111/share/applications/chromium-browser.desktop
lrwxrwxrwx 7 root root 110 Jan  1  1970 spotify.desktop -> /nix/store/w9182874m1bl56smps3m5zjj36jhp3rn-spotify-1.1.26.501.gbe11e53b-15/share/applications/spotify.desktop
lrwxrwxrwx 3 root root 107 Jan  1  1970 us.zoom.Zoom.desktop -> /nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927/share/applications/us.zoom.Zoom.desktop

…
```

هر نسخه از پروفایل شامل یک فایل مانیفست است:
- [`manifest.nix`](/pages/nix-manual/command-ref/files/manifest.nix) که توسط [`nix-env`](/pages/nix-manual/command-ref/nix-env) استفاده می‌شود.
- [`manifest.json`](/pages/nix-manual/command-ref/files/manifest.json) که توسط [`nix profile`](/pages/nix-manual/command-ref/new-cli/nix3-profile) (تجربی) استفاده می‌شود.

## پیوند پروفایل کاربر

یک پیوند نمادین (symlink) به پروفایل فعلی کاربر:

- `~/.nix-profile`
- مسیر `$XDG_STATE_HOME/nix/profile` در صورتی که گزینه [`use-xdg-base-directories`] روی مقدار `true` تنظیم شده باشد.

به طور پیش‌فرض، این پیوند نمادین به موارد زیر اشاره می‌کند:

- مسیر `$XDG_STATE_HOME/nix/profiles/profile` برای کاربران عادی
- مسیر `$NIX_STATE_DIR/profiles/per-user/root/profile` برای کاربر `root`

متغیر محیطی `PATH` باید زیرپوشه `/bin` پیوند پروفایل (مثلاً `~/.nix-profile/bin`) را شامل شود تا محیط کاربری برای کاربر قابل مشاهده باشد.
[نصب‌کننده](/pages/nix-manual/installation/installing-binary) به طور پیش‌فرض این مورد را راه‌اندازی می‌کند، مگر اینکه گزینه [`use-xdg-base-directories`] را فعال کنید.

[`nix-env`]: /pages/nix-manual/command-ref/nix-env
[`nix profile`]: /pages/nix-manual/command-ref/new-cli/nix3-profile
[`use-xdg-base-directories`]: /pages/nix-manual/command-ref/conf-file#conf-use-xdg-base-directories
