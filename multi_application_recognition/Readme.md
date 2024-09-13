## Multi-Application Recognition
**Experimental Setup.**
In real-world scenarios, users may run multiple applications simultaneously in the foreground. 
For example, a user may be playing music or downloading files while using other daily applications.
We consider a scenario where one primary application and some secondary applications are running simultaneously in the foreground. 
Our goal is to feed the classifier a set of timing data extracted when $n$ applications are running simultaneously, and the classifier can correctly output the label of the primary application.
This is a measure of the noise tolerance of the classifier, i.e., the ability to recognize the primary application in the presence of noise caused by other foreground applications.

We choose music players and download tools as secondary applications and other applications that do not conflict with their simultaneous use as primary applications. 
There are 36 combination cases for $n=2$ (one primary application along with one music player or one download tool), 48 combination cases for $n=3$, and 40 combination cases for $n=4$ 
(one primary application along with one music player and one/two download tools, or with two/three download tools).
We extract timing data for each combination case and name these datasets **TOR36** $(n=2)$, **TOR48** $(n=3)$, and **TOR40** $(n=4)$, respectively. 

**Results.**
We extract timing data for each primary application to form the dataset **SOR8**.
We then train the RF classifier on the **SOR8** dataset and test it on the datasets **TOR36**, **TOR48**, and **TOR40**, with an overall accuracy of **92.12%**, **86.58%**, and **84.60%**, respectively. 
Moreover, we compute the precision and recall values from the data of the same primary application with all paired secondary applications.
The average precision and recall are **92.81%** and **91.08%** for $n = 2$, **86.33%** and **86.52%** for $n = 3$, and **79.30%** and **81.38%** for $n=4$, respectively.
Overall, Loadshow exhibits strong noise tolerance and is able to accurately recognize the primary application in the presence of secondary applications.
