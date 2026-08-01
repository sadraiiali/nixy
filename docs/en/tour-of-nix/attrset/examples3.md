# Attribute sets: examples 3

> Lesson **17** / 35 · path `attrset/examples3`

To learn the basic syntax replace every XX in the `rec scope` with 
values from the `let scope`.

Now:

* Exercise should evaluate to true.

## Starting code

```nix
let
  attrSetBonus = {f = {add = (x: y: x + y);
                       mul = (x: y: x * y);};
                  n = {one = 1; two = 2;};};
in
rec {
  #Bonus: use only the attrSetBonus to solve this one
  exBonus = 5 == XX ( XX XX XX ) XX;
}
```

## Solution

```nix
let
  attrSetBonus = {f = {add = (x: y: x + y);
                       mul = (x: y: x * y);};
                  n = {one = 1; two = 2;};};
in
rec {
  #Bonus: use only the attrSetBonus to solve this one
  exBonus = with attrSetBonus; 5 == f.add (f.mul n.two n.two) n.one ;
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=IbRyAUZ7aKw&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=attrset/examples3) · [GitHub](https://github.com/nixcloud/tour_of_nix)
