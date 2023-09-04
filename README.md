
#  取得 Jupyter docker-stack 倉庫

從 github 下載 Jupyter docker-stack 的倉庫

```
$ git clone https://github.com/jupyter/docker-stacks.git
$ cd docker-stacks
```

# 編譯 Docker Image

打包自訂 spark 版本的 docker container

需注意 --build-arg 的參數，後續要使用 Hadoop 所以這邊需要安裝 openjdk 8

```bash
$ docker build --rm --force-rm \
    -t jupyter/pyspark-notebook:spark-3.4.1 ./images/pyspark-notebook \
    --build-arg spark_version=3.4.1 \
    --build-arg hadoop_version=3 \
    --build-arg spark_checksum=5a21295b4c3d1d3f8fc85375c711c7c23e3eeb3ec9ea91778f149d8d321e3905e2f44cf19c69a28df693cffd536f7316706c78932e7e148d224424150f18b2c5   \
    --build-arg openjdk_version=8
```

# 啟動 Jupyter Container

執行 Jupyter Container 

- 8888 : notebook
- 4040,4041 : spark

```bash
$ docker run --name jupyter -d -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/pyspark-notebook:spark-3.4.1
```

# 初次登入 Jupyter

打開瀏覽器訪問 http://{主機IP}:8888，第一次登入會要求輸入 token

在終端機使用以下面另可取得 Jupyter Token

```bash
$ docker exec jupyter jupyter server list |grep token | cut -d'=' -f2 | cut -d' ' -f1
15e0973d14a97c37fc8613538e476a354b3b32432bb2fdf1
```

# Pyspark 範例 : 1 + 2 + ... + 100 

## Local Mode

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master("local").getOrCreate()
sc = spark.sparkContext

# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(100 + 1))
rdd.sum()
#5050
```

## Standalone Mode

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master("spark://master:7077").getOrCreate()
sc = spark.sparkContext

# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(100 + 1))
rdd.sum()
# 5050
```

