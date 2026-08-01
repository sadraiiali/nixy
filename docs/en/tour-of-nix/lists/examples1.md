# Lists & attribute sets

> Lesson **21** / 35 · path `lists/examples1`

To learn the basic syntax replace every XX in the attrset with values from the let scope.


Every exercise should evaluate to true.

## Starting code

```nix
let
  attrSet = {x = "a"; y = "b"; b = {t = true; f = false;};};
  attrSet.c = 1;
  attrSet.d = 2;
  attrSet.e.f = "g";

  list1 = [attrSet.c attrSet.d];
  list2 = [attrSet.x attrSet.y];

in
{
  #List concatenation.
  ex0 = ["a" "b" 1 2] == XX ++ XX;
}
```

## Solution

```nix
let
  attrSet = {x = "a"; y = "b"; b = {t = true; f = false;};};
  attrSet.c = 1;
  attrSet.d = 2;
  attrSet.e.f = "g";

  list1 = [attrSet.c attrSet.d];
  list2 = [attrSet.x attrSet.y];

in
{
  #List concatenation.
  ex0 = ["a" "b" 1 2] == list2 ++ list1;
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=Qg4tM_ebCoU&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=lists/examples1) · [GitHub](https://github.com/nixcloud/tour_of_nix)
