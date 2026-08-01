# Integer to string

> Lesson **6** / 35 · path `strings/typeconversion`

Inserting `Strings` using the pattern `${attribute}` works great 
with `Strings`. But `${}` can do more. You can even run functions within it.

Use this and the builtin function `toString` to make the code work.

**Note:** See also <https://noogle.dev/>

**Note:** More builtin functions can be found in the [Nix manual](https://nixos.org/manual/nix/stable/expressions/builtins.html#built-in-functions).

## Starting code

```nix
let 
  h = "Strings";
  v = 4;
in
{
  helloWorld = "${h} ${v} the win!";
}
```

## Solution

```nix
let 
  h = "Strings";
  v = 4;
in
{
  helloWorld = "${h} ${toString v} the win!";
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=fyhPbWVCv_g&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=strings/typeconversion) · [GitHub](https://github.com/nixcloud/tour_of_nix)
