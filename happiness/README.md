# Data Analysis Summary
## Descriptive Statistics
              year  Life Ladder  Log GDP per capita  Social support  \
count  2363.000000  2363.000000         2335.000000     2350.000000   
mean   2014.763860     5.483566            9.399671        0.809369   
std       5.059436     1.125522            1.152069        0.121212   
min    2005.000000     1.281000            5.527000        0.228000   
25%    2011.000000     4.647000            8.506500        0.744000   
50%    2015.000000     5.449000            9.503000        0.834500   
75%    2019.000000     6.323500           10.392500        0.904000   
max    2023.000000     8.019000           11.676000        0.987000   

       Healthy life expectancy at birth  Freedom to make life choices  \
count                       2300.000000                   2327.000000   
mean                          63.401828                      0.750282   
std                            6.842644                      0.139357   
min                            6.720000                      0.228000   
25%                           59.195000                      0.661000   
50%                           65.100000                      0.771000   
75%                           68.552500                      0.862000   
max                           74.600000                      0.985000   

        Generosity  Perceptions of corruption  Positive affect  \
count  2282.000000                2238.000000      2339.000000   
mean      0.000098                   0.743971         0.651882   
std       0.161388                   0.184865         0.106240   
min      -0.340000                   0.035000         0.179000   
25%      -0.112000                   0.687000         0.572000   
50%      -0.022000                   0.798500         0.663000   
75%       0.093750                   0.867750         0.737000   
max       0.700000                   0.983000         0.884000   

       Negative affect  
count      2347.000000  
mean          0.273151  
std           0.087131  
min           0.083000  
25%           0.209000  
50%           0.262000  
75%           0.326000  
max           0.705000  

## Correlation Matrix
                                      year  Life Ladder  Log GDP per capita  \
year                              1.000000     0.046846            0.080104   
Life Ladder                       0.046846     1.000000            0.783556   
Log GDP per capita                0.080104     0.783556            1.000000   
Social support                   -0.043074     0.722738            0.685329   
Healthy life expectancy at birth  0.168026     0.714927            0.819326   
Freedom to make life choices      0.232974     0.538210            0.364816   
Generosity                        0.030864     0.177398           -0.000766   
Perceptions of corruption        -0.082136    -0.430485           -0.353893   
Positive affect                   0.013052     0.515283            0.230868   
Negative affect                   0.207642    -0.352412           -0.260689   

                                  Social support  \
year                                   -0.043074   
Life Ladder                             0.722738   
Log GDP per capita                      0.685329   
Social support                          1.000000   
Healthy life expectancy at birth        0.597787   
Freedom to make life choices            0.404131   
Generosity                              0.065240   
Perceptions of corruption              -0.221410   
Positive affect                         0.424524   
Negative affect                        -0.454878   

                                  Healthy life expectancy at birth  \
year                                                      0.168026   
Life Ladder                                               0.714927   
Log GDP per capita                                        0.819326   
Social support                                            0.597787   
Healthy life expectancy at birth                          1.000000   
Freedom to make life choices                              0.375745   
Generosity                                                0.015168   
Perceptions of corruption                                -0.303130   
Positive affect                                           0.217982   
Negative affect                                          -0.150330   

                                  Freedom to make life choices  Generosity  \
year                                                  0.232974    0.030864   
Life Ladder                                           0.538210    0.177398   
Log GDP per capita                                    0.364816   -0.000766   
Social support                                        0.404131    0.065240   
Healthy life expectancy at birth                      0.375745    0.015168   
Freedom to make life choices                          1.000000    0.321396   
Generosity                                            0.321396    1.000000   
Perceptions of corruption                            -0.466023   -0.270004   
Positive affect                                       0.578398    0.300608   
Negative affect                                      -0.278959   -0.071975   

                                  Perceptions of corruption  Positive affect  \
year                                              -0.082136         0.013052   
Life Ladder                                       -0.430485         0.515283   
Log GDP per capita                                -0.353893         0.230868   
Social support                                    -0.221410         0.424524   
Healthy life expectancy at birth                  -0.303130         0.217982   
Freedom to make life choices                      -0.466023         0.578398   
Generosity                                        -0.270004         0.300608   
Perceptions of corruption                          1.000000        -0.274208   
Positive affect                                   -0.274208         1.000000   
Negative affect                                    0.265555        -0.334451   

                                  Negative affect  
year                                     0.207642  
Life Ladder                             -0.352412  
Log GDP per capita                      -0.260689  
Social support                          -0.454878  
Healthy life expectancy at birth        -0.150330  
Freedom to make life choices            -0.278959  
Generosity                              -0.071975  
Perceptions of corruption                0.265555  
Positive affect                         -0.334451  
Negative affect                          1.000000  

