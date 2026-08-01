# Strings

> Lesson **4** / 35 · path `strings/introduction`

Nix can also insert `Strings` with `${attribute}` where `attribute` is referenced from a let scope.
 
 * Complete ex0, ex1 and ex2 to each print 'Hello World'.

## Starting code

```nix
let 
  h = "Hello";
in
{
  ex0 = "${h} X";
  ex1 = "${h + X + X}";
  ex2 = ''${h + X + X}'';
}
```

## Solution

```nix
let 
  h = "Hello";
in
{
  ex0 = "${h} World";
  ex1 = "${h + " " + "World"}";
  ex2 = ''${h + " " + "World"}'';
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=DX97PJpQLbI&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=strings/introduction) · [GitHub](https://github.com/nixcloud/tour_of_nix)
