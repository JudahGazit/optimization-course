import os

import findspark
from pyspark import SparkConf
from pyspark.sql import SparkSession


def set_environment_vars():
    spark_home = '/opt/spark'
    os.environ['SPARK_HOME'] = spark_home
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
    findspark.init(spark_home)


def create_context(master='local[2]',
                   app_name='myapp',
                   partitions=1):
    set_environment_vars()
    spark_config = {
        'spark.master': master,
        'spark.app.name': app_name,
        'spark.sql.shuffle.partitions': partitions,
        'spark.default.parallelizm': partitions
    }
    spark = SparkSession.builder.config(conf=SparkConf().setAll(spark_config.items())).getOrCreate()
    return spark
