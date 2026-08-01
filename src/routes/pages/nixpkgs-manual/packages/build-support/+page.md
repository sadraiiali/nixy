# <a id="sec-build-support"></a> پشتیبانی از ساخت

## <a id="pkgs-substitute"></a> `pkgs.substitute`

`pkgs.substitute` یک پوشان

```bash
substitute $infile $outfile --replace-fail @foo@ ${foopkg}/bin/foo
```

معادل است با:

```nix
{ substitute, foopkg }:
substitute {
  src = ./sourcefile.txt;
  substitutions = [
    "--replace"
    "@foo@"
    "${foopkg}/bin/foo"
  ];
}
```

## <a id="pkgs-replacevars"></a> `pkgs.replaceVars`

عبارت `pkgs.replaceVars &lt;src&gt; &lt;replacements&gt;` تمام نمونه‌های `@varName@` (ش

```bash
#! @bash@/bin/bash

echo @unchanged@
@hello@/bin/hello --greeting @greeting@
```

درایویشن زیر جایگزینی‌هایی را روی `@bash@`، `@hello@` و `@greeting@` اعمال خواهد کرد:

```nix
{
  replaceVars,
  bash,
  hello,
}:
replaceVars ./say-goodbye.sh {
  inherit bash hello;
  greeting = "goodbye";
  unchanged = null;
}
```

به‌طوری که `$out` به چیزی شبیه به زیر منجر خواهد شد:

```
#! /nix/store/s30jrpgav677fpc9yvkqsib70xfmx7xi-bash-5.2p26/bin/bash

echo @unchanged@
/nix/store/566f5isbvw014h7knmzmxa5l6hshx43k-hello-2.12.1/bin/hello --greeting goodbye
```

توجه داشته باشید که در مقایسه با `substituteAll` قدیمی، `unchanged = null` باید به‌طور صریح تنظیم شود.
هر الگوی `@...@` ار

```nix
{ replaceVarsWith }:
replaceVarsWith {
  src = ./say-goodbye.sh;

  replacements = {
    inherit bash hello;
    greeting = "goodbye";
    unchanged = null;
  };

  name = "say-goodbye";
  dir = "bin";
  isExecutable = true;
  meta.mainProgram = "say-goodbye";
}
```

این کار فایل حاصل را قابل اجرا می‌کند، آن را در `bin/say-goodbye` قرار می‌دهد و صفات `meta` را به ترتیب تنظیم می‌کند.
