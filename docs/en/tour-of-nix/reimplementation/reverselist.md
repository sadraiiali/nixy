# Reimplementation: reverseList

> Lesson **30** / 35 · path `reimplementation/reverselist`

Use `fold` to implement the `reverseList` function.

**Note:** You basically implement the function `lib.reverseList`.
Your function should behave exactly the same!

## Starting code

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  reverseList = lib.fold XXX;
in
rec {
  example = lib.reverseList listOfNumbers;
  result = reverseList listOfNumbers;
}
```

## Solution

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  reverseList = lib.fold (e: acc: acc ++ [ e ]) [];
in
rec {
  example = lib.reverseList listOfNumbers;
  result = reverseList listOfNumbers;
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=LApNEuzt9Is&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=reimplementation/reverselist) · [GitHub](https://github.com/nixcloud/tour_of_nix)
