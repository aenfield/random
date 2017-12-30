# assuming /opt/spark is a symlink to the spark install, run this with the following
# command line:
# spark-submit SparkSimpleApp.py 

from pyspark.sql import SparkSession

logFile = "/opt/spark/README.md"
spark = SparkSession.builder.appName("foo").master("local").getOrCreate()
logData = spark.read.text(logFile).cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()

print("----")
print(f"Lines with a: {numAs}, lines with b: {numBs}.")
print("----")

spark.stop()