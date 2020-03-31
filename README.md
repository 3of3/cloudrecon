# [cloudrecon](https://cloudrecon.readthedocs.io/en/latest/)

[![PyPi release](https://img.shields.io/pypi/v/cloudrecon.svg)](https://pypi.org/project/cloudrecon/)
[![PyPi versions](https://img.shields.io/pypi/pyversions/cloudrecon.svg)](https://pypi.org/project/cloudrecon/)
[![Documentation Status](https://readthedocs.org/projects/cloudrecon/badge/?version=latest)](https://cloudrecon.readthedocs.io/en/latest/?badge=latest)

Cloud platform data storage bucket and blob finder and crawler

<br>
<a href="https://github.com/3of3/cloudrecon">
  <p align="center"><img width="60%" src="https://raw.githubusercontent.com/3of3/cloudrecon/master/cloudrecon.jpeg" /></p>
</a>

[Check out the cloudrecon docs](https://cloudrecon.readthedocs.io/en/latest/)

## Installation
> **NOTE**: cloudrecon requires python version **>=3.6**

```bash
$ pip install cloudrecon
```

## Usage
```text

usage: cloudrecon [-h] [-o file] [-d] [-p] [-t seconds] [-v] [-c num] [-ct CLOUDTYPE]
                  word_list [word_list ...]

positional arguments:
  word_list                        read words from one or more <word-list> files

optional arguments:
  -h, --help                       show this help message and exit
  -o file, --output file           Write output to <file>
  -d, --db                         Write output to database
  -p, --public                     Only include 'public' buckets in the output
  -t seconds, --timeout seconds    HTTP request timeout in <seconds> (default: 30)
  -v, --version                    show program's version number and exit
  -c num, --concurrency num        maximum <num> of concurrent requests (default: 8)
  -ct CLOUDTYPE, --cloudtype CLOUDTYPE
                                   Input which cloud platform to query: "AWS", "GCP", "Azure", or
                                   "Alibaba"

```

## Example 1: Output to a json file

#### 1. Download a word-list.
The [SecLists](https://github.com/3of3/cloudrecon/edit/master/README.md) repository has a multitude of word-lists to choose from. For this example, let's download the sample word-list included in this repository.

```bash
$ curl -sSfL -o "word-list.txt" "https://raw.githubusercontent.com/3of3/cloudrecon/master/data/words.txt"
```

#### 2. Run `cloudrecon`.
Execute `cloudrecon` using the `word-list.txt` file and output the `public` buckets/blobs to a json file named `results.json`.

```bash
$ cloudrecon "word-list.txt" -o "results.json" --public

- PRIVATE https://s3.sa-east-1.amazonaws.com/test-lyft
- PRIVATE https://s3.ap-south-1.amazonaws.com/test.amazon
+ PUBLIC https://walmart-dev.s3.us-east-1.amazonaws.com
- PRIVATE https://s3.ap-southeast-1.amazonaws.com/apple-prod
- PRIVATE https://walmart.s3.ap-southeast-1.amazonaws.com
...
```

#### 3. Inspect the results.
Check the `results.json` output file to view the buckets/blobs you have discovered!

```bash
$ cat "results.json"
```

```json
{
    "public": {
        "total": 12,
        "hits": [
            "https://walmart-dev.s3.us-east-1.amazonaws.com",
            "https://apple-production.s3.ap-southeast-1.amazonaws.com",
            ...
        ]
    }
}
```

> **Note:** to include `private` buckets/blobs in the results omit the `-p, --public` flag from the command.

#### 4. Crawl the results.
Enumerate the static files located in each bucket/blob and record the findings.
> Coming soon!


## Example 2: Output to a MongoDB database

#### 1. Download a word-list.
The [SecLists](https://github.com/3of3/cloudrecon/edit/master/README.md) repository has a multitude of word-lists to choose from. For this example, let's download the sample word-list included in this repository.

```bash
$ curl -sSfL -o "word-list.txt" "https://raw.githubusercontent.com/3of3/cloudrecon/master/data/words.txt"
```

#### 2. Start an instance of MongoDB
```text
$ docker run --name "mongo" -p 27017:27017 -v "mongodb_data:/data/db" -v "mongodb_config:/data/configdb" -d mongo
```

#### 3. Run `cloudrecon`.
Execute `cloudrecon` using the `word-list.txt` file and output to MongoDB instance.

```bash
$ cloudrecon "word-list.txt" --db

- PRIVATE https://s3.sa-east-1.amazonaws.com/test-lyft
- PRIVATE https://s3.ap-south-1.amazonaws.com/test.amazon
+ PUBLIC https://walmart-dev.s3.us-east-1.amazonaws.com
- PRIVATE https://s3.ap-southeast-1.amazonaws.com/apple-prod
- PRIVATE https://walmart.s3.ap-southeast-1.amazonaws.com
...
```

#### 3. Inspect the results.
Check the MongoDB database: `cloudrecon` collection: `hits` to view the buckets/blobs you have discovered!

```bash
$ mongo "cloudrecon" --quiet --eval 'db.hits.find({}, {"url": 1, "access": 1, "_id": 0}).limit(5)'
```

```json
{ "url" : "https://s3.us-east-2.amazonaws.com/apple", "access" : "private" }
{ "url" : "https://s3.us-west-1.amazonaws.com/microsoft-dev", "access" : "private" }
{ "url" : "https://s3.us-west-1.amazonaws.com/dev-microsoft", "access" : "private" }
{ "url" : "https://s3.us-east-2.amazonaws.com/amazon", "access" : "private" }
{ "url" : "https://s3.us-east-1.amazonaws.com/dev-amazon", "access" : "private" }
```

#### 4. Crawl the results.
Enumerate the static files located in each bucket and record the findings.
> Coming soon!


## FAQ
#### Q: How do I configure this utility?
#### A:
`cloudrecon` can be configure using a yaml configuration file located in either the current working directory (e.g. `./cloudrecon.yml`) or your home diretory (e.g. `~/cloudrecon.yml`).

The following is the list of configurable values:
```yaml
# cloudrecon.yml

database: { host: "0.0.0.0", ... }

separators: ["-", "_", "."]

environments: ["", "backup", "backups", ...]

regions: ["ap-northeast-1", "ap-northeast-2", ...]
```

> To see the full list of configurable values (and their **defaults**) please refer to the [cloudrecon.yml](https://github.com/3of3/cloudrecon/blob/master/cloudrecon/cloudrecon.yml) file in this repository.


#### Q: How do I customize the AWS regions used in the recon?
#### A:
The AWS *regions* can be altered by setting the `regions` array in your `cloudrecon.yml` configuration file.
```yaml
# cloudrecon.yml

regions: [ "us-west-2", ...]
```


#### Q: How do I customize the environment values used in the recon?
#### A:
The *environments* are modifiers permuted with each item of the *word-list* (and the *separator*) to construct the bucket value in request.
The value can be altered by setting the `environments` array in your `cloudrecon.yml` configuration file.

For example, to only search lines from the word-list *verbatim* (i.e. without modification) you can set this value to an empty array.
```yaml
# cloudrecon.yml

environments: []
```

#### Q: How do I customize the MongoDB host and port?
#### A:
The database *host* and *port* can be configured by altering the `database` map in your `cloudrecon.yml` configuration file.

For example, `host` and `port` can be set directly inside the `database` map
```yaml
# cloudrecon.yml

database: {
  host: "0.0.0.0",
  port: 27017
}
```

#### Q: How do I use a database other than MongoDB?
#### A:
Sorry, at the moment only MongoDB is supported.

## Going Forward

- [x] Add GCP Data Storage Bucket Functionality
- [ ] Add Azure Data Storage Blob Functionality
- [ ] Add Alibaba Object Storage Service Functionality
- [ ] Create `crawl` command to crawl public/private buckets/blobs found in `find` stage.
- [ ] Separate out `find` and `crawl` as subcommands.
- [ ] Store discovered buckets/blobs in a NoSQL database.

## Disclaimer
This tools is distributed for educational and security purposes. I take no responsibility and assume no liability for the manner in which this tool is used.

## License

MIT &copy; [**Nathaniel "Q" Quist**](https://www.q-blogs.com/)
