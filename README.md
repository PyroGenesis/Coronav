# Coronav
Navigating away from the virus

In the current pandemic, it is imperative that everyone follows the principle of "social distancing". However, we can't stay at home 100% of the time since we need essential supplies to survive. So, it would be very helpful, if an app could predict whether a particular area will be crowded at a particular time or not. To facilitate this, we built Coronav - which will help you navigate to places while also avoiding the crowds.  

## How it works
It provides the user with a map interface with an additional feature of color-coding of areas according to their estimated population distribution. We are using 4 different colors to correspond to different levels of crowds.  
We also provide the user with an option to enter the day and time for which they need the predictions. The user can even enter the search text of a particular place and the map will then be focused on that location.  
The user can also enter their feedback of a particular place and we will use it to make better predictions in the future.  
To facilitate all of this, the app uses its front-end (PWA interface) and runs on a Flask + Oracle Autonomous DB back-end. We have trained and used our own Machine Learning model using GCP to make the predictions.  

## What's next for Coronav
Now, we want to make changes to the app such that it is not only as seamless as the current one but also scalable for larger areas (worldwide). There are some minor bugs related to the handling of requests in the back-end and we would like to fix those as well.
