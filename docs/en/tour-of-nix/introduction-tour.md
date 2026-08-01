# How it works...

> Lesson **2** / 35 · path `introduction-tour`

## Usability
1. You read the description/text on the `right pane`
  (That is what you are doing right now).

2. You write/fix code on the `left pane`:

  * First thing, **complete v on the left, like:**
  
    v = "understood";
    
  * Click `run` and if the grey 'output-box' turns 
  
    * **green**
    
    Everything is good! Change **v** to something else and hit `run` again!
  
    * **red**
    
    You have to fix something! If you can't think of what
    we want from you, then, and only then, click the `solution`
    button and adapt your solution.
    
3. Finally there is the `reset` button. If you screwed the code,
  just hit `reset`. 
  
  **Note:** Using `reset` you will lose the text you had
  there before.

## The shell

Whenever you hit `run`, this happens:

1. javascript writes `the editor's` contents into the file `/test.nix`

2. then it runs `nix-instantiate.js` with:

        -I nixpkgs=nixpkgs/ --eval --strict --show-trace /test.nix

**Note:** If you've got **Nix** or **NixOS** installed natively, then you 
can also execute this examples on the shell.

## Privacy

We are:
* not using **cookies** and 
* **we don't store your results.**

Happy hacking & learning!

**Note:** If you hit `reload` in your browser, everything is gone!

## Starting code

```nix
# code goes here
{
  v="";
}
```

## Solution

```nix
{ v="understood"; }
```

## Video

[YouTube](https://www.youtube.com/watch?v=pnzucIAFXn0&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

Source: [A tour of Nix](https://nixcloud.io/tour/?id=introduction-tour) · [GitHub](https://github.com/nixcloud/tour_of_nix)
