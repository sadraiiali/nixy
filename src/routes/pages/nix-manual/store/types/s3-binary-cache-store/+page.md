# S3 Binary Cache Store - Nix 2.34.9 Reference Manual

> Source: [/pages/nix-manual/store/types/s3-binary-cache-store](/pages/nix-manual/store/types/s3-binary-cache-store)

# <a id="s3-binary-cache-store"></a> S3 Binary Cache Store

**Store URL format**: `s3://`*bucket-name*

This store allows reading and writing a binary cache stored in an AWS S3 (or S3-compatible service) bucket.
This store shares many idioms with the [HTTP Binary Cache Store](/pages/nix-manual/store/types/http-binary-cache-store).

For AWS S3, the binary cache URL for a bucket named `example-nix-cache` will be exactly [s3://example-nix-cache](/pages/nix-manual/store/types/s3:/example-nix-cache).
For S3 compatible binary caches, consult that cache's documentation.

### <a id="anonymous-reads-to-your-s3-compatible-binary-cache"></a> Anonymous reads to your S3-compatible binary cache

> If your binary cache is publicly accessible and does not require authentication,
> it is simplest to use the [HTTP Binary Cache Store] rather than S3 Binary Cache Store with
> [https://example-nix-cache.s3.amazonaws.com](https://example-nix-cache.s3.amazonaws.com) instead of [s3://example-nix-cache](/pages/nix-manual/store/types/s3:/example-nix-cache).

Your bucket will need a
[bucket policy](https://docs.aws.amazon.com/AmazonS3/v1/userguide/bucket-policies.html)
like the following to be accessible:

```
{
    "Id": "DirectReads",
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowDirectReads",
            "Action": [
                "s3:GetObject",
                "s3:GetBucketLocation",
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::example-nix-cache",
                "arn:aws:s3:::example-nix-cache/*"
            ],
            "Principal": "*"
        }
    ]
}
```

### <a id="authentication"></a> Authentication

Nix will use the
[default credential provider chain](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/credentials.html)
for authenticating requests to Amazon S3.

Note that this means Nix will read environment variables and files with different idioms than with Nix's own settings, as implemented by the AWS SDK.
Consult the documentation linked above for further details.

### <a id="authenticated-reads-to-your-s3-binary-cache"></a> Authenticated reads to your S3 binary cache

Your bucket will need a bucket policy allowing the desired users to perform the `s3:GetObject`, `s3:GetBucketLocation`, and `s3:ListBucket` actions on all objects in the bucket.
The anonymous policy given above can be updated to have a restricted `Principal` to support this.

### <a id="authenticated-writes-to-your-s3-compatible-binary-cache"></a> Authenticated writes to your S3-compatible binary cache

Your account will need an IAM policy to support uploading to the bucket:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UploadToCache",
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::example-nix-cache",
        "arn:aws:s3:::example-nix-cache/*"
      ]
    }
  ]
}
```

### <a id="examples"></a> Examples

With bucket policies and authentication set up as described above, uploading works via [`nix copy`](/pages/nix-manual/command-ref/new-cli/nix3-copy) (experimental).

- To upload with a specific credential profile for Amazon S3:
$ nix copy nixpkgs.hello \
 --to 's3://example-nix-cache?profile=cache-upload&region=eu-west-2'
- To upload to an S3-compatible binary cache:
$ nix copy nixpkgs.hello --to \
 's3://example-nix-cache?profile=cache-upload&scheme=https&endpoint=minio.example.com'

## <a id="settings"></a> Settings

- `addressing-style`
The S3 addressing style to use. `auto` (default) uses
virtual-hosted-style for standard AWS endpoints and path-style
for custom endpoints; bucket names containing dots automatically
fall back to path-style to avoid TLS certificate errors. `path`
forces path-style addressing (deprecated by AWS). `virtual`
forces virtual-hosted-style addressing (bucket names must not
contain dots).
**Default:** `auto`
- `compression`
NAR compression method. One of: `xz`, `bzip2`, `gzip`, `zstd`, `none`, `br`, `compress`, `grzip`, `lrzip`, `lz4`, `lzip`, `lzma` or `lzop`.
To use a particular compression method Nix has to be built with a version of libarchive that natively supports that compression algorithm.
**Default:** `xz`
- `compression-level`
The *preset level* to be used when compressing NARs.
The meaning and accepted values depend on the compression method selected.
`-1` specifies that the default compression level should be used.
**Default:** `-1`
- `endpoint`
The S3 endpoint to use. When empty (default), uses AWS S3 with
region-specific endpoints. For S3-compatible services such as
MinIO, set this to your service's endpoint.
**Default:** *empty*
- `index-debug-info`
Whether to index DWARF debug info files by build ID. This allows [`dwarffs`](https://github.com/edolstra/dwarffs) to
fetch debug info on demand
**Default:** `false`
- `local-nar-cache`
Path to a local cache of NARs fetched from this binary cache, used by commands such as `nix store cat`.
**Default:** ``
- `log-compression`
Compression method for `log/*` files. It is recommended to
use a compression method supported by most web browsers
(e.g. `brotli`).
**Default:** ``
- `ls-compression`
Compression method for `.ls` files.
**Default:** ``
- `multipart-chunk-size`
The size (in bytes) of each part in multipart uploads. Must be
at least 5 MiB (AWS S3 requirement). Larger chunk sizes reduce the
number of requests but use more memory. Default is 5 MiB.
**Default:** `5242880`
**Deprecated alias:** `buffer-size`
- `multipart-threshold`
The minimum file size (in bytes) for using multipart uploads.
Files smaller than this threshold will use regular PUT requests.
Default is 100 MiB. Only takes effect when multipart-upload is enabled.
**Default:** `104857600`
- `multipart-upload`
Whether to use multipart uploads for large files. When enabled,
files exceeding the multipart threshold will be uploaded in
multiple parts, which is required for files larger than 5 GiB and
can improve performance and reliability for large uploads.
**Default:** `false`
- `narinfo-compression`
Compression method for `.narinfo` files.
**Default:** ``
- `parallel-compression`
Enable multi-threaded compression of NARs. This is currently only available for `xz` and `zstd`.
**Default:** `false`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `profile`
The name of the AWS configuration profile to use. By default
Nix uses the `default` profile.
**Default:** `default`
- `region`
The region of the S3 bucket. If your bucket is not in
`us-east-1`, you should always explicitly specify the region
parameter.
**Default:** `us-east-1`
- `scheme`
The scheme used for S3 requests, `https` (default) or `http`. This
option allows you to disable HTTPS for binary caches which don't
support it.

**Note**
HTTPS should be used if the cache might contain sensitive
information.

**Default:** `https`
- `secret-key`
Path to the secret key used to sign the binary cache.
**Default:** *empty*
- `secret-keys`
List of comma-separated paths to the secret keys used to sign the binary cache.
**Default:** *empty*
- `storage-class`
The S3 storage class to use for uploaded objects. When not set (default),
uses the bucket's default storage class. Valid values include:

See AWS S3 documentation for detailed storage class descriptions and pricing:
https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html
**Default:** ``
  - STANDARD (default, frequently accessed data)
  - REDUCED\_REDUNDANCY (less frequently accessed data)
  - STANDARD\_IA (infrequent access)
  - ONEZONE\_IA (infrequent access, single AZ)
  - INTELLIGENT\_TIERING (automatic cost optimization)
  - GLACIER (archival with retrieval times in minutes to hours)
  - DEEP\_ARCHIVE (long-term archival with 12-hour retrieval)
  - GLACIER\_IR (instant retrieval archival)
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `tls-certificate`
Path to an optional TLS client certificate in PEM format.
**Default:** ``
- `tls-private-key`
Path to an optional TLS client certificate private key in PEM format.
**Default:** ``
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`
- `write-nar-listing`
Whether to write a JSON file that lists the files in each NAR.
**Default:** `false`
