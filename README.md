# Neural-Network

This is my first real attempt at creating a Neural Network. It is something I have been independently researching this summer and I thought it was time to give something a try. This Net takes input from a simple game where the player moves left and right to dodge an obstacle. The game is then replicated 25 times, each with a personal NN to support the decision making. The succcess/failure of the player will influence the weights (connections between neurons), which will hopefully increase its fitness(points). Fitness is important to the development because it plays a role in my implementation of the sophisticated term Neuro-Evolution of Augmented Topologies (NEAT). After 100 trials where each NN can learn and progress, the best is selected and copied to replace the 24 others. Each new child NN is then given a mutation from to differentiate from its parent. As the generations continues to increment, the NNs get closer and closer to being capable of playing the game on their own. 

## Getting Started

All you need to get this running is to download or copy the files into whichever IDE/text-editor you prefer. If using a text-editor you can run a python file with the command 
```
$python program_name.py
```
with bash. The main.py is all you need to run (with the other files in the same directory) to see the program. 

### Prerequisites & Installing
Installations include some version of python and the pygame module. Once you have python installed, you can run 

```
$pip install pygame
```
and then 
```
$pip list
```
to ensure it was installed correctly 

## Further Development

Currently the mutations are under development as well as perfecting the bias and activation functions for the Neurons

## Built With

* [Python](https://www.python.org/downloads/) - For Everything
* [Helpful Video](https://www.youtube.com/watch?v=aeWmdojEJf0) - For some inspiration and general concept comprehension

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details 
--jk it's not

