# <a id="neovim"></a> Neovim

برای دریافت یک Neovim پایه جهت پیکربندی به صورت دستوری، `neovim-unwrapped` را نصب کنید.
این حالت نزدیک‌ترین گزینه به چیزی است که در سایر توزیع‌ها با آن مواجه می‌شوید.

`neovim` یک wrapper حول Neovim به همراه برخی پیکربندی‌های اضافی است؛ برای نمونه، برای تنظیم ارائه‌دهندگان زبان‌های مختلف مانند Python.
این wrapper را

```nix
neovim.override {
  withPython3 = true; # see `:h g:python3_host_prog`
  withNodeJs = false;
  withRuby = false;
  configure = {
    customRC = ''
      " here your custom viml configuration goes!
    '';
    packages.myVimPackage = with pkgs.vimPlugins; {
      # See examples below on how to use custom packages.
      start = [ ];
      # If a Vim plugin has a dependency that is not explicitly listed in
      # `opt`, that dependency will always be added to `start` to avoid confusion.
      opt = [ ];
    };
  };
}
```
`myVimPackage` یک نام دلخواه برای بستهٔ تولیدشده است. می‌توانید هر نامی را که دوست دارید انتخاب کنید.

اگر می‌خواهید

```nix
neovim-qt.override {
  neovim = neovim.override {
    configure = {
      customRC = ''
        " your custom viml configuration
      '';
    };
  };
}
```

می‌توانید از رپر (wrapper) ناپایدار جدید استفاده کنید، اما ممکن است رابط آن تغییر کند:
- `autoconfigure`: برخی از پلاگین‌ها برای کار با Nix به پیکربندی سفارشی نیاز دارند.
به عنوان نمونه، `sqlite-lua` برای کار کردن نیاز دارد تا `g:`

```nix
wrapNeovimUnstable neovim-unwrapped {
  autoconfigure = true;
  autowrapRuntimeDeps = true;
  luaRcContent = ''
    vim.o.sessionoptions = 'buffers,curdir,help,tabpages,winsize,winpos,localoptions'
    vim.g.mapleader = ' '
    vim.g.maplocalleader = ' '
    vim.opt.smoothscroll = true
    vim.opt.colorcolumn = { 100 }
    vim.opt.termguicolors = true
  '';
  # plugins accepts a list of either plugins or attribute sets containing:
  # { plugin = ...; config = ...; type = "viml"|"lua"; } (type defaults to "viml")
  plugins = with vimPlugins; [
    {
      plugin = vim-obsession;
      config = ''
        map <Leader>$ <Cmd>Obsession<CR>
      '';
    }
    {
      plugin = grug-far-nvim;
      type = "lua";
      config = ''
        require('grug-far').setup({
          startInInsertMode = false,
        })
      '';
    }
    (nvim-treesitter.withPlugins (p: [
      p.nix
      p.python
    ]))
    hex-nvim
  ];
  extraLuaPackages = lp: [ lp.mpack ];
  withPython3 = true;
  withNodeJs = false;
  withRuby = false;
}
```

می‌توانید پیکربندی را با `nix repl` بررسی کنید تا این گزینه‌ها را کشف کرده و آن‌ها را بازنشانی کنید. به عنوان مثال:

```nix
neovim.override {
  autowrapRuntimeDeps = false;
}
```

## <a id="neovim-plugin-specificities"></a> ویژگی‌های خاص برخی پلاگین‌ها

### <a id="neovim-plugin-required-snippet"></a> پیکربندی اختیاری پلاگین

برخی پلاگین‌ها برای کار کردن به پیکربندی خاصی نیاز دارند. ما تصمیم گرفته‌ایم این پلاگین‌ها را پچ نکنیم، بلکه پیکربندی لازم را برای پلاگین‌های Neovim تحت `PLUGIN.passthru.initLua` در دسترس قرار دهیم. به عنوان مثال، پلاگین `unicode-vim` به مسیر یک پایگاه داده یونیکد نیاز دارد، بنابراین اسنیپت زیر `vim.g.Unicode_data_directory="${'{'}'{'{'}'{'}'}self.unicode-vim{'{'}'{'}'}'{'}'}/autoload/unicode"` را تحت `vimPlugins.unicode-vim.passthru.initLua` در دسترس قرار می‌دهیم.

### <a id="neovim-plugin-license-overrides"></a> بازنشانی‌های مجوز پلاگین

پلاگین‌های تولیدشدهٔ Vim و Neovim در صورت امکان، `meta.license` خود را از متادیتای مجوز GitHub دریافت می‌کنند.
برخی از مخازن بالادستی (upstream) فایل مجوزی که GitHub بتواند آن را تشخیص دهد ارائه نمی‌دهند، یا

```nix
{
  foo-nvim = super.foo-nvim.overrideAttrs (old: {
    meta = old.meta // {
      # README says this plugin is distributed under the Vim license.
      license = lib.licenses.vim;
    };
  });
}
```

بارگذاری می‌کنند. این امر در درازمدت به معنای کار کمتر برای نگه‌دارندگان Nixpkgs است، چرا که وابستگی‌ها به صورت خودکار به‌روزرسانی می‌شوند.
این

```nix
{
  rtp-nvim = neovimUtils.buildNeovimPlugin { luaAttr = luaPackages.rtp-nvim; };
}
```
برای به‌روزرسانی این بسته‌ها، باید به‌جای آپدیتر Vim از آپدیتر Lua استفاده کنید.

برای افزودن یک بسته Lua به مجموعه `vimPlugins`، آن را به لیست `luarocksPackageNames` در [luaPackagePlugins.nix](

```nix
(pkgs.neovim.override {
  configure = {
    packages.myPlugins = with pkgs.vimPlugins; {
      start = [
        (nvim-treesitter.withPlugins (
          plugins: with plugins; [
            nix
            python
          ]
        ))
      ];
    };
  };
})
```

برای فعال‌سازی همه گرامرهای بسته‌بندی‌شده در Nixpkgs، از `pkgs.vimPlugins.nvim-treesitter.withAllGrammars` استفاده کنید.

برای نحوه پیکربندی `nvim-trees`

```nix
(pkgs.neovim.override {
  configure = {
    packages.myPlugins =
      with pkgs.vimPlugins;
      let
        # Select the grammars you need
        treesitter-grammars = with nvim-treesitter-parsers; [
          nix
          python
        ];
        # Queries are needed for treesitter based syntax highlighting and folds.
        treesitter-queries = map (p: p.associatedQuery) treesitter-grammars;
      in
      {
        start = [
          # regular plugins
        ]
        ++ treesitter-grammars
        ++ treesitter-queries;
      };
  };
})
```

### <a id="neovim-plugin-treesitter-wasm"></a> راه‌اندازی Treesitter با استفاده از پارسرها و کوئری‌های WASM

Neovim

```nix
(pkgs.wrapNeovim (pkgs.neovim-unwrapped.override { wasmSupport = true; }) {
  configure = {
    packages.myPlugins =
      with pkgs.pkgsCross.wasm32-wasip1.vimPlugins;
      let
        # Select the grammars you need
        treesitter-grammars = with nvim-treesitter-parsers; [
          nix
          python
        ];
        # Queries are needed for treesitter based syntax highlighting and folds.
        treesitter-queries = map (p: p.associatedQuery) treesitter-grammars;
      in
      {
        start = [
          # regular plugins
        ]
        ++ treesitter-grammars
        ++ treesitter-queries;
      };
  };
})
```

پارسرهای بومی و WASM را برای یک زبان یکسان به طور هم‌زمان نصب نکنید.
به عنوان مثال، نصب کردن هر دو `pkgs.vimPlugins.nvim-treesitter`

```lua
vim.api.nvim_create_autocmd('FileType', {
  pattern = { 'rust', 'javascript', 'zig' },
  callback = function(ev)
    local bufnr = ev.buf

    -- Enable treesitter syntax highlighting and parsing for the current buffer
    -- (Requires queries to be installed)
    vim.treesitter.start(bufnr)

    -- Enable treesitter based code folding
    -- (folds are window-scoped, not buffer-scoped)
    -- (Requires queries to be installed)
    vim.wo.foldexpr = 'v:lua.vim.treesitter.foldexpr()'
    vim.wo.foldmethod = 'expr'
  end,
})
```

### <a id="neovim-plugin-treesitter-grammar-dependencies"></a> گرامرهای Treesitter به عنوان وابستگی‌های پلاگین

برخی از پلاگین‌های Neovim (مانند آداپتورهای `neotest`، `markdoc-nvim`، `hurl-nvim`) به گرامرهای treesitter وابسته هستند.
این وابستگی‌ها معمولاً در بازنشانی‌های پلاگین اعلام می‌شوند.

> <span class="admonition-kind" data-kind="important"></span>
>
> **مهم**
>
> برخی از فایل‌های README پلاگین‌ها ممکن است پیشنهاد کنند که آن‌ها به `nvim-treesitter` وابسته هستند.
> **این موضوع تقریباً در تمام موارد صحت ندارد.**
>
> `nvim-treesitter` دیگر API ماژول Lua را برای استفاده‌ی سایر پلاگین‌ها ارائه نمی‌دهد.
> در اکثریت قریب به اتفاق موارد، این پلاگین‌ها:
> - **به پارسرها وابسته هستند** (نه به `nvim-treesitter` یا کوئری‌های آن).
> - **کوئری‌های خود را همراه دارند** (یا به صورت فایل‌های `*.scm` یا به صورت کدگذاری‌شده در کدهای منبع Lua).

برای افزودن گرامرها به عنوان یک وابستگی پلاگین، یک [بازنشانی](https://github.com/NixOS/nixpkgs/blob/master/

```nix
{
  foo-nvim = super.foo-nvim.overrideAttrs {
    dependencies = with self.nvim-treesitter-parsers; [
      markdown
      markdown_inline
      html
    ];
  };
}
```

اگر یک افزونه واقعاً به API ماژول قدیمی `nvim-treesitter` وابسته باشد، می‌توانید
`nvim-treesitter-legacy` را به عنوان وابستگی اضافه کنید:

```nix
{
  foo-legacy-nvim = super.foo-legacy-nvim.overrideAttrs {
    dependencies = with self; [
      nvim-treesitter-legacy
      nvim-treesitter-parsers.nix
    ];
  };
}
```

> <span class="admonition-kind" data-kind="caution"></span>
>
> **احتیاط**
>
> `nvim-treesitter-legacy` به منظور تسهیل گذار وجود دارد و در نسخه ۲۶.۱۱ حذف خواهد شد.
> اگر یک پیکربندی Neovim شامل هر دو `nvim-treesitter` و `nvim-trees`
>

> ```nix
> {
>   gitsigns-nvim = super.gitsigns-nvim.overrideAttrs {
>     dependencies = [ self.plenary-nvim ];
>     nvimRequireCheck = "gitsigns";
>   };
> }
> ```
> برخی از پلاگین‌ها دارای ماژول‌های Lua هستند که برای عملکرد درست به پیکربندی کاربر نیاز دارند یا می‌توانند شامل ماژول‌های اختیاری Lua باشند که نمی‌خواهیم با فراخوانی (require) آن‌ها را تست کنیم.
> می‌توانیم با استفاده از `nvimSkipModules` از ماژول‌های خاصی صرف‌نظر کنیم. این گزینه مانند `nvimRequireCheck` لیستی از رشته‌ها را می‌پذیرد.
> - `nvimSkipModules = [ MODULE1 MODULE2 ];`
>

> ```nix
> {
>   asyncrun-vim = super.asyncrun-vim.overrideAttrs {
>     nvimSkipModules = [
>       # vim plugin with optional toggleterm integration
>       "asyncrun.toggleterm"
>       "asyncrun.toggleterm2"
>     ];
>   };
> }
> ```
>
> در موارد نادر، ممکن است نخواهیم بارگذاری ماژول‌های Lua را برای یک پلاگین واقعاً تست کنیم. در این موارد، می‌توانیم `neovimRequireCheck` را با `doCheck = false;` غیرفعال کنیم.
>
> این کار را می‌توان به صورت دستی از طریق بازنشانی‌های تعریف پلاگین در [overrides.nix](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/editors/vim/plugins/overrides.nix) اضافه کرد.

> ```nix
> {
>   vim-test = super.vim-test.overrideAttrs {
>     # Vim plugin with a test lua file
>     doCheck = false;
>   };
> }
> ```
