# Map

> Lesson **27** / 35 · path `map`

A function called `builtins.map` exists.

The `map-function` requires these arguments: a `function` and a `list`. 
It evaluates the given function on every element of the given list. 

In the example it is used to multiply 
every number in a list by two. 

Your job:

* Use the map function to extend every `string` in **bar** with "bar". 

**Note:** You can modify the `Strings` in any way. 
They don't have to evaluate to 'foobar' (nor should they).

## Starting code

```nix
let
  bar = ["bar" "foo" "bla"];
  numbers = [1 2 3 4];
in
{
  #multiplies every number by 2
  example = map (n: n * 2) numbers; 
  #complete this
#  foobar = map ( XXX ) XXX;
}
```

## Solution

```nix
let
  bar = ["bar" "foo" "bla"];
  numbers = [1 2 3 4];
in
{
  #multiplies every number by 2
  example = map (n: n * 2) numbers; 
  #complete this
  foobar = map (x: x + "bar") bar;
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=4fp-7_yz07I&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=map) · [GitHub](https://github.com/nixcloud/tour_of_nix)
