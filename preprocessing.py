#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 21:19:51 2024

@author: colinbehr
"""
import logging
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.sql.functions import col, when, floor
from pyspark.ml.evaluation import RegressionEvaluator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("DataPreprocessing") \
    .getOrCreate()

# Log that the Spark session was started
logger.info("Spark session started.")

# Import data
data = spark.read.csv("s3://thesisbears/ALL.csv", header=True, inferSchema=True)

# Data preprocessing
# Log the start of data preprocessing
logger.info("Starting data preprocessing.")

data = data.withColumn("TotalTimeSeconds", 
                        (floor(col("TotalTime") * 60)))
data = data.withColumn("ScaledPassD", (col("Pass D") * 10).cast("integer"))
data = data.withColumn("ScaledRushD", (col("Rush D") * 10).cast("integer"))

data = data.withColumn("SituationID",
                        col("Location Actual") + 
                        col("ToGo") * 10 + 
                        col("Down") * 100 +
                        col("Lead Num") * 1000 + 
                        col("TotalTimeSeconds") * 10000 +  
                        col("ScaledPassD") * 100 +  
                        col("ScaledRushD") * 1000 +  
                        when(col("RoofType Num") == 0, 0).when(col("RoofType") == 1, 1).otherwise(2) * 1000 +   
                        when(col("Surface Num") == 1, 1).otherwise(0) * 100)

from pyspark.sql import functions as F
data = data.withColumn('WeatherID', 
                   (F.col('Hourly Feels Like').cast('int') * 10000) +
                   (F.col('Hourly Wind Gust').cast('int') * 1000) + 
                   (F.col('Hourly Wind Speed').cast('int') * 100) +
                   (F.col('Hourly Icon') * 10) + 
                   (F.col('Dark')))

data = data.withColumn('Play Type', when(col('Play Type') == 'Pass', 1).otherwise(2))

# Log completion of data preprocessing
logger.info("Data preprocessing completed.")

# Show distinct play types
# Commented out as 'display' is not available in EMR scripts
# display(data.select("Play Type").distinct().show())

# Save preprocessed data
data.write.mode('overwrite').csv("s3://thesisbears/preprocessed_data.csv", header=True)

data = data.withColumn("Yards Gained", col("Yards Gained").cast("float"))
# Displaying the data using 'show' which is suitable for EMR environment, but commenting out for large datasets
# data.select("Yards Gained").show(5)

# Log the completion of the script
logger.info("Script completed successfully.")

spark.stop()
