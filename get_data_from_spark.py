# 通过spark脚本从hive表里拉取数据
# 数据统一存储在集群上，可以通过hive拉取，也可以通过spark拉取
import findspark
findspark.init()
from pyspark.sql import SparkSession, HiveContext
import pandas
import csv

def get_session():
    spark = SparkSession.builder.master("local") \
        .appName("ai-golden-data" ) \
        .config("spark.driver.memory", "10g") \
        .config("hive.metastore.uris", "thrift://bigdata-0002:9807") \
        .enableHiveSupport() \
        .getOrCreate()
    spark.conf.set("spark.sql.crossJoin.enabled", "true")
    spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
    return spark

spark = get_session()
# df = spark.sql("select * from ai_prod.ads_ai_raw_sample_cv_jd where ds=20220821")

cv_df = spark.sql('''
                    select 
                         id, currentposition, desiredposition, industry, desiredindustry, majorname, skills, edutracks, jobtracks, projecttracks 
                     from 
                         ai_prod.ads_ai_raw_feature_cv_a 
                     where 
                         ds=20220821
                 ''')\
               .withColumnRenamed('id','cv_id')

# jd似乎遗漏了tags
jd_df = spark.sql('''
                    select 
                         jd_id, title, category_name, description, requirement 
                    from 
                         ai_prod.ads_ai_raw_feature_jd_a 
                    where 
                         ds=20220821;
               ''')

label_df = spark.sql('''

                    select 
                         cv_id, jd_id 
                    from 
                         ai_prod.ads_ai_raw_sample_cv_jd 
                    where 
                         ds=20220821
               ''')

df = label_df\
        .join(jd_df, 'jd_id', 'inner')\
        .join(cv_df, 'cv_id', 'inner')\


df.toPandas().to_csv('text_sample_20220821_spark.csv')


#========================================================================================================================

# conda activate nlp

'''
scp ai@139.159.133.197:/mnt/data/home/ai/linus/tfidf/text_sample_20220821_spark.csv .
s87i3nvs4
'''

















