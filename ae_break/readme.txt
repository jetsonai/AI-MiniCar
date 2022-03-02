* YOU MUST INSTALL PYTORCH BEFORE START THIS.!!

* IF NOT : 
   go to tis page to Install DL setting 
   
   https://github.com/katebrighteyes/jetbot_new/tree/main/StartDL
   

1. data_collection

save_block=0 # 0: free, 1:block


1) Take Blocked Picture

python3 data_collection2.py 1

# press 's' to take picture
(collect picture more than 40)

# Ctl-C to finish it

2) Take Free Picture

python3 data_collection2.py 0

# press 's' to take picture
(collect picture more than 40)

# Ctl-C to finish it

----------------------------------------
2. train_fca_model

zip dataset.zip -r ./dataset/

use colab with train_eb_model.ipynb

----------------------------------------

* YOU MUST set power mod 5W !!

3. fca_live_demo

python3 fca_live_demo.py
