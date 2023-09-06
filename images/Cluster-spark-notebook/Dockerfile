ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/pyspark-notebook
ARG spark_version=3.2.4
ARG hadoop_version=3.3.6
ARG spark_checksum=b2a49b5b1f764131e61abbd0ae161c8b8541b3636b585b727d03674f2502465f940e5ef2d4dff0c0060bc61184c747ca4ea9145bde74d62ec2e9f281e82408b7
ARG openjdk_version=8
FROM $BASE_CONTAINER

USER root

COPY opt/hadoop-3.3.6 /opt/hadoop-3.3.6
COPY opt/spark-3.2.4-bin-hadoop3.2 /opt/spark-3.2.4-bin-hadoop3.2

ARG HADOOP_HOME=/opt/hadoop-3.3.6 \
    SPARK_HOME=/opt/spark-3.2.4-bin-hadoop3.2 \
    PATH=/opt/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PIG_HOME/bin:$HIVE_HOME/bin \
    PATH=$ANACONDA_ROOT/bin:$PATH 

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/ \
    HADOOP_HOME=/opt/hadoop-3.3.6 \
    HADOOP_LOG_DIR=/tmp \
    HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop/ \
    LD_LIBRARY_PATH=$HADOOP_HOME/lib/native/ \
    HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native \
    HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native" \
    HADOOP_MAPRED_LOG_DIR="/tmp/jhslog" \
    YARN_HOME=$HADOOP_HOME \
    HADOOP_YARN_HOME=$HADOOP_HOME \
    YARN_LOG_DIR=/tmp \
    HADOOP_ROOT_LOGGER="WARN,console" \
    SPARK_HOME=/opt/spark-3.2.4-bin-hadoop3.2 \
    SPARK_CONF_DIR=$SPARK_HOME/conf \
    ANACONDA_ROOT=/opt/conda \
    PYSPARK_PYTHON=/usr/bin/python3 \
    PATH=/opt/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PIG_HOME/bin:$HIVE_HOME/bin \
    PATH=$ANACONDA_ROOT/bin:$PATH

RUN echo "PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PIG_HOME/bin:$HIVE_HOME/bin" \


    # 建立管理者帳號 bigred
RUN groupadd bigboss && echo '%bigboss ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers && \
    useradd -m -s /bin/bash bigred && echo 'bigred:bigred' | chpasswd && \
    usermod -a -G bigboss bigred

USER ${NB_UID}
WORKDIR "${HOME}" 
