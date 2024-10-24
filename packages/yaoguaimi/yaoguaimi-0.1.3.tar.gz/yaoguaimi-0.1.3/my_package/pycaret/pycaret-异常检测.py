#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pycaret.datasets import get_data
data = get_data('./datasets/anomaly')
# data = get_data('anomaly')


# In[ ]:


from pycaret.anomaly import AnomalyExperiment
s = AnomalyExperiment()
s.setup(data, session_id = 0)
# 另一种加载方式
# from pycaret.anomaly import *
# s = setup(data, session_id = 0)


# In[ ]:


iforest = s.create_model('iforest')
print(iforest)


# In[ ]:


IForest(behaviour='new', bootstrap=False, contamination=0.05,
    max_features=1.0, max_samples='auto', n_estimators=100, n_jobs=-1,
    random_state=0, verbose=0)


# In[ ]:


s.models()


# In[ ]:


result = s.assign_model(iforest)
result.head()


# In[ ]:


predictions = s.predict_model(iforest, data = data)
predictions.head()


# In[ ]:




