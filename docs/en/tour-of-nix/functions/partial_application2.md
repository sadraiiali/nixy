# Partial application II

> Lesson **14** / 35 · path `functions/partial_application2`

Functions can be called with an `attribute set`, as we have seen. This is another common 
example of partial application, so solve it!

Complete the arguments `attribute set`:

  * A must evaluate to 'HappyFunctionsAreCalled'

## Starting code

```nix
let
  arguments = {a="Happy"; b="Awesome";};

  func = {a, b}: {d, b, c}: a+b+c+d;
in
{
  A = func arguments XXX #only modify this line
}
```

## Solution

```nix
let
  arguments = {a="Happy"; b="Awesome";};

  func = {a, b}: {d, b, c}: a+b+c+d;
in
{
  A = func arguments {d="Called"; b = "Functions"; c="Are";};
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=WaiIcgidSgs&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=functions/partial_application2) · [GitHub](https://github.com/nixcloud/tour_of_nix)
