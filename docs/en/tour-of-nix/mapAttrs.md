# mapAttrs

> Lesson **28** / 35 · path `mapAttrs`

A function called `builtins.mapAttrs` exists which is similar to `builtins.map`.

The `mapAttrs`-function requires these arguments: a `function` and a `attrSet`. 

It evaluates the given function on every element of the given attribute set. 

Your Job: 

 * In the exercise, multiply every *value* by 7.

Documentation: <https://nixos.org/manual/nix/stable/language/builtins.html#builtins-mapAttrs>

**Note**: mapAttrs is builtin but not in this old version of the tour, just use `lib.mapAttrs` instead!

## Starting code

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  attrSet = { a = -2; b = 3; };
in 
{
  ex0 = lib.mapAttrs XXX
}
```

## Solution

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  attrSet = { a = -2; b = 3; };
in 
{
  ex0 = lib.mapAttrs (n: v: v * 7) attrSet;
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=JYHTVORLGA0&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=mapAttrs) · [GitHub](https://github.com/nixcloud/tour_of_nix)
