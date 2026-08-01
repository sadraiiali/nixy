# <a id="python-tree-sitter"></a> Python Tree Sitter

[Tree Sitter](https://tree-sitter.github.io/tree-sitter/) چارچوبی برای ساخت گرامر زبان‌های برنامه‌نویسی است. این ابزار درخت‌های نحو را از فایل‌های سورس تولید کرده و به کار می‌برد که برای تحلیل کد، ابزارسازی و برجسته‌سازی نحو کاربرد دارند.

اتصالات Python برای گرامرهای Tree Sitter از طریق ماژول [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter) ارائه می‌شوند. بسته Nix به نام `python3Packages.tree-sitter-grammars` گرامرهای پیش‌ساخته را برای زبان‌های گوناگون فراهم می‌کند.

برای نمونه، جهت آزمایش با گرامر Rust، می‌توانید یک محیط شل (Shell) با پیکربندی زیر ایجاد کنید:

```nix
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  name = "py-tree-sitter-dev-shell";

  buildInputs = with pkgs; [
    (python3.withPackages (
      ps: with ps; [
        tree-sitter
        tree-sitter-grammars.tree-sitter-rust
      ]
    ))
  ];
}
```

پس از ورود به شل، کد Python زیر نحوه تجزیه یک قطعه کد Rust را نشان می‌دهد:

```python
# Import the Tree Sitter library and Rust grammar
import tree_sitter
import tree_sitter_rust

# Load the Rust grammar and initialize the parser
rust = tree_sitter.Language(tree_sitter_rust.language())
parser = tree_sitter.Parser(rust)

# Parse a Rust snippet
tree = parser.parse(
    bytes(
        """
        fn main() {
          println!("Hello, world!");
        }
        """,
        "utf8"
    )
)

# Display the resulting syntax tree
print(tree.root_node)
```

تابع `tree_sitter_rust.language()` به گرامر Rust بارگذاری‌شده در شل Nix اشاره می‌کند. درخت حاصل به شما این امکان را می‌دهد که ساختار کد را به صورت برنامه‌نویسی‌شده بررسی کنید.
