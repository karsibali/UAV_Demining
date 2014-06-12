r = randi(10,400);  % 400x400 random integers between [1, 10]
r = (r>9);          % Keep only about 1/10 of: That is about 16000

num_objects = sum(sum(r));
num_mines =  num_objects * 2 / 3;
num_clutter = num_objects / 3;

mine_idx = randi(5000, 10000, 1);
clutter_idx = randi(8000, 6000, 1) > 5000;