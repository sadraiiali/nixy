# <a id="chap-language-support"></a> زبان‌ها و چارچوب‌ها

[محیط ساخت استاندارد](#chap-stdenv) ساخت بسته‌های معمول بر پایه Autotools را با کد بسیار کمی آسان می‌کند. هر نوع بسته دیگری را می‌توان با بازنشانی ف

```shell
  $ nix repl -f '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable
  nix-repl> javaPackages.<tab>
  javaPackages.compiler               javaPackages.openjfx15              javaPackages.openjfx21              javaPackages.recurseForDerivations
  javaPackages.jogl_2_4_0             javaPackages.openjfx17              javaPackages.openjfx25
  javaPackages.mavenfod               javaPackages.openjfx19              javaPackages.override
  javaPackages.openjfx11              javaPackages.openjfx20              javaPackages.overrideDerivation
  ```
شود.

Wait, "marked as broken": "به‌عنوان خراب علامت‌گذاری شده است" or "به‌عنوان معیوب علامت‌گذاری شده است".
Link text in original: [marked

```shell
  $ nix-env -qaP -f '<nixpkgs>' -A pythonPackages -I nixpkgs=channel:nixpkgs-unstable
  ```

  ```shell
  pythonPackages.avahi                                                  avahi-0.8
  pythonPackages.boost                                                  boost-1.81.0
  pythonPackages.caffe                                                  caffe-1.0
  pythonPackages.caffeWithCuda                                          caffe-1.0
  pythonPackages.cbeams                                                 cbeams-1.0.3
  …
  ```

- [Agda](/pages/nixpkgs-manual/languages-frameworks/agda)
- [Android](/pages/nixpkgs-manual/languages-frameworks/android)
- [Astal](/pages/nixpkgs-manual/languages-frameworks/astal)
- [زبان‌های BEAM (Erlang، Elixir و LFE)](/pages/nixpkgs-manual/languages-frameworks/beam)
- [CHICKEN](/pages/nixpkgs-manual/languages-frameworks/chicken)
- [COSMIC](/pages/nixpkgs-manual/languages-frameworks/cosmic)
- [Crystal](/pages/nixpkgs-manual/languages-frameworks/crystal)
- [CUDA](/pages/nixpkgs-manual/languages-frameworks/cuda)
- [Cue (Cuelang)](/pages/nixpkgs-manual/languages-frameworks/cuelang)
- [Dart](/pages/nixpkgs-manual/languages-frameworks/dart)
- [Dhall](/pages/nixpkgs-manual/languages-frameworks/dhall)
- [D (Dlang)](/pages/nixpkgs-manual/languages-frameworks/dlang)
- [Dotnet](/pages/nixpkgs-manual/languages-frameworks/dotnet)
- [Emscripten](/pages/nixpkgs-manual/languages-frameworks/emscripten)
- [Factor](/pages/nixpkgs-manual/languages-frameworks/factor)
- [GNOME](/pages/nixpkgs-manual/languages-frameworks/gnome)
- [Go](/pages/nixpkgs-manual/languages-frameworks/go)
- [Gradle](/pages/nixpkgs-manual/languages-frameworks/gradle)
- [Hare](/pages/nixpkgs-manual/languages-frameworks/hare)
- [Haskell](/pages/nixpkgs-manual/languages-frameworks/haskell)
- [Hy](/pages/nixpkgs-manual/languages-frameworks/hy)
- [Idris](/pages/nixpkgs-manual/languages-frameworks/idris)
- [Idris2](/pages/nixpkgs-manual/languages-frameworks/idris2)
- [iOS](/pages/nixpkgs-manual/languages-frameworks/ios)
- [Java](/pages/nixpkgs-manual/languages-frameworks/java)
- [Javascript](/pages/nixpkgs-manual/languages-frameworks/javascript)
- [julia](/pages/nixpkgs-manual/languages-frameworks/julia)
- [Lean 4](/pages/nixpkgs-manual/languages-frameworks/lean4)
- [lisp](/pages/nixpkgs-manual/languages-frameworks/lisp)
- [Lua](/pages/nixpkgs-manual/languages-frameworks/lua)
- [Maven](/pages/nixpkgs-manual/languages-frameworks/maven)
- [Nim](/pages/nixpkgs-manual/languages-frameworks/nim)
- [OCaml](/pages/nixpkgs-manual/languages-frameworks/ocaml)
- [Octave](/pages/nixpkgs-manual/languages-frameworks/octave)
- [Perl](/pages/nixpkgs-manual/languages-frameworks/perl)
- [PHP](/pages/nixpkgs-manual/languages-frameworks/php)
- [pkg-config](/pages/nixpkgs-manual/languages-frameworks/pkg-config)
- [پایتون](/pages/nixpkgs-manual/languages-frameworks/python)
- [Qt](/pages/nixpkgs-manual/languages-frameworks/qt)
- [R](/pages/nixpkgs-manual/languages-frameworks/r)
- [Rocq و بسته‌های rocq](/pages/nixpkgs-manual/languages-frameworks/rocq)
- [Ruby](/pages/nixpkgs-manual/languages-frameworks/ruby)
- [Rust](/pages/nixpkgs-manual/languages-frameworks/rust)
- [Scheme](/pages/nixpkgs-manual/languages-frameworks/scheme)
- [Swift](/pages/nixpkgs-manual/languages-frameworks/swift)
- [tcl](/pages/nixpkgs-manual/languages-frameworks/tcl)
- [texlive](/pages/nixpkgs-manual/languages-frameworks/texlive)
- [Typst](/pages/nixpkgs-manual/languages-frameworks/typst)
- [Vim](/pages/nixpkgs-manual/languages-frameworks/vim)
- [Neovim](/pages/nixpkgs-manual/languages-frameworks/neovim)
