#!/usr/bin/env python
# coding: utf-8
''' NOT WORKING -- PSEUDOCODE:
1.) Read game/play data
2.) Collect current weather of play
3.) Perform feature engineering (performance metrics, weighting defense, etc.)
4.) apply trained ALS model (pass or rush) to play
5.) output rec
'''
# In[3]:


from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.sql.functions import col, when, floor
from pyspark.ml.evaluation import RegressionEvaluator


# In[4]:


import sys
os.environ['PYSPARK_DRIVER_PYTHON_OPTS']= "notebook"
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['PYSPARK_PYTHON'] = sys.executable


# In[5]:


import os
os.environ['PYSPARK_PYTHON'] = '/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7'


# In[6]:


#create spark sesh/app
spark = SparkSession.builder \
    .appName("Bears' Play Recommender") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()


# In[7]:


spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")


# In[9]:


#df
data = spark.read.csv("/Users/colinbehr/Desktop/RESEARCH/ALL.csv", header=True, inferSchema=True)
#data.head(5)


# In[10]:


#do Time in sec because no ints i guess?
data = data.withColumn("TotalTimeSeconds", 
                        (floor(col("TotalTime") * 60)))
#same with pass and rushing defense 
data = data.withColumn("ScaledPassD", (col("Pass D") * 10).cast("integer"))
data = data.withColumn("ScaledRushD", (col("Rush D") * 10).cast("integer"))


# In[11]:


#situationID
data = data.withColumn("SituationID",
                        col("Location Actual") + 
                        col("ToGo") * 10 + 
                        col("Down") * 100 +
                        col("Lead Num") * 1000 + 
                        col("TotalTimeSeconds") * 10000 +  
                        col("ScaledPassD") * 100 +  
                        col("ScaledRushD") * 1000 +  
                        when(col("RoofType Num") == 0, 0).when(col("RoofType") == 1, 1).otherwise(2) * 1000 +   
                        when(col("Surface Num") == 1, 1).otherwise(0) * 100  #
                       )
#data.head()


# In[12]:


from pyspark.sql import functions as F
data = data.withColumn('WeatherID', 
                   (F.col('Hourly Feels Like').cast('int') * 10000) +  #adjust scales
                   (F.col('Hourly Wind Gust').cast('int') * 1000) + 
                   (F.col('Hourly Wind Speed').cast('int') * 100) +
                   (F.col('Hourly Icon') * 10) + 
                   (F.col('Dark')))


# In[13]:


display(data.select("Play Type").distinct().show())
data = data.withColumn('Play Type', when(col('Play Type') == 'Pass', 1).otherwise(2))
display(data.select("Play Type").distinct().show())


# In[14]:


data = data.withColumn("Yards Gained", col("Yards Gained").cast("float"))
data.select("Yards Gained").show(5)


# In[15]:


for col in data.columns:
    new_col_name = col.replace(" ", "_").replace(".", "_").replace("-", "_")
    data = data.withColumnRenamed(col, new_col_name)


# In[16]:


from pyspark.sql import functions as F

def split_train_test_spark(df):
    train_frames = []  # empty lists
    test_frames = []
    
    for season in range(2013, 2023):  # iterate through each season
        season_data = df.filter(df['SeasonID'] == season)  # filter by season
        next_season_data = df.filter(df['SeasonID'] == season + 1)  # to find next and backtrack
        
    
        first_game_id = season_data.select('GameID').orderBy('GameID').first()[0]  # grab first GameID
        first_game_data = season_data.filter(season_data['GameID'] == first_game_id)  # add to test
        test_frames.append(first_game_data)
        
        #get last seasons last game by finding next season's first
        if next_season_data.count() > 0:  # if not the last season
            next_first_game_id = next_season_data.select('GameID').orderBy('GameID').first()[0]
            last_game_data = season_data.filter(season_data['GameID'] == next_first_game_id - 1)
        else:  # if last season, take last game
            last_game_id = season_data.select('GameID').orderBy(F.desc('GameID')).first()[0]
            last_game_data = season_data.filter(season_data['GameID'] == last_game_id)
        
        # Add the last game data to the test set
        test_frames.append(last_game_data)
        
        # Every other game that is not first or last will go to the training set
        remaining_season_data = season_data.filter(
            (season_data['GameID'] != first_game_id) & 
            (season_data['GameID'] != last_game_data.select('GameID').first()[0])
        )
        train_frames.append(remaining_season_data)
        
    # Concatenate all frames for training and testing
    train = train_frames[0]
    for frame in train_frames[1:]:
        train = train.union(frame)
    
    test = test_frames[0]
    for frame in test_frames[1:]:
        test = test.union(frame)
        
    #train = train.na.drop()
    #test = test.na.drop()
    
    return train, test

#create data
train, test = split_train_test_spark(data)  

#.count() for spark apparently 
print(train.count(), test.count())


# In[19]:


als = ALS( 
    regParam=0.08, 
    userCol="SituationID", 
    itemCol="PlayID", 
    ratingCol="Yards_Gained",
    rank = 20,
    coldStartStrategy="drop", 
    nonnegative=False
)


# In[18]:


#rush_train = train_df.filter(train_df['Play Type'] == 2)
#rush_test = test_df.filter(test_df['Play Type'] == 2)
#rush_train = rush_train.na.drop(subset=["SituationID", "Play Type", "Yards Gained"])
#from pyspark.ml.recommendation import ALS
#from pyspark.ml.evaluation import RegressionEvaluator
#als_rush = ALS(userCol="SituationID", itemCol="Play Type", ratingCol="Yards Gained")
#rush_model = als_rush.fit(rush_train)
## Predict and evaluate for rush data
#predictions_rush = rush_model.transform(rush_test)
#evaluator = RegressionEvaluator(metricName="rmse", labelCol="Yards Gained", predictionCol="prediction")
#rmse_rush = evaluator.evaluate(predictions_rush)
#print("RMSE for Rush Model =", rmse_rush)
#print("Rush train count:", rush_train.count())
#print("Pass train count:", pass_train.count())
#print(data.select("Play Type").distinct().show())
#data.groupBy('Play Type').count().show()


# In[25]:


#check data types of all columns used in ALS
#als_columns = ['SituationID', 'PlayID', 'Yards Gained', 'Play Type']  # Add any other relevant columns
#for col_name in als_columns:
#    print(f"Data type of {col_name}: {data.schema[col_name].dataType}")


# In[20]:


from pyspark.sql.functions import col

#fit ALS model on training 
model = als.fit(train)

#generate preds on test
predictions = model.transform(test)

#eval
evaluator = RegressionEvaluator(metricName="rmse", labelCol="Yards_Gained", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root-mean-square error = " + str(rmse))

#put columns into pandas for easy export
result_df = predictions.select('SituationID', 'Play Type', col('Yards_Gained').alias('Actual Yards Gained'), 
                               col('prediction').alias('Predicted Yards Gained')).toPandas()

