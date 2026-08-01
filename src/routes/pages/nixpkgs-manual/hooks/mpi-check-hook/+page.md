# <a id="setup-hook-mpi-check"></a> mpiCheckPhaseHook

از این قلاب می‌توان برای راه‌اندازی یک فاز بررسی که نیازمند اجرای یک برنامه MPI است استفاده کرد. این قلاب نوع پیاده‌سازی MPI موجود را تشخیص داده و متغیرهای محیطی لازم برای استفاده از `mpirun` و `mpiexec` در یک محیط ایزوله شده (Sandboxed) Nix را صادر می‌کند.

مثال:

```nix
{ mpiCheckPhaseHook, mpi, ... }:
{
  # ...

  nativeCheckInputs = [
    openssh
    mpiCheckPhaseHook
  ];
}
```
