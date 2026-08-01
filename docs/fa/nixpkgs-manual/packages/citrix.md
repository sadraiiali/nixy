اندازی این بخش، ابتدا باید [فایل `.cr` را از Netscaler Gateway بارگیری کنید](https://its.uiowa.edu/support/article/102186). پس از آن، می‌توانید `selfservice` را به

```ShellSession
$ storebrowse -C ~/Downloads/receiverconfig.cr
$ selfservice
```

## گواهی‌های سفارشی {#sec-citrix-custom-certs}

برنامه `Citrix Workspace App` در `nixpkgs` به طور پیش‌فرض به چندین گواهی [از پایگاه داده Mozilla](https://curl.haxx.se/docs/caextract.html) اعتماد دارد. با این حال، ممکن است برخی شرکت‌هایی که از Citrix استفاده می‌کنند به گواهی سازمانی اختصاصی خود نیاز داشته باشند. در توزیع‌هایی با بسته‌بندی دستوری، این گواهی‌ها را می‌توان به راحتی در [`$ICAROOT`](https://citrix.github.io/receiver-

```nix
with import <nixpkgs> { config.allowUnfree = true; };
let
  extraCerts = [
    ./custom-cert-1.pem
    ./custom-cert-2.pem # ...
  ];
in
citrix_workspace.override { inherit extraCerts; }
```
