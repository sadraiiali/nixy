# Reimplementation: catAttrs

> Lesson **34** / 35 · path `reimplementation/catAttrs`

Write the function `catAttrs`. 

 `catAttrs "a" [{a = 1;} {b = 0;} {a = 2;}]; => [ 1 2 ]`

Attribute sets that don't contain the named attribute are ignored.

 **Note:** you can use the builtin function `concatLists`.

 **Note:** the right-hand side of the `? operator` has the same syntax as the assignment in attrsets (i.e., `{foo=42;}` and `{"foo" = 42;}`)
 
 **Warning:** This is hard!

## Starting code

```nix
with import <nixpkgs> { };
let
  list = [["a"] ["b"] ["c"]];
  
  attrList = [{a = 1;} {b = 0;} {a = 2;}];
  catAttrs = XXX
in
rec {
  example = builtins.concatLists list; #is [ "a" "b" "c" ]
  result = catAttrs "a" attrList; #should be [1 2] 
}
```

## Solution

```nix
with import <nixpkgs> { };
let
  list = [["a"] ["b"] ["c"]];

  attrList = [{a = 1;} {b = 0;} {a = 2;}];
  catAttrs = name: List: builtins.concatLists (map (x: if x ? ${name} then [x.${name}] else []) List);
in
rec {
  example = builtins.concatLists list; #is [ "a" "b" "c" ]
  result = catAttrs "a" attrList; #should be [1 2] 
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=x57JiHKo7Ec&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=reimplementation/catAttrs) · [GitHub](https://github.com/nixcloud/tour_of_nix)
