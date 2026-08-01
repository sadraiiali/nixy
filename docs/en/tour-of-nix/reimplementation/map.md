# Fold: Implementing 'map'

> Lesson **31** / 35 · path `reimplementation/map`

Use `fold` to write your own `map` function.

**Note:** The little error is intended, FIX IT!

## Starting code

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  myMap = XXX fold XXX; 
in
rec {
  #your map should create the same result as the standard map function
  example = map (x: builtins.div x 2) listOfNumbers; 
  result = myMap (x: builtins.div x 2) listOfNumbers;
}
```

## Solution

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  myMap = op: list: lib.fold (x: y: [(op x)] ++ y) [] list; 
in
rec {
  #your map should create the same result as the standard map function
  example = map (x: builtins.div x 2) listOfNumbers; 
  result = myMap (x: builtins.div x 2) listOfNumbers;
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=RZuWUn_QHnQ&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=reimplementation/map) · [GitHub](https://github.com/nixcloud/tour_of_nix)
