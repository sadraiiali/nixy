# 8.3.3.12. nix-store --print-env

## نام

`nix-store --print-env` - چاپ محیط ساخت یک derivation

## خلاصه

```text
nix-store --print-env drvpath
```

## توضیحات

عملیات `--print-env` محیط یک derivation را در قالبی چاپ می‌کند که توسط یک شل قابل ارزیابی باشد. آرگومان‌های خط فرمان سازنده (builder) در متغیر `_args` قرار می‌گیرند.

## مثال

```shell
$ nix-store --print-env $(nix-instantiate '<nixpkgs>' -A firefox)
…
export src; src='/nix/store/plpj7qrwcz94z2psh6fchsi7s8yihc7k-firefox-12.0.source.tar.bz2'
export stdenv; stdenv='/nix/store/7c8asx3yfrg5dg1gzhzyq2236zfgibnn-stdenv'
export system; system='x86_64-linux'
export _args; _args='-e /nix/store/9krlzvny65gdc8s7kpb6lkx8cd02c25c-default-builder.sh'
```
