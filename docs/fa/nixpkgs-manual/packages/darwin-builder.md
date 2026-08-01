# darwin.linux-builder {#sec-darwin-builder}

:::{.warning}
به‌طور پیش‌فرض، `darwin.linux-builder` از یک **کلید هاست** SSH خصوصی که به‌طور عمومی شناخته‌شده است استفاده می‌کند

```
extra-trusted-users = <your username goes here>
```

برای راه‌اندازی سازنده راه دور، فلیک زیر را اجرا کنید:

```ShellSession
$ nix run nixpkgs#darwin.linux-builder
```

با این کار از شما خواسته می‌شود رمز عبور `sudo` خود را وارد کنید:

```
+ sudo --reset-timestamp /nix/store/…-install-credentials.sh ./keys
Password:
```

… تا بتواند کلید خصوصی مورد استفاده برای `ssh` به سرور ساخت را نصب کند.
پس از آن، اسکریپت ماشین مجازی را راه‌اندازی کرده و به‌طور خودکار شما را به عنوان کاربر `builder` وارد می‌کند:

```
<<< Welcome to NixOS 22.11.20220901.1bd8d11 (aarch64) - ttyAMA0 >>>

Run 'nixos-help' for the NixOS manual.

nixos login: builder (automatic login)


[builder@nixos:~]$
```

> نکته: هرگاه نیاز به متوقف کردن ماشین مجازی (VM) داشتید، `shutdown now` را با کاربر `builder` اجرا کنید.

برای واگذاری ساخت‌ها به سازنده راه دور، گزینه‌های زیر را به فایل `nix.conf` خود اضافه کنید:

```
# - Replace ${ARCH} with either aarch64 or x86_64 to match your host machine
# - Replace ${MAX_JOBS} with the maximum number of builds (pick 4 if you're not sure)
builders = ssh-ng://builder@linux-builder ${ARCH}-linux /etc/nix/builder_ed25519 ${MAX_JOBS} - - - c3NoLWVkMjU1MTkgQUFBQUMzTnphQzFsWkRJMU5URTVBQUFBSUpCV2N4Yi9CbGFxdDFhdU90RStGOFFVV3JVb3RpQzVxQkorVXVFV2RWQ2Igcm9vdEBuaXhvcwo=

# Not strictly necessary, but this will reduce your disk utilization
builders-use-substitutes = true
```

برای این‌که به Nix اجازه دهید به سازنده راه دور پیش‌فرض، که روی پورت 22 اجرا نمی‌شود، متصل شود، همچنین باید یک فایل جدید در `/etc/ssh/ssh_config.d/100-linux-builder.conf` ایجاد کنید:

```
Host linux-builder
  Hostname localhost
  HostKeyAlias linux-builder
  Port 31022
  User builder
  IdentityFile /etc/nix/builder_ed25519
```

… و سپس daemon Nix خود را راه‌اندازی مجدد کنید تا تغییر اعمال شود:

```ShellSession
$ sudo launchctl kickstart -k system/org.nixos.nix-daemon
```

توجه داشته باشید که اگر سازنده در حال اجرا باشد و فایل پیکربندی SSH بالا را ایجاد کرده باشید، می‌توانید با `sudo ssh builder@linux-builder` به سازنده SSH وصل شوید.

## نمونه استفاده از فلیک {#sec-darwin-builder-example-flake}

```nix
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-22.11-darwin";
    darwin.url = "github:nix-darwin/nix-darwin/master";
    darwin.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    {
      self,
      darwin,
      nixpkgs,
      ...
    }@inputs:
    let

      inherit (darwin.lib) darwinSystem;
      system = "aarch64-darwin";
      pkgs = nixpkgs.legacyPackages."${system}";
      linuxSystem = builtins.replaceStrings [ "darwin" ] [ "linux" ] system;

      darwin-builder = nixpkgs.lib.nixosSystem {
        system = linuxSystem;
        modules = [
          "${nixpkgs}/nixos/modules/profiles/nix-builder-vm.nix"
          {
            virtualisation = {
              host.pkgs = pkgs;
              darwin-builder.workingDirectory = "/var/lib/darwin-builder";
              darwin-builder.hostPort = 22;
            };
          }
        ];
      };
    in
    {

      darwinConfigurations = {
        machine1 = darwinSystem {
          inherit system;
          modules = [
            {
              nix.distributedBuilds = true;
              nix.buildMachines = [
                {
                  hostName = "localhost";
                  sshUser = "builder";
                  sshKey = "/etc/nix/builder_ed25519";
                  system = linuxSystem;
                  maxJobs = 4;
                  supportedFeatures = [
                    "kvm"
                    "benchmark"
                    "big-parallel"
                  ];
                }
              ];

              launchd.daemons.darwin-builder = {
                command = "${darwin-builder.config.system.build.macos-builder-installer}/bin/create-builder";
                serviceConfig = {
                  KeepAlive = true;
                  RunAtLoad = true;
                  StandardOutPath = "/var/log/darwin-builder.log";
                  StandardErrorPath = "/var/log/darwin-builder.log";
                };
              };
            }
          ];
        };
      };

    };
}
```

## پیکربندی مجدد سازنده راه دور {#sec-darwin-builder-reconfiguring}

در ابتدا نباید پیکربندی سازنده راه دور را تغییر دهید، در غیر این صورت قادر به استفاده از کش باینری نخواهید بود. با این حال، پس از اینکه سازنده راه دور را به صورت محلی در حال اجرا داشتید، می‌توانید از آن برای ساخت یک سازنده راه دور تغییریافته با فضای ذخیره‌سازی یا حافظهٔ اضافی استفاده کنید.

برای انجام این کار، کافی است پارامترهای `virtualisation.darwin-builder.*` را مشابه مثال زیر تنظیم کرده و ساخت مجدد را انجام دهید.

```nix
{
  darwin-builder = nixpkgs.lib.nixosSystem {
    system = linuxSystem;
    modules = [
      "${nixpkgs}/nixos/modules/profiles/nix-builder-vm.nix"
      {
        virtualisation.host.pkgs = pkgs;
        virtualisation.darwin-builder.diskSize = 5120;
        virtualisation.darwin-builder.memorySize = 1024;
        virtualisation.darwin-builder.hostPort = 33022;
        virtualisation.darwin-builder.workingDirectory = "/var/lib/darwin-builder";
      }
    ];
  };
}
```

شما می‌توانید هر تغییر دیگری را روی ماشین مجازی (VM) خود در این مجموعه ویژگی اعمال کنید. به عنوان مثال، می‌توانید Docker یا بازارسال X11 به هاست Darwin خود را فعال کنید.

## عیب‌یابی پیکربندی ایجادشده {#sec-darwin-builder-troubleshoot}

بسته `linux-builder` صفات `nixosConfig` و `nixos

```
$ nix repl --file ~/src/nixpkgs --argstr system aarch64-darwin

nix-repl> darwin.linux-builder.nixosConfig.nix.package
«derivation /nix/store/...-nix-2.17.0.drv»

nix-repl> :p darwin.linux-builder.nixosOptions.virtualisation.memorySize.definitionsWithLocations
[ { file = "/home/user/src/nixpkgs/nixos/modules/profiles/nix-builder-vm.nix"; value = 3072; } ]

```
