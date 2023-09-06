#  取得 Jupyter docker-stack 倉庫

從 github 下載 Jupyter docker-stack 的倉庫

```
$ git clone https://github.com/CUTE-AIOT-PETER/SparkinJupyter.git
$ cd docker-stacks
```

# 編譯 Docker Image

打包自訂 spark 版本的 docker container

需注意 --build-arg 的參數，後續要使用 Hadoop 所以這邊需要安裝 openjdk 8

```bash
$ docker build --rm --force-rm \
    -t jupyter/pyspark-notebook:spark-3.2.4 ./images/pyspark-notebook \
    --build-arg spark_version=3.2.4 \
    --build-arg hadoop_version=3.2 \
    --build-arg spark_checksum=b2a49b5b1f764131e61abbd0ae161c8b8541b3636b585b727d03674f2502465f940e5ef2d4dff0c0060bc61184c747ca4ea9145bde74d62ec2e9f281e82408b7 \
    --build-arg openjdk_version=8
```

# 啟動 Jupyter Container

執行 Jupyter Container 

- 8888 : notebook
- 4040,4041 : spark

```bash
$ docker run --net=host --name jupyter -d jupyter_volume:/home/bigred/jupyter_run -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/pyspark-notebook:spark-3.2.4
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
