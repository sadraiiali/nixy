# <a id="deploy-nixos-using-terraform"></a> استقرار NixOS با استفاده از Terraform

این آموزش فرض می‌کند که شما [با اصول اولیه Terraform آشنا هستید](https://www.terraform.io/intro/index.html).
تا پایان این آموزش، یک نمونه (Instance) در آمازون وب سرویس (AWS) را با استفاده از Terraform آماده‌سازی (Provision) خواهید کرد و از نیکس برای استقرار تغییرات افزایشی روی NixOS در حال اجرا روی آن نمونه بهره خواهید برد.

ما بررسی خواهیم کرد که چگونه یک ماشین NixOS را راه‌اندازی (Boot) کنیم و چگونه تغییرات افزایشی را مستقر سازیم.

## راه‌اندازی تصویر NixOS

1. با فراهم کردن فایل اجرایی Terraform شروع کنید:

```shell
$ nix-shell -p terraform
```

۲. ما از [Terraform Cloud](https://app.terraform.io) به عنوان یک [بخشسمت سرور (Backend) حالت/قفل‌کننده](https://www.terraform.io/docs/state/purpose.html) استفاده می‌کنیم:

```shell
$ terraform login
```

3. مطمئن شوید که یک [سازمان ایجاد کنید](https://app.terraform.io/app/organizations/new)، مانند `myorganization`، در حساب کاربری Terraform Cloud خود.
4. در داخل `myorganization`، با انتخاب **CLI-driven workflow** [یک فضای کاری ایجاد کنید](https://app.terraform.io/app/cachix/workspaces/new) و نامی مانند `myapp` را انتخاب کنید.
5. در داخل فضای کاری خود، در قسمت `Settings / General`، حالت اجرا (Execution Mode) را روی `Local` تنظیم کنید.
6. در داخل یک پوشه جدید، یک فایل `main.tf` با محتوای زیر ایجاد کنید. این کار یک نمونه (instance) در AWS با تصویر NixOS با استفاده از یک جفت کلید SSH و یک گروه امنیتی SSH را راه‌اندازی می‌کند:

```terraform
terraform {
    backend "remote" {
        organization = "myorganization"

        workspaces {
            name = "myapp"
        }
    }
}

provider "aws" {
    region = "eu-central-1"
}

module "nixos_image" {
    source  = "git::https://github.com/tweag/terraform-nixos.git//aws_image_nixos?ref=5f5a0408b299874d6a29d1271e9bffeee4c9ca71"
    release = "20.09"
}

resource "aws_security_group" "ssh_and_egress" {
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = [ "0.0.0.0/0" ]
    }

    egress {
        from_port       = 0
        to_port         = 0
        protocol        = "-1"
        cidr_blocks     = ["0.0.0.0/0"]
    }
}

resource "tls_private_key" "state_ssh_key" {
    algorithm = "RSA"
}

resource "local_file" "machine_ssh_key" {
    sensitive_content = tls_private_key.state_ssh_key.private_key_pem
    filename          = "${path.module}/id_rsa.pem"
    file_permission   = "0600"
}

resource "aws_key_pair" "generated_key" {
    key_name   = "generated-key-${sha256(tls_private_key.state_ssh_key.public_key_openssh)}"
    public_key = tls_private_key.state_ssh_key.public_key_openssh
}

resource "aws_instance" "machine" {
    ami             = module.nixos_image.ami
    instance_type   = "t3.micro"
    security_groups = [ aws_security_group.ssh_and_egress.name ]
    key_name        = aws_key_pair.generated_key.key_name

    root_block_device {
        volume_size = 50 # GiB
    }
}

output "public_dns" {
    value = aws_instance.machine.public_dns
}
```

تنها قطعه‌کد مخصوص NixOS عبارت است از:

```terraform
module "nixos_image" {
  source = "git::https://github.com/tweag/terraform-nixos.git/aws_image_nixos?ref=5f5a0408b299874d6a29d1271e9bffeee4c9ca71"
  release = "20.09"
}
```

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> ماژول `aws_image_nixos` با دریافت [شماره انتشار NixOS](https://status.nixos.org) یک AMI مربوط به NixOS را برمی‌گرداند؛
> به طوری که منبع `aws_instance` می‌تواند در آرگومان [instance_type](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#instance_type) به آن AMI ارجاع دهد.

۵. حتماً [اعتبارنامه‌های AWS را پیکربندی کنید](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication).
۶. اعمال پیکربندی Terraform باید یک NixOS در حال اجرا را برای شما فراهم کند:

```shell
$ terraform init
$ terraform apply
```

## استقرار تغییرات NixOS

هنگامی که نمونه‌ی AWS در حال اجرای یک تصویر NixOS از طریق Terraform است، می‌توانیم به Terraform بیاموزیم که همیشه جدیدترین پیکربندی NixOS را بسازد و آن تغییرات را روی نمونه‌ی شما اعمال کند.

1. فایل `configuration.nix` را با محتوای زیر ایجاد کنید:

```nix
{ config, lib, pkgs, ... }: {
  imports = [ <nixpkgs/nixos/modules/virtualisation/amazon-image.nix> ];

  # Open https://search.nixos.org/options for all options
}
```

۲. قطعه کد زیر را به فایل `main.tf` خود اضافه کنید:

```terraform
module "deploy_nixos" {
    source = "git::https://github.com/tweag/terraform-nixos.git//deploy_nixos?ref=5f5a0408b299874d6a29d1271e9bffeee4c9ca71"
    nixos_config = "${path.module}/configuration.nix"
    target_host = aws_instance.machine.public_ip
    ssh_private_key_file = local_file.machine_ssh_key.filename
    ssh_agent = false
}
```

۳. استقرار:

```shell
$ terraform init
$ terraform apply
```

## هشدارها

- ماژول `deploy_nixos` مستلزم این است که NixOS روی ماشین مقصد و Nix روی ماشین میزبان نصب شده باشد.
- ماژول `deploy_nixos` زمانی که معماری‌های کاربر (client) و مقصد متفاوت باشند کار نمی‌کند (مگر اینکه از [بیلد‌های توزیع‌شده](/pages/nix-manual/advanced-topics/distributed-builds) استفاده کنید).
- اگر نیاز دارید مقداری را به درون Nix تزریق کنید، هیچ راهکار ظریفی برای آن وجود ندارد.
- هر ماشین به‌طور جداگانه ارزیابی می‌شود، بنابراین توجه داشته باشید که نیازهای حافظه شما به‌صورت خطی با تعداد ماشین‌ها رشد خواهد کرد.

## گام‌های بعدی

- امکان [مهاجرت به Google Compute Engine](https://github.com/tweag/terraform-nixos/tree/master/google_image_nixos#readme) وجود دارد.
- [ماژول `deploy_nixos`](https://github.com/tweag/terraform-nixos/tree/master/deploy_nixos#readme) از آرگومان‌های مختلفی، برای مثال جهت بارگذاری کلیدها، پشتیبانی می‌کند.
