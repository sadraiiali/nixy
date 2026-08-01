# <a id="maven"></a> Maven

Maven یک ابزار ساخت شناخته‌شده برای بوم‌سازگان Java است؛ با این حال، هنگام یکپارچه‌سازی در سیستم ساخت Nix با چالش‌هایی همراه است.

موارد زیر فهرستی از الگوهای رایج نحوه بسته‌بندی یک پروژه Maven (یا هر زبان JVM که امکان خروجی گرفتن برای Maven را دارد) به عنوان یک بسته Nix ارائه می‌دهد.

## <a id="maven-buildmavenpackage"></a> ساخت یک بسته با استفاده از `maven.buildMavenPackage`

بسته زیر را در نظر بگیرید:

```nix
{
  lib,
  fetchFromGitHub,
  jre,
  makeWrapper,
  maven,
}:

maven.buildMavenPackage (finalAttrs: {
  pname = "jd-cli";
  version = "1.2.1";

  src = fetchFromGitHub {
    owner = "intoolswetrust";
    repo = "jd-cli";
    tag = "jd-cli-${finalAttrs.version}";
    hash = "sha256-rRttA5H0A0c44loBzbKH7Waoted3IsOgxGCD2VM0U/Q=";
  };

  mvnHash = "sha256-kLpjMj05uC94/5vGMwMlFzLKNFOKeyNvq/vmB6pHTAo=";

  nativeBuildInputs = [ makeWrapper ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin $out/share/jd-cli
    install -Dm644 jd-cli/target/jd-cli.jar $out/share/jd-cli

    makeWrapper ${jre}/bin/java $out/bin/jd-cli \
      --add-flags "-jar $out/share/jd-cli/jd-cli.jar"

    runHook postInstall
  '';

  meta = {
    description = "Simple command line wrapper around JD Core Java Decompiler project";
    homepage = "https://github.com/intoolswetrust/jd-cli";
    license = lib.licenses.gpl3Plus;
    maintainers = with lib.maintainers; [ majiir ];
  };
})
```

مراجعه کنید.

Wait, "را ببینید" or "مراجعه کنید" for "see"? In Nix docs, "را ببینید" or "مراجعه کنید" works well. Let

```
overrideMavenAttrs :: (AttrSet -> Derivation) | ((AttrSet -> Attrset) -> Derivation) -> Derivation
```

خروجی `buildMavenPackage` دارای صفت (attribute) `overrideMavenAttrs` است، که تابعی است که یکی از موارد زیر را می‌پذیرد:
- هر زیرمجموعه‌ای از صفات که

```nix
jd-cli.overrideMavenAttrs (old: rec {
  version = "1.2.0";
  src = fetchFromGitHub {
    owner = old.src.owner;
    repo = old.src.repo;
    tag = "${old.pname}-${version}";
    # old source hash of 1.2.0 version
    hash = "sha256-US7j6tQ6mh1libeHnQdFxPGoxHzbZHqehWSgCYynKx8=";
  };

  # tests can be disabled by prefixing it with `!`
  # see Maven documentation for more details:
  # https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html#Multiple_Formats_in_One
  mvnParameters = lib.escapeShellArgs [
    "-Dsurefire.failIfNoSpecifiedTests=false"
    "-Dtest=!JavaDecompilerTest#basicTest,!JavaDecompilerTest#patternMatchingTest"
  ];

  # old mvnHash of 1.2.0 maven dependencies
  mvnHash = "sha256-N9XC1pg6Y4sUiBWIQUf16QSXCuiAPpXEHGlgApviF4I=";
})
```

### <a id="maven-offline-build"></a> ساخت آفلاین

به طور پیش‌فرض، `buildMavenPackage` موارد زیر را انجام می‌دهد:

1. اجرای `mvn package -Dmaven.repo.local=$out/.m2 $`در`fetchedMavenDeps`
```nix
maven.buildMavenPackage {
  manualMvnArtifacts = [
    # add dynamic test dependencies here
    "org.apache.maven.surefire:surefire-junit-platform:3.1.2"
    "org.junit.platform:junit-platform-launcher:1.10.0"
  ];
}
```

### <a id="stable-maven-plugins"></a> پلاگین‌های پایدار Maven

Maven نسخه‌های پیش‌فرضی را برای پلاگین‌های اصلی خود تعریف می‌کند، مانند `maven-compiler-plugin`. اگر پروژه شما

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-enforcer-plugin</artifactId>
  <version>3.3.0</version>
  <executions>
    <execution>
      <id>enforce-plugin-versions</id>
      <goals>
        <goal>enforce</goal>
      </goals>
      <configuration>
        <rules>
          <requirePluginVersions />
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

بندی می‌کند.

`maven_4` یک derivation مستقل است و می‌توان از آن به عنوان جایگزین در هر کجا که `maven` استفاده می‌شود بهره برد، برای

```nix
{
  lib,
  fetchFromGitHub,
  jre,
  makeWrapper,
  maven_4,
}:

maven_4.buildMavenPackage (finalAttrs: {
  pname = "jd-cli";
  version = "1.2.1";

  src = fetchFromGitHub {
    owner = "intoolswetrust";
    repo = "jd-cli";
    tag = "jd-cli-${finalAttrs.version}";
    hash = "sha256-rRttA5H0A0c44loBzbKH7Waoted3IsOgxGCD2VM0U/Q=";
  };

  mvnHash = "";

  nativeBuildInputs = [ makeWrapper ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin $out/share/jd-cli
    install -Dm644 jd-cli/target/jd-cli.jar $out/share/jd-cli

    makeWrapper ${jre}/bin/java $out/bin/jd-cli \
      --add-flags "-jar $out/share/jd-cli/jd-cli.jar"

    runHook postInstall
  '';

  meta = {
    description = "Simple command line wrapper around JD Core Java Decompiler project";
    homepage = "https://github.com/intoolswetrust/jd-cli";
    license = lib.licenses.gpl3Plus;
    maintainers = with lib.maintainers; [ majiir ];
  };
})
```

`maven_4` همان کمک‌رسان `buildMavenPackage` را مشابه `maven` ارائه می‌دهد (ببینید [](#maven-buildmavenpackage))، بنابراین تمام الگوهای مستندشده در بالا به همان صورت اعمال می‌شوند. توجه داشته باشید که وابستگی‌های Maven که توسط Maven 4 حل‌وفصل می‌شوند با موارد حل‌شده توسط Maven 3 متفاوت هستند، بنابراین `mvnHash` هنگام جابه‌جایی بین این دو باید دوباره محاسبه شود.

## <a id="maven-mvn2nix"></a> استفاده دستی از `mvn2nix`
> <span class="admonition-kind" data-kind="warning"></span>
>
> **هشدار**
>
> این روش دیگر
>

> ```xml
> <?xml version="1.0" encoding="UTF-8"?>
> <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
>         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
>   <modelVersion>4.0.0</modelVersion>
>   <groupId>io.github.fzakaria</groupId>
>   <artifactId>maven-demo</artifactId>
>   <version>1.0</version>
>   <packaging>jar</packaging>
>   <name>NixOS Maven Demo</name>
>
>   <dependencies>
>     <dependency>
>         <groupId>com.vdurmont</groupId>
>         <artifactId>emoji-java</artifactId>
>         <version>5.1.1</version>
>       </dependency>
>   </dependencies>
> </project>
> ```
>
> فایل کلاس اصلی ما بسیار ساده خواهد بود:
>

> ```java
> import com.vdurmont.emoji.EmojiParser;
>
> public class Main {
>   public static void main(String[] args) {
>     String str = "NixOS :grinning: is super cool :smiley:!";
>     String result = EmojiParser.parseToUnicode(str);
>     System.out.println(result);
>   }
> }
> ```
>
> این پروژه نمونه را می‌توانید در [https://github.com/fzakaria/nixos-maven-example](https://github.com/fzakaria/nixos-maven-example)
>

> ```bash
> # run this step within the project's source repository
> ❯ mvn org.nixos.mvn2nix:mvn2nix-maven-plugin:mvn2nix
>
> ❯ cat project-info.json | jq | head
> {
>   "project": {
>     "artifactId": "maven-demo",
>     "groupId": "org.nixos",
>     "version": "1.0",
>     "classifier": "",
>     "extension": "jar",
>     "dependencies": [
>       {
>         "artifactId": "maven-resources-plugin",
> ```
>
> این فایل سپس به تابع `buildMaven` داده می‌شود و ۲ صفت بازمی‌گرداند.
>
> **`repo`**:
>     یک مخزن Maven که یک مزرعه پیوند نماد
>

> ```nix
> {
>   pkgs ? import <nixpkgs> { },
> }:
> with pkgs;
> (buildMaven ./project-info.json).repo
> ```
>
> مزیت این روش نسبت به _فراخوانی دوگانه_، همان‌طور که در ادامه خواهیم دید، این است که ورودی _/nix/store_ یک _linkFarm_ از تمامی بسته‌هاست، بنابراین تغییر در مجموعه وابستگی‌های شما مستلزم بارگیری همه‌چیز از ابتدا نخواهد بود.
>

> ```bash
> ❯ tree $(nix-build --no-out-link build-maven-repository.nix) | head
> /nix/store/g87va52nkc8jzbmi1aqdcf2f109r4dvn-maven-repository
> ├── antlr
> │   └── antlr
> │       └── 2.7.2
> │           ├── antlr-2.7.2.jar -> /nix/store/d027c8f2cnmj5yrynpbq2s6wmc9cb559-antlr-2.7.2.jar
> │           └── antlr-2.7.2.pom -> /nix/store/mv42fc5gizl8h5g5vpywz1nfiynmzgp2-antlr-2.7.2.pom
> ├── avalon-framework
> │   └── avalon-framework
> │       └── 4.1.3
> │           ├── avalon-framework-4.1.3.jar -> /nix/store/iv5fp3955w3nq28ff9xfz86wvxbiw6n9-avalon-framework-4.1.3.jar
> ```
>
> "sandboxed" in glossary: sandboxed -> ایزوله شده (Sandboxed). In prose, "ایزوله شده" fits well.
> "download" in glossary: download -> بارگیری.
>
> Let's
>

> ```nix
> {
>   lib,
>   stdenv,
>   maven,
> }:
> stdenv.mkDerivation {
>   name = "maven-repository";
>   buildInputs = [ maven ];
>   src = ./.; # or fetchFromGitHub, cleanSourceWith, etc
>   buildPhase = ''
>     runHook preBuild
>
>     mvn package -Dmaven.repo.local=$out
>
>     runHook postBuild
>   '';
>
>   # keep only *.{pom,jar,sha1,nbm} and delete all ephemeral files with lastModified timestamps inside
>   installPhase = ''
>     runHook preInstall
>
>     find $out -type f \
>       -name \*.lastUpdated -or \
>       -name resolver-status.properties -or \
>       -name _remote.repositories \
>       -delete
>
>     runHook postInstall
>   '';
>
>   # don't do any fixup
>   dontFixup = true;
>   outputHashAlgo = null;
>   outputHashMode = "recursive";
>   # replace this with the correct SHA256
>   outputHash = lib.fakeHash;
> }
> ```
>
> ساخت (Build) با شکست مواجه خواهد شد و `outputHash` مورد انتظار برای قرار دادن را به شما اعلام می‌کند. هنگامی که هش را تنظیم کردید، ساخت با
>

> ```bash
> ❯ tree $(nix-build --no-out-link double-invocation-repository.nix) | head
> /nix/store/8kicxzp98j68xyi9gl6jda67hp3c54fq-maven-repository
> ├── backport-util-concurrent
> │   └── backport-util-concurrent
> │       └── 3.1
> │           ├── backport-util-concurrent-3.1.pom
> │           └── backport-util-concurrent-3.1.pom.sha1
> ├── classworlds
> │   └── classworlds
> │       ├── 1.1
> │       │   ├── classworlds-1.1.jar
> ```
>
> اگر بسته شما از وابستگی‌های _SNAPSHOT_ یا _بازه‌های نسخه_ استفاده می‌کند، احتمال زیادی وجود دارد که با گذشت زمان، هش خروجی شما تغییر کند؛ زیرا وابستگی‌های حل‌شده ممکن است تغییر کنند. از این رو، این روش کمتر از استفاده از `buildMaven` توصیه می‌شود.
>
> ### <a id="building-a-jar"></a> ساخت یک فایل JAR
>
> صرف‌نظر از اینکه کدام راهبرد در بالا انتخاب شده باشد، گام ساخت derivation / اشتقاق ساخت یکسان است.
>

> ```nix
> {
>   stdenv,
>   maven,
>   callPackage,
> }:
> let
>   # pick a repository derivation, here we will use buildMaven
>   repository = callPackage ./build-maven-repository.nix { };
> in
> stdenv.mkDerivation (finalAttrs: {
>   pname = "maven-demo";
>   version = "1.0";
>
>   src = fetchTarball "https://github.com/fzakaria/nixos-maven-example/archive/main.tar.gz";
>   buildInputs = [ maven ];
>
>   buildPhase = ''
>     runHook preBuild
>
>     echo "Using repository ${repository}"
>     mvn --offline -Dmaven.repo.local=${repository} package;
>
>     runHook postBuild
>   '';
>
>   installPhase = ''
>     runHook preInstall
>
>     install -Dm644 target/${finalAttrs.pname}-${finalAttrs.version}.jar $out/share/java
>
>     runHook postInstall
>   '';
> })
> ```
>
> > <span class="admonition-kind" data-kind="tip"></span>
> >
> > **راهنمایی**
> >
> > ما کتابخانه را در `$out/share/java` قرار می‌دهیم، زیرا بسته JDK دارای یک _stdenv setup hook_ است که تمام فایل‌های JAR موجود در پوشه‌های `share/java` ورودی‌های ساخت را به محیط CLASSPATH اضافه می‌کند.
>
>

> ```bash
> ❯ tree $(nix-build --no-out-link build-jar.nix)
> /nix/store/7jw3xdfagkc2vw8wrsdv68qpsnrxgvky-maven-demo-1.0
> └── share
>     └── java
>         └── maven-demo-1.0.jar
>
> 2 directories, 1 file
> ```
>
> ### <a id="runnable-jar"></a> فایل JAR قابل اجرا
>
> مثال قبلی یک فایل `jar` می‌سازد اما این فایلی نیست که بتوان آن را اجرا کرد.
>
> شما باید آن را با `java -jar $out/share/java/output.jar` استفاده کنید و مطمئن شوید که وابستگی‌ها مورد نیاز را در classpath ارائه داده‌اید.
>
> در ادامه نحوه استفاده از `makeWrapper` توضیح داده می‌شود تا derivation یک فایل اجرایی تولید کند که فایل JAR ساخته‌شده توسط شما را اجرا خواهد کرد.
>
> ما از همان مخزنی که در بالا ساختیم (خواه _double invocation_ باشد یا
>

> ```nix
> {
>   stdenv,
>   maven,
>   callPackage,
>   makeWrapper,
>   jre,
> }:
> let
>   repository = callPackage ./build-maven-repository.nix { };
> in
> stdenv.mkDerivation (finalAttrs: {
>   pname = "maven-demo";
>   version = "1.0";
>
>   src = fetchTarball "https://github.com/fzakaria/nixos-maven-example/archive/main.tar.gz";
>   nativeBuildInputs = [ makeWrapper ];
>   buildInputs = [ maven ];
>
>   buildPhase = ''
>     runHook preBuild
>
>     echo "Using repository ${repository}"
>     mvn --offline -Dmaven.repo.local=${repository} package;
>
>     runHook postBuild
>   '';
>
>   installPhase = ''
>     runHook preInstall
>
>     mkdir -p $out/bin
>
>     classpath=$(find ${repository} -name "*.jar" -printf ':%h/%f');
>     install -Dm644 target/maven-demo-${finalAttrs.version}.jar $out/share/java
>     # create a wrapper that will automatically set the classpath
>     # this should be the paths from the dependency derivation
>     makeWrapper ${jre}/bin/java $out/bin/maven-demo \
>           --add-flags "-classpath $out/share/java/maven-demo-${finalAttrs.version}.jar:''${classpath#:}" \
>           --add-flags "Main"
>
>     runHook postInstall
>   '';
> })
> ```
>
> #### <a id="manifest-file-via-maven-plugin"></a> فایل MANIFEST از طریق افزونه Maven
>
> این روش زمانی ایده‌آل است که شما مالک پروژه باشید و بخواهید `pom.xml` خود را برای تنظیم CLASSPATH در داخل آن تغییر دهید.
>
> فایل `pom.xml` را گسترش دهید تا یک فایل JAR با مانفیست زیر ایجاد شود:
>

> ```xml
> <build>
>   <plugins>
>     <plugin>
>         <artifactId>maven-jar-plugin</artifactId>
>         <configuration>
>             <archive>
>                 <manifest>
>                     <addClasspath>true</addClasspath>
>                     <classpathPrefix>../../repository/</classpathPrefix>
>                     <classpathLayoutType>repository</classpathLayoutType>
>                     <mainClass>Main</mainClass>
>                 </manifest>
>                 <manifestEntries>
>                     <Class-Path>.</Class-Path>
>                 </manifestEntries>
>             </archive>
>         </configuration>
>     </plugin>
>   </plugins>
> </build>
> ```
>
> پلاگین بالا به فایل JAR دستور می‌دهد که وابستگی‌های لازم را در پوشه نسبی `lib/` جستجو کند. چیدمان این پوشه نیز به سبک _مخزن Maven_ است.
>

> ```bash
> ❯ unzip -q -c $(nix-build --no-out-link runnable-jar.nix)/share/java/maven-demo-1.0.jar META-INF/MANIFEST.MF
>
> Manifest-Version: 1.0
> Archiver-Version: Plexus Archiver
> Built-By: nixbld
> Class-Path: . ../../repository/com/vdurmont/emoji-java/5.1.1/emoji-jav
>  a-5.1.1.jar ../../repository/org/json/json/20170516/json-20170516.jar
> Created-By: Apache Maven 3.6.3
> Build-Jdk: 1.8.0_265
> Main-Class: Main
> ```
>
> ما درایویشن بالا را تغییر خواهیم داد تا یک پیوند نمادین (symlink) به مخزن خود اضافه کنیم تا در طول `installPhase` برای JAR ما قابل دسترسی باشد.
>

> ```nix
> {
>   stdenv,
>   maven,
>   callPackage,
>   makeWrapper,
>   jre,
> }:
> let
>   # pick a repository derivation, here we will use buildMaven
>   repository = callPackage ./build-maven-repository.nix { };
> in
> stdenv.mkDerivation (finalAttrs: {
>   pname = "maven-demo";
>   version = "1.0";
>
>   src = fetchTarball "https://github.com/fzakaria/nixos-maven-example/archive/main.tar.gz";
>   nativeBuildInputs = [ makeWrapper ];
>   buildInputs = [ maven ];
>
>   buildPhase = ''
>     runHook preBuild
>
>     echo "Using repository ${repository}"
>     mvn --offline -Dmaven.repo.local=${repository} package;
>
>     runHook postBuild
>   '';
>
>   installPhase = ''
>     runHook preInstall
>
>     mkdir -p $out/bin
>
>     # create a symbolic link for the repository directory
>     ln -s ${repository} $out/repository
>
>     install -Dm644 target/maven-demo-${finalAttrs.version}.jar $out/share/java
>     # create a wrapper that will automatically set the classpath
>     # this should be the paths from the dependency derivation
>     makeWrapper ${jre}/bin/java $out/bin/maven-demo \
>           --add-flags "-jar $out/share/java/maven-demo-${finalAttrs.version}.jar"
>
>     runHook postInstall
>   '';
> })
> ```
> > <span class="admonition-kind" data-kind="note"></span>
> >
> > **نکته**
> >
> > اسکریپت ما به جای `jdk` یک وابستگی به `jre` ایجاد می‌کند تا بستار زمان اجرای لازم برای اجرای برنامه را محدود کند.
>
>
> این کار یک اسکریپت شل قابل اجرا در اختیار شما قرار می‌دهد که فایل JAR شما را همراه با تمام وابستگی‌های در دسترس اجرا می‌کند.
>

> ```bash
> ❯ tree $(nix-build --no-out-link runnable-jar.nix)
> /nix/store/8d4c3ibw8ynsn01ibhyqmc1zhzz75s26-maven-demo-1.0
> ├── bin
> │   └── maven-demo
> ├── repository -> /nix/store/g87va52nkc8jzbmi1aqdcf2f109r4dvn-maven-repository
> └── share
>     └── java
>         └── maven-demo-1.0.jar
>
> ❯ $(nix-build --no-out-link --option tarball-ttl 1 runnable-jar.nix)/bin/maven-demo
> NixOS 😀 is super cool 😃!
> ```
