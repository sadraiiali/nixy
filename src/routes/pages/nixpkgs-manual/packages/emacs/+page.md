# <a id="sec-emacs"></a> Emacs

## <a id="sec-emacs-config"></a> پیکربندی Emacs

بسته Emacs همراه با برخی کمک‌رسان‌های اضافی ارائه می‌شود تا پیکربندی آن ساده‌تر شود. `emacs.pkgs.withPackages` به شما امکان می‌دهد بسته‌ها را از ELPA مدیریت کنید. این بدان معناست که نیازی نیست آن بسته‌ها را از درون Emacs نصب کنید. برای مثال، اگر بخواهید از `company`، `counsel`، `flycheck`، `ivy`، `magit`، `projectile` و `use-package` استفاده کنید، می‌توانید از این به عنوان یک بازنشانی در `~/.config/nixpkgs/config.nix` استفاده کنید:

```nix
{
  packageOverrides =
    pkgs: with pkgs; {
      myEmacs = emacs.pkgs.withPackages (
        epkgs:
        (with epkgs.melpaStablePackages; [
          company
          counsel
          flycheck
          ivy
          magit
          projectile
          use-package
        ])
      );
    };
}
```

می‌توانید آن را مانند هر بسته دیگری از طریق `nix-env -iA myEmacs` نصب کنید. با این حال، این کار فقط آن بسته‌ها را نصب می‌کند و آن‌ها را برای ما `configure` نخواهد کرد. برای انجام این کار، باید یک فایل پیکربندی ارائه دهیم. خوشبختانه، انجام این کار از داخل Nix امکان‌پذیر است! با تغییر مثال بالا، می‌توانیم کاری کنیم که Emacs یک فایل پیکرب

```nix
{
  packageOverrides = pkgs: {
    myEmacsConfig = pkgs.writeText "default.el" ''
      (eval-when-compile
        (require 'use-package))

      ;; load some packages

      (use-package company
        :bind ("<C-tab>" . company-complete)
        :diminish company-mode
        :commands (company-mode global-company-mode)
        :defer 1
        :config
        (global-company-mode))

      (use-package counsel
        :commands (counsel-descbinds)
        :bind (([remap execute-extended-command] . counsel-M-x)
               ("C-x C-f" . counsel-find-file)
               ("C-c g" . counsel-git)
               ("C-c j" . counsel-git-grep)
               ("C-c k" . counsel-ag)
               ("C-x l" . counsel-locate)
               ("M-y" . counsel-yank-pop)))

      (use-package flycheck
        :defer 2
        :config (global-flycheck-mode))

      (use-package ivy
        :defer 1
        :bind (("C-c C-r" . ivy-resume)
               ("C-x C-b" . ivy-switch-buffer)
               :map ivy-minibuffer-map
               ("C-j" . ivy-call))
        :diminish ivy-mode
        :commands ivy-mode
        :config
        (ivy-mode 1))

      (use-package magit
        :defer
        :if (executable-find "git")
        :bind (("C-x g" . magit-status)
               ("C-x G" . magit-dispatch-popup))
        :init
        (setq magit-completing-read-function 'ivy-completing-read))

      (use-package projectile
        :commands projectile-mode
        :bind-keymap ("C-c p" . projectile-command-map)
        :defer 5
        :config
        (projectile-global-mode))
    '';

    myEmacs = emacs.pkgs.withPackages (
      epkgs:
      (with epkgs.melpaStablePackages; [
        (runCommand "default.el" { } ''
          mkdir -p $out/share/emacs/site-lisp
          cp ${myEmacsConfig} $out/share/emacs/site-lisp/default.el
        '')
        company
        counsel
        flycheck
        ivy
        magit
        projectile
        use-package
      ])
    );
  };
}
```

این یک فایل راه‌اندازی تقریباً کامل برای Emacs فراهم می‌کند. این فایل علاوه بر پیکربندی شخصی کاربر بارگذاری می‌شود. همیشه می‌توانید با پاس دادن `-q` به دستور Emacs آن را غیرفعال کنید.

گاهی

```nix
let
  overrides = self: super: rec {
    haskell-mode = self.melpaPackages.haskell-mode;
    # ...
  };
in
((emacsPackagesFor emacs).overrideScope overrides).withPackages (
  p: with p; [
    # here both these package will use haskell-mode of our own choice
    ghc-mod
    dante
  ]
)
```
{'{'}'{'}'}'{'}'}
