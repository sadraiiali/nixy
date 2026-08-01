# Packer {#sec-packer}

[Packer](https://www.packer.io) ابزاری برای ایجاد تصاویر ماشین یکسان برای چند پلتفرم از یک پیکربندی منبع واحد است.

```nix
packer.withPlugins (ps: [ ps.docker ])
```

این یک فایل اجرایی `packer` تولید می‌کند که همراه با متغیر محیطیِ تنظیم‌شدهٔ `PACKER_PLUGIN_PATH` پوشانده شده (wrapped)

```nix
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  packages = [
    (pkgs.packer.withPlugins (ps: [ ps.docker ]))
  ];
}
```

می‌توان چندین افزونه را به‌طور هم‌زمان انتخاب کرد:

```nix
packer.withPlugins (ps: [
  ps.docker
  ps.qemu
])
```

## فهرست کردن پلاگین‌های موجود {#sec-packer-list-plugins}

پلاگین‌های بسته‌بندی‌شده در قالب مجموعه ویژگی `packer.plugins` ارائه شده‌اند. برای فهرست کردن تمام پلاگین‌های موجود در نسخه Nix

```ShellSession
$ nix eval nixpkgs#packer.plugins --apply builtins.attrNames
[ "docker" "qemu" ]
```

بدون فلیک‌ها (Flakes):

```ShellSession
$ nix-env -f '<nixpkgs>' -qaP -A packer.plugins
packer.plugins.docker  packer-plugin-docker-1.1.2
packer.plugins.qemu    packer-plugin-qemu-1.1.4
```

نام صفت (attribute) (برای مثال `docker` یا `qemu`) همان چیزی است که به
`packer.withPlugins` پاس می‌دهید.

نکات:

- در حال حاضر `mkPackerPlugin` تنها از `fetchFromGitHub` به عنوان دریافت‌کننده پشتیبانی می‌کند.
