# Hello World

> Lesson **3** / 35 · path `introduction/helloworld`

A simple introduction to `Strings` in Nix:

* Complete the `String` to "Hello World", replace all 'X' with 
attributes or `Strings`.

## Let expressions

The let expression is composed of:

    let <bindings> in <body>
    
The bindings are a series of definitions separated by semi-colons. 

**Note:** In Nix you can use the `let`-construct to bind a `value` to a 
`attribute` but also a `function`. In the `<body>` you can then
refer to the `bound values`, even multiple times.

More at [Nix by example part1](https://medium.com/@MrJamesFisher/nix-by-example-a0063a1a4c55#8310) by James Fisher.

## Starting code

```nix
let 
  h = "Hello";
  w = "World";
in
{
  helloWorld = h + X + X;
}
```

## Solution

```nix
let 
  h = "Hello";
  w = "World";
in
{
  helloWorld = h + " " + w;
}
```

## Video

[YouTube](https://www.youtube.com/watch?v=p0ZB03Br3lM&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=introduction/helloworld) · [GitHub](https://github.com/nixcloud/tour_of_nix)
