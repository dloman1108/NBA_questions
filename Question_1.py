
# coding: utf-8

# In[3]:

import numpy as np


# In[4]:

#NBA lottery odds mapping
lottery_odds = {1: {1: .250, 5: 0},
                2: {1: .199, 5: .123},
                3: {1: .156, 5: .265},
                4: {1: .119, 5: .351},
                5: {1: .088, 5: .261},
                6: {1: .063, 5: 0},
                7: {1: .043, 5: 0},
                8: {1: .028, 5: 0},
                9: {1: .017, 5: 0},
                10: {1: .011, 5: 0},
                11: {1: .008, 5: 0},
                12: {1: .007, 5: 0},
                13: {1: .006, 5: 0},
                14: {1: .005, 5: 0},
                15: {1: 0, 5: 0},
                16: {1: 0, 5: 0},
                17: {1: 0, 5: 0},
                18: {1: 0, 5: 0},
                19: {1: 0, 5: 0},
                20: {1: 0, 5: 0},
                21: {1: 0, 5: 0},
                22: {1: 0, 5: 0},
                23: {1: 0, 5: 0},
                24: {1: 0, 5: 0},
                25: {1: 0, 5: 0},
                26: {1: 0, 5: 0},
                27: {1: 0, 5: 0},
                28: {1: 0, 5: 0},
                29: {1: 0, 5: 0},
                30: {1: 0, 5: 0}}


# In[41]:

#Initialize simulation
total=0.0
ones=0.0
fives=0.0
for j in range(50000):
    
    position = 5
    
    #Simulate 20 years
    for i in range(20):
        
        #Draw U(0,1) RV to choose position
        pos_rand = np.random.random()
        if (pos_rand <= .6 or position < 3) and position < 28:
            position = position + 3
        else:
            position = position - 2

        #Draw U(0,1) RV to choose pick (1, 5 or neither)
        lot_rand = np.random.random()
        
        #If the first pick is landed:
        if lot_rand <= lottery_odds[position][1]:
            ones += 1
            total += 1
            ave_years_1.append(i+1)
            continue
            
        #If the fifth pick is landed:
        if lot_rand > lottery_odds[position][1] and lot_rand <= (lottery_odds[position][1]+lottery_odds[position][5]):
            fives += 1
            total += 1
            ave_years_5.append(i+1)
            continue
            
print "First pick percentage: " + str(ones/total)
print "Fifth pick percentage: " + str(fives/total)


# In[ ]:



