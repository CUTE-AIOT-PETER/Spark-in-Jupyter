# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Spark dependencies
# Default values can be overridden at build time
# (ARGS are in lower case to distinguish them from ENV)
ARG spark_version="3.2.4"
ARG hadoop_version="3.2"
ARG scala_version
ARG spark_checksum="5a21295b4c3d1d3f8fc85375c711c7c23e3eeb3ec9ea91778f149d8d321e3905e2f44cf19c69a28df693cffd536f7316706c78932e7e148d224424150f18b2c5"
ARG openjdk_version="17"
ARG HADOOP_HOME=/opt/hadoop-3.3.6

ENV APACHE_SPARK_VERSION="${spark_version}" \
    HADOOP_VERSION="${hadoop_version}"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jre-headless" \
    ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Spark installation
WORKDIR /tmp

# You need to use https://archive.apache.org/dist/ website if you want to download old Spark versions
# But it seems to be slower, that's why we use recommended site for download
RUN if [ -z "${scala_version}" ]; then \
    curl --progress-bar --location --output "spark.tgz" \
        "https://dlcdn.apache.org/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"; \
  else \
    curl --progress-bar --location --output "spark.tgz" \
        "https://dlcdn.apache.org/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}-scala${scala_version}.tgz"; \
  fi && \
  echo "${spark_checksum} *spark.tgz" | sha512sum -c - && \
  tar xzf "spark.tgz" -C /usr/local --owner root --group root --no-same-owner && \
  rm "spark.tgz"

# Configure Spark
ENV SPARK_HOME=/usr/local/spark
ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info" \
    PATH="${PATH}:${SPARK_HOME}/bin"

RUN if [ -z "${scala_version}" ]; then \
    ln -s "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" "${SPARK_HOME}"; \
  else \
    ln -s "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}-scala${scala_version}" "${SPARK_HOME}"; \
  fi && \
  # Add a link in the before_notebook hook in order to source automatically PYTHONPATH && \
  ln -s "${SPARK_HOME}/sbin/spark-config.sh" /usr/local/bin/before-notebook.d/spark-config.sh

# Configure IPython system-wide
COPY ipython_kernel_config.py "/etc/ipython/"
RUN fix-permissions "/etc/ipython/"

USER ${NB_UID}

# Install pyarrow
# Temporarily pin pandas to version 1.5.3, see: https://github.com/jupyter/docker-stacks/issues/1924
RUN mamba install --yes \
    'pandas>=1.5.3,<2.0.0' \
    'pyarrow' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


ENV HADOOP_HOME=/opt/hadoop-3.3.6 \
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
    PATH=/opt/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PATH="${PATH}:${HADOOP_HOME}/bin:$HADOOP_HOME/sbin:$PIG_HOME/bin:$HIVE_HOME/bin \
    ANACONDA_ROOT=/opt/conda \
    PATH="${PATH}:$ANACONDA_ROOT/bin \
    PYSPARK_PYTHON=$ANACONDA_ROOT/bin/python3

USER root

    # 建立管理者帳號 bigred
RUN groupadd bigboss && echo '%bigboss ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers && \
    useradd -m -s /bin/bash bigred && echo 'bigred:bigred' | chpasswd && \
    usermod -a -G bigboss bigred 

COPY opt/hadoop-3.3.6 /opt/hadoop-3.3.6
COPY opt/spark-3.2.4-bin-hadoop3.2 /usr/local/spark-3.2.4-bin-hadoop3.2

USER ${NB_UID}
WORKDIR "${HOME}"

EXPOSE 4040
