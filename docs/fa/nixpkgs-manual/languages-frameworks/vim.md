# Vim {#vim}

می‌توان Vim را به گونه‌ای پیکربندی کرد که شامل پلاگین‌های مورد علاقه و کتابخانه‌های اضافی شما باشد.

بارگیری می‌تواند به تعویق بیفتد؛ مثال‌ها را ببینید.

در حال حاضر از دو روش مختلف برای مدیریت پلاگین‌ها پشتیبانی می‌کنیم:

- بسته‌های Vim (*توصیه‌شده*)
- vim-plug (فقط vim)

در حال حاضر دو بسته Vim در دسترس است: `vim` که بیشتر ویژگی‌های نیازمند وابستگی‌های اضافی در آن غیرفعال شده‌اند، و `vim-full` که این ویژگی‌ها در آن قابل پیکربندی بوده و به صورت پیش‌فرض فعال هستند.

::: {.note}
عبارت `vim_configurable` یک نام مستعار منسوخ‌شده برای `vim-full` است و به این واقعیت اشاره دارد که ویژگی‌های

```nix
vim-full.customize {
  # `name` optionally specifies the name of the executable and package
  name = "vim-with-plugins";

  vimrcConfig.customRC = ''
    set hidden
  '';
}
```

این پیکربندی زمانی استفاده می‌شود که Vim با دستوری که به عنوان name مشخص شده است فراخوانی شود، در این حالت `vim-with-plugins`.
همچنین می‌توانید `name` را حذف کنید تا خود Vim را سفارشی‌سازی کنید. برای تمامی گزینه‌های پشتیبانی‌شده، [تعریف `vimUtils.makeCustomizable`](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/editors/vim/plugins/vim-utils.nix#L408) را ببینید.


## مدیریت پلاگین‌ها با بسته‌های Vim {#managing-plugins-with-vim-packages}

برای ذخیره پلاگین‌های خود در بسته‌های Vim (مدیر پلاگین بومی Vim، `:help packages` را ببین

```nix
vim-full.customize {
  vimrcConfig.packages.myVimPackage = with pkgs.vimPlugins; {
    # loaded on launch
    start = [
      youcompleteme
      fugitive
    ];
    # manually loadable by calling `:packadd $plugin-name`
    # however, if a Vim plugin has a dependency that is not explicitly listed in
    # opt that dependency will always be added to start to avoid confusion.
    opt = [
      phpCompletion
      elm-vim
    ];
    # To automatically load a plugin when opening a filetype, add vimrc lines like:
    # autocmd FileType php :packadd phpCompletion
  };
}
```


بستهٔ حاصل را می‌توان به `packageOverrides` در `~/.nixpkgs/config.nix` اضافه کرد تا قابل نصب شود:

```nix
{
  packageOverrides =
    pkgs: with pkgs; {
      myVim = vim-full.customize {
        # `name` specifies the name of the executable and package
        name = "vim-with-plugins";
        # add here code from the example section
      };
      myNeovim = neovim.override {
        configure = {
          # add code from the example section here
        };
      };
    };
}
```

پس از آن می‌توانید بسته‌های پیوندخورده‌ی خاص `myVim` یا `myNeovim` خود را نصب کنید.

### اگر افزونه

```nix
{ config, pkgs, ... }:

let
  easygrep = pkgs.vimUtils.buildVimPlugin {
    name = "vim-easygrep";
    src = pkgs.fetchFromGitHub {
      owner = "dkprice";
      repo = "vim-easygrep";
      rev = "d0c36a77cc63c22648e792796b1815b44164653a";
      hash = "sha256-bL33/S+caNmEYGcMLNCanFZyEYUOUmSsedCVBn4tV3g=";
    };
  };
in
{
  environment.systemPackages = [
    (pkgs.neovim.override {
      configure = {
        packages.myPlugins = with pkgs.vimPlugins; {
          start = [
            vim-go # already packaged plugin
            easygrep # custom package
          ];
          opt = [ ];
        };
        # ...
      };
    })
  ];
}
```

اگر بسته شما به ساخت بخش‌های خاصی نیاز دارد، به‌جای آن از `pkgs.vimUtils.buildVimPlugin` استفاده کنید.

## مدیریت پلاگین‌ها با vim-plug {#managing-plugins-with-vim-plug}

برای استفاده از [vim-plug](https://github.com/junegunn/vim-plug) جهت مدیریت پلاگین‌های Vim خود، می‌توانید از مثال زیر استفاده کنید:

```nix
vim-full.customize {
  vimrcConfig.packages.myVimPackage = with pkgs.vimPlugins; {
    # loaded on launch
    plug.plugins = [
      youcompleteme
      fugitive
      phpCompletion
      elm-vim
    ];
  };
}
```

vimPlugins.nvim-treesitter)`](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/editors/vim/plugins/utils/update.py) to update the tree sitter grammars for `nvim-treesitter`.

هنگامی

```nix
{
  deoplete-fish = super.deoplete-fish.overrideAttrs (old: {
    dependencies = with super; [
      deoplete-nvim
      vim-fish
    ];
  });
}
```

گاهی اوقات پلاگین‌ها نیازمند یک بازنویسی (override) هستند که هنگام به‌روزرسانی پلاگین باید تغییر کند. این موضوع می‌تواند زمانی که پلاگین‌های Vim به صورت خودکار به‌روزرسانی می‌شوند اما بازنویسی مرتبط با آن‌ها به‌روزرسانی نمی‌شود، مشکل‌ساز شود. برای این پلاگین‌ها، بازنویسی باید به گونه‌ای نوشته شود که تمام اطلاعات لازم برای نصب پلاگین را مشخص کند و اجرای `nix-shell -p vimPluginsUpdater --run vim-plugins-updater` موجب تغییر derivation برای آن پلاگین نشود. به‌روزرسانی دستی بازنویسی برای به‌روزرسانی این نوع پلاگین‌ها ضروری است. نمونه‌ای از این دست پلاگین‌ها `LanguageClient-neovim` است.

برای افزودن یک پلاگ

```sh
nix-shell -p vimPluginsUpdater --run 'vim-plugins-updater --github-token=mytoken' # or set GITHUB_TOKEN environment variable
```

یا اینکه، برای جلوگیری از محدودسازی نرخ، تعداد پردازش‌ها را روی مقدار کمتری تنظیم کنید.

```sh
nix-shell -p vimPluginsUpdater --run 'vim-plugins-updater --proc 1'
```

برای به‌روزرسانی فقط افزونه‌های خاص، آن‌ها را بعد از دستور `update` فهرست کنید:

```sh
nix-shell -p vimPluginsUpdater --run 'vim-plugins-updater update "nvim-treesitter" "mini.nvim" "mini-nvim"'
```

اسکریپت به‌روزرسانی آرگومان‌های افزونه را در قالب‌های مختلفی می‌پذیرد:

- `"mini.nvim"` := نام مخزن GitHub، نام خام افزونه، یا نام مستعار تعریف‌شده در `vim-plugin-names`.
- `"mini-nvim"` := نام نرمال‌سازی‌شده‌ی افزونه، که با نام صفت (attribute) تولیدشده در `generated.nix` مطابقت دارد

## چگونه یک اورلی خارج از درخت (out-of-tree) از افزونه‌های vim را نگهداری کنیم؟ {#vim-out-of-tree-overlays}

شما می‌توانید از اسکریپت به‌روزرسانی برای تولید بسته‌های پایه از یک فهرست سفارشی از افزونه‌های vim استفاده کنید:

```
nix-shell -p vimPluginsUpdater --run vim-plugins-updater -i vim-plugin-names -o generated.nix --no-commit
```

با محتوای `vim-plugin-names` به عنوان مثال:

```
repo,branch,alias
pwntester/octo.nvim,,
```

سپس می‌توانید به افزونه‌های Vim تولیدشده از طریق زیر ارجاع دهید:

```nix
{
  myVimPlugins = pkgs.vimPlugins.extend ((pkgs.callPackage ./generated.nix { }));
}
```

