# Geometric-block-model
Generate &amp; recover geometric block model graph;

GBM - geometric block model;

suggesting to use python 3.8.6 or upper version;

# Using instruction

* GBM_constants(rs, rd, n)

* rs - max distance between two point which could be join by edge &amp; belong to the same cluster; (maximum 0.5)

* rd - max distance between two point which could be join by edge &amp; belongs to the different clusters; (should be at least 4 time less than rs)

* n - number of points;

* For Create Graph run GBM_Generator.py;

* For Recover Graph run GBM_Recover.py;

* For Accuracy determination run GBM_Comparator.py;

Note please if modify params (rs &amp; rd) at GBM_Generator.py do it also at GBM_Recover.py;

