# Application-Effective-Scheduling-Subject-to-Security-Constraints
This problem is of scheduling applications modeled as a directed acyclic graph in a cost-effective and reliabile way subject to a given security constraints in a multi-cloud system. The model includes the billing mechanisms and costs for transferring data across clouds for different cloud providers. Our proposed methodology is compared with the following state-of-art algorithms:

1) A GSA based hybrid algorithm for bi-objective workflow scheduling in cloud computing - Anubhav Choudhary, Indrajeet Gupta, Vishaka Singh, Prasanta K. Jha: https://www.sciencedirect.com/science/article/abs/pii/S0167739X17303217
2) Genetic Algorithm Framework for Bi-objective Task Scheduling in Cloud Computing Systems - A. S. Ajeena Beegom & M. S. Rajasree : https://link.springer.com/chapter/10.1007/978-3-319-14977-6_38

## Usage
Clone the repositary and run the command: python main.py -num -itr -p -V -smin -smax, the arguments are explained below:

1) num: Represents the number of nodes of an Epigenomics task graph.
2) itr: Represents the number of iterations to run the algorithms, with average results reported at the end.
3) p: Represents the number of cloud providers, which should be a multiple of 3: p/3 for Microsoft Azure, p/3 for AWS and p/3 for GCP type clouds.
4) V: Represents the security constraint as a factor w.r.t the least security constraint.
5) smin: Represents the lower bound for task computation requirement and edge data.
6) smax: Represents the upper bound for task computation requirement and edge data.

Upon running the command and successful execution, we get plots for the cost, makespan, reliability and security of different algorithms. The security plot also includes the security constraint for reference.

## Results
![Figure_1](https://user-images.githubusercontent.com/64606981/203858602-f4c2c1ca-0f21-4df5-8264-96dbb2bf5111.png)
