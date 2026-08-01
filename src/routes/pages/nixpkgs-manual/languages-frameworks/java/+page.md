# <a id="sec-language-java"></a> Java

بسته‌های Java مبتنی بر Ant معمولاً به صورت زیر از منبع ساخته می‌شوند:

```nix
stdenv.mkDerivation {
  pname = "...";
  version = "...";

  src = fetchurl {
    # ...
  };

  nativeBuildInputs = [
    ant
    jdk
    stripJavaArchivesHook # removes timestamp metadata from jar files
  ];

  buildPhase = ''
    runHook preBuild
    ant # build the project using ant
    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    # copy generated jar file(s) to an appropriate location in $out
    install -Dm644 build/foo.jar $out/share/java/foo.jar

    runHook postInstall
  '';
}
```

توجه داشته باشید که `jdk` یک نام مستعار برای OpenJDK است (خودساخته در صورت امکان، یا پیش‌ساخته از طریق Zulu).

همچنین توجه داشته باشید که عدم استفاده از ``

```nix
{
  buildInputs = [ libfoo ];
  nativeBuildInputs = [ jdk ];
}
```

در این صورت `CLASSPATH` برابر با
`/nix/store/...-libfoo/share/java/foo.jar`
تنظیم خواهد شد.

فایل‌های JAR خصوصی باید در مکانی مانند
`$out/share/package-name`
نصب شوند.

اگر بسته Java شما یک برنامه ارائه می‌دهد، باید یک اسکریپت wrapper تولید کنید تا آن را با استفاده از یک JRE اجرا کند. می‌توانید از `makeWrapper` برای این کار استفاده کنید:

```nix
{
  nativeBuildInputs = [ makeWrapper ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    makeWrapper ${jre}/bin/java $out/bin/foo \
      --add-flags "-cp $out/share/java/foo.jar org.foo.Main"

    runHook postInstall
  '';
}
```

از زمان معرفی سیستم ماژول پلتفرم Java در Java 9، توزیع‌های Java معمولاً دیگر همراه با یک JRE چندمنظوره عرضه نمی‌شوند؛ در عوض، آن‌ها امکان تولید یک JRE تنها با ماژول‌های مورد نیاز برای برنامه(های) شما را فراهم می‌کنند. از آنجا که نمی‌توانیم پیش‌بینی کنیم چه ماژول‌هایی در یک سیستم چندمنظوره مورد نیاز خواهد بود، بسته پیش‌فرض `jre` همان JDK کامل است. هنگام ساخت یک سیستم/تصویر حداقل، می‌توانید پارامتر `modules` را در `jre_minimal` بازنشانی کنید تا یک JRE تنها با ماژول‌های مرتبط با خود بسازید:

```nix
let
  my_jre = pkgs.jre_minimal.override {
    modules = [
      # The modules used by 'something' and 'other' combined:
      "java.base"
      "java.logging"
    ];
  };
  something = (pkgs.something.override { jre = my_jre; });
  other = (pkgs.other.override { jre = my_jre; });
in
<...>
```

همچنین می‌توانید مشخص کنید که JRE شما بر پایه کدام JDK باشد؛ برای مثال با انتخاب یک ساخت 'headless' برای جلوگیری از شامل شدن پیوند به GTK+:

```nix
{ my_jre = pkgs.jre_minimal.override { jdk = jdk11_headless; }; }
```

توجه داشته باشید که تمامی JDKها `home` را passthru می‌کنند، بنابراین اگر برنامه شما به تنظیم متغیرهای محیطی مانند `JAVA_HOME` نیاز دارد، می‌توان این کار را به شیوه‌ای عمومی با استفاده از آرگومان `--set` در `makeWrapper` انجام داد:

```bash
--set JAVA_HOME ${jdk.home}
```

امکان استفاده از کامپایلر جاوایی غیر از `javac` از OpenJDK وجود دارد. برای نمونه، برای استفاده از GNU Java Compiler:

```nix
{
  nativeBuildInputs = [
    gcj
    ant
  ];
}
```

در اینجا، Ant به جای OpenJRE به‌طور خودکار از `gij` (محیط زمان اجرای جاوای GNU) استفاده خواهد کرد.
