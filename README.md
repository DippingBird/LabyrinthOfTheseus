# The Labyrinth of Theseus
Hobby project analysing the puzzle about the labyrinth of theseus by David Well
## Table of Contents
1. **Description**
   1. Motivation   
   1. Mathematical Analysis
1. **Installation**
1. **Usage**
1. **License**
## Description
### Motivation
The idea to make this project began with the solving of the current puzzle from the column ["Mathematische Rätsel"](https://www.spektrum.de/raetsel/) titled ["Hemmes mathematische Rätsel: Das Labyrinth"](https://www.spektrum.de/raetsel/das-labyrinth/1577642) written by Heinrich Hemme and published online by the ["Spektrum der Wissenschaft Verlagsgesellschaft mbH"](https://www.spektrumverlag.de/impressum/) on the 25th October of 2018, a german version of the Scientific American.
Hemmes short summary of the puzzle translated into englisch:

> Theseus enters the labyrinth, in which Minotaurus lurks on him, through the 
> southern entrance and wants to leave it through the northern, where Ariadne waits
> on him. In order to confuse the beast, Theseus leaves no romm in which he enters 
> through the opposite exit, but rather taking a turn to the right or left. Which is
> the shortest path of this kind through the labyrinth? It should be assumed that 
> Theseus always walks parallel or cross to the walls of the rooms.

My approach was converting the labyrinth into a network and applying [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) in order to find the shortest path.
A few months passed until i wanted to learn how to program in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) after learning C# and Java. I figured writing a program analysing this puzzle as a graph would be a good first challenge, and i was curious to find out by myself, just as apparently Markus Götz from Maihingen did 1998 according to the solution, that there are 624 acyclic paths from the entrance to the exit.
However i found quite the opposite, that there were 8256 acyclic paths, more than 13-times the amount that Markus found! At this point I was sure i made a mistake, probably when reducing the graph or typing in the graph-data.
