# زبان‌ها و چارچوب‌ها {#chap-language-support}

[محیط ساخت استاندارد](#chap-stdenv) ساخت بسته‌های معمول بر پایه Autotools را با کد بسیار کمی آسان می‌کند. هر نوع بسته دیگری را می‌توان با بازنشانی ف
```shell-session
  $ nix repl -f '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable
  nix-repl> javaPackages.<tab>
  javaPackages.compiler               javaPackages.openjfx15              javaPackages.openjfx21              javaPackages.recurseForDerivations
  javaPackages.jogl_2_4_0             javaPackages.openjfx17              javaPackages.openjfx25
  javaPackages.mavenfod               javaPackages.openjfx19              javaPackages.override
  javaPackages.openjfx11              javaPackages.openjfx20              javaPackages.overrideDerivation
  ```
شود.

Wait, "marked as broken": "به‌عنوان خراب علامت‌گذاری شده‌است" or "به‌عنوان معیوب علامت‌گذاری شده‌است".
Link text in original: [marked
```shell-session
  $ nix-env -qaP -f '<nixpkgs>' -A pythonPackages -I nixpkgs=channel:nixpkgs-unstable
  ```

  ```console
  pythonPackages.avahi                                                  avahi-0.8
  pythonPackages.boost                                                  boost-1.81.0
  pythonPackages.caffe                                                  caffe-1.0
  pythonPackages.caffeWithCuda                                          caffe-1.0
  pythonPackages.cbeams                                                 cbeams-1.0.3
  …
  ```
:::

```{=include=} sections
agda.section.md
android.section.md
astal.section.md
beam.section.md
chicken.section.md
cosmic.section.md
crystal.section.md
cuda.section.md
cuelang.section.md
dart.section.md
dhall.section.md
dlang.section.md
dotnet.section.md
emscripten.section.md
factor.section.md
gnome.section.md
go.section.md
gradle.section.md
hare.section.md
haskell.section.md
hy.section.md
idris.section.md
idris2.section.md
ios.section.md
java.section.md
javascript.section.md
julia.section.md
lean4.section.md
lisp.section.md
lua.section.md
maven.section.md
nim.section.md
ocaml.section.md
octave.section.md
perl.section.md
php.section.md
pkg-config.section.md
python.section.md
qt.section.md
r.section.md
rocq.section.md
ruby.section.md
rust.section.md
scheme.section.md
swift.section.md
tcl.section.md
texlive.section.md
typst.section.md
vim.section.md
neovim.section.md
```
