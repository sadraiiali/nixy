# <a id="sec-nrfutil"></a> nrfutil

nrfutil را می‌توان با موارد قابل نصب آن به صورت زیر ساخت:

```nix
(nrfutil.withExtensions [
  "nrfutil-completion"
  "nrfutil-device"
  "nrfutil-trace"
])
```

توجه داشته باشید که ممکن است همه موارد قابل نصب برای تمامی پلتفرم‌های پشتیبانی‌شده در دسترس نباشند.
